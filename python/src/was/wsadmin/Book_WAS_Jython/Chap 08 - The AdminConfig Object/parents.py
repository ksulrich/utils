#-------------------------------------------------------------------------------
# Name: parents.py
# From: WebSphere Application Server Administration using Jython
#   By: Robert A. (Bob) Gibson [rag], Arthur Kevin McGrath, Noel J. Bergman
# ISBN: 0-13-700952-6
# Role: Displaying relationship between parent and child types
# History:
#   date   ver who what
# -------- --- --- ------------------------------------------
# 09/10/29 0.1 rag Fix - Added ISBN detail
# 08/10/17 0.0 rag New - for the book
#-------------------------------------------------------------------------------
# First, build a dictionary of the types that are allowed be parents
#-------------------------------------------------------------------------------
types = AdminConfig.types().splitlines()
kids = {}
delim = '\n' + '-' * 50 + '\n'
print '%(delim)sValid Parents%(delim)s' % locals()
for kind in types :
  parents = AdminConfig.parents( kind )
  if parents.find( 'WASX7351I' ) == -1 :
    print '%s : %s' % ( kind, str( parents.splitlines() ) )
    for parent in parents.splitlines() :
      if kids.has_key( parent ) :
        kids[ parent ].append( kind )
      else :
        kids[ parent ] = [ kind ]

print '%(delim)sValid children%(delim)s' % locals()
names = kids.keys()
names.sort()
for name in names :
  children = kids[ name ]
  children.sort()
  print '%s : %s' % ( name, str( children ) )

