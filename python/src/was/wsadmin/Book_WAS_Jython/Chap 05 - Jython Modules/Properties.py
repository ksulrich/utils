#---------------------------------------------------------------------
# Name: Properties.py
#---------------------------------------------------------------------
'Create a dictionary from a properties file.'

def propfileToDict( fileName ) :
  'Create a dictionary from a properties file.'

  import java.io.FileInputStream
  import java.util.Properties

  try :
    istream = java.io.FileInputStream( fileName )
    props   = java.util.Properties()
    props.load( istream )
    istream.close()
    result = {}
    e = props.keys()
    while e.hasMoreElements() :
      key = e.nextElement()
      result[ key ] = props.getProperty( key )
    return result
  except java.io.FileNotFoundException :
    raise IOError, 'FileNotFound: ' + fileName
