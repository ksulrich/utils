def addLDAPHosts(ldapID, hosts):
    "For an LDAP registry (configID) add hosts [[ip,port]+]"

    hostParam = [["hosts", []]]
    hostParam[0][1].extend([[["host", host[0]],["port", host[1]]] for host in hosts])

    AdminConfig.modify(ldapID, hostParam)


def setLDAPHosts(ldapID, hosts):
    "For an LDAP registry (configID) set the hosts [[ip,port]+]"

    # first reset the list so that we can add to it anew
    addLDAPHosts(ldapID, [])
    addLDAPHosts(ldapID, hosts)


def removeLDAPHosts(ldapID, hosts):
    "For an LDAP registry (configID) remove these hosts [[ip,port]+]"

    for endpoint in AdminConfig.showAttribute(ldapID, "hosts")[1:-1].split(" "):
        eph = AdminConfig.showAttribute(endpoint, "host")
        epp = int(AdminConfig.showAttribute(endpoint, "port"))
        for host in hosts:
            if (eph == host[0] and epp == host[1]):
                AdminConfig.remove(endpoint)
                break


def showLDAPHosts(ldapID):
    "For an LDAP registry, show all the hosts"

    print [[["host", AdminConfig.showAttribute(endpoint, "host")], ["port", int(AdminConfig.showAttribute(endpoint, "port"))]] for endpoint in AdminConfig.showAttribute(ldapID, "hosts")[1:-1].split(" ")]


AdminConfig.reset()
myLDAP = AdminConfig.list("LDAPUserRegistry")
#setLDAPHosts(myLDAP, [["127.0.0.1", 389],["127.0.0.2", 389]])
#AdminConfig.reset()
#addLDAPHosts(myLDAP, [["127.0.0.1", 389],["127.0.0.2", 389]])
#AdminConfig.reset()
setLDAPHosts(myLDAP, [["127.0.0.1", 389],["127.0.0.2", 389],["127.0.0.3", 389],["127.0.0.4", 389]])
showLDAPHosts(myLDAP)
removeLDAPHosts(myLDAP,[["127.0.0.3", 389],["127.0.0.2", 389]])
showLDAPHosts(myLDAP)
#AdminConfig.reset()
