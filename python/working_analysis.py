#!/usr/bin/env python
# $Id: working_analysis.py,v 1.1 2009/01/19 10:53:00 guest Exp $
#
# Call as working.py | working_analysis.py

import sys

class Day:
    def __init__(self, day, time):
        self.day = day
        self.time = time
    def __repr__(self):
        return "(Day: %s, Time: %f)" % (self.day, self.time)
    def sum(self):
        return self.time
    
class Month:
    def __init__(self, month):
        self.month = month
        self.days = dict()
    def __repr__(self):
        return "(Month: %s, days=%s)" % (self.month, self.days)
    def get_month(self):
        return self.month    
    def add_day(self, day):
        self.days[day.day] = day
    def get_days(self):
        return self.days
    def sum(self):
        sum = 0.0
        for d in self.days.keys():
            sum += self.days[d].sum()
        return sum

class Year:
    def __init__(self, year):
        self.year = year
        self.months = dict()
    def __repr__(self):
        return "(Year: %s, months=%s)" % (self.year, self.months)
    def get_year(self):
        return self.year
    def add_month(self, month):
        self.months[month.month] = month
    def get_months(self):
        return self.months
    def get_month_by_Id(self, m):
        return self.months[m]
    def sum(self):
        sum = 0.0
        for m in self.months.keys():
            sum += self.months[m].sum()
        return sum

class Working:
    def __init__(self):
        self.years = dict()
    def __repr__(self):
        return "%s" % self.years
    def get_years(self):
        return self.years
    def add(self, y, m, d, t):
        try:
            year = self.years[y]
        except KeyError:
            year = Year(y)
            self.years[y] = year
        try:
            month = year.get_month_by_Id(m)
        except KeyError:
            month = Month(m)
            year.add_month(month)
        month.add_day(Day(d, t))
    def print_summary_year(self):
        for y in sorted(self.years.keys()):
            this_year = self.years[y]
            print "%d => %.2f" % (this_year.get_year(), this_year.sum())
    def print_summary_months(self):
        for y in sorted(self.years.keys()):
            this_year = self.years[y]
            months = this_year.get_months()
            for m in sorted(months.keys()):
                print "%d-%d => %.2f" % (this_year.get_year(), months[m].month, months[m].sum())
        
def main():
    w = Working()
    # input like this: "2008-12-19 85"
    for line in sys.stdin:
        #print line
        date, hours = line.split()
        year, month, day = date.split('-')
        y = int(year) 
        m = int(month)
        d = int(day)
        h = float(int(hours))/10
        #print "%d-%d-%d -> %f" % (y, m, d, h)
        w.add(y, m, d, h)
    w.print_summary_year()
    w.print_summary_months()

if __name__ == "__main__":
    main()