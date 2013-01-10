from showAsDict import showAsDict
import re

cfgIDre = re.compile( '^(\w*\([^)]+\))$' )
servers = AdminConfig.list( 'Server' ).splitlines()

print 'Using RegExp to locate configuration IDs'
print '-' * 40
for server in servers :
  cid = cfgIDre.match( server )
  if cid :
    print cid.group( 1 )

print '\nUsing RegExp to locate nested configIDs'
print '-' * 40
sDict = showAsDict( server )
names = sDict.keys()
names.sort()
for name in names :
  val = sDict[ name ]
  cid = cfgIDre.match( val )
  if cid :
    print '%20s : %s' % ( name, cid.group( 1 ) )
