def dumpAppRoles(application):
    "Call AdminApp.view to dump the MapRolesToUsers task for a single application"
    print "Roles for: " + application
    print AdminApp.view(application, ["-MapRolesToUsers"])


def dumpAllRoles():
    "Call dumpAppRoles for all current applications"

    apps = AdminApp.list().splitlines()
    for app in apps:
        print "-----------"
        dumpAppRoles(app)
    else:
        print "-----------"

def makeRoleMapping(role, everyone="no", allAuth="no", users=[], groups=[]):
    "Construct a properly formatted role mapping for MapUsersToRoles"

    return [role, everyone, allAuth, '|'.join(users), '|'.join(groups)]

def mapOneRoleToUsersOrGroups(application, role, everyone="no", allAuth="no", users=[], groups=[]):
    "A simple sample to demonstrate editing the role mappings for an Enterprise Application or Module"

    # Parameter Structure
    # [
    #   [
    #     String: Role Name
    #     String: Everyone?          ("yes" | "no")
    #     String: All Authenticated? ("yes" | "no")
    #     String: Mapped Users       ("user1|user2|...")
    #     String: Mapped Groups      ("group1|group2|...")
    #   }+
    # ]

    options=["-MapRolesToUsers", [makeRoleMapping(role, everyone, allAuth, users, groups)]]

    print "Trying: ", options
    AdminApp.edit(application, options)
    # AdminApp.updateAccessIDs(application, "true")


dumpAppRoles("TradeApplication")
mapOneRoleToUsersOrGroups("TradeApplication", "TradeAdmin", everyone="yes")
dumpAppRoles("TradeApplication")
mapOneRoleToUsersOrGroups("TradeApplication", "TradeAdmin", allAuth="yes")
dumpAppRoles("TradeApplication")
mapOneRoleToUsersOrGroups("TradeApplication", "TradeAdmin", users=["wasadmin"])
dumpAppRoles("TradeApplication")
mapOneRoleToUsersOrGroups("TradeApplication", "TradeAdmin", users=["wasadmin", "tradeadmin"])
dumpAppRoles("TradeApplication")
mapOneRoleToUsersOrGroups("TradeApplication", "TradeAdmin", groups=["wasadmins"])
dumpAppRoles("TradeApplication")
mapOneRoleToUsersOrGroups("TradeApplication", "TradeAdmin", groups=["wasadmins", "tradeadmins"])
dumpAppRoles("TradeApplication")
mapOneRoleToUsersOrGroups("TradeApplication", "TradeAdmin")
dumpAppRoles("TradeApplication")
