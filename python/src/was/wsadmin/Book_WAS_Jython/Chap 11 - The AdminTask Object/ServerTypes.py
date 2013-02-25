#---------------------------------------------------------------------
#  Name: ServerTypes.py()
#  From: WebSphere Application Server Administration using Jython
#    By: Robert A. (Bob) Gibson [rag], Arthur Kevin McGrath, Noel J. Bergman
#  ISBN: 0-13-700952-6
#  Role: Format the output of the AdminTask.listServerTypes() and
#        AdminTask.showServerTypeInfo() commands into an easily
#        read format.
# Usage: wsadmin -lang jython -f ServerTypes.py
# History:
#   date   ver who what
# -------- --- --- ------------------------------------------
# 09/10/29 0.1 rag Fix - Added ISBN detail
# 08/12/17 0.0 rag New - based upon insight obtained while writing book
#---------------------------------------------------------------------
try :
  import sys
  import AdminTask
  from WAuJ_utilities import nvTextListAsDict
except :
  ( kind, value ) = sys.exc_info()[ :2 ]
  ( kind, value ) = str( kind ), str( value )
  if kind.endswith( 'ImportError' ) :
    print 'ServerTypes error:  import error: module not found: %s' % value.split( ' ' )[ -1 ]
  sys.exit( -1 )

#---------------------------------------------------------------------
# Name: ServerTypes()
# Role: Perform script function
#---------------------------------------------------------------------
def ServerTypes( cmdName = 'ServerTypes' ):
  try :

    #-----------------------------------------------------------------
    # allNames - Holds all of the dictionary "keys", so the longest
    #            can easily be determined.
    # allTypes - Holds all of the ServerType dictionaries for later
    #            display.
    #-----------------------------------------------------------------
    allNames = []
    allTypes = {}
    for serverType in AdminTask.listServerTypes().splitlines() :
      allTypes[ serverType ] = sDict = nvTextListAsDict( AdminTask.showServerTypeInfo( serverType ) )
      names = sDict.keys()
      names.sort()
      allNames.extend( names )

    #-----------------------------------------------------------------
    # What is the length of the longest attribute name?
    #-----------------------------------------------------------------
    width = max( [ len( x ) for x in allNames ] )

    #-----------------------------------------------------------------
    # Now, we can display a horiztonal line
    #-----------------------------------------------------------------
    hr = '-' * 70                      # horizontal rule
    print hr
    names = allTypes.keys()
    names.sort()

    #-----------------------------------------------------------------
    # For each ServerType... formatted display of the name/value pairs
    #-----------------------------------------------------------------
    for name in names :
      sDict = allTypes[ name ]
      Names = sDict.keys()
      Names.sort()
      for Name in Names :
        print '%*s : %s' % ( width, Name, sDict[ Name ] )
      print hr
  except :
    ( kind, value ) = sys.exc_info()[ :2 ]
    ( kind, value ) = str( kind ), str( value )
    print '%s error:\n Exception type: %s\n Exception info: %s' % ( cmdName, kind, value )

#---------------------------------------------------------------------
# Name: Usage()
# Role: Display script usage information, and exit (terminate script)
#---------------------------------------------------------------------
def Usage( cmdName ):
  print '''
Command: %(cmdName)s\n
Purpose: Format the output of the AdminTask.listServerTypes() and
         AdminTask.showServerTypeInfo() commands into an easily read format.\n
Examples:
  wsadmin -lang jython -f %(cmdName)s.py''' % locals()
  sys.exit( 1 )

#---------------------------------------------------------------------
# main entry point - verify that script was executed & not imported
#---------------------------------------------------------------------
if ( __name__ == 'main' ) or ( __name__ == '__main__' ) :
  if len( sys.argv ) > 0 :
    Usage( 'ServerTypes' )
  else :
    ServerTypes()
else :
  Usage( __name__ )
