#---------------------------------------------------------------------
# Name: createClusterMember
# Role: Example script, created from scratch.
#       Iteration 4 - Check that the specified member doesn't exist on
#                     the specified node.
#---------------------------------------------------------------------
import getopt, sys;
from WAuJ_utilities import showAsDict;

#---------------------------------------------------------------------
# Global dictionary to hold the user specified options & values
#---------------------------------------------------------------------
Opts = {};

#---------------------------------------------------------------------
# Name: parseOpts()
# Role: Process the user specified (command line) options
#---------------------------------------------------------------------
def parseOpts( cmdName ) :
  sOpts  = 'L:m:n:';
  lOpts  = 'clusterName=,memberName=,nodeName='.split( ',' );
  badOpt = '%(cmdName)s: Unknown/unrecognized parameter%(plural)s: %(argStr)s';
  optErr = '%(cmdName)s: Parameter error: %(argStr)s [unknown parameters?]';

  try :
    opts, args = getopt.getopt( sys.argv, sOpts, lOpts );
  except getopt.GetoptError :
    argStr = ' '.join( sys.argv );
    print optErr % locals();
    Usage( cmdName );

  #-------------------------------------------------------------------
  # Initialize the global Opts dictionary using these keys (indexes)
  #-------------------------------------------------------------------
  keys = 'clusterName,memberName,nodeName'.split( ',' );
  for key in keys : Opts[ key ] = None;

  #-------------------------------------------------------------------
  # Process the list of options returned by getOpt()
  #-------------------------------------------------------------------
  for opt, val in opts :
    if opt in   ( '-L', '--clusterName' ) : Opts[ 'clusterName' ] = val
    elif opt in ( '-m', '--memberName' )  : Opts[ 'memberName' ] = val
    elif opt in ( '-n', '--nodeName' )    : Opts[ 'nodeName' ] = val


  #-------------------------------------------------------------------
  # Check for unhandled/unrecognized options
  #-------------------------------------------------------------------
  if ( args != [] ) :        # If any unhandled parms exist => error
    argStr = ' '.join( args )
    plural = ''
    if ( len( args ) > 1 ) : plural = 's'
    print badOpt % locals()
    Usage( cmdName )

#---------------------------------------------------------------------
# Name: Usage()
# Role: Display script usage information, and exit (terminate script)
#---------------------------------------------------------------------
def Usage( cmdName ):
  print '''
Command: %(cmdName)s\n
Purpose: WebSphere (wsadmin) script used to create a new cluster member.
  Usage: %(cmdName)s [options]\n
Required switches:
  -L | --clusterName <name> = Name of existing cluster to which member
                              is to be added.
  -m | --memberName  <name> = Name of member to be created
  -n | --nodeName    <name> = Name of node onto which member is to be
                              created.
\nNotes:
- Long form option values may be separated/delimited from their associated
  value using either a space, or an equal sign ('=').\n
- Short form option values may be sepearated from their associated value using
  an optional space.\n
- Text containing blanks should be enclosed in double quotes.\n
Examples:  [Note: all of the following should examples be entered on one line.]
  wsadmin -lang jython -f %(cmdName)s.py --clusterName=C1 --nodeName N1 --memberName M1\n
  wsadmin -lang jython -f %(cmdName)s.py -LC1 -m M1 -n Node01
''' % locals()
  sys.exit( 1 )

#---------------------------------------------------------------------
# Name: getConfigIDs()
# Role: Function used find, and return a string containing all
#       matching configuration IDs.
# e.g., We can have multiple Cluster Members with the same name as
#       long as each name is unique to the node on which it is
#       configured.
#---------------------------------------------------------------------
def getConfigIDs( name, dataType, scopeID = None ) :
  result = [];                              # Start with an empty list
  if scopeID :                              # If a scope configID is provided...
    items = AdminConfig.list( dataType, scopeID );
  else :                                    #
    items = AdminConfig.list( dataType );   # unscoped item list
  for configID in items.splitlines() :      # Process each configID
    ID = configID                           # Leave configID alone...
    if ( ID[ 0 ] == '"' ) and ( ID[ -1 ] == '"' ) :
      ID = ID[ 1:-1 ];                      # Strip leading/trailing quotes
    if name == ID.split( '(', 1 )[ 0 ] :    # Does this config name match?
      result.append( configID );            #   Yes - Specified  name found
  return '\n'.join( result );               # Return string of all matches

#----------------------------------------------------------------------
# Name: localMode()
# Role: Return true (1) if the script is currently executing in "local
#       mode", false (0) otherwise.
# Note: It is possible for the connection to the server to be dropped,
#       in which case, this routine will return true
#----------------------------------------------------------------------
def localMode() :
  result = 0;
  try :
    AdminControl.getType();
  except :
    result = 1;
  return result;

#---------------------------------------------------------------------
# Name: DMpresent()
# Role: Determine if any of the available server types is a Deployment
#       Manager (DM)
# Note: Returns true (1) if any of the available servers is a DM,
#       otherwise, returns false (0)
#---------------------------------------------------------------------
def DMpresent() :
  for serverID in AdminConfig.list( 'Server' ).splitlines() :
    if showAsDict( serverID )[ 'serverType' ] == 'DEPLOYMENT_MANAGER' :
      return 1
  return 0
     
#---------------------------------------------------------------------
# Name: createClusterMember()
# Role: Function used to create a new cluster member
#---------------------------------------------------------------------
def createClusterMember( cmdName = 'createClusterMember' ) :
  fewParms = '%(cmdName)s: Insufficient parameters provided.';
  required = '%(cmdName)s: Required parameter missing: %(parm)s';
  badClust = '%(cmdName)s: Unknown cluster %(clusterName)s';
  ambClust = '%(cmdName)s: Ambiguous cluster %(clusterName)s';
  badNode  = '%(cmdName)s: Unknown node %(nodeName)s';
  conflict = '%(cmdName)s: Specified member %(memberName)s already exists.';
  DMreqd   = '%(cmdName)s: A Deployment Manager is required.';

  argc = len( sys.argv );                   # Number of arguments
  if ( argc < 3 ) :                         # If too few are present,
    print fewParms % locals();              #   tell the user, and
    Usage( cmdName );                       #   provide the Usage info
  else :                                    # otherwise
    parseOpts( cmdName );                   #   parse the command line

  #-------------------------------------------------------------------
  # Assign values from the user Options dictionary, to make value
  # access simplier, and easier.  For example, instead of using:
  #   Opts[ 'clusterName' ]
  # we will be able to simply use:
  #   clusterName
  # to access the value.  Additionally, this allows us to make use of
  # mapped error messages (e.g., see "required" above & below).
  #-------------------------------------------------------------------
  for key in Opts.keys() :
    cmd = '%s=Opts["%s"]' % ( key, key );
    exec( cmd );

  #-------------------------------------------------------------------
  # Verify that all required parameters have been specified.
  #-------------------------------------------------------------------
  error = 0;
  for parm in 'clusterName,memberName,nodeName'.split( ',' ) :
    if not Opts[ parm ] :
      print required % locals();
      error += 1;
      
  if error > 0 :
    Usage( cmdName );
  
  #-------------------------------------------------------------------
  # Result of parsing command line parameters
  #-------------------------------------------------------------------
  parms = '%(cmdName)s: --clusterName %(clusterName)s --memberName %(memberName)s --nodeName %(nodeName)s';
  print parms % locals();

  #-------------------------------------------------------------------
  # Does the cluster exist?
  #-------------------------------------------------------------------
  clusterID = getConfigIDs( clusterName, 'ServerCluster' );
  if clusterID == '' :
    print badClust % locals();
    Usage( cmdName );

  #-------------------------------------------------------------------
  # Is it possible for getConfigIDs() to return multiple clusters with
  # the same name?  I don't think so, but it is really easy to check
  # for...
  #-------------------------------------------------------------------
  if len( clusterID.splitlines() ) > 1 :
    print ambClust % locals();
    Usage( cmdName );

  #-------------------------------------------------------------------
  # Does the node exist?
  #-------------------------------------------------------------------
  nodeID = getConfigIDs( nodeName, 'Node' );
  if nodeID == '' :
    print badNode % locals();
    Usage( cmdName );

  #-------------------------------------------------------------------
  # Is it possible for getConfigIDs() to return multiple nodes with
  # the same name?  No, not really.  However, it is really easy to add
  # a check for an ambiguous result.
  #-------------------------------------------------------------------
  if len( nodeID.splitlines() ) > 1 :
    print ambNode % locals();
    Usage( cmdName );
    
  #-------------------------------------------------------------------
  # Does the member already exist on this node?
  #-------------------------------------------------------------------
  memberID = getConfigIDs( memberName, 'ClusterMember', nodeID );
  if memberID != '' :
    print conflict % locals();
    Usage( cmdName );

  #-------------------------------------------------------------------
  # Use the validated values to perform the cluster member creation.
  #-------------------------------------------------------------------
  if localMode() :
    if DMpresent() :
      AdminConfig.createClusterMember( clusterID, nodeID, [[ 'memberName', memberName ]] );
      AdminConfig.save();
    else :
      print DMreqd % locals();
  else :
    cell  = AdminControl.getCell()
    node  = AdminControl.getNode()
    oName = 'cell=%s,node=%s,type=Server,*' % ( cell, node )
    sObj  = AdminControl.completeObjectName( oName )
    pType = AdminControl.getAttribute( sObj, 'processType' )
    if pType == 'DeploymentManager' :
      AdminConfig.createClusterMember( clusterID, nodeID, [[ 'memberName', memberName ]] );
      AdminConfig.save();
      #---------------------------------------------------------------
      # Synchronize the node
      #---------------------------------------------------------------
      sync = AdminControl.completeObjectName( 'type=NodeSync,node=%s,*' % nodeName );
      AdminControl.invoke( sync, 'sync' );
    else :
      print DMreqd % locals();

#---------------------------------------------------------------------
# Role: main entry point
# Note: This is where execution begins.
#---------------------------------------------------------------------
if ( __name__ == 'main' ) or ( __name__ == '__main__' ) :
  createClusterMember();
else :
  Usage( __name__ );
