#---------------------------------------------------------------------
#  Name: installApp.py()
#  From: WebSphere Application Server Administration using Jython
#    By: Robert A. (Bob) Gibson [rag], Arthur Kevin McGrath, Noel J. Bergman
#  ISBN: 0-13-700952-6
#  Role: Install specified application using defaults
# Usage: wsadmin -lang jython -f installApp.py filename.ear
#  Note: See Usage routine for more details
# History:
#   date   ver who what
# -------- --- --- ------------------------------------------
# 09/10/29 0.1 rag Fix - Added ISBN detail
# 08/11/19 0.0 rag New - based upon insight obtained while writing book
#---------------------------------------------------------------------
import getopt, sys, os.path
from WAuJ_utilities import fixFileName

#---------------------------------------------------------------------
# Global dictionary to hold the user specified options & values
#---------------------------------------------------------------------
Opts = {}

#---------------------------------------------------------------------
# Name: parseOpts()
# Role: Process the user specified (command line) options
# Note: wsadmin consumes any occurrence of the following "short"
#       option letters/characters: -c, -f, -h, -p, -?
#---------------------------------------------------------------------
def parseOpts( cmdName ) :
  sOpts  = 'e:'
  lOpts  = 'earFile='.split( ',' )
  badOpt = '%(cmdName)s: Unknown/unrecognized parameter%(plural)s: %(argStr)s'
  optErr = '%(cmdName)s: Error encountered processing: %(argStr)s'
  noFile = '%(cmdName)s: Specified EAR file not found: %(val)s'

  try :
    opts, args = getopt.getopt( sys.argv, sOpts, lOpts )
  except getopt.GetoptError :
    argStr = ' '.join( sys.argv )
    print optErr % locals()
    Usage( cmdName )

  #-------------------------------------------------------------------
  # Initialize the global Opts dictionary using these keys (indexes)
  #-------------------------------------------------------------------
  keys = 'earFile'.split( ',' )
  for key in keys : Opts[ key ] = None

  #-------------------------------------------------------------------
  # Process the list of options returned by getOpt()
  #-------------------------------------------------------------------
  for opt, val in opts :
    if opt in ( '-e', '--earFile' ) :
      val = fixFileName( val )         # Fix a common error condition
      if os.path.exists( val ) :
        if Opts[ 'earFile' ] :
          Opts[ 'earFile' ].append( val )
        else :
          Opts[ 'earFile' ] = [ val ]
      else :
        print noFile % locals()

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
Purpose: Install specified application(s) using default value\n
  Usage: %(cmdName)s [options]\n
Required switches:
  -e | --earFile   <fileName> = Fuly qualified path of EAR to be installed.\n
Notes:
- Multiple instances of the -e or --earFile parameter are allowed.\n
- Long form option values may be separated/delimited from their associated
  value using either a space, or an equal sign ('=').\n
- Short form option values may be sepearated from their associated value using
  an optional space.\n
Examples:
  wsadmin -lang jython -f %(cmdName)s.py --earFile="C:\\myApp.ear"\n
  wsadmin -lang jython -f %(cmdName)s.py -e "C:\\temp\\myApp.ear"
''' % locals()
  sys.exit( 1 )

#---------------------------------------------------------------------
# Name: installApp()
# Role: Process the user specified (command line) options
#---------------------------------------------------------------------
def installApp( cmdName = 'installApp' ) :
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

# print 'earFile: ' + str( earFile )
  #-------------------------------------------------------------------
  # For each ear file, do a simple AdminApp.install()
  #-------------------------------------------------------------------
  for ear in earFile :
    print 'Installing: %s' % ear
    AdminApp.install( ear )
    print '-' * 70

  #-------------------------------------------------------------------
  # Check for: 'WASX7241I: There are no unsaved changes in this workspace.'
  #-------------------------------------------------------------------
  if not AdminConfig.queryChanges().startswith( 'WASX7241I' ) :
    print 'Saving configuration.'
    AdminConfig.save()

#---------------------------------------------------------------------
# main entry point - verify that script was executed, and not imported
#---------------------------------------------------------------------
if ( __name__ == 'main' ) or ( __name__ == '__main__' ) :
  installApp()
else :
  Usage( __name__ )
