#-------------------------------------------------------------------------------
# Name: parents.01.py
# From: WebSphere Application Server Administration using Jython
#   By: Robert A. (Bob) Gibson [rag], Arthur Kevin McGrath, Noel J. Bergman
# ISBN: 0-13-700952-6
# Role: 2nd attempt at displaying relationship between parent and child types
# History:
#   date   ver who what
# -------- --- --- ------------------------------------------
# 09/10/29 0.1 rag Fix - Added ISBN detail
# 08/10/17 0.0 rag New - for the book
#-------------------------------------------------------------------------------
# First, build a dictionary of the types that are allowed be parents
#-------------------------------------------------------------------------------
types  = AdminConfig.types().splitlines()
result = {}
for kind in types :
  parents = AdminConfig.parents( kind )
  if not parents.startswith( 'WASX7351I' ) :
    result[ kind ] = parents

#-------------------------------------------------------------------------------
# Next, display the information in a slightly easier to read format
#-------------------------------------------------------------------------------
kinds = result.keys()                  # List of the allowed parent types
kinds.sort()                           # ... sorted alphabetically
lengths = [ len( x ) for x in kinds ]  # List of these type name lengths
widest  = -max( lengths )              # Widest type name found
for kind in kinds :                    # For each type, display the allowed kids
  print '%*s : %s' % ( widest, kind, result[ kind ].splitlines() )
