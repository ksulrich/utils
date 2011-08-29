#************************************************************************
# Licensed Materials - Property of IBM
# 5724-M24
# Copyright IBM Corporation 2010.  All rights reserved.
# US Government Users Restricted Rights - Use, duplication or disclosure
# restricted by GSA ADP Schedule Contract with IBM Corp.
#************************************************************************

#
# Use ErrorQ MBean to Resubmit failed events and Resume failed instances
#
# Set 'myModelID' to the model ID. example: MyModel
# Set 'myVersionDate' to the formatted versionDate. example: 2010-05-14T08:18:55 
#

import javax.management as mgmt 
import time
from com.ibm.wbimonitor.lifecycle.spi import LifecycleVersionDate

AdminControl.trace( 'com.ibm.wbimonitor.*=all=enabled' )

################################################
# Start doing work 
################################################

# Set these variables to the correct values or read from input
myModelID = "TestMonitor_MM"
myVersionDate = "2010-09-28T22:00:59"

# -----------------------------------------------------------
# Get the ErrorQ MBean in a form where Objects are returned
# -----------------------------------------------------------
eqObjNameString = AdminControl.completeObjectName('WebSphere:type=ErrorQ,*') 
eqObjName =  mgmt.ObjectName(eqObjNameString) 
# -----------------------------------------------------------
# Get the ErrorQ MBean in a form where Strings are returned
# -----------------------------------------------------------
eqmb = AdminControl.queryNames('WebSphere:type=ErrorQ,*')

# Get the list of model versions that have failed instances.
# Use invoke_jmx to get the result as a list of ModelVersionBeans
parms = None
signature = None
verList = AdminControl.invoke_jmx(eqObjName, 'listFailedModelVersions', parms, signature)

# Loop through the list of ModelVersionBeans
versionDate = LifecycleVersionDate.parse( myVersionDate )
modelDBID = 0
if verList != None:
	for ver in verList:
		print 'ModelVersion DBID=' + ver.getId() + ', modelID=' + ver.getModel() + ', version=' + str(ver.getVersion())
		if myModelID == ver.getModel() and versionDate == ver.getVersion():
			print 'Found the model version'
			modelDBID = ver.getId()
			break

if modelDBID == 0:
	print 'Model version was not found. Nothing to do'
	sys.exit(1)

# Get the number of failed events for the model version
parms = [modelDBID]
signature = ['java.lang.String'] 
cnt = AdminControl.invoke_jmx(eqObjName, 'getFailedEventCount', parms, signature)
print 'Found ' + str(cnt) + ' failed events'

# Get the list of failed instances for this model version
# Use invoke_jmx to get the result as a list of InstanceBeans
# Pass the model DBID as the parm
parms = [modelDBID]
signature = ['java.lang.String'] 
instanceList = AdminControl.invoke_jmx(eqObjName, 'listFailedInstances', parms, signature)

# Loop through the list of InstanceBeans
if instanceList != None:
	print '\nProcessing instances'
	for instance in instanceList:
		instanceDBID = instance.getId()
		rootId = instance.getRootInstanceId()
		print '\nInstance DBID=' + instanceDBID + ', rootID=' + rootId

		# Get the list of failed events for this Instance
		# Use invoke_jmx to get the result as a list of EventBeans
		# Pass the instance DBID as the parm
		parms = [ instanceDBID ] 
		signature = ['java.lang.String'] 
		eventList = AdminControl.invoke_jmx(eqObjName, 'listFailedEvents', parms, signature)
		if eventList != None:
			print '  Processing events'
			for event in eventList:
				eventDBID = event.getId()
				print '  Event DBID=' + eventDBID + ', sequence number=' + str(event.getErrorQueueSequenceNumber()) + ', GUID=' + event.getGlobalUniqueInstanceId() + ', failure=' + event.getFailureSummary()
				# Resubmit the failed event
				AdminControl.invoke(eqmb, 'resubmitEvents', '[' + instanceDBID + ' ' + eventDBID + ' ' + modelDBID + ']')
				# Wait 2 seconds for the event to be processed
				time.sleep(2)

		# ***************** Alternative solution *********************************
		# Instead of resubmitting each failed event individually,
		# you can resubmit all the failed events for an instance.
		# Don't use this solution if the instance has thousands of failed
		# events because it could result in a transaction timeout.
		#
		# AdminControl.invoke(eqmb, 'resubmitInstance', '[' + instanceDBID + ']')
		# ***************** Alternative solution *********************************

		# After resubmitting the events, need to resume the instance
		print '  Resume the instance', instanceDBID
		AdminControl.invoke(eqmb, 'resumeInstance', '[' + instanceDBID + ']')
		# Wait 2 seconds for the instance to be resumed
		time.sleep(2)

print 'The script has finished'
