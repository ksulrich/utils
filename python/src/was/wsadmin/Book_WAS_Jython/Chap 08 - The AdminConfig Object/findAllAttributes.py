#-------------------------------------------------------------------------------
# Name: findAllAttributes.py
# From: WebSphere Application Server Administration using Jython
#   By: Robert A. (Bob) Gibson [rag], Arthur Kevin McGrath, Noel J. Bergman
# ISBN: 0-13-700952-6
# Role: Traverse the configuration object hierarchy rooted at the specified
#       configID, looking for attributes having the specified name.
# History
#   date   ver who what
# -------- --- --- --------------------
# 09/10/29 0.1 rag Fix - Added ISBN detail
# 08/10/06 0.0 rag New - based upon work done for book
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Name: findAllAttributes()
#-------------------------------------------------------------------------------
def findAllAttributes( configID, attr ) :
  import re                            #
  from   showAsDict import showAsDict  #
  seen   = {}                          # hash of configIDs that have been seen
  found  = []                          # list of matching attributes found
  todo   = [ configID ]                # list of as yet unchecked configIDs
  #-----------------------------------------------------------------------------
  # Regular Expressions used to locate a single configID and a configID list
  #-----------------------------------------------------------------------------
  Cid    = re.compile( '(\w*\([^)]+\)|"[ \w]+\([^)]+\)")' )
  idList = re.compile( '^"?\[([^\]]+)]\"?$' )
  #-----------------------------------------------------------------------------
  # While unchecked configID remain to be processed...
  #-----------------------------------------------------------------------------
  while len( todo ) > 0 :              # while unchecked configIDs remain
    cid = todo.pop( 0 )                #   attrName & configID to be processed
    if seen.has_key( cid ) :           #   has this configID been seen?
      seen[ cid ] += 1                 #     yes, increment seen count
      continue                         #     and skip to the next one
    else :                             #
      seen[ cid ] = 1                  #     no, process it
    objDict = showAsDict( cid )        #   generate the attribute dictionary
    names = objDict.keys()             #   list of attribute names
    names.sort()                       #   ... in alphabetical order
    for name in names :                #   for each attribute name
      val = objDict[ name ]            #     get its value
      if attr == name :                #     has a match been found?
        found.append( ( val, cid ) )   #       Yes, save value & configID found
      IDattr = idList.match( val )     #   Try to match a configID list
      Cattr  = Cid.match( val )        #   Try to match a single configID
      if IDattr :                      #   Is it a configID list?
        IDs = Cid.findall( IDattr.group( 1 ) )
        for ID in IDs :                #     For each configID in the list...
          todo.append( ID )            #       ... add it to the ToDo list
      elif Cattr :                     #   Is it a single configID?
        ID = Cattr.group( 1 )          #     Extract it
        todo.append( ID )              #     ... add it to the ToDo list
  return found                         # return the list of found items

#-------------------------------------------------------------------------------
# main entry
#-------------------------------------------------------------------------------
if ( __name__ == 'main' ) or ( __name__ == '__main__' ) :
  print 'Example use of findAllAttributes():\n'
  print 'Port#| configuration ID\n' + '-----+' + ( '-' * 18 )
  server = AdminConfig.list( 'Server' ).splitlines()[ 0 ]
  for ( val, cfgID ) in findAllAttributes( server, 'port' ) :
    print '%5d|%s' % ( val, cfgID )
