#----------------------------------------------------------------------
# Name: beanConstructors.py
# From: WebSphere Application Server Administration using Jython
#   By: Robert A. (Bob) Gibson [rag], Arthur Kevin McGrath, Noel J. Bergman
# ISBN: 0-13-700952-6
# Role: Script used to display the Help.constructors() text for all
#       active MBeans having constructors.
# History:
#   date   ver who what
# -------- --- --- ----------------------------------------------------
# 09/10/29 0.1 rag Fix - Added ISBN detail
# 09/17/08 0.0 rag New - insight obtained while writing the book
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# Name: beanConstructors()
#----------------------------------------------------------------------
def beanConstructors() :
  try :
    names = AdminControl.queryNames( '*' ).splitlines()
    empty = Help.constructors( names[ 0 ] )
    sep   = '-' * 70
    for name in names :
      text = Help.constructors( name )
      if text != empty :
        print '%(sep)s\n%(name)s\n%(sep)s\n%(text)s' % locals()

  except :
    ( kind, value ) = sys.exc_info()[ :2 ]
    ( kind, value ) = str( kind ), str( value )
    if kind.endswith( 'ScriptingException' ) :
      value = value[ len( kind ) + 2: ]
      if value.startswith( 'AdminControl' ) :
        print 'beanConstructors Error: ' + value
        print 'Are you connected to an application server?'
      else :
        print 'beanConstructors ScriptingException: "%s"' % value
    else :
      print 'Exception  type: "%s"' % kind
      print 'Exception value: "%s"' % value

#---------------------------------------------------------------------
# Name: Usage()
# Role: Routine used to describe how the script should be used.
#---------------------------------------------------------------------
def Usage( cmd = 'beanConstructors' ) :
  print '''     File: %(cmd)s.py\n
     Role: Script used to display the Help.constructors() text for all
           active WebSphere Application Server MBeans having constructors.\n
     From: WebSphere Application Server Automation using Jython
   Author: Robert A. (Bob) Gibson
Published: July 2009 - IBM Press
     ISBN: <TBD>\n
Usage:\n
     Unix:
       ./wsadmin.sh  -f %(cmd)s.py\n
     Windows:
       wsadmin[.bat] -f %(cmd)s.py''' % locals()

#----------------------------------------------------------------------
# main: Verify that this file was executed, and not imported.
#----------------------------------------------------------------------
if __name__ == 'main' :
  beanConstructors()
else :
  Usage( __name__ )
