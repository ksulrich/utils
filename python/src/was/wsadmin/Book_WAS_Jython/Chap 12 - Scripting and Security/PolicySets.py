# List All Policy Sets
for type in ["application", "system", "system/trust", "default"]:
    print type + ":";
    print AdminTask.listPolicySets(["-policySetType", type])

# Prepare argument list
args=[]
args.append("-policySet")
args.append("%(policySet)s")

# List Information About Policy Set
policySet="Username SecureConversation"
print AdminTask.getPolicySet([item % locals() for item in args])

policySet="Username WSSecurity default"
print AdminTask.getPolicySet([item % locals() for item in args])

# Prepare argument list
args=[]
args.append("-policySet")
args.append("%(policySet)s")
args.append("-pathName")
args.append("%(pathName)s")

# Export Policy Sets
policySet="Username SecureConversation"
pathName="/tmp/UsernameSecureConversation.zip"
AdminTask.exportPolicySet([item % locals() for item in args])

policySet="Username WSSecurity default"
pathName="/tmp/UsernameWSSecuritydefault.zip"
AdminTask.exportPolicySet([item % locals() for item in args])

# Prepare Argument List
args=[]
args.append("-policySet")
args.append("%(policySet)s")

# List Policy Types
print AdminTask.listPolicyTypes([item % locals() for item in args])

# Prepare Argument List
args=[]
args.append("-policySet")
args.append("%(policySet)s")
args.append("-policyType")
args.append("%(policyType)s")
policyType="WSSecurity"

# Display Policy Information
print AdminTask.getPolicyType([item % locals() for item in args])

# Prepare Argument List
args=[]
args.append("-policySet")
args.append("%(policySet)s")

# List Attachments for a Policy Set
print AdminTask.listAttachmentsForPolicySet([item % locals() for item in args])

# Prepare Argument List
args=[]
args.append("-sourcePolicySet")
args.append("%(sourcePolicySet)s")
args.append("-newPolicySet")
args.append("%(newPolicySet)s")
args.append("-newDescription")
args.append("%(newDescription)s")
args.append("-transferAttachments")
args.append("%(transferAttachments)s")

sourcePolicySet="Username WSSecurity default"
newPolicySet="PingServicePolicySet"
newDescription="Policy for Working with the Ping Service"
transferAttachments="false"

AdminTask.copyPolicySet([item % locals() for item in args])

for type in ["application", "system", "system/trust", "default"]:
    print type + ":";
    print AdminTask.listPolicySets(["-policySetType", type])

AdminConfig.reset()
