#for domain in AdminConfig.list("SecurityDomain").splitlines():
#    AdminTask.deleteSecurityDomain(['-securityDomainName', AdminConfig.showAttribute(domain, "name"), '-force', 'true'])

#print AdminConfig.list("SecurityDomain")
#print AdminConfig.list("AppSecurity")

#AdminConfig.save()

secdomain = AdminTask.copySecurityDomainFromGlobalSecurity(["-securityDomainName", "mySecurityDomain", "-securityDomainDescription", "Start with Global Security Config"])
secdomainId = "(" + secdomain + ")"
print AdminConfig.getObjectType(secdomainId)

print "Java 2 Security: ", AdminConfig.showAttribute(secdomainId, "enforceJava2Security")

AdminConfig.modify(secdomainId,[['enforceJava2Security','true']])

print "Java 2 Security: ", AdminConfig.showAttribute(secdomainId, "enforceJava2Security")

AdminConfig.modify(secdomainId,[['enforceJava2Security','false']])

print "Java 2 Security: ", AdminConfig.showAttribute(secdomainId, "enforceJava2Security")

AdminTask.setAppActiveSecuritySettings('[-securityDomainName mySecurityDomain -enforceJava2Security true]')

print "Java 2 Security: ", AdminConfig.showAttribute(secdomainId, "enforceJava2Security")

AdminTask.modifySecurityDomain(['-securityDomainName', 'mySecurityDomain', '-securityDomainDescription', 'My Tweaked Security Domain'])

AdminTask.mapResourceToSecurityDomain('[-securityDomainName mySecurityDomain -resourceName Cell=:ServerCluster=TradeCluster]')
AdminTask.mapResourceToSecurityDomain('[-securityDomainName mySecurityDomain -resourceName Cell=:SIBus=msgBus]')

secdomain = AdminTask.createSecurityDomain(['-securityDomainName', 'newDomain', '-securityDomainDescription', 'new security domain'])
secdomainId = "(" + secdomain + ")"
print AdminConfig.getObjectType(secdomainId)

print AdminConfig.list("SecurityDomain")
print AdminConfig.list("AppSecurity")

print AdminTask.listSecurityDomains(['-listDescription', 'true'])

print "My Security Domain Resources: ", AdminTask.listResourcesInSecurityDomain(['-securityDomainName', "mySecurityDomain"]).splitlines()

print "TradeCluster mapped to ", AdminTask.getSecurityDomainForResource('[-resourceName Cell=:ServerCluster=TradeCluster]')
print "msgBus mapped to ", AdminTask.getSecurityDomainForResource('[-resourceName Cell=:SIBus=msgBus]')

AdminTask.removeResourceFromSecurityDomain('[-securityDomainName mySecurityDomain -resourceName Cell=:ServerCluster=TradeCluster]')
AdminTask.removeResourceFromSecurityDomain('[-securityDomainName mySecurityDomain -resourceName Cell=:SIBus=msgBus]')
