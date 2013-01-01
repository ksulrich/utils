#!/usr/bin/python
#
# Put several files to ecurep
# Usage: puttoecurep <PMR-Number> <list-of-files>
# 
import sys
import subprocess
import datetime

if (len(sys.argv) < 3):
    print("Usage: " + sys.argv[0] + " <PMR-Nubmer> <list-of-files>")
    sys.exit(1)

pmr = sys.argv[1]
directory = "/ecurep/pmr/" + pmr[0] + "/" + pmr[1] + "/" + pmr

now = datetime.datetime.now()
newdir= directory + '/{0:04d}-{1:02d}-{2:02d}'.format(now.year, now.month, now.day)
command = "ssh klulrich@ecurep.mainz.de.ibm.com -t mkdir -p " + newdir
print(command)
subprocess.check_call(command.split())

command = "scp " + ' '.join(sys.argv[2:]) + " klulrich@ecurep.mainz.de.ibm.com:" + newdir + "/."
print(command)
subprocess.check_call(command.split())