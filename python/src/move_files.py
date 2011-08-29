import sys
import os

__author__ = 'Klaus Ulrich'

def main(files):
    #print "files=%s" % (files)
    file = os.path.basename(files)
    index = 1
    for line in open(files):
        line = line.rstrip()
        #print "file='%s', input='%s'" % (file, line)
        new = line.lstrip('0123456789')
        print "mv {0} {1:02d}{2}".format(line, index, new)
        index += 1


if __name__ == "__main__":
    file = sys.stdin
    if sys.argv[1:]:
        files = sys.argv[1]
    main(files)