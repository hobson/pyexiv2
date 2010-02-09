#!/usr/bin/python
# -*- coding: utf-8 -*-

# ******************************************************************************
#
# Copyright (C) 2008-2010 Olivier Tilloy <olivier@tilloy.net>
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
#
# File:      ReadMetadataTestCase.py
# Author(s): Olivier Tilloy <olivier@tilloy.net>
#
# ******************************************************************************

import unittest
import testutils
import os.path
import pyexiv2
import datetime

class ReadMetadataTestCase(unittest.TestCase):

    """
    Test case on reading the metadata contained in a file.
    """

    def checkEXIFTypeAndValue(self, tag, etype, evalue):
        """
        Check the type and the value of an EXIF tag against expected values.

        Keyword arguments:
        tag -- the full name of the tag (eg. 'Exif.Image.DateTime')
        etype -- the expected type of the tag value
        evalue -- the expected value of the tag
        """
        self.assertEqual(type(tag.value), etype)
        self.assertEqual(tag.value, evalue)

    def checkIPTCTypeAndValue(self, tag, etype, evalue):
        """
        Check the type and the value of an IPTC tag against expected values.

        Keyword arguments:
        tag -- the full name of the tag (eg. 'Exif.Image.DateTime')
        etype -- the expected type of the tag value
        evalue -- the expected value of the tag
        """
        if issubclass(etype, tuple):
            self.assertEqual(list(tag.values), list(evalue))
        else:
            self.assertEqual(type(tag.values[0]), etype)
            self.assertEqual(tag.values[0], evalue)

    def assertCorrectFile(self, filename, md5sum):
        """
        Ensure that the filename and the MD5 checksum match up.
        """
        self.assert_(testutils.CheckFileSum(filename, md5sum))

    def testReadMetadata(self):
        """
        Perform various tests on reading the metadata contained in a file.
        """
        # Check that the reference file is not corrupted
        filename = os.path.join('data', 'smiley1.jpg')
        md5sum = 'c066958457c685853293058f9bf129c1'
        self.assertCorrectFile(filename, md5sum)

        # Read the image metadata
        image = pyexiv2.ImageMetadata(filename)
        image.read()

        # Exhaustive tests on the values of EXIF metadata
        exifTags = [('Exif.Image.ImageDescription', str, 'Well it is a smiley that happens to be green'),
                    ('Exif.Image.XResolution', pyexiv2.Rational, pyexiv2.Rational(72, 1)),
                    ('Exif.Image.YResolution', pyexiv2.Rational, pyexiv2.Rational(72, 1)),
                    ('Exif.Image.ResolutionUnit', int, 2),
                    ('Exif.Image.Software', str, 'ImageReady'),
                    ('Exif.Image.DateTime', datetime.datetime, datetime.datetime(2004, 7, 13, 21, 23, 44)),
                    ('Exif.Image.Artist', str, 'No one'),
                    ('Exif.Image.Copyright', str, ''),
                    ('Exif.Image.ExifTag', long, 226L),
                    ('Exif.Photo.Flash', int, 80),
                    ('Exif.Photo.PixelXDimension', long, 167L),
                    ('Exif.Photo.PixelYDimension', long, 140L)]
        self.assertEqual(image.exif_keys, [tag[0] for tag in exifTags])
        for key, ktype, value in exifTags:
            self.checkEXIFTypeAndValue(image[key], ktype, value)

        # Exhaustive tests on the values of IPTC metadata
        iptcTags = [('Iptc.Application2.Caption', str, 'yelimS green faced dude (iptc caption)'),
                    ('Iptc.Application2.Writer', str, 'Nobody'),
                    ('Iptc.Application2.Byline', str, 'Its me'),
                    ('Iptc.Application2.ObjectName', str, 'GreeenDude'),
                    ('Iptc.Application2.DateCreated', datetime.date, datetime.date(2004, 7, 13)),
                    ('Iptc.Application2.City', str, 'Seattle'),
                    ('Iptc.Application2.ProvinceState', str, 'WA'),
                    ('Iptc.Application2.CountryName', str, 'USA'),
                    ('Iptc.Application2.Category', str, 'Things'),
                    ('Iptc.Application2.Keywords', tuple, ('Green', 'Smiley', 'Dude')),
                    ('Iptc.Application2.Copyright', str, '\xa9 2004 Nobody')]
        self.assertEqual(image.iptc_keys, [tag[0] for tag in iptcTags])
        for key, ktype, value in iptcTags:
            self.checkIPTCTypeAndValue(image[key], ktype, value)

    def testReadMetadataXMP(self):
        filename = os.path.join('data', 'exiv2-bug540.jpg')
        md5sum = '64d4b7eab1e78f1f6bfb3c966e99eef2'
        self.assertCorrectFile(filename, md5sum)

        # Read the image metadata
        image = pyexiv2.ImageMetadata(filename)
        image.read()

        xmpTags = [('Xmp.dc.creator', 'seq ProperName', [u'Ian Britton']),
                   ('Xmp.dc.description', 'Lang Alt', {u'x-default': u'Communications'}),
                   ('Xmp.dc.rights', 'Lang Alt', {u'x-default': u'ian Britton - FreeFoto.com'}),
                   ('Xmp.dc.source', 'Text', u'FreeFoto.com'),
                   ('Xmp.dc.subject', 'bag Text', [u'Communications']),
                   ('Xmp.dc.title', 'Lang Alt', {u'x-default': u'Communications'}),
                   ('Xmp.exif.ApertureValue',
                    'Rational',
                    pyexiv2.utils.Rational(8, 1)),
                   ('Xmp.exif.BrightnessValue',
                    'Rational',
                    pyexiv2.utils.Rational(333, 1280)),
                   ('Xmp.exif.ColorSpace', 'Closed Choice of Integer', 1),
                   ('Xmp.exif.DateTimeOriginal',
                    'Date',
                    datetime.datetime(2002, 7, 13, 15, 58, 28, tzinfo=pyexiv2.utils.FixedOffset())),
                   ('Xmp.exif.ExifVersion', 'Closed Choice of Text', u'0200'),
                   ('Xmp.exif.ExposureBiasValue',
                    'Rational',
                    pyexiv2.utils.Rational(-13, 20)),
                   ('Xmp.exif.ExposureProgram', 'Closed Choice of Integer', 4),
                   ('Xmp.exif.FNumber',
                    'Rational',
                    pyexiv2.utils.Rational(3, 5)),
                   ('Xmp.exif.FileSource', 'Closed Choice of Integer', 0),
                   ('Xmp.exif.FlashpixVersion', 'Closed Choice of Text', u'0100'),
                   ('Xmp.exif.FocalLength',
                    'Rational',
                    pyexiv2.utils.Rational(0, 1)),
                   ('Xmp.exif.FocalPlaneResolutionUnit', 'Closed Choice of Integer', 2),
                   ('Xmp.exif.FocalPlaneXResolution',
                    'Rational',
                    pyexiv2.utils.Rational(3085, 256)),
                   ('Xmp.exif.FocalPlaneYResolution',
                    'Rational',
                    pyexiv2.utils.Rational(3085, 256)),
                   ('Xmp.exif.GPSLatitude',
                    'GPSCoordinate',
                    pyexiv2.utils.GPSCoordinate.from_string('54,59.380000N')),
                   ('Xmp.exif.GPSLongitude',
                    'GPSCoordinate',
                    pyexiv2.utils.GPSCoordinate.from_string('1,54.850000W')),
                   ('Xmp.exif.GPSMapDatum', 'Text', u'WGS84'),
                   ('Xmp.exif.GPSTimeStamp',
                    'Date',
                    datetime.datetime(2002, 7, 13, 14, 58, 24, tzinfo=pyexiv2.utils.FixedOffset())),
                   ('Xmp.exif.GPSVersionID', 'Text', u'2.0.0.0'),
                   ('Xmp.exif.ISOSpeedRatings', 'seq Integer', [0]),
                   ('Xmp.exif.MeteringMode', 'Closed Choice of Integer', 5),
                   ('Xmp.exif.PixelXDimension', 'Integer', 2400),
                   ('Xmp.exif.PixelYDimension', 'Integer', 1600),
                   ('Xmp.exif.SceneType', 'Closed Choice of Integer', 0),
                   ('Xmp.exif.SensingMethod', 'Closed Choice of Integer', 2),
                   ('Xmp.exif.ShutterSpeedValue',
                    'Rational',
                    pyexiv2.utils.Rational(30827, 3245)),
                   ('Xmp.pdf.Keywords', 'Text', u'Communications'),
                   ('Xmp.photoshop.AuthorsPosition', 'Text', u'Photographer'),
                   ('Xmp.photoshop.CaptionWriter', 'ProperName', u'Ian Britton'),
                   ('Xmp.photoshop.Category', 'Text', u'BUS'),
                   ('Xmp.photoshop.City', 'Text', u' '),
                   ('Xmp.photoshop.Country', 'Text', u'Ubited Kingdom'),
                   ('Xmp.photoshop.Credit', 'Text', u'Ian Britton'),
                   ('Xmp.photoshop.DateCreated', 'Date', datetime.date(2002, 6, 20)),
                   ('Xmp.photoshop.Headline', 'Text', u'Communications'),
                   ('Xmp.photoshop.State', 'Text', u' '),
                   ('Xmp.photoshop.SupplementalCategories', 'bag Text', [u'Communications']),
                   ('Xmp.photoshop.Urgency', 'Integer', 5),
                   ('Xmp.tiff.Artist', 'ProperName', u'Ian Britton'),
                   ('Xmp.tiff.BitsPerSample', 'seq Integer', [8]),
                   ('Xmp.tiff.Compression', 'Closed Choice of Integer', 6),
                   ('Xmp.tiff.Copyright',
                    'Lang Alt',
                    {u'x-default': u'ian Britton - FreeFoto.com'}),
                   ('Xmp.tiff.ImageDescription', 'Lang Alt', {u'x-default': u'Communications'}),
                   ('Xmp.tiff.ImageLength', 'Integer', 400),
                   ('Xmp.tiff.ImageWidth', 'Integer', 600),
                   ('Xmp.tiff.Make', 'ProperName', u'FUJIFILM'),
                   ('Xmp.tiff.Model', 'ProperName', u'FinePixS1Pro'),
                   ('Xmp.tiff.Orientation', 'Closed Choice of Integer', 1),
                   ('Xmp.tiff.ResolutionUnit', 'Closed Choice of Integer', 2),
                   ('Xmp.tiff.Software', 'AgentName', u'Adobe Photoshop 7.0'),
                   ('Xmp.tiff.XResolution',
                    'Rational',
                    pyexiv2.utils.Rational(300, 1)),
                   ('Xmp.tiff.YCbCrPositioning', 'Closed Choice of Integer', 2),
                   ('Xmp.tiff.YResolution',
                    'Rational',
                    pyexiv2.utils.Rational(300, 1)),
                   ('Xmp.xmp.CreateDate',
                    'Date',
                    datetime.datetime(2002, 7, 13, 15, 58, 28, tzinfo=pyexiv2.utils.FixedOffset())),
                   ('Xmp.xmp.ModifyDate',
                    'Date',
                    datetime.datetime(2002, 7, 19, 13, 28, 10, tzinfo=pyexiv2.utils.FixedOffset())),
                   ('Xmp.xmpBJ.JobRef', 'bag Job', []),
                   ('Xmp.xmpBJ.JobRef[1]', '', ''),
                   ('Xmp.xmpBJ.JobRef[1]/stJob:name', '', 'Photographer'),
                   ('Xmp.xmpMM.DocumentID',
                    'URI',
                    'adobe:docid:photoshop:84d4dba8-9b11-11d6-895d-c4d063a70fb0'),
                   ('Xmp.xmpRights.Marked', 'Boolean', True),
                   ('Xmp.xmpRights.WebStatement', 'URL', 'www.freefoto.com')]
        for key, xtype, value in xmpTags:
            tag = image[key]
            self.assertEqual(tag.type, xtype)
            self.assertEqual(tag.value, value)
