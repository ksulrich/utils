#!/usr/bin/env python
#
# From Python Cookbook Recipe 2.3 on p 67

import os, sys

nargs = len(sys.argv)
if not 3 <= nargs <= 5:
    print 'usage: %s search_text replace_text [infile [outfile]]' % \
        os.path.basename(sys.argv[0])
else:
    stext = sys.argv[1]
    rtext = sys.argv[2]
    input_file = sys.stdin
    output_file = sys.stdout
    if nargs > 3:
        input_file = open(sys.argv[3])
    if nargs > 4:
        output_file = open(sys.argv[4], 'w')
    for s in input_file:
        output_file.write(s.replace(stext, rtext))
    output_file.close()
    input_file.close()

    