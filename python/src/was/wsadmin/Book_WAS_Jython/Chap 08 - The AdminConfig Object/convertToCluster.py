#---------------------------------------------------------------------
#    Name: convertToCluster.py
#    From: WebSphere Application Server Administration using Jython
#      By: Robert A. (Bob) Gibson [rag], Arthur Kevin McGrath, Noel J. Bergman
#    ISBN: 0-13-700952-6
#    Role: Script used to create a new ServerCluster having the
#          user specified name, and making the user specified server
#          the first member.
#    Note: See Usage routine for more details
# History:
#   Date   ver who what
# -------- --- --- --- ----------
# 09/10/29 0.1 rag Fix - Added ISBN detail
# 08/10/25 0.0 rag New - for the book
#---------------------------------------------------------------------
import getopt, sys

#---------------------------------------------------------------------
# Global dictionary to hold the user specified options & values
#---------------------------------------------------------------------
Opts = {}

#---------------------------------------------------------------------
# Name: validWord
# Role: Verify that the specified name, contains at least 1 char, and
#       only uses "word" characters (i.e., [a-zA-Z0-9_]
#---------------------------------------------------------------------
def validWord( name ) :
  import re
  return ( re.search( re.compile( r'^\w+$' ), name ) != None )

#---------------------------------------------------------------------
# Name: convertToCluster()
# Role: routine used to implement desired action
#---------------------------------------------------------------------
def convertToCluster( cmdName = 'convertToCluster' ) :

  #-------------------------------------------------------------------
  # Define some mapped error messages.
  # Note: A mapped "error" message is one that contains the name of
  #       local variables that should be used during the generation
  #       of the message to display specific values.  For example,
  #         print "%(cmdName)s" % locals()
  #       is interpreted as though we had typed:
  #         print "%s" % cmdName
  #-------------------------------------------------------------------
  parmErr     = '%(cmdName)s: Insufficient parameters provided '
  parmErr    += '(2 required, %(argc)d found).\n'
  required    = '%(cmdName)s: Required module not found: %(modName)s'
  ambiguous   = '%(cmdName)s failed: Ambiguous request nodeName parameter required.'
  nodeNameErr = '%(cmdName)s failed: nodeName is undefined, and indeterminate'
  badNodeName = '%(cmdName)s: Invalid nodeName value: %(nodeName)s'
  unknownSvr  = '%(cmdName)s failed: Unknown serverName: %(servName)s'
  unknownNode = '%(cmdName)s failed: Unknown nodeName: %(nodeName)s'
  getidErr    = '%(cmdName)s failed: AdminConfig.getid() failed.'
  pTypeErr    = 'Invalid processType: "%(pType)s" -- DeploymentManager required.'
  cmdParms    = '--clusterName %(clustName)s --serverName %(servName)s'

  try :
    from WAuJ_utilities import showAsDict
    from WAuJ_utilities import ConfigIdAsDict
  except ImportError, ie :
    modName = str( ie ).split( ' ' )[ -1 ]
    print required % locals()
    sys.exit( -1 )

  argc = len( sys.argv )                    # Number of arguments
  if ( argc < 2 ) :                         # If too few are present,
    print parmErr % locals()
    Usage( cmdName )                        #   provide the Usage info & exit
                                            #
  parseOpts( cmdName )                      # Otherwise, parse the command line

  #-------------------------------------------------------------------
  # Assign values from the user Options dictionary.  To make value
  # access simplier.  For example, instead of using:
  #   Opts[ 'servName' ]
  # we will be able to simply use:
  #   servName
  # to access the value.  In addition, we can make use of these names
  # in any mapped messages, see below.
  #-------------------------------------------------------------------
  for key in Opts.keys() :
    cmd = str( key ) + ' = Opts[ "' + str( key ) + '" ]'
    exec( cmd )

  #-------------------------------------------------------------------
  # Verify the required parameters have valid (alphanumeric) values
  # Note: Check that the variable is not None first (i.e., using a
  #       "not variable" test), so that a later exception is avoided.
  #-------------------------------------------------------------------
  if not clustName or not validWord( clustName ) :
    print '%s: Missing or invalid required parameter: --clusterName' % cmdName
    Usage( cmdName )

  if not servName or not validWord( servName ) :
    print '%s: Missing or invalid required parameter: --serverName' % cmdName
    Usage( cmdName )

  #-------------------------------------------------------------------
  # Verify that nodeName, if provided, is valid (alphanumeric)
  #-------------------------------------------------------------------
  if nodeName and not validWord( nodeName ) :
    print badNodeName % locals()
    Usage( cmdName )

  #-------------------------------------------------------------------
  # If we get here, we have valid required and/or default options.
  # Determine the kind of node to which we are connected (and we MUST
  # be connected).  To do so, we look for the process type (processType)
  # of the current node.  However, to obtain this we must first get the
  # completeObjectName for this node (i.e., the server object (saved in
  # sObj).
  #-------------------------------------------------------------------
  try :
    cell  = AdminControl.getCell()          # What's the cell Name?
  except :                                  #
    ( kind, value ) = sys.exc_info()[ :2 ]  #
    ( kind, value ) = str( kind ), str( value )
    if value.find( 'AdminControl' ) > -1 :  # "AdminControl service not available"?
      print '%s: A connection to an active Deployment Manager is required.' % cmdName
    else :                                  #
      print '''%(cmdName)s: An unexpected exception occurred.\n
  Exception  type: "%(kind)s"
  Exception value: "%(value)s"''' % locals()
    sys.exit( -1 )                          #
                                            #
  node  = AdminControl.getNode()            # What's the node Name?
  sObj  = AdminControl.completeObjectName( 'cell=%s,node=%s,type=Server,*' % ( cell, node ) )
  pType = AdminControl.getAttribute( sObj, 'processType' )

  #-------------------------------------------------------------------
  # The convertToCluster() method should only be executed on a
  # DeploymentManager (aka ND) node.
  #-------------------------------------------------------------------
  if pType == 'DeploymentManager' :
    #-----------------------------------------------------------------
    # Verify that the nodeName is known, or unambiguous, which occurs
    # when only 1 server of the specified name exists, or if we have
    # only 1 non-ND nodename.  Begin by obtaining the list of currently
    # configured servers and nodes.
    # Note: These are actually the configIDs for the items of interest
    #-----------------------------------------------------------------
    servers  = AdminConfig.list( 'Server' ).splitlines()
    nodes    = AdminConfig.list( 'Node' ).splitlines()

    #-----------------------------------------------------------------
    # Next, use list comprehension to build the list of server, and
    # node names.
    # Note: The configID characters up to '(' are the nodeName
    #-----------------------------------------------------------------
    svrList  = [ x.split( '(' )[ 0 ] for x in servers ]
    nodeList = [ x.split( '(' )[ 0 ] for x in nodes   ]

    #-----------------------------------------------------------------
    # Is nodeName specified, and valid?
    #-----------------------------------------------------------------
    if nodeName and nodeName not in nodeList :
      print unknownNode % locals()          # Mapped error message
      sys.exit( 1 )                         #   give up...

    #-----------------------------------------------------------------
    # Do we have only 1 occurrence of the specified serverName?
    #-----------------------------------------------------------------
    if not nodeName and svrList.count( servName ) > 1 :
      print ambiguous % locals()            #   Mapped error message
      sys.exit( 1 )                         #   give up...

    #-----------------------------------------------------------------
    # Given exactly 1 matchine server name, verify that:
    # - either the nodeName was not supplied
    # - or, the nodeName matches the actual value
    #-----------------------------------------------------------------
    if not nodeName :
      if servName in svrList :
#       print 'servName: %s' % servName
#       print '   index: %d' % svrList.index( servName )
#       print '  server: %s' % servers[ svrList.index( servName ) ]
        nodeName = ConfigIdAsDict( servers[ svrList.index( servName ) ] )[ 'nodes' ]
#       print 'nodeName: %s' % nodeName
      else :                                #
        print unknownSvr % locals()         # Mapped error message
        sys.exit( 1 )                       #   give up...
  else :                                    # Unrecognized processType
    print pTypeErr % locals()               #
    sys.exit( 1 )                           #

  #-------------------------------------------------------------------
  # Everything should be as good as we can verify.
  #-------------------------------------------------------------------

  #-------------------------------------------------------------------
  # convertToCluster
  # Notes:
  # - Any exception message (eMsg) should include a WebSphere message
  #   identifier of the form "ADMx####y" where x & y are letters and
  #   "####" is a four digit number.  For example:
  #   ADMG0248E:<serverName> exists within node <nodeName>.
  #-------------------------------------------------------------------
  # First, build the command parameter string, including any optional
  # values specified by the user, then, display the long form of the
  # command being executed...
  #-------------------------------------------------------------------
  if nodeName :
    cmdParms += ' --nodeName %(nodeName)s'

  parms = cmdParms % locals()
  print cmdName + ' ' + parms

  #-------------------------------------------------------------------
  # We (should) have all of the information required in order to
  # uniquely identify a specific server configuration ID.
  #-------------------------------------------------------------------
  id = AdminConfig.getid( '/Cell:%(cell)s/Node:%(nodeName)s/Server:%(servName)s/' % locals() )
  if len( id ) < 1 :                        #
    print getidErr % locals()               # Display mapped error message
    print 'cell: ' + cell                   # Provide all specified parms
    print 'node: ' + nodeName               #
    print 'server: ' + servName             #
    sys.exit( -1 )                          #

  try :
    clusterId = AdminConfig.convertToCluster( id, clustName  )
    print '%s completed successfully.' % cmdName
    try :
      AdminConfig.save()
      print 'Save complete.'
    except :
      print 'Error encountered during save: %s' % sys.exc_info()[ 1 ]
  except :
    eMsg = str( sys.exc_info()[ 1 ] )       # We only need the message
    pos  = eMsg.rfind( ': ADM' )            # Does it contain a msgID?
    if pos > -1 : eMsg = eMsg[ pos + 2: ]   # If so, use only it...
    print '%s failed: %s' % ( cmdName, eMsg )

#---------------------------------------------------------------------
# Name: parseOpts()
# Role: Process the user specified (command line) options
#---------------------------------------------------------------------
def parseOpts( cmdName ) :
  sOpts = 's:n:L:'                          # Short form option flags
  lOpts = 'serverName=,nodeName=,clusterName='.split( ',' )
  badOpt = '%(cmdName)s: Unknown/unrecognized parameter%(plural)s: %(argStr)s'
  optErr = '%(cmdName)s: Error encountered processing: %(argStr)s'

  #-------------------------------------------------------------------
  # Use the previously defined short and long form option values to
  # parse/process the user specified command line options.
  # Note: Should an unknown option be encountered, a GetoptError will
  #       be raised.
  #-------------------------------------------------------------------
  try :
    opts, args = getopt.getopt( sys.argv, sOpts, lOpts )
  except getopt.GetoptError :
    argStr = ' '.join( sys.argv )
    print optErr % locals()
    Usage( cmdName )                # print help information and exit

  #-------------------------------------------------------------------
  # Initialize the global Opts dictionary using keywords
  #-------------------------------------------------------------------
  for key in 'servName,nodeName,clustName'.split( ',' ) :
    Opts[ key ] = None

  #-------------------------------------------------------------------
  # process the list of options returned by getOpt()
  #-------------------------------------------------------------------
  for opt, val in opts :
    if opt in   ( '-s', '--serverName' )   : Opts[ 'servName' ] = val
    elif opt in ( '-n', '--nodeName' )     : Opts[ 'nodeName' ] = val
    elif opt in ( '-L', '--clusterName' )  : Opts[ 'clustName' ] = val

  #-------------------------------------------------------------------
  # Check for unhandled/unrecognized options
  #-------------------------------------------------------------------
  if ( args != [] ) :
    argStr = ' '.join( args )
    if len( args ) > 1 :
      plural = 's'
    else :
      plural = ''
    print badOpt % locals()
    Usage( cmdName )

#---------------------------------------------------------------------
# Name: Usage()
# Role: Provide details about how this script should be used
#---------------------------------------------------------------------
def Usage( cmdName ) :
  print '''
Command: %(cmdName)s\n
Purpose: WebSphere (wsadmin) script used to create a new cluster having the
         user specified name, and using the specified application server as
         the first cluster member.\n
  Usage: %(cmdName)s [options]\n
Required switches:
  -L | --clusterName  <text> = Name of new cluster to be created
  -s | --serverName   <name> = Name of server to be used/added to cluster\n
Optional switches:
  -n | --nodeName     <name> = Name of node on which server exists\n
Notes:
- Long form option values may be separated/delimited from their associated
  value using either a space, or an equal sign ('=').\n
- Short form option values may be sepearated from their associated value using
  an optional space.\n
- The short form option letter c is used by wsadmin, and is therefore
  unavailable to scripts.\n
Examples:
  wsadmin -lang jython -f %(cmdName)s.py --serverName=s1 --clusterName C1\n
  wsadmin -lang jython -f %(cmdName)s.py -ss1 -L C1 -n node01''' % locals()
  sys.exit( 1 )

#---------------------------------------------------------------------
# main entry point - verify that script is executed, not imported
#---------------------------------------------------------------------
if ( __name__ == 'main' ) | ( __name__ == '__main__' ) :
  convertToCluster()
else :
  Usage( __name__ )
