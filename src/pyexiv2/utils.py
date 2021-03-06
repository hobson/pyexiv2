# -*- coding: utf-8 -*-

# ******************************************************************************
#
# Copyright (C) 2006-2012 Olivier Tilloy <olivier@tilloy.net>
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
# Contributors: Hobson Lane <hobson@totalgood.com>
#
# ******************************************************************************

"""
Utility classes and functions.
"""

# Enable true division.
from __future__ import division

import datetime
import re

# pyexiv2 uses fractions.Fraction when available (Python ≥ 2.6), or falls back
# on the custom Rational class. This should be transparent to the application
# developer as both classes have a similar API.
# This module contains convenience functions to ease manipulation of fractions.
try:
    from fractions import Fraction
except ImportError:
    Fraction = None


class FixedOffset(datetime.tzinfo):

    """
    Fixed positive or negative offset from a local time east from UTC.

    :attribute sign: the sign of the offset ('+' or '-')
    :type sign: string
    :attribute hours: the absolute number of hours of the offset
    :type hours: int
    :attribute minutes: the absolute number of minutes of the offset
    :type minutes: int
    """

    def __init__(self, sign='+', hours=0, minutes=0):
        """
        Initialize an offset from a sign ('+' or '-') and an absolute value
        expressed in hours and minutes.
        No check on the validity of those values is performed, it is the
        responsibility of the caller to pass valid values.

        :param sign: the sign of the offset ('+' or '-')
        :type sign: string
        :param hours: an absolute number of hours
        :type hours: int
        :param minutes: an absolute number of minutes
        :type minutes: int
        """
        self.sign = sign
        self.hours = hours
        self.minutes = minutes

    def utcoffset(self, dt):
        """
        Return offset of local time from UTC, in minutes east of UTC.
        If local time is west of UTC, this value will be negative.

        :param dt: the local time
        :type dt: :class:`datetime.time`

        :return: a whole number of minutes in the range -1439 to 1439 inclusive
        :rtype: :class:`datetime.timedelta`
        """
        total = self.hours * 60 + self.minutes
        if self.sign == '-':
            total = -total
        return datetime.timedelta(minutes = total)

    def dst(self, dt):
        """
        Return the daylight saving time (DST) adjustment.
        In this implementation, it is always nil.

        :param dt: the local time
        :type dt: :class:`datetime.time`

        :return: the DST adjustment (always nil)
        :rtype: :class:`datetime.timedelta`
        """
        return datetime.timedelta(0)

    def tzname(self, dt):
        """
        Return a string representation of the offset in the format '±%H:%M'.
        If the offset is nil, the representation is, by convention, 'Z'.

        :param dt: the local time
        :type dt: :class:`datetime.time`

        :return: a human-readable representation of the offset
        :rtype: string
        """
        if self.hours == 0 and self.minutes == 0:
            return 'Z'
        else:
            return '%s%02d:%02d' % (self.sign, self.hours, self.minutes)

    def __eq__(self, other):
        """
        Test equality between this offset and another offset.

        :param other: another offset
        :type other: :class:`FixedOffset`

        :return: True if the offset are equal, False otherwise
        :rtype: boolean
        """
        return (self.sign == other.sign) and (self.hours == other.hours) and \
            (self.minutes == other.minutes)

def latin_to_ascii(s):
    s2=''
    for c in s:
        if ord(c) < 128:
            s2 += c
        else:
            s2 += '\\x'+hex(ord(c))[2:].zfill(2) 
    return s2

# from string.printable
PRINTABLE = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
def escape_unprintable(s):
    s2=''
    for c in s:
        if ord(c) < 128 and c in PRINTABLE:
            s2 += c
        else:
            s2 += '\\x'+hex(ord(c))[2:].zfill(2) 
    return s2

def try_int(s):
    try:
        return int(s)
    except ValueError:
        return False # return 0

def undefined_to_human(undefined):
    """
    Convert an exif.Undefined type string to a human-readable string.
    
    The "Undefined" string of space-delimitted decimal integers is converted to 
    ASCII characters and backslash-escaped hex codes for humans.
    The undefined string must contain space-delimmetted decimal numbers,
    e.g. "48 50 50 49" becomes "0221".
    
    The Undefined type is part of the EXIF specification.
    
    Examples:
    >>> undefined_to_human("48 50 50 49")
    '0221'

    ### These doctests don't work due to the inpolation and indentation of tripple-quoted strings
    ### Should define these tests in an external function called _test
    #>>> maker_note = '70 85 74 73 70 73 76 77 13 10 32 32 32 32 0 0 0 30 0 0 0 7 0'
	#    >>> undefined_to_human(maker_note)
	#    'FUJIFILM\\r\\n    \\x00\\x00\\x00\\x1e\\x00\\x00\\x00\\x07\\x00'
	#    >>> print escape_unprintable(undefined_to_human(latin_to_ascii(maker_note)))
	#    FUJIFILM
	#    \\x00\\x00\\x00\\x1e\\x00\\x00\\x00\\x07\\x00
    
    TODO:
    1. Look for repeats of \x00 and "summarize" or human-encode them with something like
       '\x00(repeated {0} times)'.format(undefined.count('\x00'))
    :param undefined: an exif Undefined string
    :type undefined: string
    :return: decoded (human-readable) python string
    :rtype: string
    """
    if undefined == '':
        return ''
    return escape_unprintable(undefined_to_string(latin_to_ascii(undefined)))

def undefined_to_string(undefined):
    """
    Convert an undefined string into its corresponding sequence of bytes.
    The undefined string must contain the ascii codes of a sequence of bytes,
    separated by white spaces (e.g. "48 50 50 49" will be converted into
    "0221").
    The Undefined type is part of the EXIF specification.

    :param undefined: an undefined string
    :type undefined: string

    :return: the corresponding decoded string
    :rtype: string
    """
    if undefined == '':
        return ''
    return ''.join(map(lambda x: chr(int(x)), undefined.rstrip().split(' ')))

def string_to_undefined(sequence):
    """
    Convert a string into its undefined form.
    The undefined form contains a sequence of ascii codes separated by white
    spaces (e.g. "0221" will be converted into "48 50 50 49").
    The Undefined type is part of the EXIF specification.

    :param sequence: a sequence of bytes
    :type sequence: string

    :return: the corresponding undefined string
    :rtype: string
    """
    return ''.join(map(lambda x: '%d ' % ord(x), sequence)).rstrip()


class Rational(object):

    """
    A class representing a rational number.

    Its numerator and denominator are read-only properties.

    Do not use this class directly to instantiate a rational number.
    Instead, use :func:`make_fraction`.
    """

    _format_re = re.compile(r'(?P<numerator>-?\d+)(?:/(?P<denominator>\d+))?')

    def __init__(self, numerator, denominator):
        """
        :param numerator: the numerator
        :type numerator: long
        :param denominator: the denominator
        :type denominator: long

        :raise ZeroDivisionError: if the denominator equals zero
        """
        if denominator == 0:
            msg = 'Denominator of a rational number cannot be zero.'
            raise ZeroDivisionError(msg)
        self._numerator = long(numerator)
        self._denominator = long(denominator)

    @property
    def numerator(self):
        """The numerator of the rational number."""
        return self._numerator

    @property
    def denominator(self):
        """The denominator of the rational number."""
        return self._denominator

    @staticmethod
    def match_string(string):
        """
        Match a string against the expected format for a :class:`Rational`
        (``[-]numerator/denominator``) and return the numerator and denominator
        as a tuple.

        :param string: a string representation of a rational number
        :type string: string

        :return: a tuple (numerator, denominator)
        :rtype: tuple of long

        :raise ValueError: if the format of the string is invalid
        """
        match = Rational._format_re.match(string)
        if match is None:
            raise ValueError('Invalid format for a rational: %s' % string)
        gd = match.groupdict()
        return (long(gd['numerator']), long(gd['denominator']))

    @staticmethod
    def from_string(string):
        """
        Instantiate a :class:`Rational` from a string formatted as
        ``[-]numerator/denominator``.

        :param string: a string representation of a rational number
        :type string: string

        :return: the rational number parsed
        :rtype: :class:`Rational`

        :raise ValueError: if the format of the string is invalid
        """
        numerator, denominator = Rational.match_string(string)
        return Rational(numerator, denominator)

    def to_float(self):
        """
        :return: a floating point number approximation of the value
        :rtype: float
        """
        return float(self._numerator) / self._denominator

    def __eq__(self, other):
        """
        Compare two rational numbers for equality.

        Two rational numbers are equal if their reduced forms are equal.

        :param other: the rational number to compare to self for equality
        :type other: :class:`Rational`
        
        :return: True if equal, False otherwise
        :rtype: boolean
        """
        return (self._numerator * other._denominator) == \
               (other._numerator * self._denominator)

    def __str__(self):
        """
        :return: a string representation of the rational number
        :rtype: string
        """
        return '%d/%d' % (self._numerator, self._denominator)

    def __repr__(self):
        """
        :return: the official string representation of the object
        :rtype: string
        """
        return '%s(%d, %d)' % (self.__class__.__name__, self._numerator, self._denominator)



def is_fraction(obj):
    """
    Test whether the object is a valid fraction.
    """
    if Fraction is not None and isinstance(obj, Fraction):
        return True
    elif isinstance(obj, Rational):
        return True
    else:
        return False


def make_fraction(*args):
    """
    Make a fraction.

    The type of the returned object depends on the availability of the
    fractions module in the standard library (Python ≥ 2.6).

    :raise TypeError: if the arguments do not match the expected format for a
                      fraction
    """
    if len(args) == 1:
        numerator, denominator = Rational.match_string(args[0])
        if not denominator:
            denominator = 1
        # print numerator,denominator
    elif len(args) == 2:
        numerator = args[0]
        denominator = args[1]
        if not denominator:
            denominator = 1
    else:
        raise TypeError('Invalid format for a fraction: %s' % str(args))
    if denominator == 0 and numerator == 0:
        # Null rationals are often stored as '0/0'.
        # We want to be fault-tolerant in this specific case
        # (see https://bugs.launchpad.net/pyexiv2/+bug/786253).
        denominator = 1
    if Fraction is not None:
        return Fraction(numerator, denominator)
    else:
        return Rational(numerator, denominator)


def fraction_to_string(fraction):
    """
    Return a string representation of a fraction, suitable to pass to libexiv2.

    The returned string is always in the form '[numerator]/[denominator]'.

    :raise TypeError: if the argument is not a valid fraction
    """
    if Fraction is not None and isinstance(fraction, Fraction):
        # fractions.Fraction.__str__ returns '0' for a null numerator.
        return '%s/%s' % (fraction.numerator, fraction.denominator)
    elif isinstance(fraction, Rational):
        return str(fraction)
    else:
        raise TypeError('Not a fraction')


class ListenerInterface(object):

    """
    Interface that an object that wants to listen to changes on another object
    should implement.
    """

    def contents_changed(self):
        """
        React on changes on the object observed.
        Override to implement specific behaviours.
        """
        raise NotImplementedError()


class NotifyingList(list):

    """
    A simplistic implementation of a notifying list.
    Any changes to the list are notified in a synchronous way to all previously
    registered listeners. A listener must implement the
    :class:`ListenerInterface`.
    """

    # Useful documentation:
    # file:///usr/share/doc/python2.5/html/lib/typesseq-mutable.html
    # http://docs.python.org/reference/datamodel.html#additional-methods-for-emulation-of-sequence-types

    def __init__(self, items=[]):
        super(NotifyingList, self).__init__(items)
        self._listeners = set()

    def register_listener(self, listener):
        """
        Register a new listener to be notified of changes.

        :param listener: any object that listens for changes
        :type listener: :class:`ListenerInterface`
        """
        self._listeners.add(listener)

    def unregister_listener(self, listener):
        """
        Unregister a previously registered listener.

        :param listener: a previously registered listener
        :type listener: :class:`ListenerInterface`

        :raise KeyError: if the listener was not previously registered
        """
        self._listeners.remove(listener)

    def _notify_listeners(self, *args):
        for listener in self._listeners:
            listener.contents_changed(*args)

    def __setitem__(self, index, item):
        # FIXME: support slice arguments for extended slicing
        super(NotifyingList, self).__setitem__(index, item)
        self._notify_listeners()

    def __delitem__(self, index):
        # FIXME: support slice arguments for extended slicing
        super(NotifyingList, self).__delitem__(index)
        self._notify_listeners()

    def append(self, item):
        super(NotifyingList, self).append(item)
        self._notify_listeners()

    def extend(self, items):
        super(NotifyingList, self).extend(items)
        self._notify_listeners()

    def insert(self, index, item):
        super(NotifyingList, self).insert(index, item)
        self._notify_listeners()

    def pop(self, index=None):
        if index is None:
            item = super(NotifyingList, self).pop()
        else:
            item = super(NotifyingList, self).pop(index)
        self._notify_listeners()
        return item

    def remove(self, item):
        super(NotifyingList, self).remove(item)
        self._notify_listeners()

    def reverse(self):
        super(NotifyingList, self).reverse()
        self._notify_listeners()

    def sort(self, cmp=None, key=None, reverse=False):
        super(NotifyingList, self).sort(cmp, key, reverse)
        self._notify_listeners()

    def __iadd__(self, other):
        self = super(NotifyingList, self).__iadd__(other)
        self._notify_listeners()
        return self

    def __imul__(self, coefficient):
        self = super(NotifyingList, self).__imul__(coefficient)
        self._notify_listeners()
        return self

    def __setslice__(self, i, j, items):
        # __setslice__ is deprecated but needs to be overridden for completeness
        super(NotifyingList, self).__setslice__(i, j, items)
        self._notify_listeners()

    def __delslice__(self, i, j):
        # __delslice__ is deprecated but needs to be overridden for completeness
        deleted = self[i:j]
        super(NotifyingList, self).__delslice__(i, j)
        if deleted:
            self._notify_listeners()

# TODO:
# The XMP struct type tags (Flash, Dimension, Colorant, etc) need objects
#   to encapsulate them, implementing container methods like get, set, repr(),
#   like datetime or utils.GPSCoordinate.
#   Unlike other data type classes, might be good to also implement dict() and/or
#   iterator interfaces
# These data type objects should be defined in utils, where GPSCoordinate is located
# docs.python.org uses this pattern:
#class C(object):
#    def __init__(self):
#        self._x = None
#    def getx(self):
#        return self._x
#    def setx(self, value):
#        self._x = value
#    def delx(self):
#        del self._x
#    x = property(getx, setx, delx, "I'm the 'x' property.")

class Dimensions(object):
    """
    An XMP Dimensions data type.

    Properties:
    - width: image width ('w' in XMP Spec)
    - height: image height ('h' in XMP Spec)
    - unit: units of measure for the image dimensions
    """
    # would be more robust if order of fields didn't matter
    _format_re = re.compile(
                            r'w\w*:(?P<w>\d+)'
                            r',\s*h\w*:(?P<h>\d+)'
                            r'(?:,\s*unit\w?:(?P<unit>\d+))?',
                            flags=re.IGNORECASE) 
    def __init__(self, width=1, height=1, unit='pixels'):
        """
        :param width: image width
        :type width: int
        :param width: image height
        :type width: int
        :param unit: units of measure for image dimensions
        :type unit: str
        :raise ValueError: if any of the parameter is not in the expected range
                           of values
        """
        self._width = width
        self._height = height
        self._unit = unit

    # Makes Dimensions.width read-only, unless @width.setter decorates setter method
    @property  
    def width(self):
        """The width of the image."""
        # xmp.py and exif.py use the getter/setter, utils.py doesn't
        # return self._getWidth() 
        return self._width
    @property
    def height(self):
        """The height of the image."""
        # return self._getHeight()
        return self._height
    @property
    def unit(self):
        """
        The units used to indicate width and height.
        Examples: inch, mm, pixel, pixels, pica, point
        """
        # return self._getUnit()
        return self._unit
        
    @staticmethod
    def from_string(string):
        """
        Instantiate a :class:`Dimensions` from a string formatted as
        ``w:<int>, h:<int>, unit:<str>`` or ``<int>, <int>, <str>``.
        :param string: a string representation of a XMP Dimensions data type
        :type string: string
        :return: the XMP Dimensions data type parsed
        :rtype: :class:`Dimensions`
        :raise ValueError: if the format of the string is invalid
        """
        match = Dimensions._format_re.match(string)
        if match is None:
            raise ValueError('Invalid format for image Dimensions: %s' % string)
        gd = match.groupdict()
        return Dimensions(int(gd['width']), int(gd['height']), gd['unit'])
        
    def __eq__(self, other):
        """
        Compare two XMP image Dimensions for equality.
        Two Dimensions are equal if all their components are equal.
        :param other: the XMP image Dimensions to compare to self for equality
        :type other: :class:`Dimensions`
        :return: True if equal, False otherwise
        :rtype: boolean
        """
        return (self._width == other._width) and \
               (self._height == other._height) and \
               (self._unit == other._unit) 
    def __str__(self):
        """
        :return: a string representation of the image Dimensions conforming to 
                 the XMP specification
        :rtype: string
        """
        return 'w:%d, h:%d, unit:%s' % (self._width, self._height, self._unit)

class Flash(object):
    """
    An XMP Flash data type.
    Properties:
    - fired: whether flash fired
    - return: whether flash/strobe return is supported or detected (0,2, or 3)
    - mode: flash/strobe mode (unknown, compulsory, flash off, auto)
    - function: whether flash function is present
    - red_eye_mode: whether red-eye reduction is supported
    """
    
    # would be more robust if order of fields didn't matter
    _format_re = re.compile(r'(?P<fired>\d+)',flags=re.IGNORECASE) 
    
    def __init__(self, fired=0, retrn=0, mode=0, function=0, red_eye_mode=0):
        """
        :param fired: whether flash fired
        :type fired: boolean
        :param return: whether flash/strobe return is supported or detected (0,2, or 3)
        :type return: int
        :param mode: flash/strobe mode (unknown, compulsory, flash off, auto)
        :type mode: int
        :param function: whether flash function is present
        :type function: boolean
        :param red_eye_mode: whether red-eye reduction is supported
        :type return: boolean
        :raise ValueError: if any of the parameter is not in the expected range
                           of values
        """
#        #TODO: DRY this by using static method Flash.from_string(fired) here
#        if isinstance(fired,str):
#            self._fired = int(fired)
#        else:
        self._fired = fired
        self._return = retrn
        self._mode = mode
        self._function = function
        self._red_eye_mode = red_eye_mode

    @property  
    def fired(self):
        """Whether the flash fired."""
        # xmp.py and exif.py use the getter/setter, utils.py doesn't
        # return self._getWidth() 
        return self._fired

    @property
    def mode(self):
        """Flash or strobe mode (0=unknown, 1=compulsory, 2=flash off, 3=auto)."""
        # return self._getHeight()
        return self._mode

    @staticmethod
    def from_string(s):
        """
        Instantiate a :class:`Flash` from a string formatted as
        ``<int>``.
        :param string: a string representation of a XMP Flash data type
        :type string: string
        :return: the XMP Flash data type parsed
        :rtype: :class:`Flash`
        :raise ValueError: if the format of the string is invalid
        """
        match = Flash._format_re.match(s)
        if match is None:
            raise ValueError('Invalid format for image Flash: %s' % s)
        gd = match.groupdict()
        print gd
        return Flash( int(gd['fired']) )

    def __eq__(self, other):
        """
        Compare two XMP Flash instances for equality.
        Two Flash are equal if all their components are equal.
        :param other: the XMP Flash instances to compare to self for equality
        :type other: :class:`Flash`
        :return: True if equal, False otherwise
        :rtype: boolean
        """
        return (self._fired == other._fired) and \
               (self._mode == other._mode) 

    def __str__(self):
        """
        :return: a string representation of the Flash instance conforming to 
                 the XMP specification
        :rtype: string
        """
        print 'fired = "'+str(self._fired)+'"'
        return str((self._fired))+str((self._mode))

class Colorant(object):
    """
    An XMP Colorant type.
    """
    pass


class GPSCoordinate(object):

    """
    A class representing GPS coordinates (e.g. a latitude or a longitude).

    Its attributes (degrees, minutes, seconds, direction) are read-only
    properties.
    """

    _format_re = \
        re.compile(r'(?P<degrees>-?\d+),'
                    '(?P<minutes>\d+)(,(?P<seconds>\d+)|\.(?P<fraction>\d+))'
                    '(?P<direction>[NSEW])')

    def __init__(self, degrees, minutes, seconds, direction):
        """
        :param degrees: degrees
        :type degrees: int
        :param minutes: minutes
        :type minutes: int
        :param seconds: seconds
        :type seconds: int
        :param direction: direction ('N', 'S', 'E' or 'W')
        :type direction: string

        :raise ValueError: if any of the parameter is not in the expected range
                           of values
        """
        if direction not in ('N', 'S', 'E', 'W'):
            raise ValueError('Invalid direction: %s' % direction)
        self._direction = direction
        if (direction in ('N', 'S') and (degrees < 0 or degrees > 90)) or \
           (direction in ('E', 'W') and (degrees < 0 or degrees > 180)):
            raise ValueError('Invalid value for degrees: %d' % degrees)
        self._degrees = degrees
        if minutes < 0 or minutes > 60:
            raise ValueError('Invalid value for minutes: %d' % minutes)
        self._minutes = minutes
        if seconds < 0 or seconds > 60:
            raise ValueError('Invalid value for seconds: %d' % seconds)
        self._seconds = seconds

    @property
    def degrees(self):
        """The degrees component of the coordinate."""
        return self._degrees

    @property
    def minutes(self):
        """The minutes component of the coordinate."""
        return self._minutes

    @property
    def seconds(self):
        """The seconds component of the coordinate."""
        return self._seconds

    @property
    def direction(self):
        """The direction component of the coordinate."""
        return self._direction

    @staticmethod
    def from_string(string):
        """
        Instantiate a :class:`GPSCoordinate` from a string formatted as
        ``DDD,MM,SSk`` or ``DDD,MM.mmk`` where ``DDD`` is a number of degrees,
        ``MM`` is a number of minutes, ``SS`` is a number of seconds, ``mm`` is
        a fraction of minutes, and ``k`` is a single character N, S, E, W
        indicating a direction (north, south, east, west).

        :param string: a string representation of a GPS coordinate
        :type string: string

        :return: the GPS coordinate parsed
        :rtype: :class:`GPSCoordinate`

        :raise ValueError: if the format of the string is invalid
        """
        match = GPSCoordinate._format_re.match(string)
        if match is None:
            raise ValueError('Invalid format for a GPS coordinate: %s' % string)
        gd = match.groupdict()
        fraction = gd['fraction']
        if fraction is not None:
            seconds = int(round(int(fraction[:2]) * 0.6))
        else:
            seconds = int(gd['seconds'])
        return GPSCoordinate(int(gd['degrees']), int(gd['minutes']), seconds,
                             gd['direction'])

    def __eq__(self, other):
        """
        Compare two GPS coordinates for equality.

        Two coordinates are equal if and only if all their components are equal.

        :param other: the GPS coordinate to compare to self for equality
        :type other: :class:`GPSCoordinate`

        :return: True if equal, False otherwise
        :rtype: boolean
        """
        return (self._degrees == other._degrees) and \
               (self._minutes == other._minutes) and \
               (self._seconds == other._seconds) and \
               (self._direction == other._direction)

    def __str__(self):
        """
        :return: a string representation of the GPS coordinate conforming to the
                 XMP specification
        :rtype: string
        """
        return '%d,%d,%d%s' % (self._degrees, self._minutes, self._seconds,
                               self._direction)

class DateTimeFormatter(object):

    """
    Convenience object that exposes static methods to convert a date, time or
    datetime object to a string representation suitable for various metadata
    standards.

    This is needed because python’s
    `strftime() <http://docs.python.org/library/datetime.html#strftime-strptime-behavior>`_
    doesn’t work for years before 1900.

    This class mostly exists for internal usage only. Clients should never need
    to use it.
    """

    @staticmethod
    def timedelta_to_offset(t):
        """
        Convert a time delta to a string representation in the form ``±%H:%M``.

        :param t: a time delta
        :type t: :class:`datetime.timedelta`

        :return: a string representation of the time delta in the form
                 ``±%H:%M``
        :rtype: string
        """
        # timedelta.total_seconds() is only available starting with Python 2.7
        # (http://docs.python.org/library/datetime.html#datetime.timedelta.total_seconds)
        #seconds = t.total_seconds()
        seconds = (t.microseconds + (t.seconds + t.days * 24 * 3600) * 10**6) / 10**6
        hours = int(seconds / 3600)
        minutes = abs(int((seconds - hours * 3600) / 60))
        return '%+03d:%02d' % (hours, minutes)

    @staticmethod
    def exif(d):
        """
        Convert a date/time object to a string representation conforming to
        libexiv2’s internal representation for the EXIF standard.

        :param d: a datetime or date object
        :type d: :class:`datetime.datetime` or :class:`datetime.date`

        :return: a string representation conforming to the EXIF standard
        :rtype: string

        :raise TypeError: if the parameter is not a datetime or a date object
        """
        if isinstance(d, datetime.datetime):
            return '%04d:%02d:%02d %02d:%02d:%02d' % \
                (d.year, d.month, d.day, d.hour, d.minute, d.second)
        elif isinstance(d, datetime.date):
            return '%04d:%02d:%02d' % (d.year, d.month, d.day)
        else:
            raise TypeError('expecting an object of type '
                            'datetime.datetime or datetime.date')

    @staticmethod
    def iptc_date(d):
        """
        Convert a date object to a string representation conforming to
        libexiv2’s internal representation for the IPTC standard.

        :param d: a datetime or date object
        :type d: :class:`datetime.datetime` or :class:`datetime.date`

        :return: a string representation conforming to the IPTC standard
        :rtype: string

        :raise TypeError: if the parameter is not a datetime or a date object
        """
        if isinstance(d, (datetime.date, datetime.datetime)):
            # ISO 8601 date format.
            # According to the IPTC specification, the format for a string
            # field representing a date is '%Y%m%d'. However, the string
            # expected by exiv2's DateValue::read(string) should be
            # formatted using pattern '%Y-%m-%d'.
            return '%04d-%02d-%02d' % (d.year, d.month, d.day)
        else:
            raise TypeError('expecting an object of type '
                            'datetime.datetime or datetime.date')

    @staticmethod
    def iptc_time(d):
        """
        Convert a time object to a string representation conforming to
        libexiv2’s internal representation for the IPTC standard.

        :param d: a datetime or time object
        :type d: :class:`datetime.datetime` or :class:`datetime.time`

        :return: a string representation conforming to the IPTC standard
        :rtype: string

        :raise TypeError: if the parameter is not a datetime or a time object
        """
        if isinstance(d, (datetime.time, datetime.datetime)):
            # According to the IPTC specification, the format for a string
            # field representing a time is '%H%M%S±%H%M'. However, the
            # string expected by exiv2's TimeValue::read(string) should be
            # formatted using pattern '%H:%M:%S±%H:%M'.
            r = '%02d:%02d:%02d' % (d.hour, d.minute, d.second)
            if d.tzinfo is not None:
                t = d.utcoffset()
                if t is not None:
                    r += DateTimeFormatter.timedelta_to_offset(t)
            else:
                r += '+00:00'
            return r
        else:
            raise TypeError('expecting an object of type '
                            'datetime.datetime or datetime.time')

    @staticmethod
    def xmp(d):
        """
        Convert a date/time object to a string representation conforming to
        libexiv2’s internal representation for the XMP standard.

        :param d: a datetime or date object
        :type d: :class:`datetime.datetime` or :class:`datetime.date`

        :return: a string representation conforming to the XMP standard
        :rtype: string

        :raise TypeError: if the parameter is not a datetime or a date object
        """
        if isinstance(d, datetime.datetime):
            t = d.utcoffset()
            if d.tzinfo is None or t is None or t == datetime.timedelta(0):
                tz = 'Z'
            else:
                tz = DateTimeFormatter.timedelta_to_offset(t)
            if d.hour == 0 and d.minute == 0 and \
                d.second == 0 and d.microsecond == 0 and \
                (d.tzinfo is None or d.utcoffset() == datetime.timedelta(0)):
                return '%04d-%02d-%02d' % (d.year, d.month, d.day)
            elif d.second == 0 and d.microsecond == 0:
                return '%04d-%02d-%02dT%02d:%02d%s' % \
                    (d.year, d.month, d.day, d.hour, d.minute, tz)
            elif d.microsecond == 0:
                return '%04d-%02d-%02dT%02d:%02d:%02d%s' % \
                    (d.year, d.month, d.day, d.hour, d.minute, d.second, tz)
            else:
                r = '%04d-%02d-%02dT%02d:%02d:%02d.' % \
                    (d.year, d.month, d.day, d.hour, d.minute, d.second)
                r += str(int(d.microsecond) / 1E6)[2:]
                r += tz
                return r
        elif isinstance(d, datetime.date):
            return '%04d-%02d-%02d' % (d.year, d.month, d.day)
        else:
            raise TypeError('expecting an object of type '
                            'datetime.datetime or datetime.date')

def _test():
    import doctest
    doctest.testmod()
    
if __name__ == "__main__":
    _test()


