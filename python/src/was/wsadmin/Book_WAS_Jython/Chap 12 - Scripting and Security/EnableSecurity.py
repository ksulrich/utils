def enforceJava2Security():
    ""

    securityConfigID = AdminConfig.getid("/Security:/")
    AdminConfig.modify(securityConfigID,[['enforceJava2Security','true']])


def disableJava2Security():
    ""

    securityConfigID = AdminConfig.getid("/Security:/")
    AdminConfig.modify(securityConfigID,[['enforceJava2Security','false']])


def enableApplicationSecurity:
    ""
    
    securityConfigID = AdminConfig.getid("/Security:/")
    AdminConfig.modify(securityConfigID,[['appEnabled','true']])


def diableApplicationSecurity:
    ""
    securityConfigID = AdminConfig.getid("/Security:/")
    AdminConfig.modify(securityConfigID,[['appEnabled','false']])
