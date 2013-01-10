# Prepare argument list
args=[]
args.append("-applicationName")
args.append("%(appName)s")
args.append("-attachmentType")
args.append("%(attachmentType)s")
args.append("-policySet")
args.append("%(policySet)s")
args.append("-resources")
args.append("[%(resource)s]")

policySet="PingServicePolicySet"

listArgs=args[:4]
listArgs.append("-expandResources")
listArgs.append("*")

# Prepare to apply Web sevice provider attachment

appName="PingServiceApplication"
attachmentType="provider"

# Application Level Attachment
resource="WebService:/"
print AdminTask.createPolicySetAttachment([item % locals() for item in args])
print AdminTask.getPolicySetAttachments([item % locals() for item in listArgs])
AdminConfig.reset()
# Web Service Level Attachment
resource="WebService:/PingService.war:{http://services.wasscripting.com/}PingServiceService"
print AdminTask.createPolicySetAttachment([item % locals() for item in args])
print AdminTask.getPolicySetAttachments([item % locals() for item in listArgs])
AdminConfig.reset()
# Endpoint Level Attachment
resource="WebService:/PingService.war:{http://services.wasscripting.com/}PingServiceService/PingServicePort"
print AdminTask.createPolicySetAttachment([item % locals() for item in args])
print AdminTask.getPolicySetAttachments([item % locals() for item in listArgs])
AdminConfig.reset()
# Operation Level Attachment
resource="WebService:/PingService.war:{http://services.wasscripting.com/}PingServiceService/PingServicePort/ping"
print AdminTask.createPolicySetAttachment([item % locals() for item in args])
print AdminTask.getPolicySetAttachments([item % locals() for item in listArgs])
AdminConfig.reset()

# Prepare to apply Client-side Web service provider attachment

appName="PingServiceClientApplication"
attachmentType="client"

# Client Side Application Level Attachment
resource="WebService:/"
print AdminTask.createPolicySetAttachment([item % locals() for item in args])
print AdminTask.getPolicySetAttachments([item % locals() for item in listArgs])
AdminConfig.reset()
# Client Side Web Service Level Attachment
resource="WebService:/PingServiceClient.war:{http://services.wasscripting.com/}PingServiceService"
print AdminTask.createPolicySetAttachment([item % locals() for item in args])
print AdminTask.getPolicySetAttachments([item % locals() for item in listArgs])
AdminConfig.reset()
# Client Side Endpoint Level Attachment
resource="WebService:/PingServiceClient.war:{http://services.wasscripting.com/}PingServiceService/PingServicePort"
print AdminTask.createPolicySetAttachment([item % locals() for item in args])
print AdminTask.getPolicySetAttachments([item % locals() for item in listArgs])
AdminConfig.reset()
# Client Side Operation Level Attachment
resource="WebService:/PingServiceClient.war:{http://services.wasscripting.com/}PingServiceService/PingServicePort/ping"
print AdminTask.createPolicySetAttachment([item % locals() for item in args])
print AdminTask.getPolicySetAttachments([item % locals() for item in listArgs])
AdminConfig.reset()
