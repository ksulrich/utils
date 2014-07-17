#!/usr/bin/env python

import os
import sys
import datetime
import logging

FILE_EXT = 'Wissen' + os.sep + 'working.txt'
DB = os.getenv('HOME', 'c:/tmp')
FILE = DB + os.sep + FILE_EXT

def calc():
    dict = read_data()
    keys = dict.keys()
    keys.sort()
    for k in keys:
        print "%s %3.1d" % (k, dict.get(k))

def read_data():
    d = {}
    logging.info("Read data from %s", FILE)
    for i in open(FILE):
        logging.debug("Read: '%s'", i.rstrip())
        if i.find('#') == 0:
            continue 
        date, value = i.strip().split()
        v = int(value)
        if d.has_key(date):
            d[date] = d[date] + v
            logging.debug("Add value %s to entry %s: New value=%s", v, date, d[date])
        else:
            d[date] = v
            logging.debug("Create new entry for %s: New value=%s", date, d[date])
        logging.info("Have: %s -> %s", date, d[date])
    return d

def main():
    arg = 0
    d = datetime.date.today()
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        
    if arg > 0:
        out = open(FILE, 'a')
        out.write("%s %s\n" % (d, arg))
    else: 
        calc()
    
if __name__ == '__main__':
    # Enable logging as needed. Use logging.INFO or logging.DEBUG
    #logging.basicConfig(level=logging.DEBUG)
    main()
