#---------------------------------------------------------------------
# Name: envInfo.py
# From: WebSphere Application Server Administration using Jython
#   By: Robert A. (Bob) Gibson [rag], Arthur Kevin McGrath, Noel J. Bergman
# ISBN: 0-13-700952-6
# Role: Script used to demonstrate the use of the AdminControl
#       environment related methods.
# Note: Requires an active connection to a WebSphere Application Server
# History:
#   date   ver who what
# -------- --- --- ----------------------------------------------------
# 09/10/29 0.1 rag Fix - Added ISBN detail
# 08/10/31 0.0 rag New - for the book
#---------------------------------------------------------------------

#---------------------------------------------------------------------
# Name: envInfo()
# Role: Demonstrate use of AdminControl environment methods
#---------------------------------------------------------------------
def envInfo():
  try :
    cell = AdminControl.getCell()
    node = AdminControl.getNode()
    host = AdminControl.getHost()
    port = AdminControl.getPort()
    kind = AdminControl.getType()
    print '''Connected to:
    Cell = %(cell)s
    Node = %(node)s
    Host = %(host)s
    Port = %(port)d
Protocol = %(kind)s''' % locals()

  except :
    ( kind, info ) = sys.exc_info()[ :2 ]
    ( kind, info ) = str( kind ), str( info )
    if info.find( 'AdminControl' ) < 0 :
      print 'Unexpected exception encountered.'
      print '  Exception type: ' + kind
      print '  Exception info: ' + info
    else :
      print 'Error:' + info.split( ':' )[ -1 ]
      print '\nA connection to an active application server is required.'

#---------------------------------------------------------------------
# Name: Usage()
#---------------------------------------------------------------------
def Usage( cmdName = 'envInfo' ) :
  print '''Command: %(cmdName)s\n
 Purpose: WebSphere (wsadmin) script used to demonstrate the use of the
           AdminControl environment related methods.\n
   Usage: %(cmdName)s\n
Examples:
  wsadmin -f %(cmdName)s.py''' % locals()
  sys.exit( 1 )

#---------------------------------------------------------------------
# main entry point - verify that the script was executed, not imported
#---------------------------------------------------------------------
if ( __name__ == 'main' ) or ( __name__ == '__main__' ) :
  envInfo()
else :
  Usage( __name__ )
