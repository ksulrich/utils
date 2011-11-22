@echo off
setlocal
@echo Pass the name (without the .py extension) of the Jython script to run

@rem set these variables to the correct values for your system
rem set SCRIPT_DIR=D:/topics/jython/wsadmin/ErrorQ/scripts
set SCRIPT_DIR=C:/cygwin/tmp/python/src/was/wsadmin/ErrorQ/scripts
set MY_PROFILE_HOME=C:/IBM/WID7_WTE/runtimes/bi_v7/profiles/qmwps
set MY_WAS=C:/IBM/WID7_WTE/runtimes/bi_v7
set MY_SOAP_PORT=8881
set MY_USERID=admin
set MY_PW=admin

set EQ_JAR=com.ibm.wbimonitor.errorq_6.1.0.jar
set LC_JAR=com.ibm.wbimonitor.lifecycle.spi_6.1.0.jar

set MY_SOAP=-conntype SOAP -port %MY_SOAP_PORT%
set MY_CP=-wsadmin_classpath %MY_WAS%/plugins/%EQ_JAR%;%MY_WAS%/plugins/%LC_JAR%

@rem to pass userid info directly to wsadmin, uncomment the next line
set SECURITY_PARM=-user %MY_USERID% -password %MY_PW%

set PY_FILE=%SCRIPT_DIR%/%1

@echo on
call "%MY_PROFILE_HOME%\bin\wsadmin.bat" -lang jython %MY_CP% %MY_SOAP% %SECURITY_PARM% -f %PY_FILE%
@echo off
endlocal
