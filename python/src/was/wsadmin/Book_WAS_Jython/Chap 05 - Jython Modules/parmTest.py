#---------------------------------------------------------------------
# Name: parmTest()
# Role: Example script demonstrating one technique for processing
#       command line parameters
#---------------------------------------------------------------------
import getopt, sys

#---------------------------------------------------------------------
# Global dictionary to hold the user specified options & values
#---------------------------------------------------------------------
Opts = {}

#---------------------------------------------------------------------
# Name: parseOpts()
# Role: Process the user specified (command line) options
#---------------------------------------------------------------------
def parseOpts( cmdName ) :
  sOpts  = 's:bn:'
  lOpts  = 'serverName=,boolName,nodeName='.split( ',' )
  badOpt = '%(cmdName)s: Unknown/unrecognized parameter%(plural)s: %(argStr)s'
  optErr = '%(cmdName)s: Error encountered processing: %(argStr)s'

  try :
    opts, args = getopt.getopt( sys.argv, sOpts, lOpts )
  except getopt.GetoptError :
    argStr = ' '.join( sys.argv )
    print optErr % locals()
    Usage( cmdName )

  #-------------------------------------------------------------------
  # Initialize the global Opts dictionary using these keys (indexes)
  #-------------------------------------------------------------------
  keys = 'servName,nodeName,boolName'.split( ',' )
  for key in keys : Opts[ key ] = None

  #-------------------------------------------------------------------
  # Process the list of options returned by getOpt()
  #-------------------------------------------------------------------
  for opt, val in opts :
    if opt in   ( '-s', '--serverName' ) : Opts[ 'servName' ] = val
    elif opt in ( '-n', '--nodeName' )   : Opts[ 'nodeName' ] = val
    elif opt in ( '-b', '--boolName' )   : Opts[ 'boolName' ] = 1

  #-------------------------------------------------------------------
  # Check for unhandled/unrecognized options
  #-------------------------------------------------------------------
  if ( args != [] ) :
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
Purpose: WebSphere (wsadmin) script used to demonstrate the parsing
         of command line parameters.
  Usage: %(cmdName)s [options]\n
Required switches:
  -s | --serverName <name> = Name of basis server
\nOptional switches:
  -n | --nodeName   <name> = Name of node on which server exists
  -b | --boolName          = Example "no value" parameter
\nNotes:
- Long form option values may be separated/delimited from their associated
  value using either a space, or an equal sign ('=').\n
- Short form option values may be sepearated from their associated value using
  an optional space.\n
- Description text containing blanks should be enclosed in double quotes.\n
Examples:
  wsadmin -lang jython -f %(cmdName)s.py --serverName=s1 --nodeName N1\n
  wsadmin -lang jython -f %(cmdName)s.py -ss1 -b -n ragibsonNode01
''' % locals()
  sys.exit( 1 )

#---------------------------------------------------------------------
# Name: parmTest()
# Role: Process the user specified (command line) options
#---------------------------------------------------------------------
def parmTest( cmdName = 'parmTest' ) :
  fewParms = '%(cmdName)s: Insufficient parameters provided.'

  argc = len( sys.argv );                   # Number of arguments
  if ( argc < 1 ) :                         # If too few are present,
    print fewParms % locals();              #   tell the user, and
    Usage( cmdName );                       #   provide the Usage info
  else :                                    # otherwise
    parseOpts( cmdName );                   #   parse the command line

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
  # Result of parsing command line parameters
  #-------------------------------------------------------------------
  parms = '%(cmdName)s: --serverName %(servName)s --nodeName %(nodeName)s'
  if ( boolName != None ):
    parms += ' --boolName'

  print parms % locals()

#---------------------------------------------------------------------
# Role: main entry point
# Note: Idiom to allow script to be executed using either wsadmin or
#       the IBM Application Server Toolkit for WebSphere Application
#       Server
#---------------------------------------------------------------------
if ( __name__ == 'main' ) or ( __name__ == '__main__' ) :
  parmTest()
else :
  Usage( __name__ )
