#!/usr/bin/env python
# $Id$
#
# Usage: ./telefon.py < $HOME/Wissen/telefon.txt <pattern>

import re
import sys

pats = list()
linePat = re.compile("^---")
if len(sys.argv) <= 2:
    print """
Usage: telefon.py <telefon> <pattern_1> <pattern_2> ...  <pattern_n>
       where <pattern_i> is a regular expression like "ul.*"
       The patterns are ANDed, so you can search for that:
       ./telefon.py telefon.txt klaus "ul.*"
       and you are searching for klaus (case does not matter) AND 
       any word starting with ul 
        """
    sys.exit(1)

file = sys.argv[1]
for i in sys.argv[2:]:
    pats.append(re.compile(i, re.IGNORECASE))

def main():
    text = None
    for line in open(file, "r"):
        #print line,
        if linePat.search(line):
            #print "--- found"
            # first or next entry found
            if not text:
                #print "===reset text 1"
                # first entry
                text = ""
            else:
                # entry ended -> search for pattern
                #print "TEXT:", text
                found = True
                for p in pats:
                    match = p.search(text)
                    if (match):
                        found &= True
                    else:
                        found = False
                if found:
                    print "%s" %(79*"-")
                    print "%s" % text,
                # new entry found -> reset text
                #print "===reset text 2"
                text = ""
        elif text is not None:
            # we need to collect data
            #print "===add line"
            text += line

if __name__ == "__main__":
    main()
