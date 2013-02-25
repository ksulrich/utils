#-------------------------------------------------------------------------------
# Name: aLC.py
# Role: display the alias attribute for the applicationLoginConfig entries
#-------------------------------------------------------------------------------
import re
from showAsDict import showAsDict
#-------------------------------------------------------------------------------
# For each security configuration ID
#-------------------------------------------------------------------------------
for security in AdminConfig.list( 'Security' ).splitlines() :
  try :
    #---------------------------------------------------------------------------
    # 1. Create a dictionary of the security entry
    # 2. Create a dictionary of the contained applicationLoginConfig entry
    # 3. Create a list of entries
    # 4. For each entry, display any alias value
    #---------------------------------------------------------------------------
    aLCdict = showAsDict( showAsDict( security )[ 'applicationLoginConfig' ] )
    entries = aLCdict[ 'entries' ][ 2:-2 ].split( ' ' )
    for entry in entries :
      try :
        eDict = showAsDict( entry )
        alias = eDict[ 'alias' ]
        mods  = eDict[ 'loginModules' ][ 1:-1 ].split( ' ' )
        print '%25s : ' % alias,
        for mod in mods :
#         print 'mod: ' + mod
          mDict = showAsDict( mod )
          options = mDict[ 'options' ]
          match = re.compile( '^"\[([^\]]*)\]"$' ).match( options )
          if match :
            options = match.group( 1 ).split( ' ' )
          else :
            options = options[ 1:-1 ].split( ' ' )
#         print options
          for opt in options :
#           print opt
            oDict = showAsDict( opt )
#           print oDict.keys()
            if oDict[ 'name' ] == 'delegate' :
              print oDict[ 'name' ], oDict[ 'required' ]
#         print
      except :
        pass
  except :
    pass