#----------------------------------------
# Name: Thing
# Role: Define a Thing object
#----------------------------------------
class Thing :

  'A simple Thing object'         # class docstring

  myName = 'anonymous'            # default attribute value

  #--------------------------------------
  # Name: Thing.setName()
  # Role: Used to set the name attribute
  #--------------------------------------
  def setName( self, name ) :
    'Assign the instance name'    # method docsctring
    self.myName = name            # assignment instance attribute

  #--------------------------------------
  # Name: Thing.getName()
  # Role: Used to get the name attribute
  #--------------------------------------
  def getName( self ) :
    'Return the instance name'    # method docstring
    return self.myName            # return instance attribute

