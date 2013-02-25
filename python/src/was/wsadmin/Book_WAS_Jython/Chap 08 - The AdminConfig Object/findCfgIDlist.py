from showAsDict import showAsDict
import re

cListre = re.compile( '^"?\[([^\]]+)]\"$' )
servers = AdminConfig.list( 'Server' ).splitlines()

print 'Using RegExp to locate configID lists'
print '-' * 37
for server in servers :
  cid = cListre.match( server )
  if cid :
    cids = cid.group( 1 ).split( ' ' )
    print '\n'.join( cids )

print '\nUsing RegExp to locate nested configID lists'
print '-' * 44
sDict = showAsDict( server )
names = sDict.keys()
names.sort()

prefix = '\n' + ( ' ' * 23 )

for name in names :
  val = sDict[ name ]
  cid = cListre.match( val )
  if cid :
    cids = cid.group( 1 ).split( ' ' )
    print '%20s : %s' % ( name, prefix.join( cids ) )
