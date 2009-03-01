# -*- coding: utf-8 -*-

# ******************************************************************************
#
# Copyright (C) 2009 Olivier Tilloy <olivier@tilloy.net>
#
# This file is part of the pyexiv2 distribution.
#
# pyexiv2 is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# pyexiv2 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyexiv2; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, 5th Floor, Boston, MA 02110-1301 USA.
#
# Author: Olivier Tilloy <olivier@tilloy.net>
#
# ******************************************************************************

import unittest
from pyexiv2 import ExifTag, ExifValueError
import datetime


class TestExifTag(unittest.TestCase):

    def test_convert_to_python_ascii(self):
        xtype = 'Ascii'
        # Valid values: datetimes
        self.assertEqual(ExifTag._convert_to_python('2009-03-01 12:46:51', xtype),
                         datetime.datetime(2009, 03, 01, 12, 46, 51))
        self.assertEqual(ExifTag._convert_to_python('2009:03:01 12:46:51', xtype),
                         datetime.datetime(2009, 03, 01, 12, 46, 51))
        self.assertEqual(ExifTag._convert_to_python('2009-03-01T12:46:51Z', xtype),
                         datetime.datetime(2009, 03, 01, 12, 46, 51))
        # Valid values: strings
        self.assertEqual(ExifTag._convert_to_python('Some text.', xtype), u'Some text.')
        self.assertEqual(ExifTag._convert_to_python('Some text with exotic chàräctérʐ.', xtype),
                         u'Some text with exotic chàräctérʐ.')
        # Invalid values: datetimes
        self.assertEqual(ExifTag._convert_to_python('2009-13-01 12:46:51', xtype),
                         u'2009-13-01 12:46:51')
        self.assertEqual(ExifTag._convert_to_python('2009-12-01', xtype),
                         u'2009-12-01')

    def test_convert_to_string_ascii(self):
        xtype = 'Ascii'
        # Valid values: datetimes
        self.assertEqual(ExifTag._convert_to_string(datetime.datetime(2009, 03, 01, 12, 54, 28), xtype),
                         '2009-03-01 12:54:28')
        self.assertEqual(ExifTag._convert_to_string(datetime.date(2009, 03, 01), xtype),
                         '2009-03-01 00:00:00')
        # Valid values: strings
        self.assertEqual(ExifTag._convert_to_string(u'Some text', xtype), 'Some text')
        self.assertEqual(ExifTag._convert_to_string(u'Some text with exotic chàräctérʐ.', xtype),
                         'Some text with exotic chàräctérʐ.')
        self.assertEqual(ExifTag._convert_to_string('Some text with exotic chàräctérʐ.', xtype),
                         'Some text with exotic chàräctérʐ.')
        # Invalid values
        self.failUnlessRaises(ExifValueError, ExifTag._convert_to_string, None, xtype)

    def test_convert_to_python_short(self):
        xtype = 'Short'
        # Valid values
        self.assertEqual(ExifTag._convert_to_python('23', xtype), 23)
        self.assertEqual(ExifTag._convert_to_python('+5628', xtype), 5628)
        # Invalid values
        self.failUnlessRaises(ExifValueError, ExifTag._convert_to_python, 'abc', xtype)
        self.failUnlessRaises(ExifValueError, ExifTag._convert_to_python, '5,64', xtype)
        self.failUnlessRaises(ExifValueError, ExifTag._convert_to_python, '47.0001', xtype)
        self.failUnlessRaises(ExifValueError, ExifTag._convert_to_python, '1E3', xtype)

    def test_convert_to_string_short(self):
        xtype = 'Short'
        # Valid values
        self.assertEqual(ExifTag._convert_to_string(123, xtype), '123')
        # Invalid values
        self.failUnlessRaises(ExifValueError, ExifTag._convert_to_string, -57, xtype)
        self.failUnlessRaises(ExifValueError, ExifTag._convert_to_string, 'invalid', xtype)
        self.failUnlessRaises(ExifValueError, ExifTag._convert_to_string, 3.14, xtype)

    def test_convert_to_python_long(self):
        xtype = 'Long'
        # Valid values
        self.assertEqual(ExifTag._convert_to_python('23', xtype), 23)
        self.assertEqual(ExifTag._convert_to_python('+5628', xtype), 5628)
        # Invalid values
        self.failUnlessRaises(ExifValueError, ExifTag._convert_to_python, 'abc', xtype)
        self.failUnlessRaises(ExifValueError, ExifTag._convert_to_python, '5,64', xtype)
        self.failUnlessRaises(ExifValueError, ExifTag._convert_to_python, '47.0001', xtype)
        self.failUnlessRaises(ExifValueError, ExifTag._convert_to_python, '1E3', xtype)

    def test_convert_to_string_long(self):
        xtype = 'Long'
        # Valid values
        self.assertEqual(ExifTag._convert_to_string(123, xtype), '123')
        self.assertEqual(ExifTag._convert_to_string(678024, xtype), '678024')
        # Invalid values
        self.failUnlessRaises(ExifValueError, ExifTag._convert_to_string, -57, xtype)
        self.failUnlessRaises(ExifValueError, ExifTag._convert_to_string, 'invalid', xtype)
        self.failUnlessRaises(ExifValueError, ExifTag._convert_to_string, 3.14, xtype)

    def test_convert_to_python_slong(self):
        xtype = 'SLong'
        # Valid values
        self.assertEqual(ExifTag._convert_to_python('23', xtype), 23)
        self.assertEqual(ExifTag._convert_to_python('+5628', xtype), 5628)
        self.assertEqual(ExifTag._convert_to_python('-437', xtype), -437)
        # Invalid values
        self.failUnlessRaises(ExifValueError, ExifTag._convert_to_python, 'abc', xtype)
        self.failUnlessRaises(ExifValueError, ExifTag._convert_to_python, '5,64', xtype)
        self.failUnlessRaises(ExifValueError, ExifTag._convert_to_python, '47.0001', xtype)
        self.failUnlessRaises(ExifValueError, ExifTag._convert_to_python, '1E3', xtype)

    def test_convert_to_string_slong(self):
        xtype = 'SLong'
        # Valid values
        self.assertEqual(ExifTag._convert_to_string(123, xtype), '123')
        self.assertEqual(ExifTag._convert_to_string(678024, xtype), '678024')
        self.assertEqual(ExifTag._convert_to_string(-437, xtype), '-437')
        # Invalid values
        self.failUnlessRaises(ExifValueError, ExifTag._convert_to_string, 'invalid', xtype)
        self.failUnlessRaises(ExifValueError, ExifTag._convert_to_string, 3.14, xtype)