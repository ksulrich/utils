# see
# https://www-304.ibm.com/support/docview.wss?uid=swg21417899

import javax.management as mgmt 

AdminControl.trace( 'com.ibm.wbimonitor.*=all=enabled' )

################################################
# Start doing work 
################################################

# Set these variables to the correct values
# Replace <modelID> with the value of the Model column displayed in the 
# administrative console and <versionDate> with the model version date, 
# in the format YYYY-MM-DDTHH:MM:SS as it is shown in the admin console

myModel = 'ClipsAndTacks'
myVersion = '20070911120730'

print "Reset failed events for model", myModel, myVersion

eqmb = AdminControl.queryNames('WebSphere:type=ErrorQ,*')
modelVer = AdminControl.invoke(eqmb, 'resetModelVersion', '[' + myModel + ' ' + myVersion + ']')

print "Done"
