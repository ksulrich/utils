#
# Delete all of the failed events for a model version
#
# Set 'myModel' and 'myVersion' to the correct values
# before running this script.
#

import javax.management as mgmt 

AdminControl.trace( 'com.ibm.wbimonitor.*=all=enabled' )

################################################
# Start doing work 
################################################

# Set these variables to the correct values
myModel = 'ClaimProcessingTracker'
myVersion = '20100302111955'

# ------------------------------------------
# Get the ErrorQ MBean
# ------------------------------------------
eqmb = AdminControl.queryNames('WebSphere:type=ErrorQ,*')

# Get the DBID for the model version
# Use invoke() to get the result as a String representation of
# a ModelVersionBean. The format is 
# "ModelVersionBean[ <databaseID> ] <modelID>.<versionDate>]".
# For example, "ModelVersionBean[528EA96DB0791FADB3C36397]ClaimProcessingTracker.20100302111955"

modelVer = AdminControl.invoke(eqmb, 'getModelVersion', '[' + myModel + ' ' + myVersion + ']')
print 'modelVer= ', modelVer
temp1 = modelVer.split('[')[1]
modelDBID = temp1.split(']')[0]
print 'modelDBID=', modelDBID

# ------------------------------------------
# Get the ErrorQ MBean another way
# ------------------------------------------
eqObjNameString = AdminControl.completeObjectName('WebSphere:type=ErrorQ,*') 
eqObjName =  mgmt.ObjectName(eqObjNameString) 

# Get the list of failed instances for the model version
# Use invoke_jmx to get the result as a list of InstanceBeans
# Pass the model DBID as the parm
parms = [ modelDBID ] 
signature = ['java.lang.String'] 
instanceList = AdminControl.invoke_jmx(eqObjName, 'listFailedInstances', parms, signature)

# Loop through the list of InstanceBeans
if instanceList != None:
	for instance in instanceList:
		print 'Instance DBID=' + instance.getId() + ', rootID=' + instance.getRootInstanceId()
		# Get the list of failed events  for this Instance
		# Use invoke_jmx to get the result as a list of EventBeans
		# Pass the instance DBID as the parm
		parms = [ instance.getId() ] 
		signature = ['java.lang.String'] 
		eventList = AdminControl.invoke_jmx(eqObjName, 'listFailedEvents', parms, signature)
		if eventList != None:
			for event in eventList:
				print 'Event DBID=' + event.getId() + ', GUID=' + event.getGlobalUniqueInstanceId()
				# Delete the failed event
                                REMARK: Only the events get deleted. The entry in the failed events view are still there
				AdminControl.invoke(eqmb, 'deleteEvents', '[' + instance.getId() + ' ' + event.getId() + ']')
print 'The script has finished'
