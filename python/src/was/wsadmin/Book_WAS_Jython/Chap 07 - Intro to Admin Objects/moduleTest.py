#--------------------------------------------------------------------
# Name: moduleTest
# Role: Demonstrate the difference between module & profile namespaces
#--------------------------------------------------------------------
print 'moduleTest.py'
print 'namespace before import: ' + str( dir() )
import AdminApp, AdminConfig, AdminControl, AdminTask, Help
print 'namespace  after import: ' + str( dir() )
