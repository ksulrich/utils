#!/usr/bin/env python

from oswalkplus import all_files

for path in all_files('/tmp', '*.py;*.htm;*.html;*.txt'):
    print path