import javax.management as mgmt 

AdminControl.trace( 'com.ibm.wbimonitor.*=all=enabled' )

# Only delete maxEvents for one failed instance in one run
# if set to -1, all failed events gets deleted in one run
# and the failed instances gets resetted
maxEvents = -1 # delete all

if len(sys.argv) > 0:
    maxEvents = int(sys.argv[0])

print "Process only ", maxEvents, "for every instance"

################################################
# Start doing work 
################################################

# Set these variables to the correct values
# Replace <modelID> with the value of the Model column displayed in the 
# administrative console and <versionDate> with the model version date, 
# in the format YYYY-MM-DDTHH:MM:SS as it is shown in the admin console

myModel = 'ClipsAndTacks'
myVersion = '20070911120730'

eqmb = AdminControl.queryNames('WebSphere:type=ErrorQ,*')
modelVer = AdminControl.invoke(eqmb, 'getModelVersion', '[' + myModel + ' ' + myVersion + ']')
print 'modelVer= ', modelVer
temp1 = modelVer.split('[')[1]
modelDBID = temp1.split(']')[0]
print 'modelDBID=', modelDBID
eqObjNameString = AdminControl.completeObjectName('WebSphere:type=ErrorQ,*') 
eqObjName = mgmt.ObjectName(eqObjNameString) 

## Begin delete failed events ##                  
instancesByDBID = AdminControl.invoke(eqmb, 'listFailedInstances', '[' + modelDBID + ']').split(lineSeparator)                  
for instance in instancesByDBID :
    instance = instance.split('[')[1]
    instance = instance.split(']')[0]
    print "instance=", instance
    eventIds = AdminControl.invoke(eqmb, 'listFailedEventIds', '[' + instance + ']').split(lineSeparator)
    print "eventIds=", eventIds
    counter = 0
    for eventId in eventIds:
        if counter < maxEvents:
            if eventId != '':
                print "delete ", eventId
                AdminControl.invoke(eqmb, 'deleteEvents', '[' + instance + ' ' + eventId + ']')
                counter += 1
## End delete failed events ##

if maxEvents != -1:
    print "Only deleted", maxEvents, "failed events for every instance"
    print "You might need to rerun the script"
    sys.exit(0)

## Begin delete failed instances ##
# Get the MBean
eqObjNameString = AdminControl.completeObjectName('WebSphere:type=ErrorQ,*') 
eqObjName = mgmt.ObjectName(eqObjNameString)

# Pass the model DBID as the parm
parms = [ modelDBID ] 
signature = ['java.lang.String'] 
instList = AdminControl.invoke_jmx(eqObjName, 'listFailedInstances', parms, signature)

# Loop through the list of InstanceBeans
if instList != None:
    for inst in instList:
        rootInstId = inst.getRootInstanceId()
        #rootInstId = rootInstId.replace(";", ";")
        print "rootInstId=", rootInstId
        AdminControl.invoke(eqmb, 'resetEventSequenceInstance', '["' + myModel + '" ' + myVersion + ' "' + rootInstId + '"]')
## End delete failed instances ##

