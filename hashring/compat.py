# coding=utf-8
import sys

'''
This module ensure compatibility between Python 2 and 
Python 3.
'''

_ver = sys.version_info

#: Python 2.x?
is_PY2 = (_ver[0] == 2)

#: Python 3.x?
is_PY3 = (_ver[0] == 3)


if is_PY2:
    range_ = xrange
    string_types = basestring

elif is_PY3:
    range_ = range
    string_types = str
