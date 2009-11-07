#!/usr/bin/env python
# $Id: working_week.py,v 1.1 2008/12/10 18:12:50 guest Exp $
#
# Call as working.py | working_week.py

import sys
import datetime

found = False
week = 0

for line in sys.stdin:
    date, hours = line.split()
    year, month, day = date.split('-')
    #print "xxx:", year, month, day, "->", hours
    day = datetime.date(int(year), int(month), int(day))
    if (day.weekday() == 0):
        if (found):
            print "From %s to %s -> %1.1f hours" % (monday, lastday, float(week)/10)
        found = True;
        week = int(hours)
        monday = day;
    elif (found):
        week += int(hours)
        lastday = day
