# Go to /shared/dokuwiki/data/pages and execute this file like
# python replaceAll.py

import os, fnmatch
def findReplace(directory, find, replace, filePattern):
    for path, dirs, files in os.walk(os.path.abspath(directory)):
        for filename in fnmatch.filter(files, filePattern):
            filepath = os.path.join(path, filename)
            with open(filepath) as f:
                s = f.read()
            s = s.replace(find, replace)
            with open(filepath, "w") as f:
                f.write(s)

findReplace(".", "http://mm01.boeblingen.de.ibm.com:8080/dokuwiki/", "this>", "*.txt") 
