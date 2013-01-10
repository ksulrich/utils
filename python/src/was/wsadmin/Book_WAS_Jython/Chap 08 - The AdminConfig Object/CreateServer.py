#---------------------------------------------------------------------
#    Name: CreateServer.py
#    From: WebSphere Application Server Administration using Jython
#      By: Robert A. (Bob) Gibson [rag], Arthur Kevin McGrath, Noel J. Bergman
#    ISBN: 0-13-700952-6
#    Role: Script used to create an application server on the user
#          specified node using a existing ApplicationServer template
#   Usage: wsadmin -lang jython -f CreateServer.py [options]
#    Note: See Usage routine for more details
# History:
#   date   ver who what
# -------- --- --- ----------------------------------------------------
# 09/10/29 0.3 rag Fix - Added ISBN detail
# 08/10/29 0.2 rag Fix: if > 2 nodes -n nodeName didn't work
#                       -t default - didn't work
# 08/04/30 0.1 rag Fix: Allow "word" characters in names, not just
#                       alphanumeric characters
# 08/02/29 0.0 rag New - for Impact 2008
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
def validWord( name ):
  import re
  return ( re.search( re.compile( r'^\w+$' ), name ) != None )

#---------------------------------------------------------------------
# Name: CreateServer
# Role: routine used to implement desired action
#---------------------------------------------------------------------
def CreateServer( cmdName = 'CreateServer' ) :
  argc = len( sys.argv )                    # Number of arguments
  if ( argc < 2 ) :                         # If too few are present,
    print '%s: Insufficient parameters provided.' % cmdName
    Usage( cmdName )                        #   provide the Usage info
  else :                                    # otherwise
    parseOpts( cmdName )                    #   parse the command line

  #-------------------------------------------------------------------
  # Assign values from the user Options dictionary.  To make value
  # access simplier.  For example, instead of using:
  #   Opts[ 'servName' ]
  # we will be able to simply use:
  #   servName
  # to access the value.  In addition, we can make use of these names
  # in any mapped messages, see unknownNode below.
  #-------------------------------------------------------------------
  for key in Opts.keys() :
    cmd = str( key ) + ' = Opts[ "' + str( key ) + '" ]'
    exec( cmd )

  #-------------------------------------------------------------------
  # verify the required parameters have valid (alphanumeric) values
  # Note: We check that servName is not None first, so that we don't
  #       cause an exception later.
  #-------------------------------------------------------------------
  if not servName or not validWord( servName ) :
    print 'Missing or invalid required parameter: --serverName'
    Usage( cmdName )

  if not tempName or not validWord( tempName ) :
    print 'Missing or invalid required parameter: --templateName'
    Usage( cmdName )

  #-------------------------------------------------------------------
  # verify that nodeName, if provided, is valid (alphanumeric)
  #-------------------------------------------------------------------
  if nodeName and not validWord( nodeName ) :
    print 'Invalid nodeName value: ' + str( nodeName )
    Usage( cmdName )

  #-------------------------------------------------------------------
  # If we get here, we have valid serverName and/or default options.
  # So, now we need to find out if we are connected to a Base, or
  # Network Deployment (ND) node.  To do so, we look for the process
  # type (processType) of the current node.  However, to obtain this
  # we must first get the completeObjectName for this node (i.e.,
  # the server object aka sObj).
  #-------------------------------------------------------------------
  cell  = AdminControl.getCell()            # What's the cell Name?
  node  = AdminControl.getNode()            # What's the node Name?
  sObj  = AdminControl.completeObjectName( 'cell=%s,node=%s,type=Server,*' % ( cell, node ) )
  pType = AdminControl.getAttribute( sObj, 'processType' )

  #-------------------------------------------------------------------
  # Define the mapped error messages.
  # Note: A mapped "error" message is one that contains the name of
  #       local variables that should be used during the generation
  #       of the message to display specific values.  For example,
  #         print "%(cmdName)s" % locals()
  #       is interpreted as though we had typed::
  #         print "%s" % cmdName
  #-------------------------------------------------------------------
  cmdParms    = '--serverName %(servName)s --nodeName %(nodeName)s --templateName %(tempName)s'
  nodeNameErr = '%(cmdName)s failed: nodeName is undefined, and indeterminate'
  unknownNode = '%(cmdName)s failed: Unknown nodeName: %(nodeName)s'
  NDnodeName  = '%(cmdName)s failed: Deployment Manager nodeName not allowed: %(nodeName)s'
  unknownTemp = '%(cmdName)s failed: Unknown templateName: %(tempName)s'
  pTypeErr    = 'Unrecognized processType: %(pType)s'

  #-------------------------------------------------------------------
  # For an unManagedProcess, we are working with a single node, so
  # either nodeName is None (meaning use this node), or it must match
  # the name of the node to which we are connected.
  #-------------------------------------------------------------------
  if pType == 'UnManagedProcess' :
    #-----------------------------------------------------------------
    # If target nodeName is None, use current node as target
    #-----------------------------------------------------------------
    if not nodeName :                       #
      nodeName = node                       # Default to current node
    elif nodeName != node :                 # Was the right one given?
      print unknownNode % locals()          # Mapped error message
      sys.exit( 1 )                         # give up...
  elif pType == 'DeploymentManager' :       #
    #-----------------------------------------------------------------
    # Since we're connected to the Deployment Manager, we need to
    # verify that the nodeName is either known, or unambiguous.
    # Note: nodeNames is the list of known nodes, and is build using
    #       list comprehension.  Each node configID starts with the
    #       nodeName, followed by '('
    #-----------------------------------------------------------------
    nodeList  = AdminConfig.list( 'Node' ).splitlines()
    nodeNames = [ x.split( '(' )[ 0 ] for x in nodeList ]

    #-----------------------------------------------------------------
    # If a nodeName wasn't specified, can we determine it?
    #-----------------------------------------------------------------
    if not nodeName :
      #---------------------------------------------------------------
      # No, do we have the sitatution where exactly 2 nodes exist?
      # If so, then 1 is for the DeploymentManager and the other is
      # for the Application Server.  We "assume" that the user wants
      # to create the server on this "other" node.
      #---------------------------------------------------------------
      if len( nodeList ) == 2 :             # Can we determine it?
        #---------------------------------------------------------------
        # Locate (and save) the non-ND node name
        #---------------------------------------------------------------
        for nodeID in nodeList :            #
          nName = AdminConfig.showAttribute( nodeID, 'name' )
          if nName != node :                # Is this the ND node?
            nodeName = nName                # No, use it
      else :                                #
        print nodeNameErr % locals()        #
        sys.exit( 1 )                       #
    elif nodeName == node :                 # Was ND nodeName specified?
      print NDnodeName % locals()           #
      sys.exit( 1 )                         #
    elif nodeName not in nodeNames :        #
      print unknownNode % locals()          #
      sys.exit( 1 )                         #
  else :                                    # Unrecognized processType
    print pTypeErr % locals()               #
    sys.exit( 1 )                           #

  #-------------------------------------------------------------------
  # tempList  = the list of APPLICATION_SERVER templates.
  # tempNames = Use list comprehension to get the template names from
  #             these template config IDs
  #-------------------------------------------------------------------
  tempList  = str( AdminConfig.listTemplates( 'Server', 'APPLICATION_SERVER' ) ).splitlines()
  tempNames = [ x.split( '(' )[ 0 ] for x in tempList ]
  if tempName in tempNames :                # Is tempName in the list?
    tempID = tempList[ tempNames.index( tempName ) ]
  else :                                    #
    print unknownTemp % locals()            #
    sys.exit( 1 )                           #

  #-------------------------------------------------------------------
  # Everything should be as good as we can verify.  So, before we try
  # the creation, we need to obtain the configID of the specified node
  #-------------------------------------------------------------------
  nodeID = AdminConfig.getid( '/Node:%s/' % nodeName )

  #-------------------------------------------------------------------
  # Create "Application Server" using a known template ID
  # Notes:
  # - Any exception message (eMsg) should include a WebSphere message
  #   identifier of the form "ADMx####y" where x & y are letters and
  #   "####" is a four digit number.  For example:
  #   ADMG0248E:<serverName> exists within node <nodeName>.
  #-------------------------------------------------------------------
  # First, build the command parameter string, including any optional
  # values specified by the user
  #-------------------------------------------------------------------
  parms = cmdParms % locals()
  if descript :
    parms += ' --description "%s"' % descript
  print cmdName + ' ' + parms

  try :
    AdminConfig.createUsingTemplate( 'Server', nodeID, [[ 'name', servName ]], tempID )
    print '%s completed successfully' % cmdName
    try :
      AdminConfig.save()
      print 'Save complete'
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
  sOpts = 's:t:n:d:'                        # Short form option flags
  lOpts = 'serverName=,templateName=,nodeName=,description='.split( ',' )
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
  except getopt.GetoptError:
    argStr = ' '.join( sys.argv )
    print optErr % locals()
    Usage( cmdName )                # print help information and exit:

  #-------------------------------------------------------------------
  # Initialize the global Opts dictionary using the following keywords
  #-------------------------------------------------------------------
  keys = 'servName,tempName,nodeName,descript'.split( ',' )
  for key in keys : Opts[ key ] = None

  #-------------------------------------------------------------------
  # process the list of options returned by getOpt()
  #-------------------------------------------------------------------
  for opt, val in opts :
    if opt in   ( '-s', '--serverName' )   : Opts[ 'servName' ] = val
    elif opt in ( '-t', '--templateName' ) : Opts[ 'tempName' ] = val
    elif opt in ( '-n', '--nodeName' )     : Opts[ 'nodeName' ] = val
    elif opt in ( '-d', '--description' )  : Opts[ 'descript' ] = val

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
# Role: Provide details about how this script is to be used
#---------------------------------------------------------------------
def Usage( cmdName ) :
  print '''
Command: %s\n
Purpose: WebSphere (wsadmin) script used to create an Application Server
         using an existing Appliction Server template.\n
  Usage: %s [options]\n
Required switches:
  -s | --serverName   <name> = Name of server to be created
  -t | --templateName <name> = Name of template to be used\n
Optional switches:
  -d | --description  <text> = Text to be associated with server
  -n | --nodeName     <name> = Name of node on which server should be created\n
Notes:
- Long form option values may be separated/delimited from their associated
  value using either a space, or an equal sign ('=').\n
- Short form option values may be sepearated from their associated value using
  an optional space.\n
- Description text containing blanks should be enclosed in double quotes.\n
Examples:
  wsadmin -lang jython -f %s.py --serverName=s1 --templateName T1\n
  wsadmin -lang jython -f %s.py -ss1 -t T1 -d "My AppServer"
''' % ( ( cmdName, ) * 4 )
  sys.exit( 1 )

#---------------------------------------------------------------------
# main entry point - verify that script is executed, not imported
#---------------------------------------------------------------------
if ( __name__ == 'main' ) or ( __name__ == '__main__' ) :
  CreateServer()
else :
  Usage( __name__ )
