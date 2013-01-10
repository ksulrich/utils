#----------------------------------------------------------------------
# Name: beanClassnames.py
# From: WebSphere Application Server Administration using Jython
#   By: Robert A. (Bob) Gibson [rag], Arthur Kevin McGrath, Noel J. Bergman
# ISBN: 0-13-700952-6
# Role: Script used to display the Help.classname() text for the active
#       MBeans.
# History:
#   date   ver who what
# -------- --- --- ----------------------------------------------------
# 09/10/29 0.1 rag Fix - Added ISBN detail
# 09/17/08 0.0 rag New - insight obtained while writing the book
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# Name: beanClassnames()
#----------------------------------------------------------------------
def beanClassnames() :
  try :
    #------------------------------------------------------------------
    # import the utility routine used to convert an MBean name to a
    # dictionary
    #------------------------------------------------------------------
    from WAuJ_utilities import MBnameAsDict

    #------------------------------------------------------------------
    # Get the list of active MBeans
    #------------------------------------------------------------------
    names = AdminControl.queryNames( '*' ).splitlines()
    info  = {}
    #------------------------------------------------------------------
    # For each MBean, get the classname, and put this information into
    # a dictionary indexed by the MBean type
    #------------------------------------------------------------------
    for name in names :
      dict = MBnameAsDict( name )
      kind = dict[ 'type' ]
      info[ kind ] = Help.classname( name )

    #------------------------------------------------------------------
    # For each MBean type, display the type and the associated classname
    #------------------------------------------------------------------
    kinds = info.keys()
    kinds.sort()
    for kind in kinds :
      print '%-35s  %s' % ( kind, info[ kind ] )

  except ImportError, ie :
    name = str( ie ).split( ' ' )[ -1 ]
    print 'Required module missing: ' + name

  except :
    ( kind, value ) = sys.exc_info()[ :2 ]
    ( kind, value ) = str( kind ), str( value )
    if kind.endswith( 'ScriptingException' ) :
      value = value[ len( kind ) + 2: ]
      if value.startswith( 'AdminControl' ) :
        print 'beanClassnames Error: ' + value
        print 'Are you connected to an application server?'
      else :
        print 'beanClassnames ScriptingException: "%s"' % value
    else :
      print 'Exception  type: "%s"' % kind
      print 'Exception value: "%s"' % value

#---------------------------------------------------------------------
# Name: Usage()
# Role: Routine used to describe how the script should be used.
#---------------------------------------------------------------------
def Usage( cmd = 'beanClassnames' ) :
  print '''     File: %(cmd)s.py\n
     Role: Script used to display the Help.classname() text for all
           active WebSphere Application Server MBeans.\n
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
  beanClassnames()
else :
  Usage( __name__ )
