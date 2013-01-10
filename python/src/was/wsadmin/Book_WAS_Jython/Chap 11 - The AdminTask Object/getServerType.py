from WAuJ_utilities import ConfigIdAsDict
for server in AdminConfig.list( ‘Server’ ).splitlines() :
  sDict = ConfigIdAsDict( server )
  server = sDict[ ‘servers’ ]
  node = sDict[ ‘nodes’ ]
  parms = ‘[-serverName %s -nodeName %s]’ % ( server, node )
  sType = AdminTask.getServerType( parms )
  print ‘%10s : %21s : %s’ % ( server, node, sType )