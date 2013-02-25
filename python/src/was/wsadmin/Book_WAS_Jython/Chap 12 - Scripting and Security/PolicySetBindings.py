print AdminTask.getDefaultBindings()

# Prepare Argument List
args=[]
args.append("-bindingName")
args.append("%(bindingName)s")
args.append("-pathName")
args.append("%(pathName)s")

# Export Default Bindings
bindingName="Client sample"
pathName="/tmp/ClientSampleBinding.zip"
AdminTask.exportBinding([item % locals() for item in args])

bindingName="Provider sample"
pathName="/tmp/ProviderSampleBinding.zip"
AdminTask.exportBinding([item % locals() for item in args])

# Delete an existing binding
args=[]
args.append("-bindingLocation")
args.append("%(bindingLocation)s")
args.append("-bindingName")
args.append("%(bindingName)s")
args.append("-remove")
args.append("true")

bindingLocation=""
bindingName="PingProviderBindings"

AdminTask.setBinding([item % locals() for item in args])

# Copy the default Provider sample binding
args=[]
args.append("-sourceBinding")
args.append("%(sourceBinding)s")
args.append("-newBinding")
args.append("%(newBinding)s")
args.append("-newDescription")
args.append("%(newDescription)s")

sourceBinding="Provider sample"
newBinding="PingProviderBindings"
newDescription="Bindings used to connect policies for the Ping service to resources."

AdminTask.copyBinding([item % locals() for item in args])

# Print current WSSecurity attributes for the new policy
args=[]
args.append("-policyType")
args.append("%(policyType)s")
args.append("-bindingLocation")
args.append("%(bindingLocation)s")
args.append("-bindingName")
args.append("%(bindingName)s")

policyType="WSSecurity"
bindingLocation=""
bindingName="PingProviderBindings"

AdminTask.getBinding([item % locals() for item in args])

# [6/9/09 18:04:26:235 EDT] General provider policy set bindings > PingProviderBindings > WS-Security > Keys and certificates > Trust anchor
# Set our service's trust store
args=[]
args.append("-policyType")
args.append("%(policyType)s")
args.append("-attachmentType")
args.append("%(attachmentType)s")
args.append("-bindingScope")
args.append("%(bindingScope)s")

policyType="WSSecurity"
attachmentType="application"
bindingScope="domain"

args.append("-bindingName")
args.append("%(bindingName)s")
args.append("-bindingLocation")
args.append("%(bindingLocation)s")

attributes=[]
attr=[]
attr.append("application.securityinboundbindingconfig.trustanchor_999.keystore.path")
attr.append("%(keystorePath)s")
attributes.append(attr)

attr=[]
attr.append("description")
attr.append("%(newDescription)s")
attributes.append(attr)

attr=[]
attr.append("application.securityinboundbindingconfig.trustanchor_999.name")
attr.append("%(trustAnchorName)s")
attributes.append(attr)

attr=[]
attr.append("domain")
attr.append("global")
attributes.append(attr)

attr=[]
attr.append("application.securityinboundbindingconfig.trustanchor_999.keystore.type")
attr.append("JKS")
attributes.append(attr)

attr=[]
attr.append("application.securityinboundbindingconfig.trustanchor_999.keystore.storepass")
attr.append("%(storepass)s")
attributes.append(attr)

keystorePath="/tmp/pingServiceKeys.jks"
trustAnchorName="PingServiceTrustStore"
storepass="storew0rd"
bindingName="PingProviderBindings"
bindingLocation=""

argList=[items % locals() for items in args]
argList.append("-replace")
argList.append("-attributes")
argList.append([[item[0],item[1] % locals()] for item in attributes])

AdminTask.setBinding(argList)

#AdminTask.setBinding('[-policyType WSSecurity -attachmentType application -bindingScope domain -attributes [ [application.securityinboundbindingconfig.trustanchor_999.keystore.path /tmp/pingServiceKeys.jks] [application.securityinboundbindingconfig.trustanchor_999.keystore.keystoreref ] [description [Bindings used to connect policies for the Ping service to resources.]] [application.securityinboundbindingconfig.trustanchor_999.name PingServiceTrustStore] [domain global] [application.securityinboundbindingconfig.trustanchor_999.keystore.type JKS] [application.securityinboundbindingconfig.trustanchor_999.keystore.storepass storew0rd] ] -bindingName PingProviderBindings -bindingLocation ]')



# [6/9/09 18:11:07:947 EDT] General provider policy set bindings > PingProviderBindings > WS-Security > Authentication and protection > con_signx509token > Callback handler
# Configure the callback handler for consuming signed messages to use our store

attr=[]
attr.append("application.securityinboundbindingconfig.tokenconsumer_2.callbackhandler.classname")
attr.append("%(consumerCallBackHandler)s")

attr=[]
attr.append("application.securityinboundbindingconfig.tokenconsumer_2.callbackhandler.certpathsettings.trustanchorref.reference")
attr.append("%(trustAnchorName)s")
attributes.append(attr)

consumerCallBackHandler="com.ibm.websphere.wssecurity.callbackhandler.X509ConsumeCallbackHandler"

argList=[items % locals() for items in args]
argList.append("-attributes")
argList.append([[item[0],item[1] % locals()] for item in attributes])

AdminTask.setBinding(argList)

attr=[]
attr.append("")
attr.append("%()s")

attr=[]
attr.append("")
attr.append("%()s")


AdminTask.setBinding('[-policyType WSSecurity -attachmentType application -bindingScope domain -attributes [ [application.securityinboundbindingconfig.tokenconsumer_2.callbackhandler.key ] [application.securityinboundbindingconfig.tokenconsumer_2.callbackhandler.keystore ] [application.securityinboundbindingconfig.tokenconsumer_2.callbackhandler.certpathsettings.certstoreref.reference ] [application.securityinboundbindingconfig.tokenconsumer_2.callbackhandler.certpathsettings.trustanycertificate ] [description [Bindings used to connect policies for the Ping service to resources.]] [application.securityinboundbindingconfig.tokenconsumer_2.callbackhandler.classname com.ibm.websphere.wssecurity.callbackhandler.X509ConsumeCallbackHandler] [domain global] [application.securityinboundbindingconfig.tokenconsumer_2.callbackhandler.certpathsettings.trustanchorref.reference PingServiceTrustStore] ] -bindingName PingProviderBindings -bindingLocation ]')

# [6/9/09 18:12:27:365 EDT] General provider policy set bindings > PingProviderBindings > WS-Security > Authentication and protection > con_signx509token
# Configure the binding so that we will trust senders whose X.509 key is in our trust store (established above)
AdminTask.setBinding('[-policyType WSSecurity -attachmentType application -bindingScope domain -attributes [ [application.securityinboundbindingconfig.tokenconsumer_2.valuetype.localname http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-x509-token-profile-1.0#X509v3] [application.securityinboundbindingconfig.tokenconsumer_2.jaasconfig.configname system.wss.consume.x509] [domain global] [application.securityinboundbindingconfig.tokenconsumer_2.enforcetokenversion false] [application.securityinboundbindingconfig.tokenconsumer_2.properties_1.value true] [application.securityinboundbindingconfig.tokenconsumer_2.properties_1.name com.ibm.ws.console.webservices.policyset.protectionToken] [description [Bindings used to connect policies for the Ping service to resources.]] [application.securityinboundbindingconfig.tokenconsumer_2.classname com.ibm.ws.wssecurity.wssapi.token.impl.CommonTokenConsumer] [application.securityinboundbindingconfig.tokenconsumer_2.valuetype.uri ] ] -bindingName PingProviderBindings -bindingLocation ]')


# [6/9/09 18:17:23:062 EDT] General provider policy set bindings > PingProviderBindings > WS-Security > Authentication and protection > gen_signx509token > Callback handler > Custom keystore configuration
# Configure the keystore we will use for signing
AdminTask.setBinding('[-policyType WSSecurity -attachmentType application -bindingScope domain -attributes [ [application.securityoutboundbindingconfig.tokengenerator_0.callbackhandler.keystore.path /tmp/pingServiceKeys.jks] [application.securityoutboundbindingconfig.tokengenerator_0.callbackhandler.keystore.storepass storew0rd] [application.securityoutboundbindingconfig.tokengenerator_0.callbackhandler.key.name cn=server1,O=wasscripting,C=US] [application.securityoutboundbindingconfig.tokengenerator_0.callbackhandler.key.keypass keyw0rd] [application.securityoutboundbindingconfig.tokengenerator_0.callbackhandler.key.alias server1] [description [Bindings used to connect policies for the Ping service to resources.]] [domain global] [application.securityoutboundbindingconfig.tokengenerator_0.callbackhandler.keystore.type JKS] ] -bindingName PingProviderBindings -bindingLocation ]')


# [6/9/09 18:17:41:193 EDT] General provider policy set bindings > PingProviderBindings > WS-Security > Authentication and protection > gen_signx509token > Callback handler
# Configure the outgoing signing token callback handler to use our key for signing
AdminTask.setBinding('[-policyType WSSecurity -attachmentType application -bindingScope domain -attributes [ [application.securityoutboundbindingconfig.tokengenerator_0.callbackhandler.keystore.path /tmp/pingServiceKeys.jks] [application.securityoutboundbindingconfig.tokengenerator_0.callbackhandler.certpathsettings.certstoreref.reference ] [application.securityoutboundbindingconfig.tokengenerator_0.callbackhandler.key.keypass keyw0rd] [domain global] [application.securityoutboundbindingconfig.tokengenerator_0.callbackhandler.classname com.ibm.websphere.wssecurity.callbackhandler.X509GenerateCallbackHandler] [application.securityoutboundbindingconfig.tokengenerator_0.callbackhandler.key.alias server1] [application.securityoutboundbindingconfig.tokengenerator_0.callbackhandler.keystore.type JKS] [application.securityoutboundbindingconfig.tokengenerator_0.callbackhandler.key.name cn=server1,O=wasscripting,C=US] [application.securityoutboundbindingconfig.tokengenerator_0.callbackhandler.keystore.keystoreref ] [description [Bindings used to connect policies for the Ping service to resources.]] [application.securityoutboundbindingconfig.tokengenerator_0.callbackhandler.keystore.storepass storew0rd] ] -bindingName PingProviderBindings -bindingLocation ]')

# [6/9/09 18:17:52:041 EDT] General provider policy set bindings > PingProviderBindings > WS-Security > Authentication and protection > gen_signx509token
# Configure the outgoing signing token
AdminTask.setBinding('[-policyType WSSecurity -attachmentType application -bindingScope domain -attributes [ [application.securityoutboundbindingconfig.tokengenerator_0.properties_1.value true] [application.securityoutboundbindingconfig.tokengenerator_0.valuetype.localname http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-x509-token-profile-1.0#X509v3] [application.securityoutboundbindingconfig.tokengenerator_0.valuetype.uri ] [application.securityoutboundbindingconfig.tokengenerator_0.enforcetokenversion false] [domain global] [application.securityoutboundbindingconfig.tokengenerator_0.jaasconfig.configname system.wss.generate.x509] [application.securityoutboundbindingconfig.tokengenerator_0.classname com.ibm.ws.wssecurity.wssapi.token.impl.CommonTokenGenerator] [application.securityoutboundbindingconfig.tokengenerator_0.properties_1.name com.ibm.ws.console.webservices.policyset.protectionToken] [description [Bindings used to connect policies for the Ping service to resources.]] ] -bindingName PingProviderBindings -bindingLocation ]')

----------------------------------

# [6/9/09 19:42:22:414 EDT] General provider policy set bindings > PingProviderBindings > WS-Security > Authentication and protection > con_encx509token > Callback handler > Custom keystore configuration
# Configure the callback handler for consuming encrypted messages to use our keystore
AdminTask.setBinding('[-policyType WSSecurity -attachmentType application -bindingScope domain -attributes [ [application.securityinboundbindingconfig.tokenconsumer_0.callbackhandler.keystore.storepass storew0rd] [application.securityinboundbindingconfig.tokenconsumer_0.callbackhandler.keystore.type JCEKS] [application.securityinboundbindingconfig.tokenconsumer_0.callbackhandler.keystore.path /tmp/pingServiceKeys.jks] [application.securityinboundbindingconfig.tokenconsumer_0.callbackhandler.key.name cn=server1,O=wasscripting,C=US] [description [Bindings used to connect policies for the Ping service to resources.]] [domain global] [application.securityinboundbindingconfig.tokenconsumer_0.callbackhandler.key.keypass keyw0rd] [application.securityinboundbindingconfig.tokenconsumer_0.callbackhandler.key.alias server1] ] -bindingName PingProviderBindings -bindingLocation ]')

# [6/9/09 19:44:10:891 EDT] General provider policy set bindings > PingProviderBindings > WS-Security > Authentication and protection > con_encx509token > Callback handler
# Configure the callback handler for consuming encrypted messages
AdminTask.setBinding('[-policyType WSSecurity -attachmentType application -bindingScope domain -attributes [ [application.securityinboundbindingconfig.tokenconsumer_0.callbackhandler.key.alias server1] [application.securityinboundbindingconfig.tokenconsumer_0.callbackhandler.certpathsettings.certstoreref.reference ] [application.securityinboundbindingconfig.tokenconsumer_0.callbackhandler.keystore.keystoreref ] [application.securityinboundbindingconfig.tokenconsumer_0.callbackhandler.certpathsettings.trustanchorref.reference ] [application.securityinboundbindingconfig.tokenconsumer_0.callbackhandler.classname com.ibm.websphere.wssecurity.callbackhandler.X509ConsumeCallbackHandler] [application.securityinboundbindingconfig.tokenconsumer_0.callbackhandler.key.name cn=server1,O=wasscripting,C=US] [domain global] [application.securityinboundbindingconfig.tokenconsumer_0.callbackhandler.keystore.storepass storew0rd] [application.securityinboundbindingconfig.tokenconsumer_0.callbackhandler.keystore.type JCEKS] [application.securityinboundbindingconfig.tokenconsumer_0.callbackhandler.certpathsettings.trustanycertificate true] [description [Bindings used to connect policies for the Ping service to resources.]] [application.securityinboundbindingconfig.tokenconsumer_0.callbackhandler.keystore.path /tmp/pingServiceKeys.jks] [application.securityinboundbindingconfig.tokenconsumer_0.callbackhandler.key.keypass keyw0rd] ] -bindingName PingProviderBindings -bindingLocation ]')

# [6/9/09 19:45:39:768 EDT] General provider policy set bindings > PingProviderBindings > WS-Security > Authentication and protection > con_encx509token
# Configure the token consumer for encrypted messages
AdminTask.setBinding('[-policyType WSSecurity -attachmentType application -bindingScope domain -attributes [ [application.securityinboundbindingconfig.tokenconsumer_0.properties_1.value true] [application.securityinboundbindingconfig.tokenconsumer_0.valuetype.uri ] [application.securityinboundbindingconfig.tokenconsumer_0.valuetype.localname http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-x509-token-profile-1.0#X509v3] [domain global] [application.securityinboundbindingconfig.tokenconsumer_0.enforcetokenversion false] [application.securityinboundbindingconfig.tokenconsumer_0.properties_1.name com.ibm.ws.console.webservices.policyset.protectionToken] [application.securityinboundbindingconfig.tokenconsumer_0.jaasconfig.configname system.wss.consume.x509] [application.securityinboundbindingconfig.tokenconsumer_0.classname com.ibm.ws.wssecurity.wssapi.token.impl.CommonTokenConsumer] [description [Bindings used to connect policies for the Ping service to resources.]] ] -bindingName PingProviderBindings -bindingLocation ]')

--------------------------------

# [6/9/09 19:56:38:251 EDT] General provider policy set bindings > PingProviderBindings > WS-Security > Authentication and protection > gen_encx509token > Callback handler > Custom keystore configuration
AdminTask.setBinding('[-policyType WSSecurity -attachmentType application -bindingScope domain -attributes [ [application.securityoutboundbindingconfig.tokengenerator_2.callbackhandler.keystore.type JCEKS] [application.securityoutboundbindingconfig.tokengenerator_2.callbackhandler.keystore.storepass storew0rd] [application.securityoutboundbindingconfig.tokengenerator_2.callbackhandler.keystore.path /tmp/pingServiceKeys.jks] [application.securityoutboundbindingconfig.tokengenerator_2.callbackhandler.key.name cn=client,O=wasscripting,C=US] [application.securityoutboundbindingconfig.tokengenerator_2.callbackhandler.key.alias client] [description [Bindings used to connect policies for the Ping service to resources.]] [domain global] [application.securityoutboundbindingconfig.tokengenerator_2.callbackhandler.key.keypass ] ] -bindingName PingProviderBindings -bindingLocation ]')

# [6/9/09 19:56:45:860 EDT] General provider policy set bindings > PingProviderBindings > WS-Security > Authentication and protection > gen_encx509token > Callback handler
AdminTask.setBinding('[-policyType WSSecurity -attachmentType application -bindingScope domain -attributes [ [application.securityoutboundbindingconfig.tokengenerator_2.callbackhandler.certpathsettings.certstoreref.reference ] [application.securityoutboundbindingconfig.tokengenerator_2.callbackhandler.key.name cn=client,O=wasscripting,C=US] [application.securityoutboundbindingconfig.tokengenerator_2.callbackhandler.keystore.type JCEKS] [domain global] [application.securityoutboundbindingconfig.tokengenerator_2.callbackhandler.key.keypass ] [application.securityoutboundbindingconfig.tokengenerator_2.callbackhandler.classname com.ibm.websphere.wssecurity.callbackhandler.X509GenerateCallbackHandler] [application.securityoutboundbindingconfig.tokengenerator_2.callbackhandler.key.alias client] [application.securityoutboundbindingconfig.tokengenerator_2.callbackhandler.keystore.keystoreref ] [application.securityoutboundbindingconfig.tokengenerator_2.callbackhandler.keystore.path /tmp/pingServiceKeys.jks] [description [Bindings used to connect policies for the Ping service to resources.]] [application.securityoutboundbindingconfig.tokengenerator_2.callbackhandler.keystore.storepass storew0rd] ] -bindingName PingProviderBindings -bindingLocation ]')

# [6/9/09 19:56:52:129 EDT] General provider policy set bindings > PingProviderBindings > WS-Security > Authentication and protection > gen_encx509token
AdminTask.setBinding('[-policyType WSSecurity -attachmentType application -bindingScope domain -attributes [ [application.securityoutboundbindingconfig.tokengenerator_2.enforcetokenversion false] [application.securityoutboundbindingconfig.tokengenerator_2.properties_1.name com.ibm.ws.console.webservices.policyset.protectionToken] [application.securityoutboundbindingconfig.tokengenerator_2.classname com.ibm.ws.wssecurity.wssapi.token.impl.CommonTokenGenerator] [domain global] [application.securityoutboundbindingconfig.tokengenerator_2.jaasconfig.configname system.wss.generate.x509] [application.securityoutboundbindingconfig.tokengenerator_2.properties_1.value true] [application.securityoutboundbindingconfig.tokengenerator_2.valuetype.uri ] [description [Bindings used to connect policies for the Ping service to resources.]] [application.securityoutboundbindingconfig.tokengenerator_2.valuetype.localname http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-x509-token-profile-1.0#X509v3] ] -bindingName PingProviderBindings -bindingLocation ]')

# Associate Policy Set Binding with Application and Policy Set Attachment

args=[]
args.append("-bindingScope")
args.append("%(bindingScope)s")
args.append("-bindingName")
args.append("%(bindingName)s")
args.append("-attachmentType")
args.append("%(attachmentType)s")

attributes=[]
attr=[]
attr.append("application")
attr.append("%(application)s")
attributes.append(attr)

attr=[]
attr.append("attachmentId")
attr.append("%(attachmentId)s")
attributes.append(attr)

application="PingServiceApplication"
attachmentId="007"

argList=[items % locals() for items in args]
argList.append("-bindingLocation")
argList.append([[item[0],item[1] % locals()] for item in attributes])

AdminTask.setBinding(argList)

# AdminTask.setBinding('[-bindingScope domain -bindingName PingProviderBindings -attachmentType application -bindingLocation [ [application PingServiceApplication] [attachmentId 345] ]]')
#['-bindingScope', 'domain', '-bindingName', 'PingProviderBindings', '-attachmentType', 'application', '-bindingLocation', [['application', 'PingServiceApplication'], ['attachmentId', '007']]]
