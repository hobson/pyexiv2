#!/usr/bin/python
# -*- coding: utf-8 -*-

# ******************************************************************************
#
# Copyright (C) 2008-2009 Olivier Tilloy <olivier@tilloy.net>
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

# Test cases to run
#from ReadMetadataTestCase import ReadMetadataTestCase
#from Bug146313_TestCase import Bug146313_TestCase
#from Bug173387_TestCase import Bug173387_TestCase
#from Bug175070_TestCase import Bug175070_TestCase
#from Bug183332_TestCase import Bug183332_TestCase
#from Bug183618_TestCase import Bug183618_TestCase
from rational import TestRational
from notifying_list import TestNotifyingList
from exif import TestExifTag
from iptc import TestIptcTag
from xmp import TestXmpTag
from metadata import TestImageMetadata


if __name__ == '__main__':
    # Instantiate a test suite containing all the test cases
    suite = unittest.TestSuite()
    #suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ReadMetadataTestCase))
    #suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Bug146313_TestCase))
    #suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Bug173387_TestCase))
    #suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Bug175070_TestCase))
    #suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Bug183332_TestCase))
    #suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Bug183618_TestCase))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestRational))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestNotifyingList))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestExifTag))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestIptcTag))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestXmpTag))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestImageMetadata))
    # Run the test suite
    unittest.TextTestRunner(verbosity=2).run(suite)