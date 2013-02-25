#---------------------------------------------------------------------
#  Name: SmartStartStop.py
#  From: WebSphere Application Server Administration using Jython
#    By: Robert A. (Bob) Gibson [rag], Arthur Kevin McGrath, Noel J. Bergman
#  ISBN: 0-13-700952-6
#  Role: Script used to start or stop all managed application servers
#        in the cell.
# Usage: wsadmin -lang jython -f SmartStartStop.py
#  Note: See Usage routine for more details
# History:
#   date   ver who what
# -------- --- --- ------------------------------------------
# 09/10/29 0.1 rag Fix - Added ISBN detail
# 08/11/04 0.0 rag New - for the book
#---------------------------------------------------------------------
import getopt, sys

#---------------------------------------------------------------------
# Name: SmartStartStop()
# Role: routine used to implement desired action
#---------------------------------------------------------------------
def SmartStartStop( cmdName = 'SmartStartStop' ) :
  #-------------------------------------------------------------------
  # Name: oops()
  # Role: exception handler
  #-------------------------------------------------------------------
  def oops( cmdName, kind, info ):
    ( kind, info ) = str( kind ), str( info )
    seTxt = 'ScriptingException'              # Special exception text
    sePos = info.find( seTxt )
    if sePos > -1 :
      seMsg = info[ sePos + len( seTxt ) + 2 : ]
      if seMsg.startswith( 'AdminControl' ) :
        print '%s: error - The Deployment Manager appears to be stopped.' % cmdName
      else :
        print '%s: error - %s' % ( cmdName, seMsg )
    else :
      print '''%(cmdName)s: unexpected error encountered.
  Exception type: %(kind)s
  Exception info: %(info)s''' % locals()

  #-------------------------------------------------------------------
  # Name: startServer()
  # Role: nested routine used to stop a specific application server
  # Note: This version of startServer() is slightly different than
  #       some of the other instances of this routine found in other
  #       scripts in the book.  It includes the mbean parameter, so
  #       that a check can be made to determine whether or not the
  #       specified server is active before we try to start it.
  #-------------------------------------------------------------------
  def startServer( serverName, nodeName, mbean ) :
    try :
      if mbean :
        print '  startServer( "%(serverName)s", "%(nodeName)s" ) - server already active' % locals()
      else :
        print '  startServer( "%(serverName)s", "%(nodeName)s" )' % locals()
        AdminControl.startServer( serverName, nodeName )
    except :
      ( kind, info ) = sys.exc_info()[ :2 ]
      oops( cmdName, kind, info )

  #-------------------------------------------------------------------
  # Name: stopServer()
  # Role: nested routine used to stop a specific application server
  # Note: This version of stopServer() is slightly different than some
  #       of the other instances of this routine found in other
  #       scripts in the book.  It includes the mbean parameter, so
  #       that a check can be made to determine whether or not the
  #       specified server is active before we try to stop it.
  #-------------------------------------------------------------------
  def stopServer( serverName, nodeName, mbean ) :
    try :
      if mbean :
        print '  stopServer( "%(serverName)s", "%(nodeName)s" )' % locals()
        AdminControl.stopServer( serverName, nodeName )
      else :
        print '  stopServer( "%(serverName)s", "%(nodeName)s" ) - server not active' % locals()
    except :
      ( kind, info ) = sys.exc_info()[ :2 ]
      oops( cmdName, kind, info )

  #-------------------------------------------------------------------
  # Import required functions
  #-------------------------------------------------------------------
  try :
    from WAuJ_utilities import ConfigIdAsDict
    from WAuJ_utilities import MBnameAsDict
    from WAuJ_utilities import showAsDict
  except ImportError, ie :
    modName = str( ie ).split( ' ' )[ -1 ]
    print '%(cmdName)s: Error - Required module not found: %(modName)s' % locals()
    sys.exit( 1 )
  except :
    ( kind, info ) = sys.exc_info()[ :2 ]
    oops( cmdName, kind, info )
    sys.exit( 1 )

  #-------------------------------------------------------------------
  # SmartStartStop - code
  #-------------------------------------------------------------------
  action = parseOpts( cmdName )        # What action is to be done?
  try :
    #-----------------------------------------------------------------
    # First, verify that wsadmin is connected to a Network Deployment
    # (ND) node.  To do so, determine the process type (processType)
    # attribute of the current node.  To do this, get the MBean name
    # (completeObjectName) for this node (i.e., NDbean).
    #-----------------------------------------------------------------
    # Note: If wsadmin is not connected to an application server (e.g.,
    #       wsadmin started with "-conntype none"), an exception will
    #       be thrown because the AdminControl object is not available.
    #-----------------------------------------------------------------
    cell   = AdminControl.getCell()    # What's the cell Name?
    NDnode = AdminControl.getNode()    # What's the ND node Name?
    NDbean = AdminControl.completeObjectName( 'cell=%s,node=%s,type=Server,*' % ( cell, NDnode ) )
    NDdict = MBnameAsDict( NDbean )    # Make MBean info more accessible

    #-----------------------------------------------------------------
    # Verify the processType of the current node
    #-----------------------------------------------------------------
    if NDdict[ 'processType' ] == 'DeploymentManager' :
      #---------------------------------------------------------------
      # Get the ND configID
      #---------------------------------------------------------------
      NDid = AdminConfig.getid( '/Node:%s/Server:%s/' % ( NDdict[ 'node' ], NDdict[ 'name' ] ) )
      #---------------------------------------------------------------
      # nodes = the list of all node configuration IDs
      # NDnodeID = ND node configuration ID
      #---------------------------------------------------------------
      # Note: The filter() function returns a list containing entries
      #       from parameter 2 (i.e., the nodes list) for which the
      #       function specified in parameter 1 returns "true".  Since
      #       the string method "startswith" returns an int, we needed
      #       to define an anonymous function (using lambda) that will
      #       return "true" when its string parameter starts with the
      #       NDnode name.  To be particularly paranoid, we make sure
      #       that the NDnode name to be matched is immediately
      #       followed by '(', just so that result of the filter will
      #       only match the ND node entry, not just node names that
      #       have the same NDnode name as a prefix.
      #---------------------------------------------------------------
      nodes = AdminConfig.list( 'Node' ).splitlines()
      NDnodeId = filter( lambda x : x.startswith( NDnode + '(' ) > 0, nodes )[ 0 ]

      #---------------------------------------------------------------
      # nodes = the list of (non-ND) node configuration IDs
      #---------------------------------------------------------------
      nodes.remove( NDnodeId )

      #---------------------------------------------------------------
      # What servers exist on the ND node?
      # It is a best practice to only have 1.  Verify this ...
      #---------------------------------------------------------------
      servers = AdminConfig.list( 'Server', NDnodeId ).splitlines()
      if len ( servers ) > 1 :
        print '''%(cmdName)s: Warning - multiple servers found on the ND node.''' % locals()
        #-------------------------------------------------------------
        # For each application server, invoke the requested action...
        #-------------------------------------------------------------
        sNames = []                    # Name & MBean name (info) for servers
        naBean = None                  # Node Agent MBean name string
        for server in servers :
          sDict = showAsDict( server )
          MBean = AdminConfig.getObjectName( server )
          #-----------------------------------------------------------
          # We can't do anything if the node agent isn't active...
          # In fact, if it isn't active, we can't even tell the status
          # of any managed node, so all requests to getObjectName()
          # for any managed server will return an empty string
          #-----------------------------------------------------------
          if ( server != NDid ) :
            if ( sDict[ 'serverType' ] == 'NODE_AGENT' ) :
              naBean = MBean
            else :
              sNames.append( ( sDict[ 'name' ], MBean ) )
        else :
          #-----------------------------------------------------------
          # All servers in this (ND) node have been checked.  If the
          # node agent is active, perform the requested action (start,
          # or stop) on each managed node
          #-----------------------------------------------------------
          if naBean :
            for ( sName, mbean ) in sNames :
              if action == 'start' :
                startServer( sName, NDnode, mbean )
              else :
                stopServer( sName, NDnode, mbean )

      #---------------------------------------------------------------
      # The nodes list contains the configuration IDs for all of the
      # non-ND nodes.  In order to start, or stop the servers on each
      # of these nodes, the nodeagent needs to be active.  So, first,
      # we need to locate the nodeagent, and see it if has an MBean in
      # order to determine if it is "active".
      #---------------------------------------------------------------
      # Note: Just because a nodeagent MBean exists does not guarantee
      #       that the nodeagent will respond to the request.
      #---------------------------------------------------------------
      for node in nodes :
        nDict    = ConfigIdAsDict( node )
        nodeName = nDict[ 'Name' ]

        servers = AdminConfig.list( 'Server', node ).splitlines()
        sNames  = []                   # List of non-NA servers
        naName  = naBean = None        # Just in case we don't find one
        #-------------------------------------------------------------
        # For all servers on this node, which is the nodeagent?
        #-------------------------------------------------------------
        for server in servers :
          sDict = showAsDict( server )
          MBean = AdminConfig.getObjectName( server )
          if sDict[ 'serverType' ] == 'NODE_AGENT' :
            naName = sDict[ 'name' ]
            naBean = MBean
          else :
            sNames.append( ( sDict[ 'name' ], MBean ) )
        else :
          if naName :
            if not naBean :
              print '%(cmdName)s : Warning - nodeagent inactive for node: %(nodeName)s' % locals()
            else :
              #-------------------------------------------------------
              # For each of the managed servers, do the deed...
              #-------------------------------------------------------
              for ( sName, mbean ) in sNames :
                if action == 'start' :
                  startServer( sName, nodeName, mbean )
                else :
                  stopServer( sName, nodeName, mbean )
          else :
            if len( servers ) > 1 :
              print '%(cmdName)s : Warning - nodeagent not found for node: %(nodeName)s' % locals()

    else :
      print '%(cmdName)s: error - connection to Deployment Manager required.' % locals()
  except :
    ( kind, info ) = sys.exc_info()[ :2 ]
    oops( cmdName, kind, info )

#---------------------------------------------------------------------
# Name: parseOpts()
# Role: Process the user specified (command line) options
#---------------------------------------------------------------------
def parseOpts( cmdName ) :
  sOpts = lOpts = ''                   # No parameters are allowed

  #-------------------------------------------------------------------
  # Use the previously defined short and long form option values to
  # parse/process the user specified command line options.
  # Note: Should an unknown option be encountered, a GetoptError will
  #       be raised.
  #-------------------------------------------------------------------
  try:
    opts, args = getopt.getopt( sys.argv, sOpts, lOpts )
  except getopt.GetoptError:
    print '%s: Option error: %s' % ( cmdName, ' '.join( sys.argv ) )
    Usage( cmdName )                # print help information and exit:

  #-------------------------------------------------------------------
  # Check for unhandled/unrecognized options
  # Note: This test differs from many of the other scripts provided
  #       with this book
  #-------------------------------------------------------------------
  if ( len( args ) < 1 ) :
    print '%s: Parameter error - required action missing' % cmdName
    Usage( cmdName )
    sys.exit( 1 )
  elif ( len( args ) > 1 ) :
    argStr = ' '.join( args )
    print '%s: Parameter error - too many options specified: %s' % ( cmdName, argStr )
    Usage( cmdName )
    sys.exit( 1 )
  else :
    request = args[ 0 ]
    if request.lower() not in [ 'stop', 'start' ] :
      print '%s: Unrecognized option - %s' % ( cmdName, request )
      Usage( cmdName )
      sys.exit( 1 )
  return request.lower()

#---------------------------------------------------------------------
# Name: Usage()
# Role: Provide details about how this script is to be used
#---------------------------------------------------------------------
def Usage( cmdName ) :
  print '''
Command: %(cmdName)s\n
Purpose: WebSphere (wsadmin) script used to start, or stop all "managed"
         Application Servers within the cell.\n
  Usage: wsadmin -lang jython -f %(cmdName)s.py [option]\n
  Where: option = stop  - To stop  all managed Application Servers in the cell.
         option = start - To start all managed Application Servers in the cell.\n
Example: wsadmin -lang jython -f %(cmdName)s.py stop
         wsadmin -lang jython -f %(cmdName)s.py start\n
   Note: This script can only function when connected to an active Deployment
         Manager (Network Deployment) node, and will only attempt to perform the
         request action (start, or stop) for those nodes for which an active
         nodeagent can be identified, and located.
''' % locals()
  sys.exit( 1 )

#---------------------------------------------------------------------
# main entry point - verify that the script was executed, not imported
#---------------------------------------------------------------------
if ( __name__ == 'main' ) or ( __name__ == '__main__' ) :
  SmartStartStop()
else :
  Usage( __name__ )
