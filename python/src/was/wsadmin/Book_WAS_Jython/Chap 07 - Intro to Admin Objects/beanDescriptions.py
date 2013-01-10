#----------------------------------------------------------------------
# Name: beanDescriptions.py
# From: WebSphere Application Server Administration using Jython
#   By: Robert A. (Bob) Gibson [rag], Arthur Kevin McGrath, Noel J. Bergman
# ISBN: 0-13-700952-6
# Role: Script to display description information about the active beans
# History:
#   date   ver who what
# -------- --- --- ----------------------------------------------------
# 09/10/29 0.1 rag Fix - Added ISBN detail
# 09/17/08 0.0 rag New - insight obtained while writing the book
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# Name: beanDescriptions()
#----------------------------------------------------------------------
def beanDescriptions():
  try :
    from WAuJ_utilities import MBnameAsDict
    beans = AdminControl.queryNames( '*' ).splitlines()
    info  = {}
    #------------------------------------------------------------------
    # For each active bean name - get the description, and put this
    # text in a dictionary, indexed by the MBean type value.
    #------------------------------------------------------------------
    for bean in beans :
      dict = MBnameAsDict( bean )      # MBean name as a dictionary
      kind = dict[ 'type' ]            # Type value from MBean name
      info[ kind ] = Help.description( bean )

    #------------------------------------------------------------------
    # Get the list of active MBean types, and sort the list
    #------------------------------------------------------------------
    names = info.keys()
    names.sort()
    #------------------------------------------------------------------
    # For each type, display the type value, and the description
    #------------------------------------------------------------------
    for name in names :
      print '%s\n  %s' % ( name, info[ name ] )

  except ImportError, ie :
    name = str( ie ).split( ' ' )[ -1 ]
    print 'Required module not found: ' + name

  except :
    ( kind, value ) = sys.exc_info()[ :2 ]
    print 'Exception  type: ' + str( kind )
    print 'Exception value: ' + str( value )

#---------------------------------------------------------------------
# Name: Usage()
# Role: Routine used to describe how the script should be used.
#---------------------------------------------------------------------
def Usage( cmd = 'beanDescriptions' ) :
  print '''     File: %(cmd)s.py\n
     Role: Script used to display description information for the
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
  beanDescriptions()
else :
  Usage( __name__ )

