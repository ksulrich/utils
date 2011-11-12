"""Unit test for apihelper.py

This program is part of "Dive Into Python", a free Python book for
experienced programmers.  Visit http://diveintopython.org/ for the
latest version.
"""

__author__ = "Mark Pilgrim (f8dy@diveintopython.org)"
__version__ = "$Revision: 1.1.1.1 $"
__date__ = "$Date: 2002/02/21 18:45:44 $"
__copyright__ = "Copyright (c) 2001 Mark Pilgrim"
__license__ = "Python"

import unittest
import apihelper
import sys
from StringIO import StringIO

class Redirector(unittest.TestCase):
	def setUp(self):
		self.savestdout = sys.stdout
		self.redirect = StringIO()
		sys.stdout = self.redirect

	def tearDown(self):
		sys.stdout = self.savestdout

class KnownValues(Redirector):
	def testApiHelper(self):
		"""help should return known result for apihelper"""
		apihelper.help(apihelper)
		self.redirect.seek(0)
		self.assertEqual(self.redirect.read(),
"""help       Print methods and doc strings. Takes module, class, list, dictionary, or string.
""")

class ParamChecks(Redirector):
	def testSpacing(self):
		"""help should honor spacing argument"""
		apihelper.help(apihelper, spacing=20)
		self.redirect.seek(0)
		self.assertEqual(self.redirect.read(),
"""help                 Print methods and doc strings. Takes module, class, list, dictionary, or string.
""")

	def testCollapse(self):
		"""help should honor collapse argument"""
		apihelper.help(apihelper, collapse=0)
		self.redirect.seek(0)
		self.assertEqual(self.redirect.read(),
"""help       Print methods and doc strings.

	Takes module, class, list, dictionary, or string.
""")

class BadInput(unittest.TestCase):
	def testNoObject(self):
		"""help should fail with no object"""
		self.assertRaises(TypeError, apihelper.help, spacing=20)

if __name__ == "__main__":
	unittest.main()
