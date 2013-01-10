#---------------------------------------------------------------------
# Name: Helphelp2.py
# From: WebSphere Application Server Administration using Jython
#   By: Robert A. (Bob) Gibson [rag], Arthur Kevin McGrath, Noel J. Bergman
# ISBN: 0-13-700952-6
# Role: Attempt #2 to display all of the help information for
#       each of the Help methods returned by Help.help()
# History:
#   date   ver who what
# -------- --- --- ----------------------------------------------------
# 09/10/29 0.1 rag Fix - Added ISBN detail
#---------------------------------------------------------------------
import re
mNames  = re.compile( r'^(\w+)(?:\s+.*)$', re.MULTILINE )
helpTxt = Help.help()
methods = mNames.findall( helpTxt )
delim   = '#' + '-' * 70
print '%(delim)s\n# Help.help()\n%(delim)s\n%(helpTxt)s\n' % locals()

for name in methods :
  print '%(delim)s\n# Help.help( "%(name)s" )\n%(delim)s' % locals()
  print Help.help( name ) + '\n'

