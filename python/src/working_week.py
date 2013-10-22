#!/usr/bin/env python
# $Id: working_week.py,v 1.1 2008/12/10 18:12:50 guest Exp $
#
# Call as working.py | working_week.py

import sys
import datetime
from datetime import timedelta

lastMonday = None
nextMonday = None
week = 0

def previousMonday(day):
    while (day.weekday() != 0):
        day = day + timedelta(days=-1)
    return day

def comingMonday(day):
    while (day.weekday() != 0):
        day = day + timedelta(days=1)
    return day

for line in sys.stdin:
    # a line has the form "2013-10-21 93"
    date, hours = line.split()
    year, month, day = date.split('-')
    day = datetime.date(int(year), int(month), int(day))
    if (lastMonday == None):
        lastMonday = previousMonday(day)
        nextMonday = comingMonday(day)
    if (day < nextMonday):
        week += int(hours)
    else:
        print "From %s to %s -> %4.1f hours" % \
              (lastMonday, (nextMonday + timedelta(days=-1)), float(week) / 10)
        week = int(hours)
        lastMonday = previousMonday(day)
        nextMonday = comingMonday(day + timedelta(days=1))
