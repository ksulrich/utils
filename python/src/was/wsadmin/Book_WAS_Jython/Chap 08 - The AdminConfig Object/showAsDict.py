#-------------------------------------------------------------------------------
# Name: showAsDict.py
# From: WebSphere Application Server Administration using Jython
#   By: Robert A. (Bob) Gibson [rag], Arthur Kevin McGrath, Noel J. Bergman
# ISBN: 0-13-700952-6
# Role: Convert result of AdminConfig.show( configID ) to a dictionary
# Note: Depends upon availability of WSAS Admin Objects via sys.modules
# History:
#   date   ver who what
# -------- --- --- ------------------------------------------
# 09/10/29 0.1 rag Fix - Added ISBN detail
# 09/06/08 0.0 rag New - Based upon work down for IMPACT 2008
#-------------------------------------------------------------------------------
# Example use:
# > from showAsDict import showAsDict
# > servers = AdminConfig.list( 'Server' ).splitlines()
# > svrDict = showAsDict( servers[ 0 ] )
#-------------------------------------------------------------------------------
def showAsDict( configID ) :
  'Convert result of AdminConfig.show( configID ) to a dictionary & return it.'
  result = {}
  try :
    import sys, AdminConfig            # Get access to WSAS objects
    #---------------------------------------------------------------------------
    # The result of the AdminConfig.show() should be a string containing many
    # lines.  Each line of which starts and ends with brackets.  The "name"
    # portion should be separated from the associated value by a space.
    #---------------------------------------------------------------------------
    for item in AdminConfig.show( configID ).splitlines() :
      if ( item[ 0 ] == '[' ) and ( item[ -1 ] == ']' ) :
        ( key, value ) = item[ 1:-1 ].split( ' ', 1 )
        result[ key ] = value
  except NameError, e :
    print 'Name not found: ' + str( e )
  except :
    ( kind, value ) = sys.exc_info()[ :2 ]
    print 'Exception  type: ' + str( kind )
    print 'Exception value: ' + str( value )
  return result

#-------------------------------------------------------------------------------
# Name: Usage()
#-------------------------------------------------------------------------------
def Usage( cmd = 'showAsDict' ) :
  print '''     File: %(cmd)s.py\n
     Role: Module containing function %(cmd)s to call AdminConfig.show(...)
           and convert the result to a dictionary.\n
     From: WebSphere Application Server Administration using Jython
   Author: Robert A. (Bob) Gibson
Published: July 2009 - IBM Press
     ISBN: <TBD>\n
Usage:
  import %(cmd)s\n
    or\n
  from %(cmd)s import %(cmd)s''' % locals()

#-------------------------------------------------------------------------------
# main: Verify that this file was imported, and not executed.
#-------------------------------------------------------------------------------
if ( __name__ == 'main' ) or ( __name__ == '__main__' ) :
  Usage( __name__ )

