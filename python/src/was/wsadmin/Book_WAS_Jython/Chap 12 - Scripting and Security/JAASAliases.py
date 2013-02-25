def createJAASAlias(alias, userid, password, description=None):
    "Define a JAAS (J2C) Alias"

    # There is a singleton of type Security that is the parent container for all of the JAAS Aliases
    securityConfigID = AdminConfig.getid("/Security:/")
    # Create JAAS Alias (type JAASAuthData) and return its configuration ID
    return AdminConfig.create( 'JAASAuthData', securityConfigID, [ item for item in ['alias', alias], ['description', description], ['userId', userid], ['password',password] if item[1] ] )


def showJAASEntry(entry):
    "Show a JAAS Alias using AdminConfig.show"

    print AdminConfig.show(entry)


def showJAASEntries():
    "Show JAAS Entries using AdminConfig.show"

    for entry in AdminConfig.list("JAASAuthData").splitlines():
        print "---------"
        showJAASEntry(entry)
    else:
        print "---------"


def getJAASByAlias(alias):
    for entry in AdminConfig.list("JAASAuthData").splitlines():
        if alias.strip() == AdminConfig.showAttribute(entry, "alias"):
            return entry
    return


def showJAASAlias(alias):
    "Show a JAAS Alias, given its alias"

    entry = getJAASByAlias(alias)
    if entry:
        showJAASEntry(entry)


def changeJAASAlias(alias, userid=None, password=None, description=None):
    "Modify specified attributes of a JAAS Alias"
    entry = getJAASByAlias(alias)
    if entry:
        AdminConfig.modify(entry, [ item for item in ['description', description], ['userId', userid], ['password',password] if item[1] ] )

    
def changeJAASPassword(alias, newpass):
    "Change the password for a JAAS Alias"

    changeJAASAlias(alias, password=newpass)


def changeJAASUserId(alias, newuser):
    "Change the userId for a JAAS Alias"

    changeJAASAlias(alias, userid=newuser)


def deleteJAASAlias(alias):
    "Delete a named JAAS entry by alias"

    entry = getJAASByAlias(alias)
    if entry:
        AdminConfig.remove(entry)

