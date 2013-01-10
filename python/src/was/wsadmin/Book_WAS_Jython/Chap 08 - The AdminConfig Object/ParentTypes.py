#---------------------------------------------------------------------
# Name: ParentTypes.py
# From: WebSphere Application Server Administration using Jython
#   By: Robert A. (Bob) Gibson [rag], Arthur Kevin McGrath, Noel J. Bergman
# ISBN: 0-13-700952-6
# Role: Display the Parent type information
# History:
#   date   ver who what
# -------- --- --- ----------------------------------------------------
# 09/10/29 0.1 rag Fix - Added ISBN detail
# 09/02/03 0.0 rag New - for the book
#---------------------------------------------------------------------
'Find the parent and associated child types allowed by WebSphere.'

#---------------------------------------------------------------------
# Name: parentTypesAsDict()
# Returns: A dictionary containing elements of the form:
#
#       name  | description
#       ------+-----------------------------------
#       key   | parent type name
#       value | list of valid child type names
#---------------------------------------------------------------------
def parentTypesAsDict():
  'Return a dictionary of valid parent/child type names.'

  #-------------------------------------------------------------------
  # Guarantee accessability to AdminConfig Administration object
  # Note: This requires that sys.modules is properly initialized
  #-------------------------------------------------------------------
  if 'AdminConfig' not in dir() :
    import AdminConfig

  #-------------------------------------------------------------------
  # Generate the list of valid types
  #-------------------------------------------------------------------
  types  = AdminConfig.types().splitlines()
  result = {}

  #-------------------------------------------------------------------
  # For each type, see if it has any valid parents()
  #-------------------------------------------------------------------
  for kind in types :
    parents = AdminConfig.parents( kind )
    #-----------------------------------------------------------------
    # If so, add this child to each specified parent type, using the
    # parent name as the dictionary key, and the type name as the
    # associated value.  Note, this parent name already exists in the
    # dictionary, this child type name needs to be added to the list
    #-----------------------------------------------------------------
    if parents.find( 'WASX7351I' ) == -1 :
      for parent in parents.splitlines() :
        if result.has_key( parent ) :
          result[ parent ].append( kind )
        else :
          result[ parent ] = [ kind ]

  return result

#---------------------------------------------------------------------
# Name: DisplayParentTypes()
#---------------------------------------------------------------------
def DisplayParentTypes() :
  'Display the parent type name and the associated child type names.'

  delim   = '-' * 70
  parents = parentTypesAsDict()

  #-------------------------------------------------------------------
  # Retrieve the names of the valid parent types
  #-------------------------------------------------------------------
  names = parents.keys()
  names.sort()

  #-------------------------------------------------------------------
  # Find the length of the longest parent name
  #-------------------------------------------------------------------
  width = 0
  for name in names :
    if width < len( name ) :
      width = len( name )

  print '%s\n%*s : Allowed child type(s)\n%s' % ( delim, -width, 'Parent type', delim )

  #-------------------------------------------------------------------
  # For each parent type name ...
  #-------------------------------------------------------------------
  for name in names :
    children = parents[ name ]
    children.sort()
    print '%*s : %s' % ( -width, name, ', '.join( children ) )

#---------------------------------------------------------------------
# main - script entry point
#---------------------------------------------------------------------
if __name__ == 'main' :
  DisplayParentTypes()
