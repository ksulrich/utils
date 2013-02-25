#---------------------------------------------------------------------
#    Name: TraceService.py
#    From: WebSphere Application Server Administration using Jython
#      By: Robert A. (Bob) Gibson [rag], Arthur Kevin McGrath, Noel J. Bergman
#    ISBN: 0-13-700952-6
#    Role: Script used to enable/disable WebContainer tracing
#   Usage: wsadmin -lang jython -f TraceService.py [options]
#   Parms: See Usage routine for more details
# History:
#   Date    who ver what
# --------  --- --- ----------
# 09/09/19  rag 0.3 Add: ISBN information
# 08/11/11  rag 0.2 Fix: Review & cleanup for book, including code
#                        dealing with nodeName verification.
# 08/04/30  rag 0.1 Fix: Allow "word" characters in names, not just
#                        alphanumeric characters
# 08/02/29  rag 0.0 New
#---------------------------------------------------------------------
import getopt, sys, re

#---------------------------------------------------------------------
# Global dictionary to hold the user specified options & values
#---------------------------------------------------------------------
Opts = {}

#---------------------------------------------------------------------
# Name: validWord
# Role: Verify that the specified name, contains at least 1 char, and
#       only uses "word" characters (i.e., [a-zA-Z0-9_])
#---------------------------------------------------------------------
def validWord( name ) :
  return ( re.search( re.compile( r'^\w+$' ), name ) != None )

#---------------------------------------------------------------------
# User defined exception
#---------------------------------------------------------------------
class Error( Exception ) :
  '''Base class for exceptions in this module.'''
  def __init__( self, value ) :
    self.value = value
  def __str__( self ) :
    return repr( self.value )

#---------------------------------------------------------------------
# Name: parseOpts()
# Role: Process the user specified (command line) options
#---------------------------------------------------------------------
def parseOpts( cmdName ) :
  from string import lower
  sOpts = 'bdeI:lm:n:N:o:rs:t:z:'
  lOpts = ( 'memBuffer,disable,enable,histFiles=,logFile,mBuffSize=,nodeName=' + \
            'fileName=,recycle,serverName=,traceFormat=,traceStr=,fileSize=' ) \
          .split( ',' )
  noOpt  = '%(cmdName)s: Required option missing'
  badOpt = '%(cmdName)s: Unknown/unrecognized parameter%(plural)s: %(argStr)s'
  optErr = '%(cmdName)s: Error encountered processing parameter string: %(argStr)s'

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
  # Initialize the global Opts dictionary using the following keywords
  #-------------------------------------------------------------------
  keys = ( 'memBuffer,disable,enable,histFiles,logFile,mBuffSize,nodeName,' + \
           'fileName,recycle,traceFormat,servName,traceStr,fileSize' ).split( ',' )
  for key in keys : Opts[ key ] = None

  #-------------------------------------------------------------------
  # process the list of options returned by getOpt()
  #-------------------------------------------------------------------
  for opt, val in opts :
    if opt   in ( '-b', '--memBuffer'   ) : Opts[ 'memBuffer'   ] =   1
    elif opt in ( '-d', '--disable'     ) : Opts[ 'disable'     ] =   1
    elif opt in ( '-e', '--enable'      ) : Opts[ 'enable'      ] =   1
    elif opt in ( '-I', '--histFiles'   ) : Opts[ 'histFiles'   ] = val
    elif opt in ( '-l', '--logFile'     ) : Opts[ 'logFile'     ] =   1
    elif opt in ( '-m', '--mBuffSize'   ) : Opts[ 'mBuffSize'   ] = val
    elif opt in ( '-n', '--nodeName'    ) : Opts[ 'nodeName'    ] = val
    elif opt in ( '-N', '--fileName'    ) : Opts[ 'fileName'    ] = val
    elif opt in ( '-o', '--traceFormat' ) : Opts[ 'traceFormat' ] = val
    elif opt in ( '-r', '--recycle'     ) : Opts[ 'recycle'     ] =   1
    elif opt in ( '-s', '--serverName'  ) : Opts[ 'servName'    ] = val
    elif opt in ( '-t', '--traceStr'    ) : Opts[ 'traceStr'    ] = val
    elif opt in ( '-z', '--fileSize'    ) : Opts[ 'fileSize'    ] = val

  #-------------------------------------------------------------------
  # Check for missing, or unhandled/unrecognized options
  #-------------------------------------------------------------------
  if ( args != [] ) :
    argStr = ' '.join( args )
    plural = ''
    if ( len( args ) > 1 ) : plural = 's'
    print badOpt % locals()
    Usage( cmdName )

#---------------------------------------------------------------------
# Name: Usage()
# Role: Provide details about how this script is to be used
#---------------------------------------------------------------------
def Usage( cmdName ) :
  print '''
Command: %(cmdName)s\n
Purpose: WebSphere (wsadmin) script used to display/modify the WebSphere
         Application Server TraceService settings.\n
  Usage: %(cmdName)s [options]\n
Required switches:
  -s | --serverName   <name>  = name of target Application Server\n
Optional switches:
  -n | --nodeName     <name>  = Name of node on which server exists
  -o | --traceFormat  [B|A|L] = Basic, Advanced, or LogAnalyzer format
  -r | --recycle              = Stop and restart the specified server
  -t | --traceStr     <data>  = trace string to be used on restart\n
Mutually exclusive options:
  -e | --enable               = enable  the log service
  -d | --disable              = disable the log service\n
Mutually exclusive options:
  -b | --memBuffer            = use memory buffer tracing
  -l | --logFile              = use output file tracing\n
Memory Buffer setting:
  -m | --mBuffSize    <#>     = Memory Buffer Size (thousand entries)\n
Output File settings:
  -z | --fileSize     <#>     = Maximum FileSize (MB)
  -I | --histFiles    <#>     = Maximum # of Historical files
  -N | --fileName     <name>  = Output filename\n
Notes:
- Long form option values may be separated/delimited from their associated
  value using either a space, or an equal sign ('=').\n
- Short form option values may be sepearated from their associated value using
  an optional space.\n
Examples:
  wsadmin -lang jython -f %(cmdName)s.py --serverName=s1 --disable --recycle\n
  wsadmin -f %(cmdName)s.py -e -l -I 5 -r -s s1 -N %(cmdName)s.out -t "*=info"
''' % locals()
  sys.exit( 1 )

#---------------------------------------------------------------------
# Name: TraceService()
# Role: routine used to implement desired action
#---------------------------------------------------------------------
def TraceService( cmdName = 'TraceService' ) :
  argc = len( sys.argv )                    # Number of arguments supplied
  if ( argc < 1 ) :                         #
    print '%s: Insufficient parameters provided.' % cmdName
    Usage( cmdName )
  else :                                    # otherwise
    parseOpts( cmdName )                    #   parse the command line

  #-------------------------------------------------------------------
  # Assign values from the user Options dictionary, to make value
  # access simplier, and easier.  For example, instead of using:
  #   Opts[ 'servName' ]
  # we will be able to simply use:
  #   servName
  # to access the value.  Additionally, this allows us to make use of
  # mapped error messages (e.g., see unknownNode below).
  #-------------------------------------------------------------------
  for key in Opts.keys() :
    cmd = '%s=Opts["%s"]' % ( key, key )
    exec( cmd )

  #-------------------------------------------------------------------
  # verify the required parameters have valid (alphanumeric) values
  # Note: We check for None first, so that we don't cause an exception
  #       later
  #-------------------------------------------------------------------
  if not servName or not validWord( servName ) :
    print 'Missing or invalid required parameter: --serverName'
    Usage( cmdName )

  #-------------------------------------------------------------------
  # check for mutually exclusive options
  #-------------------------------------------------------------------
  if ( ( disable == 1 ) and ( enable == 1 ) ) or \
     ( ( memBuffer == 1 ) and ( logFile == 1 ) ) :
    print '%s: Mutually exclusive options specified.' % cmdName
    Usage( cmdName )

  #-------------------------------------------------------------------
  # Define the mapped error messages.
  # Note: A mapped "error" message is one that contains the name of
  #       local variables that should be used during the generation
  #       of the message to display specific values.  For example,
  #         print "%(cmdName)s" % locals()
  #       is interpreted as though we had typed:
  #         print "%s" % cmdName
  #-------------------------------------------------------------------
  nodeNameErr = '%(cmdName)s failed: nodeName is undefined, and indeterminate'
  pTypeErr    = 'Unrecognized processType: %(pType)s'
  unknownNode = '%(cmdName)s failed: Unknown nodeName: %(nodeName)s'
  NDnodeName  = '%(cmdName)s failed: Deployment Manager nodeName not allowed: %(nodeName)s'
  unknownSvr  = '%(cmdName)s failed: Unknown serverName: %(servName)s'
  nonnumMS    = '%(cmdName)s warning: Non-numeric memoryBufferSize "%(mBuffSize)s" ignored.'
  nonnumFS    = '%(cmdName)s warning: Non-numeric Maximum File Size "%(fileSize)s" ignored.'
  nonnumHF    = '%(cmdName)s warning: Non-numeric Historical Files "%(histFiles)s" ignored.'
  badTF       = '%(cmdName)s warning: Invalid/unrecognized traceFormat value "%(traceFormat)s" ignored.'

  #-------------------------------------------------------------------
  # Which server did the user specify?
  #-------------------------------------------------------------------
  try :
    #-----------------------------------------------------------------
    # First, we need to find out if we are connected to a Base, or ND
    # (Network Deployment) node.  To do so, we look for the process type
    # (processType) attribute of the current node.  However, to obtain
    # this we must first get the completeObjectName for this node (from
    # the server object - sObj).
    #-----------------------------------------------------------------
    cell   = AdminControl.getCell()         # current cell name
    NDnode = AdminControl.getNode()         # current node Name
    sObj   = AdminControl.completeObjectName( 'cell=%s,node=%s,type=Server,*' % ( cell, NDnode ) )
    pType  = AdminControl.getAttribute( sObj, 'processType' )

    #-----------------------------------------------------------------
    # processType of the current node
    #-----------------------------------------------------------------
    if pType == 'UnManagedProcess' :
      #---------------------------------------------------------------
      # If target nodeName is None, use current node as target
      #---------------------------------------------------------------
      if not nodeName :                     #
        nodeName = NDnode                   # Default to current node
      elif nodeName != NDnode :             # Was the right one given?
        raise Error( unknownNode % locals() )
    elif pType == 'DeploymentManager' :
      #---------------------------------------------------------------
      # Since we're connected to the Deployment Manager, we need to
      # verify that the nodeName is either known, or unambiguous.
      # Note: nodeNames is the list of known nodes, and is build using
      #       list comprehension.  Each node configID starts with the
      #       nodeName, followed by '('
      #---------------------------------------------------------------
      nodeList  = AdminConfig.list( 'Node' ).splitlines()
      nodeNames = [ x.split( '(' )[ 0 ] for x in nodeList ]

      #---------------------------------------------------------------
      # If a nodeName wasn't specified, can we determine it?
      #---------------------------------------------------------------
      if not nodeName :
        #-------------------------------------------------------------
        # No, do we have the sitatution where exactly 2 nodes exist?
        # If so, then 1 is for the DeploymentManager and the other is
        # for the Application Server.  We "assume" that the user wants
        # to create the server on this "other" node.
        #-------------------------------------------------------------
        if len( nodeList ) == 2 :             # Can we determine it?
          #-----------------------------------------------------------
          # Locate (and save) the non-ND node name
          #-----------------------------------------------------------
          for nodeID in nodeList :
            nName = AdminConfig.showAttribute( nodeID, 'name' )
            if nName != node :              # Is this the ND node?
              nodeName = nName              # No, use it
        else :
          raise Error( nodeNameErr % locals() )
      elif nodeName == NDnode :             # Was ND nodeName specified?
        raise Error( NDnodeName % locals() )
      elif nodeName not in nodeNames :
        raise Error( unknownNode % locals() )
    else :                                  #
      raise Error( pTypeErr % locals() )    # Unrecognized processType
    #-----------------------------------------------------------------
    # Get the server id for the (user specified) Application Server
    # Note: fqs == fully qualified server
    #-----------------------------------------------------------------
    fqs = '/Cell:%(cell)s/Node:%(nodeName)s/Server:%(servName)s/' % locals()
    sID = AdminConfig.getid( fqs )          # Does the server exist?
    if sID == '' : raise Error( unknownSvr % locals() )

    ts  = AdminConfig.list( 'TraceService', sID )
    tl  = AdminConfig.list( 'TraceLog', ts )

    TSchanges = []
    #-----------------------------------------------------------------
    # Change trace state?
    #-----------------------------------------------------------------
    if ( disable == 1 ) or ( enable == 1 ) :
      if enable == 1 :
        enabled = 'true'
      else :
        enabled = 'false'
      TSchanges.append( [ 'enable', enabled ] )

    #-----------------------------------------------------------------
    # Change traceOutputType?
    #-----------------------------------------------------------------
    if ( memBuffer == 1 ) or ( logFile == 1 ) :
      if memBuffer == 1 :
        tOT = 'MEMORY_BUFFER'
      else :
        tOT = 'SPECIFIED_FILE'
      TSchanges.append( [ 'traceOutputType', tOT ] )

    #-----------------------------------------------------------------
    # Change memoryBufferSize?
    #-----------------------------------------------------------------
    if ( mBuffSize != None ) :
      if ( mBuffSize.isdigit() ) :
        TSchanges.append( [ 'memoryBufferSize', mBuffSize ] )
      else :
       print nonnumMS % locals()

    #-----------------------------------------------------------------
    # Change traceFormat?
    #-----------------------------------------------------------------
    if ( traceFormat != None ) :
      tf = ''
      if traceFormat.upper() == 'B'   : tf = 'BASIC'
      elif traceFormat.upper() == 'A' : tf = 'ADVANCED'
      elif traceFormat.upper() == 'L' : tf = 'LOG_ANALYZER'
      if tf != '' :
        TSchanges.append( [ 'traceFormat', tf ] )
      else :
        print badTF % locals()

    #-----------------------------------------------------------------
    # Change traceString?
    #-----------------------------------------------------------------
    if ( traceStr != None ) :
      TSchanges.append( [ 'startupTraceSpecification', traceStr ] )

    TLchanges = []
    #-----------------------------------------------------------------
    # Change fileSize value?
    #-----------------------------------------------------------------
    if ( fileSize != None ) :
      if ( fileSize.isdigit() ) :
        TLchanges.append( [ 'rolloverSize', fileSize ] )
      else :
        print nonnumSS % locals()

    #-----------------------------------------------------------------
    # Change histFiles?
    #-----------------------------------------------------------------
    if ( histFiles != None ) :
      if ( histFiles.isdigit() ) :
        TLchanges.append( [ 'maxNumberOfBackupFiles', histFiles ] )
      else :
        print nonnumHF % locals()

    #-----------------------------------------------------------------
    # Change fileName?
    #-----------------------------------------------------------------
    if ( fileName != None ) :
      TLchanges.append( [ 'fileName', fileName ] )

    #-----------------------------------------------------------------
    # Make the requested changes
    #-----------------------------------------------------------------
    if ( TSchanges != [] ) :
      AdminConfig.modify( ts, TSchanges )

    if ( TLchanges != [] ) :
      AdminConfig.modify( tl, TLchanges )

    if ( ( TSchanges != [] ) or ( TLchanges != [] ) ) :
      AdminConfig.save()

    #-----------------------------------------------------------------
    # Parse the TraceService and TraceLog values, displaying only the
    # one of interest
    # Note: Use a RegExp to match and extract the name / value pair
    #-----------------------------------------------------------------
    fields = { 'enable'                    : 'Log enabled',
               'fileName'                  : 'File Name',
               'maxNumberOfBackupFiles'    : 'Max # of Historical Files',
               'memoryBufferSize'          : 'Maximum Buffer Size',
               'rolloverSize'              : 'Maximum File Size',
               'startupTraceSpecification' : 'Trace Specification',
               'traceFormat'               : 'Trace Output Format',
               'traceOutputType'           : 'Trace output type'
             }
    pair = re.compile( r'\[\s*(\w+)\s+([=:*.\w]+)]$' )
    for TS in AdminConfig.show( ts ).splitlines() :
      m = pair.match( TS )
      if m :
        ( name, value ) =  m.groups()
        print '%25s : %s' % ( fields[ name ], value )

    pair = re.compile( r'\[\s*(\w+)\s+([\${}\/\\=:*.\w]+)]$' )
    for TL in AdminConfig.show( tl ).splitlines() :
      m = pair.match( TL )
      if m :
        ( name, value ) =  m.groups()
        print '%25s : %s' % ( fields[ name ], value )

    #-----------------------------------------------------------------
    # Recycle requested?
    # Note: This option is only allowed/supported on an ND node...
    #-----------------------------------------------------------------
    if ( recycle == 1 ) :
      if pType == 'DeploymentManager' :

        #-------------------------------------------------------------
        # First, we try to stop the specified server.
        # Note: If the server is stopped, this is not an error
        #-------------------------------------------------------------
        try :
          print 'Stopping server %s' % servName
          AdminControl.stopServer( servName, nodeName )
          result = 'was successful'
        except :
          result = 'failed - was it already stopped?'
        print 'Stopping of server %s %s' % ( servName, result )

        #-------------------------------------------------------------
        # Now, try to start it...
        #-------------------------------------------------------------
        try :
          print 'Starting server %s' % servName
          AdminControl.startServer( servName, nodeName )
          result = 'was successful'
        except :
          result = 'failed - is the nodeagent running?'
        print 'Restart of server %s %s' % ( servName, result )

      else :
        raise Error( 'The recycle request is not supported when processType = "%s"' % pType )

  except Error, e :
    print e.value
  except :
    ( kind, value ) = sys.exc_info()[ :2 ]
    ( kind, value ) = str( kind ), str( value )
    notAvail = 'AdminControl service not available'
    if value.endswith( notAvail ) :
      print '%(cmdName)s error: %(notAvail)s\nA server connection is required.' % locals()
    else :
      print '%(cmdName)s error:\n Type: %(kind)s\n Value: %(value)s' % locals()

#---------------------------------------------------------------------
# main - verify that script was executed & not imported
#---------------------------------------------------------------------
if ( __name__ == 'main' ) or ( __name__ == '__main__' ) :
  TraceService()
else :
  Usage( __name__ )
