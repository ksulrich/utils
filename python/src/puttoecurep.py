#!/usr/bin/python
#
# Put several files to ecurep
# Usage: puttoecurep <PMR-Number> <list-of-files>
# 
import sys
import subprocess
import datetime

server = "ecurep.mainz.de.ibm.com"
user = "klulrich"

def call(command):
    ''' Call command via subprocess '''
    print(command)
    subprocess.check_call(command)
    
if __name__ == "__main__":
    if (len(sys.argv) < 3):
        print("Usage: " + sys.argv[0] + " <PMR-Nubmer> <list-of-files>")
        sys.exit(1)

    pmr = sys.argv[1]
    directory = "/ecurep/pmr/" + pmr[0] + "/" + pmr[1] + "/" + pmr

    # create directory with current date in root direcotory of the PMR
    now = datetime.datetime.now()
    newdir= directory + '/{0:04d}-{1:02d}-{2:02d}'.format(now.year, now.month, now.day)
    command = ["ssh", user + "@" + server, "-t", "mkdir -p " + newdir]
    call(command)

    # Copy all the files to the new directory
    command = ["scp"] + [i for i in sys.argv[2:]] + [user + "@" + server + ":" + newdir + "/." ]
    call(command)