#-------------------------------------------------------------------------------
# Name: ListPorts()
# From: WebSphere Application Server Administration using Jython
#   By: Robert A. (Bob) Gibson [rag], Arthur Kevin McGrath, Noel J. Bergman
# ISBN: 0-13-700952-6
# Role: Display the Port Numbers configured for each AppServer
# History:
#   date   ver who what
# -------- --- --- ----------------------------------------------------
# 09/10/29 0.2 rag Fix - Added ISBN detail
# 09/01/08 0.1 rag Minor cleanup for book
# 04/30/08 0.0 rag New - written for presentation at IMPACT 2008
#-------------------------------------------------------------------------------
def ListPorts() :
  from showAsDict import showAsDict

  #-----------------------------------------------------------------------------
  # Ensure that AdminConfig object is available
  # Note: See WAuJ.py script explained, and described in the book
  #-----------------------------------------------------------------------------
  try :
    import AdminConfig
  except :
    print 'Required WebSphere Administrative object unavailable: AdminConfig'
    return

  #-----------------------------------------------------------------------------
  # Get the list of available ServerEntry configuration IDs
  # ... then, process each configID
  #-----------------------------------------------------------------------------
  SEs = AdminConfig.list( 'ServerEntry' ).splitlines()
  for SE in SEs :
    SEname = SE.split( '(', 1 )[ 0 ]   # The server name occurs before the '('
    print '''
Server name: %s\n
Port#|EndPoint Name
-----+-------------''' % SEname        # Display server name & column headings
    #---------------------------------------------------------------------------
    # For the given server configID (SE) get the list of NamedEndPoints
    # Then, for each NamedEndPoint, display the port # and endPointName values
    #---------------------------------------------------------------------------
    NEPs = AdminConfig.list( 'NamedEndPoint', SE ).splitlines()
    for NEP in NEPs :
      NEPdict = showAsDict( NEP )
      EPdict  = showAsDict( NEPdict[ 'endPoint' ] )
      print '%5d|%s' % ( EPdict[ 'port' ], NEPdict[ 'endPointName' ] )

#-------------------------------------------------------------------------------
# main entry point
#-------------------------------------------------------------------------------
if ( __name__ == '__main__' ) or ( __name__ == 'main' ) :
  ListPorts()
