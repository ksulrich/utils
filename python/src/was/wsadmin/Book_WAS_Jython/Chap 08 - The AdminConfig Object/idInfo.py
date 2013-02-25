#---------------------------------------------------------------------
# Name: idInfo.py
# Role: Display resutlts of AdminConfig.getid for each "type"
#---------------------------------------------------------------------
types  = AdminConfig.types().splitlines()
tLen   = [ len( x ) for x in types ]
widest = max( tLen )
info   = ( len( types ), min( tLen), widest )
print '# of types: %d  Lengths: min/max = %d/%d' % info
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7
for kind in types :
  info = AdminConfig.getid( '/%s:/' % kind ).splitlines()
  if len( info ) > 0 :
    text = ( '\n' + ' ' * (widest + 3 ) ).join( info )
    print '%*s : %s ' % ( widest, kind, text )
