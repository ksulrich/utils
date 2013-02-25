#------------------------------------------------------------------
# Name: SysInfo.py
# Role: Display information about the built in sys module items
#------------------------------------------------------------------
names = dir( sys )                     # Get the list of item names
names.sort()                           # Sort the list of names
                                       #
widest = 0                             # Determine the widest name
for name in names :                    # For every name in the list
  if len( name ) > widest :            #   Is this the longest?
    widest = len( name )               #     Yes, save its length
                                       #
count = 0                              #
for name in names :                    # For every name ...
  try :                                #   determine item type()
    kind = str( eval( 'type( sys.%s )' % name ) )
  except :                             #
    kind = '<unknown>'                 #   some don't type()...
  count += 1                           # number of items displayed
  print '%2d: %*s = %s' % ( count, -widest, name, kind )     
