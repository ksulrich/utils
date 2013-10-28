#!/usr/bin/env python

import os
import re
from datetime import datetime, timedelta

FILE_EXT = 'Wissen' + os.sep + 'zeiten.txt'
DB = os.getenv('HOME', 'c:/tmp')
FILE = DB + os.sep + FILE_EXT

class Element:

    IN = 0
    OUT = 1

    def __init__(self, type, dt):
        self.element = { 'type': type, 'dt': dt }

    def __repr__(self):
        return "Element(%d, %s)" % (self.element['type'], self.element['dt'])

    def key(self):
        return self.element['dt'].date()

    def value(self):
        return self.element['dt']

    def type(self):
        return self.element['type']


class Data:
    def __init__(self):
        self.data = {}

    def add(self, e):
        key = e.key()
        if self.data.has_key(key):
            elements = self.data[key]
            assert elements[-1].type() != e.type(), 'illegal IN and OUT sequence'
            self.data[key].append(e)
        else:
            self.data[key] = []
            self.data[key].append(e)

    def getForDay(self, date):
        sum = timedelta(0)
        #print "Data::getForDay(", date, "): return ", self.data[date]
        if self.data.has_key(date):
            i_in = None
            i_out = None
            for i in self.data[date]:
                if (i.type() == 0):
                    i_in = i
                elif (i.type() == 1):
                    i_out = i
                else:
                    raise ValueError("Illegal type found: ", i.type())
                if (i_in != None) and (i_out != None):
                    sum += i_out.value() - i_in.value()
                    i_in = None
                    i_out = None
        return sum

def main():
    data = Data()
    # 03/07/2006	9:30:00
    pin = re.compile('^IN:\s+(\d+)/(\d+)/(\d+)\s+(\d+):(\d+):(\d+)')
    pout = re.compile('^\s+OUT:\s+(\d+)/(\d+)/(\d+)\s+(\d+):(\d+):(\d+)')

    for i in open(FILE):
        if i.find('#') == 0:
            # ignore comments
            continue
        m_in = pin.match(i)
        if (m_in):
            print "IN found: ", m_in.group(1, 2, 3, 4, 5, 6)
            d = datetime(int(m_in.group(3)),
                         int(m_in.group(2)),
                         int(m_in.group(1)),
                         int(m_in.group(4)),
                         int(m_in.group(5)),
                         int(m_in.group(6)))
            print "d=%s, date=%s" % (d, d.date())
            data.add(Element(Element.IN, d))
        m_out = pout.match(i)
        if (m_out):
            print "OUT found: ", m_out.group(1, 2, 3, 4, 5, 6)
            d = datetime(int(m_out.group(3)),
                         int(m_out.group(2)),
                         int(m_out.group(1)),
                         int(m_out.group(4)),
                         int(m_out.group(5)),
                         int(m_out.group(6)))
            print "d=", d
            data.add(Element(Element.OUT, d))


if __name__ == '__main__':
    main()