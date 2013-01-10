#---------------------------------------------------------------------
# Name: Helphelp1.py
# From: WebSphere Application Server Administration using Jython
#   By: Robert A. (Bob) Gibson [rag], Arthur Kevin McGrath, Noel J. Bergman
# ISBN: 0-13-700952-6
# Role: Initial attempt to display all of the help information for
#       each of the Help methods returned by Help.help()
# Note: For an explanation of the regular expression (RegExp), see
#       the text
# History:
#   date   ver who what
# -------- --- --- ----------------------------------------------------
# 09/10/29 0.1 rag Fix - Added ISBN detail
#---------------------------------------------------------------------
import re
mNames  = re.compile( r'^(\w+)(?:\s+.*)$', re.MULTILINE )
methods = mNames.findall( Help.help() )
for name in methods :
  print 'Help.help( "%s" )\n%s' % ( name, '-' * 70 )
  print Help.help( name )
  print '-' * 70

