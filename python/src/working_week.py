#!/usr/bin/env python
# $Id: working_week.py,v 1.1 2008/12/10 18:12:50 guest Exp $
#
# Sums up all hours for one week and prints out result
#
# Call as working.py | working_week.py

import sys
import datetime

# found marks if Monday was found
found = False

# sum counter for one week
week = 0

for line in sys.stdin:
    date, hours = line.split()
    year, month, day = date.split('-')
    #print "xxx:", year, month, day, "->", hours
    day = datetime.date(int(year), int(month), int(day))
    if (day.weekday() == 0):
        # we have a Monday
        if (found):
            # We have already data collected, print it out
            print "From %s to %s -> %1.1f hours" % (monday, lastday, float(week)/10)
        found = True;
        # Reset sum counter and start again
        week = int(hours)
        # remember this monday for next print out
        monday = day;
    elif (found):
        # No Monday, sum it up
        week += int(hours)
        # remember this day in variable lastday
        lastday = day
