#---------------------------------------------------------------------
#  Name: AdminTaskHelp.py
# From: WebSphere Application Server Administration using Jython
#   By: Robert A. (Bob) Gibson [rag], Arthur Kevin McGrath, Noel J. Bergman
# ISBN: 0-13-700952-6# History:
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
#       found at the beginning of a line
#---------------------------------------------------------------------
def methods( text ) :
  #-------------------------------------------------------------------
  # Regular Expression to match "words" at the start of line
  #-------------------------------------------------------------------
  return re.compile( r'^(\w+)(?:\s+.*)$', re.MULTILINE ).findall( text )

#---------------------------------------------------------------------
# Name: Usage()
# Role: Routine used to describe how the script should be used.
#---------------------------------------------------------------------
def Usage( cmd = 'AdminTaskHelp' ) :
  print '''     File: %(cmd)s.py\n
     Role: Script used to generate the help for the WebSphere Application
           Server AdminTask Administrative scripting object, its commands,
           and commandGroups.\n
     From: WebSphere Application Server Automation using Jython
   Author: Robert A. (Bob) Gibson
Published: July 2009 - IBM Press
     ISBN: <TBD>\n
Usage:
  Unix:
    ./wsadmin.sh  -conntype none -f %(cmd)s.py >%(cmd)s.out\n
  Windows:
    wsadmin[.bat] -conntype none -f %(cmd)s.py >%(cmd)s.out''' % locals()

#---------------------------------------------------------------------
# Name: AdminTaskHelp()
# Role: Generate the desired output
#---------------------------------------------------------------------
def AdminTaskHelp() :
  import AdminTask
  sep = '\n#' + '-' * 70               # Separator line
  #-------------------------------------------------------------------
  # AdminTask.help() - "Special case #1"
  #-------------------------------------------------------------------
  print sep[ 1: ] + '\n# AdminTask.help() ' + sep
  print AdminTask.help()

  #-------------------------------------------------------------------
  # AdminTask.help( cmd )
  #-------------------------------------------------------------------
  cmds = '-commands,-commandGroups'.split( ',' )
  for cmd in cmds :
    data = AdminTask.help( cmd )
    print "%s\n# AdminTask.help( '%s' )%s" % ( sep[ 1: ], cmd, sep )
    print data.replace( '\r', '' )    # without extra CR chars
    mNames = methods( data )           #
    for meth in mNames :               # For each method...
      try :                            #
        info = AdminTask.help( meth )  #   Does help text exist?
        print "%s\n# AdminTask.help( '%s' )%s" % ( sep[ 1: ], meth, sep )
        print info.replace( '\r', '' )  #   Yes, display without
        print                          #       extra CR characters
      except :                         #
        pass                           #     no, ignore any error
    print                              #

#---------------------------------------------------------------------
# main: Verify that this file was executed, and not imported.
#---------------------------------------------------------------------
if ( __name__ == 'main' ) or ( __name__ == '__main__' ) :
  AdminTaskHelp()
else :
  Usage( __name__ )
