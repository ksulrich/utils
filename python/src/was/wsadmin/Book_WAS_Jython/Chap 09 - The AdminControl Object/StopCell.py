#---------------------------------------------------------------------
#  Name: StopCell.py
#  From: WebSphere Application Server Administration using Jython
#    By: Robert A. (Bob) Gibson [rag], Arthur Kevin McGrath, Noel J. Bergman
#  ISBN: 0-13-700952-6
#  Role: Script used to stop all active application servers in the cell.
# Usage: wsadmin -lang jython -f StopCell.py
#  Note: See Usage routine for more details
# History:
#   date   ver who what
# -------- --- --- ------------------------------------------
# 09/10/29 0.1 rag Fix - Added ISBN detail
# 08/11/03 0.0 rag New - based upon insight obtained while writing book
#---------------------------------------------------------------------
import getopt, sys

#---------------------------------------------------------------------
# Name: StopCell()
# Role: routine used to implement desired action
#---------------------------------------------------------------------
def StopCell( cmdName = 'StopCell' ) :
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

  #---------------------------------------------------------------------
  # Import required function
  #---------------------------------------------------------------------
  try :
    from WAuJ_utilities import showAsDict
  except ImportError, ie :
    modName = str( ie ).split( ' ' )[ -1 ]
    print '%(cmdName)s: Error - Required module not found: %(modName)s' % locals()
    sys.exit( 1 )
  except :
    ( kind, info ) = sys.exc_info()[ :2 ]
    oops( cmdName, kind, info )
    sys.exit( 1 )

  #---------------------------------------------------------------------
  # StopCell - code
  #---------------------------------------------------------------------
  parseOpts( cmdName )                      # Were parameters specified?
  try :
    #-------------------------------------------------------------------
    # First, verify that wsadmin is connected to a Network Deployment
    # (ND) node.  To do so, determine the process type (processType)
    # attribute of the current node.  To do this, we must first get the
    # completeObjectName for this node (i.e., server object aka sObj).
    #-------------------------------------------------------------------
    # Note: If wsadmin is not connected to an application server (e.g.,
    #       wsadmin started with "-conntype none"), an exception will be
    #       thrown because the AdminControl object is not available.
    #-------------------------------------------------------------------
    cell   = AdminControl.getCell()         # Cell name (not configID)
    NDnode = AdminControl.getNode()         # ND node name
    sObj   = AdminControl.completeObjectName( 'cell=%s,node=%s,type=Server,*' % ( cell, NDnode ) )
    pType  = AdminControl.getAttribute( sObj, 'processType' )

    #-------------------------------------------------------------------
    # Verify the processType of the current node
    #-------------------------------------------------------------------
    if pType == 'DeploymentManager' :
      #-----------------------------------------------------------------
      # Locate all of the nodes within the current cell, and all of the
      # servers within each node, and try to start each
      #-----------------------------------------------------------------
      for node in AdminConfig.list( 'Node' ).splitlines() :
        nName = AdminConfig.showAttribute( node, 'name' )
        #---------------------------------------------------------------
        # Save the Network Deployment server name (e.g., "dmgr")
        # Note: To be "politically correct", we won't "hard code" the
        #       ND name.  Instead, we'll "presume" that the 1st (and
        #       only) server in the ND node is the ND server, and use
        #       its configuration ID to obtain name of the server.
        #---------------------------------------------------------------
        if nName == NDnode :
          NDname = showAsDict( AdminConfig.list( 'Server', node ).splitlines()[ 0 ] )[ 'name' ]
        else :
          #-------------------------------------------------------------
          # for each server in the current node...
          #-------------------------------------------------------------
          for server in AdminConfig.list( 'Server',  node ).splitlines() :
            sDict = showAsDict( server )
            sName = sDict[ 'name' ]
            #-----------------------------------------------------------
            # Save the nodeagent name until all of the managed servers
            # have been stopped.
            #-----------------------------------------------------------
            if sDict[ 'serverType' ] == 'NODE_AGENT' :
              NAname = sName
            else :
              stopServer( sName, nName )
          else :
            #-------------------------------------------------------------
            # After all of the managed servers have been stopped, we can
            # now stop the Node Agent server...
            #-------------------------------------------------------------
            stopServer( NAname, nName )
      else :
        #-------------------------------------------------------------
        # After all of the managed servers and their node agents have
        # been stopped, we can now stop the Deployment Manager server
        #-------------------------------------------------------------
        stopServer( NDname, NDnode )
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
         Servers within the cell.\n
  Usage: wsadmin -lang jython -f %(cmdName)s.py\n
   Note: This script can only function when connected to an active Deployment
         Manager (Network Deployment) node.
''' % locals()
  sys.exit( 1 )

#---------------------------------------------------------------------
# main entry point - verify that the script was executed, not imported
#---------------------------------------------------------------------
if ( __name__ == 'main' ) or ( __name__ == '__main__' ) :
  StopCell()
else :
  Usage( __name__ )
