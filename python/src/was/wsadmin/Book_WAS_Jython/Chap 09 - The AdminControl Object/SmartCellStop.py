#---------------------------------------------------------------------
#  Name: SmartCellStop.py
#  From: WebSphere Application Server Administration using Jython
#    By: Robert A. (Bob) Gibson [rag], Arthur Kevin McGrath, Noel J. Bergman
#  ISBN: 0-13-700952-6
#  Role: Script used to stop all active application servers in the cell,
#        and inform user about inactive nodeagents, and associated
#        (unreachable) application servers.
# Usage: wsadmin -lang jython -f SmartCellStop.py
#  Note: See Usage routine for more details
# History:
#   date   ver who what
# -------- --- --- ------------------------------------------
# 09/10/29 0.1 rag Fix - Added ISBN detail
# 08/11/03 0.0 rag New - based upon insight obtained while writing book
#---------------------------------------------------------------------
import getopt, sys

#---------------------------------------------------------------------
# Name: SmartCellStop()
# Role: routine used to implement desired action
#---------------------------------------------------------------------
def SmartCellStop( cmdName = 'SmartCellStop' ) :
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
  # Name: stopServer()
  # Role: nested routine used to stop a specific application server
  #-------------------------------------------------------------------
  def stopServer( serverName, nodeName ) :
    try :
      print '  stopServer( "%(serverName)s", "%(nodeName)s" )' % locals()
      AdminControl.stopServer( serverName, nodeName )
    except :
      ( kind, info ) = sys.exc_info()[ :2 ]
      oops( cmdName, kind, info )

  #-------------------------------------------------------------------
  # Import required function
  #-------------------------------------------------------------------
  try :
    from WAuJ_utilities import ConfigIdAsDict
    from WAuJ_utilities import showAsDict
    from WAuJ_utilities import MBnameAsDict
  except ImportError, ie :
    modName = str( ie ).split( ' ' )[ -1 ]
    print '%(cmdName)s: Error - Required module not found: %(modName)s' % locals()
    sys.exit( 1 )
  except :
    ( kind, info ) = sys.exc_info()[ :2 ]
    oops( cmdName, kind, info )
    sys.exit( 1 )

  #-------------------------------------------------------------------
  # SmartCellStop - code
  #-------------------------------------------------------------------
  parseOpts( cmdName )                      # Were parameters specified?
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
    cell   = AdminControl.getCell()    # Cell name (not configID)
    NDnode = AdminControl.getNode()    # ND node name
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
      # If any exist (they shouldn't), stop the application servers
      # first, then the node agent.  Save the dmgr for last
      #---------------------------------------------------------------
      servers = AdminConfig.list( 'Server', NDnodeId ).splitlines()
#     print 'ND servers:\n' + '\n'.join( servers )
      if len( servers ) > 1 :
        print '''%(cmdName)s: Warning - multiple servers found on the ND node.''' % locals()
        #-------------------------------------------------------------
        # Get the name of each application server that exists on the
        # ND node, remembering to save the node agent name for later.
        #-------------------------------------------------------------
        NAname = None
        sNames = []
        for server in servers :
          sDict = showAsDict( server )
          if ( server != NDid ) :
            mbean = AdminConfig.getObjectName( server )
            if sDict[ 'serverType' ] == 'NODE_AGENT' :
              NAname = sDict[ 'name' ]
              NAbean = mbean
            else :
              sNames.append( ( sDict[ 'name' ], mbean ) )
        else :
          #-----------------------------------------------------------
          # After processing the list of servers on this node, we need
          # to verify the existance and status of any node agent.
          #-----------------------------------------------------------
          if NAname :
            #---------------------------------------------------------
            # A node agent exists... This is not a best practice...
            # Is it active?  If so, check for, and stop all active
            # servers, then stop the node agent.
            # If no, there's nothing we can do except warn the user.
            #---------------------------------------------------------
            if NAbean :
              for ( sName, mbean ) in sNames :
                if mbean :
                  stopServer( sName, NDnode )
              else :
                stopServer( NAname, NDnode )
            else :
              print '%(cmdName)s: Warning - nodeagent is inactive on node: %(NDnode)s' % locals()

      #---------------------------------------------------------------
      # The nodes list contains the configuration IDs for all of the
      # non-ND nodes.  In order to stop the servers on each of these
      # nodes, the nodeagent needs to be active.  So, first, we need
      # to locate the nodeagent, and see it if has an MBean in order
      # to determine if it is "active".
      #---------------------------------------------------------------
      # Note: Just because a nodeagent MBean exists does not
      #       guarantee that the nodeagent will respond to the
      #       request.
      #---------------------------------------------------------------
      for node in nodes :
        nDict = ConfigIdAsDict( node )
        nodeName = nDict[ 'Name' ]

        servers = AdminConfig.list( 'Server', node ).splitlines()
        sNames  = []                 # List of managed servers
        naName  = naBean = None      # Just in case we don't find one
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
          #-----------------------------------------------------------
          # After checking each server in this node, and separating
          # the node agent server from the others, check to see if
          # a node agent server exists in the list.
          #-----------------------------------------------------------
          if naName :
            #---------------------------------------------------------
            # Is the node agent active?
            #---------------------------------------------------------
            if naBean == '' :
              print '%(cmdName)s : Warning - nodeagent inactive for node: %(nodeName)s' % locals()
            else :
              #-------------------------------------------------------
              # Stop each managed servers
              #-------------------------------------------------------
              for ( sName, mbean ) in sNames :
                stopServer( sName, nodeName )
              else :
                stopServer( naName, nodeName )
          else :
            print '%(cmdName)s : Warning - nodeagent not found for node: %(nodeName)s' % locals()
      else :
        #-------------------------------------------------------------
        # After all of the managed servers and their node agents have
        # been stopped, we can now stop the Deployment Manager server
        #-------------------------------------------------------------
        stopServer( NDdict[ 'name' ], NDdict[ 'node' ] )
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
  #-------------------------------------------------------------------
  if ( args != [] ) :
    argStr = ' '.join( args )
    plural = ''
    if ( len( args ) != 1 ) : plural = 's'
    print '%s: Unrecognized/unknown value%s: %s' % ( cmdName, plural , argStr )
    Usage( cmdName )

#---------------------------------------------------------------------
# Name: Usage()
# Role: Provide details about how this script is to be used
#---------------------------------------------------------------------
def Usage( cmdName ) :
  print '''
Command: %(cmdName)s\n
Purpose: WebSphere (wsadmin) script used to stop all active Application
         Servers within the cell.  The user is informed about nodes for
         which the nodeagent is inactive/unreachable and for which any
         associated application servers remain active.\n
  Usage: wsadmin -lang jython -f %(cmdName)s.py\n
   Note: This script can only function when connected to an active Deployment
         Manager (Network Deployment) node.
''' % locals()
  sys.exit( 1 )

#---------------------------------------------------------------------
# main entry point - verify that the script was executed, not imported
#---------------------------------------------------------------------
if ( __name__ == 'main' ) or ( __name__ == '__main__' ) :
  SmartCellStop()
else :
  Usage( __name__ )
