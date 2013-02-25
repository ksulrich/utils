#-------------------------------------------------------------------------------
# Name: parents.00.py
# From: WebSphere Application Server Administration using Jython
#   By: Robert A. (Bob) Gibson [rag], Arthur Kevin McGrath, Noel J. Bergman
# ISBN: 0-13-700952-6
# Role: First attempt at displaying relationship between parent and child types
# History:
#   date   ver who what
# -------- --- --- ------------------------------------------
# 09/10/29 0.1 rag Fix - Added ISBN detail
# 08/10/17 0.0 rag New - for the book
#-------------------------------------------------------------------------------
types = AdminConfig.types().splitlines()
for kind in types :
  parents = AdminConfig.parents( kind )
  if not parents.startswith( 'WASX7351I' ) :
    print '%s : %s' % ( kind, parents.splitlines() )

