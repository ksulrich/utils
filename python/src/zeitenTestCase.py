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
        dt1 = datetime.now()
        delta = timedelta(hours=2)
        dt11 = dt1 + delta
        dt2 = dt1 + timedelta(days=1)
        e1 = Element(Element.IN, dt1)
        e11 = Element(Element.OUT, dt11)
        e2 = Element(Element.IN, dt2)
        zeitDaten.add(e1)
        zeitDaten.add(e11)
        zeitDaten.add(e2)
        self.assertEqual(zeitDaten.getForDay(dt1.date()), delta, 'getForDay not working')

if __name__ == '__main__':
    unittest.main()