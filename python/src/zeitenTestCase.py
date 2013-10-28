__author__ = 'klaus'

import unittest
from zeiten import Data, Element
from datetime import datetime, timedelta

class ZeitenTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_add(self):
        zeitDaten = Data()

        dt1 = datetime(year=2010, month=10, day=28, hour=9, minute=0, second=0)
        zeitDaten.add(Element(Element.IN, dt1))
        delta = timedelta(hours=2)
        zeitDaten.add(Element(Element.OUT, dt1 + delta))

        dt1 += timedelta(hours=4)
        zeitDaten.add(Element(Element.IN, dt1))
        zeitDaten.add(Element(Element.OUT, dt1 + delta))

        self.assertEqual(zeitDaten.getForDay(dt1.date()), delta + delta, 'getForDay not working')

if __name__ == '__main__':
    unittest.main()