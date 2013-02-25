#---------------------------------------------------------------------
#  Name: CellStatus.py
#  From: WebSphere Application Server Administration using Jython
#    By: Robert A. (Bob) Gibson [rag], Arthur Kevin McGrath, Noel J. Bergman
#  ISBN: 0-13-700952-6
#  Role: Script used to display the status of the application servers
#        in the cell.
# Usage: wsadmin -lang jython -f CellStatus.py
#  Note: See Usage routine for more details
# History:
#   date   ver who what
# -------- --- --- ------------------------------------------
# 09/10/29 0.1 rag Fix - Added ISBN detail
# 08/11/06 0.0 rag New - based upon insight obtained while writing book
#---------------------------------------------------------------------
import getopt, sys

#---------------------------------------------------------------------
# Name: CellStatus()
# Role: routine used to implement desired action
#---------------------------------------------------------------------
def CellStatus( cmdName = 'CellStatus' ) :
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
  # Name: NodeStatus
  # Role: Process the specified node
  #-------------------------------------------------------------------
  def NodeStatus( configId ):
    nodeName = ConfigIdAsDict( configId )[ 'Name' ]
    servers = AdminConfig.list( 'Server', configId ).splitlines()
    NAname  = None
    NAbean  = None
    sNames  = []
    for server in servers :
      sDict = showAsDict( server )
      kind  = sDict[ 'serverType' ]
      if kind == 'DEPLOYMENT_MANAGER' :
        pass
      elif kind == 'NODE_AGENT' :
        NAname = sDict[ 'name' ]
        NAbean = AdminConfig.getObjectName( server )
      else :
        sNames.append( ( sDict[ 'name' ], AdminConfig.getObjectName( server ) ) )
    else :
      if NAname :
        if NAbean :
          status = 'running'
        else :
          status = 'stopped'
        print '  %s  %s - %s' % ( nodeName, NAname, status )
        for ( sName, mbean ) in sNames :
          if not NAbean :
            status = 'unknown'
          else :
            if mbean :
              status = 'running'
            else :
              status = 'stopped'
          print '    %s - %s' % ( sName, status )

  #-------------------------------------------------------------------
  # Import required function
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
  # CellStatus - code
  #-------------------------------------------------------------------
  parseOpts( cmdName )                 # Were parameters specified?
  try :
    #-----------------------------------------------------------------
    # First, verify that wsadmin is connected to a Network Deployment
    # (ND) node.  To do so, determine the process type (processType)
    # attribute of the current node.  To do this, we must first get the
    # completeObjectName for this node (i.e., the MBean name).
    #-----------------------------------------------------------------
    # Note: If wsadmin is not connected to an application server (e.g.,
    #       wsadmin started with "-conntype none"), an exception will be
    #       thrown because the AdminControl object is not available.
    #-----------------------------------------------------------------
    cell   = AdminControl.getCell()         # Cell name (not configID)
    NDnode = AdminControl.getNode()         # ND node name
    NDbean = AdminControl.completeObjectName( 'cell=%s,node=%s,type=Server,*' % ( cell, NDnode ) )
    NDdict = MBnameAsDict( NDbean )

    #-----------------------------------------------------------------
    # Verify the processType of the current node
    #-----------------------------------------------------------------
    if NDdict[ 'processType' ] == 'DeploymentManager' :
      #---------------------------------------------------------------
      # Get the ND configID, this allows us to process the ND node 1st
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
      print NDdict[ 'node' ] + ' - running'
      NodeStatus( NDnodeId )

      #---------------------------------------------------------------
      # nodes = the list of managed node configuration IDs
      #---------------------------------------------------------------
      nodes.remove( NDnodeId )

      #---------------------------------------------------------------
      # Locate all of the nodes within the cell, and all of the servers
      # within each node, and get the status of each
      #---------------------------------------------------------------
      for node in nodes :
        NodeStatus( node )
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
Purpose: WebSphere (wsadmin) script used to display the status of the
         Application Servers within the cell.\n
  Usage: wsadmin -lang jython -f %(cmdName)s.py\n
  Notes:
         1. This script can only function when connected to an active Deployment
            Manager (Network Deployment) node.
         2. When a nodeagent is inactive, the status of the servers managed
            through that nodeagent will be unknown.''' % locals()
  sys.exit( 1 )

#---------------------------------------------------------------------
# main entry point - verify that the script was executed, not imported
#---------------------------------------------------------------------
if ( __name__ == 'main' ) or ( __name__ == '__main__' ) :
  CellStatus()
else :
  Usage( __name__ )
