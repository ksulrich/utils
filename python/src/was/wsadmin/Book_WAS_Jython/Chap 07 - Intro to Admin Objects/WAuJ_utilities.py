#---------------------------------------------------------------------
# Name: WAuJ_utilities.py
# From: WebSphere Application Server Administration using Jython
#   By: Robert A. (Bob) Gibson [rag], Arthur Kevin McGrath, Noel J. Bergman
# ISBN: 0-137-00952-6
# Role: Module used to contain some useful routines
# Note: Depends upon availability of WSAS Admin Objects via sys.modules
# History:
#   Date    who ver what
# --------  --- --- ----------
# 09/10/29  rag 0.4 Fix - Corrected author list
# 08/12/17  rag 0.3 Add - nvTextListAsDict() routine
# 08/12/09  rag 0.2 Add - docstring for fixFileName() & Usage() routines
# 08/11/07  rag 0.1 Add - docstring
# 08/10/31  rag 0.0 New - for the book
#---------------------------------------------------------------------
'''
     From: WebSphere Application Server Administration using Jython (WAuJ)
       By: Robert A. (Bob) Gibson
Published: IBM Press - July 2009
     ISBN: 0137009526
     Role: Provide a collection of library routines to assist with the
           Administration of a WebSphere Application Server environment.
'''

#---------------------------------------------------------------------
# Name: ConfigIdAsDict.py
# Role: Utility routine used to return a dictionary of name/value
#       details from an configuration ID (configID)
# Note: Exception handler requires sys module
# History:
#   date   ver who what
# -------- --- --- ---------------------------------------------------
# 08/12/03 0.2 rag Mod - Change "unexpected situation" message
# 08/11/04 0.1 rag Add - Add the "Name" attribute to the dictionary
# 08/10/27 0.0 rag New - insight obtained while writing the book
#---------------------------------------------------------------------
def ConfigIdAsDict( configID ) :
  'Given a configID, return a dictionary of the name/value components.'
  funName = 'ConfigIdAsDict'           # Name of this function
  result  = {}                         # Result is a dictionary
  hier    = []                         # Initialize to simplifiy checks
  try :                                # Be prepared for an error
    import sys, re                     # Is sys.exc_info() available?
    #-----------------------------------------------------------------
    # Does the specified configID match our RegExp pattern?
    # Note: mo == Match Object, if mo != None, a match was found
    #-----------------------------------------------------------------
    mo = re.compile( r'^(\w+)\(([^|]+)\|[^)]+\)$' ).match( configID )
    if mo :
      Name = mo.group( 1 )
      hier = mo.group( 2 ).split( '/' )
    if mo and ( len( hier ) % 2 == 0 ) :
      #---------------------------------------------------------------
      # hier == Extracted config hierarchy string
      #---------------------------------------------------------------
      for i in range( 0, len( hier ), 2 ) :
        ( name, value ) = hier[ i ], hier[ i + 1 ]
        result[ name ] = value
      if result.has_key( 'Name' ) :
        print '''%s: Unexpected situation - "Name" attribute conflict,
  Name = "%s", Name prefix ignored: "%s"''' % ( funName, result[ 'Name' ], Name )
      else :
        result[ 'Name' ] = Name
    else :
      print '''%(funName)s:
  Warning: The specified configID doesn\'t match the expected pattern,
           and is ignored.
  configID: "%(configID)s"''' % locals()
  except :
    ( kind, value ) = sys.exc_info()[ :2 ]
    print '''%(funName)s: Unexpected exception.\n
  Exception  type: %(kind)s
  Exception value: %(value)s''' % locals()
  return result

#---------------------------------------------------------------------
# Name: clusterInfo()
# Role: Return a dictionary having the primray key being the unique
#       cluster names, and the values being the associated configID
#       for that cluster
# Note: The parameter specified is only used should an error message
#       need to be displayed.
#   Usage: clusters = clusterInfo( commandName )
# Example: clusters = clusterInfo( 'createClusterMember' )
# History:
#   date   ver who what
# -------- --- --- ------------------------------------------
# 08/10/29 0.0 rag New - based upon need for createClusterMember.py
#---------------------------------------------------------------------
def clusterInfo( cmdName ) :
  'Return a dictionary of the cluster members, and their coniguration IDs.'
  nameConflict = '%s: Cluster name conflict.\nCluster name: %s\n  Instance 1: %s\n  Instance 2: %s'
  errors = 0                           # Number of errors encountered
  result = {}                          # What we are trying to build
  #-------------------------------------------------------------------
  # Get the list of known cluster members (each entry is a configID)
  #-------------------------------------------------------------------
  try :
    import AdminConfig
    clusterMembers = AdminConfig.list( 'ClusterMember' ).splitlines()
    for member in clusterMembers :
      cmDict = showAsDict( member )      # Retrieve info about this entry
      if cmDict.has_key( 'cluster' ):    # It really better have this...
        name = cmDict[ 'cluster' ].split( '(' )[ 0 ]
        #-------------------------------------------------------------
        # This should be a new, unique addition to our dictionary
        #-------------------------------------------------------------
        if result.has_key( name ) :
          if result[ name ] != cmDict[ 'cluster' ] :
            print nameConflict % ( cmdName, name, result[ name ], member )
            errors += 1
        else :
          result[ name ] = cmDict[ 'cluster' ]
      else :
        print '%(cmdName)s: error - entry missing "cluster" attribute' % locals()
        print AdminConfig.show( cluster )
        errors += 1
    if errors > 0 :
      print '%(cmdName)s: %(errors)d errors encountered.'
      sys.exit( -1 )
  except NameError, e :
    print 'Name not found: ' + str( e )
  except :
    ( kind, value ) = sys.exc_info()[ :2 ]
    print 'Exception  type: ' + str( kind )
    print 'Exception value: ' + str( value )
  return result

#---------------------------------------------------------------------
# Name: fixFileName()
# Role: Unfortunately, an ugly "wart" exists when dealing with Windows
#       fileNames.  Specifically, some Windows fileNames, when passed
#       into a wsadmin script can inadvertently cause "correct"
#       filename characters to be misinterpreted as special Jython
#       "escape" characters.  This occurs when the filename, or
#       directory name character that occur immediately after a
#       directory delimiter (i.e., '\\') happen to be one of the
#       "special" Jython escape characters.  Instead of correctly
#       identifying the directory delimiter as '\\', and leaving the
#       subsequent character alone, the directory delimiter and the
#       character that follows are interpreted as one of these
#       "special" Jython escape character.  So, the purpose of this
#       routine is to correct that interpretation error.
# Note: This routine is equivalent to:
#       def fixFileName( fileName ) :
#         result = fileName.replace( '\a', r'\a' )
#         result = result.replace( '\b', r'\b' )
#         result = result.replace( '\f', r'\f' )
#         result = result.replace( '\n', r'\n' )
#         result = result.replace( '\r', r'\r' )
#         result = result.replace( '\t', r'\t' )
#         result = result.replace( '\v', r'\v' )
#         return result
#---------------------------------------------------------------------
def fixFileName( fileName ) :
  'Return the specified string with selected escape characters unescaped.'
  return fileName.replace(
    '\a', r'\a' ).replace(
    '\b', r'\b' ).replace(
    '\f', r'\f' ).replace(
    '\n', r'\n' ).replace(
    '\r', r'\r' ).replace(
    '\t', r'\t' ).replace(
    '\v', r'\v' )

#---------------------------------------------------------------------
# Name: MBattrAsDict.py
# Role: Utility routine used to return a dictionary of attributes for
#       the specified mbean
# Note: Depends upon availability of WSAS Admin Objects via sys.modules
# History:
#   date   ver who what
# -------- --- --- ---------------------------------------------------
# 09/11/10 0.1 rag Add - Add 'Modifiable' value to result
# 09/04/08 0.0 rag New - insight obtained while writing the book
#---------------------------------------------------------------------
def MBattrAsDict( mbean ) :
  "Given an MBean string, return a dictionary of it's attributes."
  import re
  funName = 'MBattrAsDict'             # Name of this function
  result = {}                          # Result is a dictionary
  #-------------------------------------------------------------------
  # The first line of Help.attributes() result contains the "column
  # headings", not values, and is ignored by slicing using [ 1: ].
  # For each valid attribute, we use the name to get the value
  #-------------------------------------------------------------------
  try :                                # Be prepared for an error
    import sys, Help, AdminControl     # Get access to WSAS objects
    attr = Help.attributes( mbean ).splitlines()[ 1: ]
    for att in attr :
      name = att.split( ' ', 1 )[ 0 ]  # Everything ahead of 1st space
      #---------------------------------------------------------------
      # Unfortunately, for some attribute names, an attempt to
      # getAttribute() will cause an exception, these we ignore.
      #---------------------------------------------------------------
      try :
        result[ name ] = AdminControl.getAttribute( mbean, name )
      except :
        pass
    #-----------------------------------------------------------------
    # After all available attributes have been retrieved, see if one
    # name "Modifiable" exists.  If it does, we have a problem, which
    # needs to be reported.
    # Otherwise, use list comprehension to locate those attributes
    # that are specified as "Read-Write".  Put all of these attribute
    # names into a list, and save it as result[ 'Modifiable' ].
    #-----------------------------------------------------------------
    # Note: Specifying x.split( ' ', 1 )[ 0 ] means that a maximum of
    #       1 split will occur (i.e., strings will be created), and
    #       only the first (i.e., the leading non-blank characters)
    #       will be returned.
    #-----------------------------------------------------------------
    if result.has_key( 'Modifiable' ) :
      print '%(funName)s: "Modifiable" attribute already exists, and not replace.' % locals()
    else :
      result[ 'Modifiable' ] = [ x.split( ' ', 1 )[ 0 ] for x in attr if x.endswith( 'RW' ) ]
  except :
    notavail = 'AdminControl service not available'
    #-----------------------------------------------------------------
    # One likely source of errors is that an invalid MBean was
    # provided, in which case an empty dictionary is returned.
    #-----------------------------------------------------------------
    ( kind, value ) = sys.exc_info()[ :2 ]
    ( kind, value ) = str( kind ), str( value )
    if value.endswith( notavail ) :
      if 'AdminTask' in sys.modules.keys() :
        print '%(funName)s "%(notavail)s": Was wsadmin started with "-conntype none"?' % locals()
      else :
        print '%(funName)s "%(notavail)s": wsadmin isn\'t connected to a server.' % locals()
    elif value.find( 'WASX7025E' ) > -1 :
      print '%(funName)s: Invalid mbean identifier: %(mbean)s' % locals()
    else :
      print 'Exception  type: ' + kind
      print 'Exception value: ' + value
  return result

#---------------------------------------------------------------------
# Name: MBnameAsDict.py
# Role: Utility routine used to return a dictionary of name/value
#       details from an MBean name
# Note: Exception handler requires sys module
# History:
#   date   ver who what
# -------- --- --- ---------------------------------------------------
# 08/10/27 0.1 rag Minor code cleanup
# 08/09/17 0.0 rag New - insight obtained while writing the book
#---------------------------------------------------------------------
def MBnameAsDict( beanName ) :
  'Given an MBean name, return a dictionary of its name/value components.'
  funName = 'MBnameAsDict'             # Name of this function
  domain  = 'WebSphere:'               # MBean name prefix
  result  = {}                         # Result is a dictionary
  try :                                # Be prepared for an error
    import sys                         # Is sys.exc_info() available?
    #-----------------------------------------------------------------
    # Verify that we are working with a WebSphere MBean
    #-----------------------------------------------------------------
    if beanName.startswith( domain ) :
      #---------------------------------------------------------------
      # The rest of MBean name should be composed of comma separated
      # name=value pairs.
      #---------------------------------------------------------------
      for field in beanName[ len( domain ): ].split( ',' ) :
        ( name, value ) = field.split( '=', 1 )
        result[ name ] = value
    else :
      print '''%(funName)s:
Warning: Specified MBean name doesn\'t start with "%(domain)s" and is ignored.
  MBean name: "%(beanName)s"''' % locals()
  except :
    ( kind, value ) = sys.exc_info()[ :2 ]
    print '''%(funName)s: Unexpected exception.\n
  Exception  type: %(kind)s
  Exception value: %(value)s''' % locals()
  return result

#---------------------------------------------------------------------
# Name: nvTextListAsDict.py
# Role:
# Note: Depends upon availability of WSAS Admin Objects via sys.modules
# History:
#   date   ver who what
# -------- --- --- ------------------------------------------
# 08/12/18 0.1 rag Fix - Handle "no value" pair (e.g., "[nodeShortName ]")
# 08/12/17 0.0 rag New - Based upon work for book
#---------------------------------------------------------------------
# Example use:
# > from WAuJ_utilities import nvTextListAsDict
# > sType = AdminTask.listServerTypes().splitlines()[ 0 ]
# > sDict = nvTextListAsDict( sType )
#---------------------------------------------------------------------
def nvTextListAsDict( text ) :
  cmdName = 'nvTextListAsDict'
  #-------------------------------------------------------------------
  # Initialize the dictionary to be returned
  #-------------------------------------------------------------------
  result = {}
  #-------------------------------------------------------------------
  # Verify that the specified string "looks" right...
  #-------------------------------------------------------------------
  if ( text.count( '[' ) == text.count( ']' ) ) and ( text[ 0 ] == '[' ) and ( text[ -1 ] == ']' ) :
    #-----------------------------------------------------------------
    # Remove outer brackets (i.e., '[]') and then leading/trailing blanks
    #-----------------------------------------------------------------
    innerText = text[ 1:-1 ].strip()
    #-----------------------------------------------------------------
    # Locate a possible unused character so the list of values can
    # easily be split into name value pairs
    #-----------------------------------------------------------------
    delimiters = ',.|!@#'              # Possible delimiter values
    for delim in delimiters :
      #---------------------------------------------------------------
      # If this char (delim) doesn't exist in the string, put it in,
      # between the close and open brackets so that it can be used to
      # split the line into a list of strings like '[name value]'.
      #---------------------------------------------------------------
      if innerText.count( delim ) == 0 :
        for pair in innerText.replace( '] [', ']%s[' % delim ).split( delim ) :
          #-----------------------------------------------------------
          # verify that the string starts and ends with brackets...
          # Note: a == b == c is only true if both a == b and b == c
          #-----------------------------------------------------------
          if ( pair.count( '[' ) == pair.count( ']' ) == 1 ) and ( pair[ 0 ] == '[' ) and ( pair[ -1 ] == ']' ) :
            #---------------------------------------------------------
            # Occasionally, we have a situation where pair contains
            # only a name, and not a name/value pair.
            # So, this code was added to handle that rare situation.
            #---------------------------------------------------------
            contents = pair[ 1:-1 ].strip()
            try :
              ( name, value ) = contents.split( ' ', 1 )
            except :
              ( name, value ) = ( contents, '' )
            result[ name ] = value
          else :
            print '%s error - Unexpected text: "%s" (ignored).' % ( cmdName, pair )
        #-------------------------------------------------------------
        # All name/pair sub-strings have been processed, we're done
        #-------------------------------------------------------------
        break
    else :
      print '%s error - Unable to split data, empty dictionary returned.' % cmdName
      return {}
  else :
    print '%s error - Unexpected data format: "%s", empty dictionary returned.' % ( cmdName, text )
  return result

#---------------------------------------------------------------------
# Name: showAsDict.py
# Role: Convert result of AdminConfig.show( configID ) to a dictionary
# Note: Depends upon availability of WSAS Admin Objects via sys.modules
# History:
#   date   ver who what
# -------- --- --- ------------------------------------------
# 08/09/06 0.0 rag New - Based upon work down for IMPACT 2008
#---------------------------------------------------------------------
# Example use:
# > from WAuJ_utilities import showAsDict
# > servers = AdminConfig.list( 'Server' ).splitlines()
# > svrDict = showAsDict( servers[ 0 ] )
#---------------------------------------------------------------------
def showAsDict( configID ) :
  'Return a dictionary of the AdminConfig.show( configID ) result.'
  result = {}
  try :
    import sys, AdminConfig            # Get access to WSAS objects
    #-----------------------------------------------------------------
    # The result of the AdminConfig.show() should be a string
    # containing many lines.  Each line of which starts and ends
    # with brackets.  The "name" portion should be separated from the
    # associated value by a space.
    #-----------------------------------------------------------------
    for item in AdminConfig.show( configID ).splitlines() :
      if ( item[ 0 ] == '[' ) and ( item[ -1 ] == ']' ) :
        ( key, value ) = item[ 1:-1 ].split( ' ', 1 )
        result[ key ] = value
  except NameError, e :
    print 'Name not found: ' + str( e )
  except :
    ( kind, value ) = sys.exc_info()[ :2 ]
    print 'Exception  type: ' + str( kind )
    print 'Exception value: ' + str( value )
  return result

#---------------------------------------------------------------------
# Name: Usage()
#---------------------------------------------------------------------
def Usage( cmd = 'WAuJ_utilities' ) :
  'Display the usage information for the module.'
  #-------------------------------------------------------------------
  # To be able to access to the module docstring (i.e., __doc__), we
  # have to:
  #-------------------------------------------------------------------
  # 1. Define a global variable, and bind the value of __doc__ to it
  #    (see below)
  # 2. Copy the contents of the global variable to a local variable
  #    This lets us use locals() to access the value.
  #-------------------------------------------------------------------
  info = docstring

  print '''     File: %(cmd)s.py
%(info)s
 Examples:
   import %(cmd)s\n
   ...
   from %(cmd)s import showAsDict''' % locals()

#---------------------------------------------------------------------
# main: Verify that this file was imported, and not executed.
#---------------------------------------------------------------------
docstring = __doc__
if ( __name__ == 'main' ) or ( __name__ == '__main__' ) :
  Usage( __name__ )


