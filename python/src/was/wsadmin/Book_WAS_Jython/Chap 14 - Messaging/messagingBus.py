#messagingBus.py

import AdminConfig
import AdminTask


# You should be able to modify this example pretty extensivly
# just by changing the values of the following variables
nameOfBus = "VerySimpleBus"

# Node and Server names for bus members
# If you add a Cluster as a bus member
# substitute the Cluster name in  place of
# the Node name / Server name combination
oneNodeName = "Node01"
oneServerName = "Q01Srv"

anotherNodeName = "Node02"
anotherServerName = "Q02Srv"

nameOfFactory = "SimpleSIBFactory"
jndiNameOfFactory = "jms/simpleSIB01"
connectionFactoryScope = "/Cell:Cell01/"
connectionFactoryDescription = "\"The factory for our " + \
nameOfBus + "\""

nameOfQueue = "SimpleBusDestination-AQueue"
sibDestinationDescription =                           \
"\"Just some tables in a database that supports our " \
+ nameOfBus + "\""

# your choices here are EITHER:
# 1. a node name and a server name OR
#         -node MyNodeName -server SomeServerInThatNode
# 2. the name of a cluster
#         -cluster TheNameOfSomeCluster
actualLocationOfQueue = ' -node ' + oneNodeName + \
' -server ' + oneServerName

nameOfJMSQueue = "SimpleQueueJMSWrapper"
jndiNameOfJMSQueue = "jms/simpleQueueWrapper"
jmsQueueDescription = \
"\"This wrapper allows an application to use our " \
+ nameOfQueue + \
" queue even if we change messaging software in the future\""




def create():
  """Create an example of a messaging queue"""
  
  # create the plumbing inside an ApplicationServer
  print AdminTask.createSIBus('[-bus ' + nameOfBus + '  ]')
  
  # tell us the name of the bus
  # tell us the server or cluster that will be
  # a part of the bus
  # tell us if the bus member will use a database or
  # the file system to hold messages
  print AdminTask.addSIBusMember('[-bus ' + nameOfBus +      \
  ' -node ' + oneNodeName +                                  \
  '  -server ' + oneServerName + ' -fileStore  ]')
  
  # create plumbing for a Queue
  print AdminTask.createSIBDestination('[-bus ' + nameOfBus + \
  ' -name ' + nameOfQueue + '  -type Queue ' +                \
  actualLocationOfQueue + '   -description ' +                \
  sibDestinationDescription + ' ]')
  
  factoryVisibility = AdminConfig.getid(connectionFactoryScope)
  print factoryVisibility
  srvCfgID = AdminConfig.getid( '/Node:' + oneNodeName +     \
  '/Server:' + oneServerName + '/' )
  print srvCfgID
  
  #create the plumbing applications need in order
  # to use our VerySimpleBus
  factoryID = AdminTask.createSIBJMSConnectionFactory(    \
  factoryVisibility, '[-name ' + nameOfFactory +          \
  ' -jndiName ' +   jndiNameOfFactory +                   \
  '  -busName ' + nameOfBus +                             \
  '    -category Experiment01   -description ' +          \
  connectionFactoryDescription + '   ]')
  print factoryID
  
  jmsQueueWrapper = AdminTask.createSIBJMSQueue( srvCfgID,    \
  '[-name ' + nameOfJMSQueue + ' -queueName ' + nameOfQueue  +\
  ' -busName ' + nameOfBus + ' -jndiName ' +                  \
  jndiNameOfJMSQueue +                                        \
  ' -description ' + jmsQueueDescription + '  ]')

def createDBBased():
  """Create an example of a messaging queue"""
  
  # create the plumbing inside an ApplicationServer
  print AdminTask.createSIBus('[-bus ' + nameOfBus + '  ]')
  
  # tell us the name of the bus
  # tell us the server or cluster that will be
  # a part of the bus
  # tell us if the bus member will use a database or
  # the file system to hold messages
  print AdminTask.addSIBusMember('[-bus ' + nameOfBus +      \
  ' -node ' + oneNodeName +                                  \
  '  -server ' + oneServerName + ' -fileStore  ]')
  
  # create plumbing for a Queue
  print AdminTask.createSIBDestination('[-bus ' + nameOfBus + \
  ' -name ' + nameOfQueue + '  -type Queue ' +                \
  actualLocationOfQueue + '   -description ' +                \
  sibDestinationDescription + ' ]')
  
  factoryVisibility = AdminConfig.getid(connectionFactoryScope)
  print factoryVisibility
  srvCfgID = AdminConfig.getid( '/Node:' + oneNodeName +     \
  '/Server:' + oneServerName + '/' )
  print srvCfgID
  
  #create the plumbing applications need in order
  # to use our VerySimpleBus
  factoryID = AdminTask.createSIBJMSConnectionFactory(    \
  factoryVisibility, '[-name ' + nameOfFactory +          \
  ' -jndiName ' +   jndiNameOfFactory +                   \
  '  -busName ' + nameOfBus +                             \
  '    -category Experiment01   -description ' +          \
  connectionFactoryDescription + '   ]')
  print factoryID
  
  jmsQueueWrapper = AdminTask.createSIBJMSQueue( srvCfgID,    \
  '[-name ' + nameOfJMSQueue + ' -queueName ' + nameOfQueue  +\
  ' -busName ' + nameOfBus + ' -jndiName ' +                  \
  jndiNameOfJMSQueue +                                        \
  ' -description ' + jmsQueueDescription + '  ]')


def delete():
  """Delete all the artifacts of our messaging queue"""
  print "About to delete " + nameOfBus
  # This deletes:
  #    the bus itself
  #    all bus members
  #    the messaging engines
  AdminTask.deleteSIBus( '[-bus ' + nameOfBus + ' ]' )
  
  # This deletes the rest of the Queue artifacts
  
  #    the SIBJMSQueue (really a J2CAdminObject)
  print "Trying to find " + nameOfJMSQueue +      \
  " so we can delete it"
  q = findIDbyName( 'J2CAdminObject', nameOfJMSQueue )
  print "About to delete " + nameOfJMSQueue
  AdminTask.deleteSIBJMSQueue(q)
  #    the ConnectionFactory
  print "Trying to find " + nameOfFactory +   \
  " so we can delete it"
  c = findIDbyName( 'ConnectionFactory', nameOfFactory )
  print "About to delete " + nameOfFactory
  AdminTask.deleteSIBJMSConnectionFactory( c )
  print "Deleted everything"


def secureTheBus():
  """Properly enable bus security"""
  busID = AdminConfig.getid( '/SIBus:' + nameOfBus + '/' )
  # this attribute's value must be "true"
  print AdminConfig.showAttribute( busID, 'secure' )
  # this attribute's value must be SSL_ENABLED
  print AdminConfig.showAttribute( busID,'usePermittedChains')
  
  secMgrID = AdminConfig.list( 'Security' )
  # create JAAS authentication identity data
  desc = 'for users of ' + nameOfBus
  uid = nameOfBus + '-User'
  pwd = 'TopSecretPassword'
  print "In WAS Version 5, user names had to be less",    \
  "than 12 characters"
  print "The same restriction applies to WebSphere MQ"
  print uid,"is",str(  len(uid)   ),"characters long"
  
  jaasID = AdminConfig.create( 'JAASAuthData', secMgrID,  \
  [ ['alias', 'SimpleBusAuthenticationAlias'],            \
  ['description', desc],                                  \
  ['userId', uid], ['password',pwd]  ] )
  print jaasID
  
  # revoke default authorizations
  print AdminTask.removeDefaultRoles( '[-bus ' + \
  nameOfBus + ' ]'  )
  # authorize the new identity to access the bus
  print AdminTask.addUserToBusConnectorRole(    \
  '[ -bus ' + nameOfBus + '  -user ' + uid + ' ]' )
  print AdminTask.addUserToDefaultRole(         \
  '[ -bus ' + nameOfBus + ' -role Sender ' +    \
  '-user ' + uid + ' ]' )
  print AdminTask.addUserToDefaultRole(         \
  '[ -bus ' + nameOfBus + ' -role Receiver ' +  \
  '-user ' + uid + ' ]' )
  print AdminTask.addUserToDefaultRole(         \
  '[ -bus ' + nameOfBus + ' -role Browser ' +   \
  '-user ' + uid + ' ]' )
  print AdminTask.addUserToDefaultRole(         \
  '[ -bus ' + nameOfBus + ' -role Creator ' +   \
  '-user ' + uid + ' ]' )
  # all insecure chains should be DISabled
  insecure = getBasicMessagingChains()
  print str( len(insecure) ),"INsecure chains"
  for c in insecure:
    enabled = AdminConfig.showAttribute( c, 'enable' )
    if enabled != 'false':
      print c
      print "Enabled is ",enabled
  # all secure chains should be ENabled
  secure = getSecureMessagingChains()
  print str( len(secure) ),"SECURE chains"
  for c in secure:
    enabled = AdminConfig.showAttribute( c, 'enable' )
    if enabled == 'false':
      print c
      print "Enabled is ",enabled
  # Adjust ConnectionFactory settings
  c = findIDbyName( 'ConnectionFactory', nameOfFactory )
  AdminConfig.modify( c, [ [ 'authDataAlias', jaasID ], \
  [ 'xaRecoveryAuthAlias', jaasID ]  ] )
  print "Successfully secured",nameOfBus



def getBasicMessagingChains():
  """Find all the INsecure transport chains"""
  messagingChains = []
  srvCfgID = AdminConfig.getid( '/Node:' + oneNodeName +     \
  '/Server:' + oneServerName + '/' )
  raw = AdminConfig.list( 'Chain', srvCfgID )
  array = raw.splitlines()
  for c in array:
    chainName = AdminConfig.showAttribute( c, 'name' )
    if chainName.find( 'BasicMessag' ) > -1:
      messagingChains.append( c )
      continue
    if chainName.find( 'DCS(' ) > -1:
      messagingChains.append( c )
      continue
  return messagingChains



def getSecureMessagingChains():
  """Find all the SECURE transport chains"""
  messagingChains = []
  srvCfgID = AdminConfig.getid( '/Node:' + oneNodeName +     \
  '/Server:' + oneServerName + '/' )
  raw = AdminConfig.list( 'Chain', srvCfgID )
  array = raw.splitlines()
  for c in array:
    chainName = AdminConfig.showAttribute( c, 'name' )
    if chainName.find( 'SecureMessag' ) > -1:
      messagingChains.append( c )
      continue
    if chainName.find( 'DCS-Secure' ) > -1:
      messagingChains.append( c )
      continue
  return messagingChains


def findIDbyName( wasType, name ):
  """Search all the ConfigIDs of given type for name"""
  array = AdminConfig.list( wasType ).splitlines()
  for t in array:
    if AdminConfig.showAttribute( t, 'name' ) == name:
      return t
  return None


def oldFashionedDelete():
  # We will need this configuration ID in several places
  # you will need one configuration ID for each bus member
  # If any bus member was a cluster rather than a server
  # you will need the configuration of the cluster
  # rather than the ID of a server
  srvCfgID = AdminConfig.getid( '/Node:' + oneNodeName + \
  '/Server:' + oneServerName + '/' )
  
  # get the ID of the bus we want to delete
  busID = AdminConfig.getid( '/SIBus:' + nameOfBus + '/' )
  print "About to delete:\n" + busID
  AdminConfig.remove( busID )
  
  #get rid of all the bus members
  array = AdminConfig.getid( '/SIBus:' + nameOfBus +    \
  '/SIBusMember:/' ).splitlines()
  print "\nSIBusMembers"
  for m in array:
    print "About to delete:\n" + m
    AdminConfig.remove( m )
  
  # get rid of all the messaging engines
  # (getting rid of the bus member does not
  #      get rid of the messaging engine)
  # (there will be one messaging engine for each bus member)
  raw = AdminConfig.list( 'SIBMessagingEngine', srvCfgID )
  array = raw.splitlines()
  for m in array:
    # The messaging engine(s) we want will have
    # the name of the bus as part of their name
    if m.find( nameOfBus ) > -1:
      print "About to delete:\n" + m
      AdminConfig.remove(m)
  
  #get rid of all SIBQueue
  #There will be one inbound and one outbound
  # (getting rid of the bus does not get rid of the SIBQueue)
  raw = AdminConfig.getid( '/SIBus:' + nameOfBus + '/SIBQueue:/' )
  array = raw.splitlines()
  for q in array:
    print "About to delete:\n" + q
    AdminConfig.remove(q)
      
  #get rid of all connection factories
  array = AdminConfig.list( 'ConnectionFactory' ).splitlines()
  for c in array:
    if AdminConfig.showAttribute( c, 'name' ) == nameOfFactory:
      AdminConfig.remove(c)
  
  
  #get rid of JMSQueue
  #These show up as J2CAdminObjects
  # (if you make a cluster a member of a bus, you need the ID of 
  #       the cluster ratner than the ID of an individual server)
  # (if you have more than one Queue, you will need to repeat
  #  this section for each Queue)
  array = AdminConfig.list( 'J2CAdminObject', srvCfgID )
  for m in array:
    if AdminConfig.showAttribute( m, 'name' ) == nameOfJMSQueue:
      print "About to delete:"
      print m
      AdminConfig.remove(m)



# the real main function code starts here
# the only purpose of this code is 
# to provide confirmation that the module loaded
if __name__ == "main":
  print "threadMonitor is running standalone . . ."
else:
  print  __name__ , "module is loaded"
  #print __name__,"can see "
  #print dir()
