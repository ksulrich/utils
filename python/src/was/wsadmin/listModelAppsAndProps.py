#************************************************************************
# DISCLAIMER:
# The following source code is sample code created by IBM Corporation.
# This sample code is provided to you solely for the purpose of assisting you 
# in the use of the product. The code is provided 'AS IS', without warranty or 
# condition of any kind. IBM shall not be liable for any damages arising out of your
# use of the sample code, even if IBM has been advised of the possibility of
# such damages.
#************************************************************************

import javax.management as mgmt

from com.ibm.wbimonitor.lifecycle.spi import LifecycleConstants
from com.ibm.wbimonitor.lifecycle.spi import LifecycleVersionDate
from com.ibm.wbimonitor.lifecycle.spi.mbeans import LifecycleServicesMBeanFactory

# --------------------------------------------------------------------
# Get the LifecycleServices MBean in a form where Objects are returned
# --------------------------------------------------------------------
lsObjNameString = AdminControl.completeObjectName('WebSphere:type=LifecycleServices,*') 
lsObjName =  mgmt.ObjectName(lsObjNameString) 

parms = [] 
signature = []
versions = AdminControl.invoke_jmx(lsObjName, 'listVersions', parms, signature)

print "Total number of models deployed = %s" % len(versions)

for version in versions:
    modelID = version.getModelID()
    versionDate = version.getVersionDate()
    application = version.getApplication()
    print "Model = %s, Version = %s, Application = %s" % (modelID, versionDate, application)

    # --------------------
    # Get model properties
    # --------------------

    ls_mbean = LifecycleServicesMBeanFactory.getMBean(AdminControl.getAdminClient())

    props = ls_mbean.readVersionGeneralProperties(modelID, versionDate)    
    print 'All properties = ' + props.toString()

    # ---------------------------------
    # Processing mode (6.1 MT or 6.0.2)
    # ---------------------------------
    processingStrategy = props.getProperty("MODEL_ProcessingStrategy")
    if processingStrategy.find("MT") != -1:
        processingMode = "6.1"
    else:
        processingMode = "6.0.2"

    # --------------------------
    # Reordering (true or false)
    # --------------------------
    reorderingSupported = props.getProperty("MODEL_EventReordering")

    print "Processing mode = %s, Reordering = %s" % (processingMode, reorderingSupported)
