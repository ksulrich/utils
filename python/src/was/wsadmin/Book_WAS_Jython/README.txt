Comments by Klaus

You need to add the WAuJ.py script to the property com.ibm.ws.scripting.profiles in the wsadmin.properties file under your profile directory:

...
#-------------------------------------------------------------------------
# The profiles property is a list of profiles to be run before
# running user commands, scripts, or an interactive shell.
# securityProcs is included here by default to make security
# configuration easier.
#-------------------------------------------------------------------------
com.ibm.ws.scripting.profiles=/opt/ibm/BPM/v8.0.1/bin/securityProcs.jacl;/opt/ibm/BPM/v8.0.1/bin/LTPA_LDAPSecurityProcs.jacl;/opt/ibm/BPM/v8.0.1/scripts/WAuJ.py
...

Copy the script showAsDict.py to <WAS_ROOT>/scripts directory.

Now you can run the jython scripts:

root@ku24bpm801rhel64 /opt/ibm/BPM/v8.0.1/profiles/Dmgr01/bin
# ./wsadmin.sh -user admin -password admin -lang jython -f Book_WAS_Jython/Chap\ 06\ -\ wsadmin/ListPorts.py 
WASX7209I: Connected to process "dmgr" on node ku24bpm801rhel64CellManager01 using SOAP connector;  The type of process is: DeploymentManager
-------------------------------------------------------------------------------
Actions performed by WAuJ.py:
> from __future__ import nested_scopes
> sys.modules.update( WSASobjects )  # All admin objects added
> sys.modules[ 'sys' ] = sys
> wasroot = r'/opt/ibm/BPM/v8.0.1'
> sys.path.append( r'/opt/ibm/BPM/v8.0.1/scripts' )
-------------------------------------------------------------------------------

Server name: BPM.AppTarget.ku24bpm801rhel64Node03.0

Port#|EndPoint Name
-----+-------------
 2812|BOOTSTRAP_ADDRESS
 8882|SOAP_CONNECTOR_ADDRESS
...

