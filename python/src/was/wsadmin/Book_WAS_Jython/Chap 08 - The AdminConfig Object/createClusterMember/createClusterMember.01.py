#---------------------------------------------------------------------
# Name: createClusterMember
# Role: Example script, created from scratch.
#       Iteration 1 - Check for missing required parameters
#---------------------------------------------------------------------
import getopt, sys;

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
# Name: createClusterMember()
# Role: Function used to create a new cluster member
#---------------------------------------------------------------------
def createClusterMember( cmdName = 'createClusterMember' ) :
  fewParms = '%(cmdName)s: Insufficient parameters provided.';
  required = '%(cmdName)s: Required parameter missing: %(parm)s';

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
  # mapped error messages (e.g., see unknownNode below).
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

#---------------------------------------------------------------------
# Role: main entry point
# Note: This is where execution begins.
#---------------------------------------------------------------------
if ( __name__ == 'main' ) or ( __name__ == '__main__' ) :
  createClusterMember();
else :
  Usage( __name__ );
