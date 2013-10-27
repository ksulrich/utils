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
        zeitDaten.add(Element(Element.IN, dt1))
        delta1 = timedelta(hours=2)
        zeitDaten.add(Element(Element.OUT, dt1 + delta1))

        dt1 += timedelta(hours=4)
        e1 = Element(Element.IN, dt1)
        zeitDaten.add(e1)
        delta1 = timedelta(hours=2)
        dt11 = dt1 + delta1
        e11 = Element(Element.OUT, dt11)
        zeitDaten.add(e11)

        self.assertEqual(zeitDaten.getForDay(dt1.date()), delta1 + delta1, 'getForDay not working')

if __name__ == '__main__':
    unittest.main()