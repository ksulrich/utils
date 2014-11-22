#!/usr/bin/env python3
# $Id: working_week.py,v 1.1 2008/12/10 18:12:50 guest Exp $
#
# Call as working.py | working_week.py

import sys
import datetime
from datetime import timedelta

def previousMonday(day):
    while day.weekday() != 0:
        day -= timedelta(days=1)
    return day

def printout(lastMonday, nextMonday, week):
    print("From %s to %s -> %4.1f hours" % \
          (lastMonday, (nextMonday + timedelta(days=-1)), float(week) / 10))

def main(f):
    lastMonday = None
    nextMonday = None
    week = 0
    for line in f:
        # a line has the form "2013-10-21 93"
        #print "Line: ", line,
        date, hours = line.split()
        year, month, day = date.split('-')
        day = datetime.date(int(year), int(month), int(day))
        #print "Day: %s, lM=%s, nM=%s, week=%d" % (day, lastMonday, nextMonday, week)
        if lastMonday is None:
            lastMonday = previousMonday(day)
            nextMonday = lastMonday + timedelta(days=7)
            week = 0
        while day > nextMonday:
            # we are over next monday already
            printout(lastMonday, nextMonday, week)
            lastMonday = nextMonday
            nextMonday = lastMonday + timedelta(days=7)
            week = 0
        if day == nextMonday:
            # we are at next monday
            printout(lastMonday, nextMonday, week)
            lastMonday = nextMonday
            nextMonday = lastMonday + timedelta(days=7)
            week = 0
        if day >= lastMonday and day < nextMonday:
            week += int(hours)

if __name__ == '__main__':
    f = sys.stdin
    if len(sys.argv) > 1:
        f = open(sys.argv[1])
    main(f)
