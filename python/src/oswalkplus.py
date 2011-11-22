#!/usr/bin/env python
#
# From Python Cookbook 2.16 on p 88 
# 
# Usage:
# 
# for path in all_files('/tmp', '*.py;*.htm;*.html'):
#    print path

import os, fnmatch
def all_files(root, patterns='*', single_level=False, yield_folders=False):
    # Expand patterns from semicolon-separated string to list
    patterns = patterns.split(';')
    for path, subdirs, files in os.walk(root):
        if yield_folders:
            files.extend(subdirs)
        files.sort()
        for name in files:
            for pattern in patterns:
                if fnmatch.fnmatch(name, pattern):
                    yield os.path.join(path, name)
                    break
        if single_level:
            break

                