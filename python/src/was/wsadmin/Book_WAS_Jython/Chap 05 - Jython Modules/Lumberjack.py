#-------------------------------------------------------------
# Name: Lumberjack
# Role: Define an exception object type
#-------------------------------------------------------------
class Lumberjack( Exception ) :

  def __init__( self, value ) :
    self.value = value # Save parm as instance attrib

  def __str__( self ) :
    return repr( self.value ) # Return value as string
