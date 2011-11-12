"""Convert to and from Roman numerals

This program is part of "Dive Into Python", a free Python book for
experienced programmers.  Visit http://diveintopython.org/ for the
latest version.
"""

__author__ = "Mark Pilgrim (f8dy@diveintopython.org)"
__version__ = "$Revision: 1.1.1.1 $"
__date__ = "$Date: 2002/02/21 18:45:46 $"
__copyright__ = "Copyright (c) 2001 Mark Pilgrim"
__license__ = "Python"

#Define exceptions
class RomanError(Exception): pass
class OutOfRangeError(RomanError): pass
class NotIntegerError(RomanError): pass
class InvalidRomanNumeralError(RomanError): pass

def toRoman(n):
    """convert integer to Roman numeral"""
    pass

def fromRoman(s):
    """convert Roman numeral to integer"""
    pass
