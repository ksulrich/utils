#---------------------------------------------------------------------
#    Name: ObjHelp.py
# From: WebSphere Application Server Administration using Jython
#   By: Robert A. (Bob) Gibson [rag], Arthur Kevin McGrath, Noel J. Bergman
# ISBN: 0-13-700952-6
# History:
#   date   ver who what
# -------- --- --- ----------
# 09/10/29 0.1 rag Fix - Added ISBN detail
# 08/09/02 0.0 rag New - based upon work done for IMPACT 2008
#---------------------------------------------------------------------
import re                                   # RegExp package/module

#---------------------------------------------------------------------
# Name: methods( text )
# Role: Return the method names found in the specified help text
# Note: Method names are defined to be consecutive "word" characters
#       found at the beginning of a line.  The regular expression
#       (RegExp) pattern identifies these parts of the multi-line
#       text string.
#---------------------------------------------------------------------
def methods( text ) :
  return re.compile( r'^(\w+)(?:\s+.*)$', re.MULTILINE ).findall( text )

#---------------------------------------------------------------------
# Name: Usage()
# Role: Routine used to describe how the script should be used.
#---------------------------------------------------------------------
def Usage() :
  print '''     File: ObjHelp.py\n
     Role: Script used to generate the help for most of the WebSphere
           Application Server Administrative scripting objects.\n
     From: WebSphere Application Server Automation using Jython
   Author: Robert A. (Bob) Gibson
Published: July 2009 - IBM Press
     ISBN: <TBD>\n
Usage:\n
     Unix:
       ./wsadmin.sh  -conntype none -f ObjHelp.py >ObjHelp.out\n
     Windows:
       wsadmin[.bat] -conntype none -f ObjHelp.py >ObjHelp.out'''

#---------------------------------------------------------------------
# Name: ObjHelp()
# Role: Primary routine invoked when this file is executed within
#       wsadmin
#---------------------------------------------------------------------
def ObjHelp() :
  import AdminApp, AdminControl, AdminConfig
  objects = { 'AdminApp'     : AdminApp,
              'AdminControl' : AdminControl,
              'AdminConfig'  : AdminConfig,
              'Help'         : Help
            }
  sep = '\n#' + '-' * 70               # Separator line
  names = objects.keys()               # WebSphere scripting objects
  names.sort()                         # ... sorted alphabetically
  for name in names :                  # for each object name
    obj = objects[ name ]              # obj -> scripting object
    print sep[ 1: ] + '\n# ' + name + '.help() ' + sep
    text = obj.help()                  # Call the object.help() method
    print ( text + '\n' ).replace( '\r', '' )
    mNames = methods( text )           # List of object methods
    for meth in mNames :               # For each method...
      print sep[ 1: ] + '\n# ' + name + ".help( '" + meth + "' )" + sep
      print obj.help( meth ).replace( '\r', '' )
      print                            #
    print                              #

#---------------------------------------------------------------------
# main: Verify that this file was executed, and not imported.
#---------------------------------------------------------------------
if ( __name__ == 'main' ) or ( __name__ == '__main__' ) :
  ObjHelp()
else :
  Usage()

