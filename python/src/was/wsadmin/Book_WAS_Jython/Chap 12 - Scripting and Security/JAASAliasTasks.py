def createJAASAlias_Task(alias, user, password, description=None, domain=None):
    "Define a JAAS (J2C) Alias using AdminTask.createAuthDataEntry"

    params = denest([ item for item in ['-alias', alias], ['-description', description], ['-securityDomainName', domain], ['-password',password], ['-user', user] if item[1] ])
    # Create authentication data aentry and return its configuration ID
    return AdminTask.createAuthDataEntry(params)

def showJAASEntries_Task(domain=None):
    "Show all JAAS Auth Data Entries using AdminTask.listAuthDataEntries()"

    if domain == None:
        print AdminTask.listAuthDataEntries()
    else:
        print AdminTask.listAuthDataEntries(["-securityDomainName", domain])

def deleteJAASAlias_Task(alias, domain=None):
    "Delete a named JAAS entry by alias"

    params = denest([ item for item in ['-alias', alias], ['-securityDomainName', domain] if item[1] ])
    AdminTask.deleteAuthDataEntry(params)
