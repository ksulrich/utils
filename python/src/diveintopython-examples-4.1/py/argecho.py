"""Echo command line arguments

This program is part of "Dive Into Python", a free Python book for
experienced programmers.  Visit http://diveintopython.org/ for the
latest version.
"""

__author__ = "Mark Pilgrim (f8dy@diveintopython.org)"
__version__ = "$Revision: 1.1 $"
__date__ = "$Date: 2002/07/28 21:22:20 $"
__copyright__ = "Copyright (c) 2002 Mark Pilgrim"
__license__ = "Python"

import sys

for arg in sys.argv:
    print arg
