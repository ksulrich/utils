#--------------------------------------------------------------
# Name: countdown.py
# Role: Simple demonstration of a Jython Module
#--------------------------------------------------------------
'A holding place for some potentially useful functions'

#--------------------------------------------------------------
# Name: countdown()
# Role: Simple function
#--------------------------------------------------------------
def countdown( start=10 ):
  'Simple function used to display countdown data'
  while start > 0 :
    print start,
    start -= 1
  print 'done'

#--------------------------------------------------------------
# Statements executed when the file is loaded
#--------------------------------------------------------------
if ( __name__ == 'main' ) or ( __name__ == '__main__' ) :
  print 'countdown.py executed as a stand-alone script file'
else :
  print 'countdown.py loaded as a module'

print 'dir():', dir()
