// *****************************************************************************
/*
 * Copyright (C) 2006-2010 Olivier Tilloy <olivier@tilloy.net>
 *
 * This file is part of the pyexiv2 distribution.
 *
 * pyexiv2 is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * pyexiv2 is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with pyexiv2; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, 5th Floor, Boston, MA 02110-1301 USA.
 */
/*
  Author: Olivier Tilloy <olivier@tilloy.net>
 */
// *****************************************************************************

#include "exiv2wrapper.hpp"

#include "exiv2/exv_conf.h"
#include "exiv2/version.hpp"

#include <boost/python.hpp>

using namespace boost::python;

using namespace exiv2wrapper;

boost::python::tuple exiv2_version = \
    boost::python::make_tuple(EXIV2_MAJOR_VERSION,
                              EXIV2_MINOR_VERSION,
                              EXIV2_PATCH_VERSION);

BOOST_PYTHON_MODULE(libexiv2python)
{
    scope().attr("exiv2_version_info") = exiv2_version;

    register_exception_translator<Exiv2::Error>(&translateExiv2Error);

    class_<ExifTag>("_ExifTag", init<std::string>())

        .def("_setRawValue", &ExifTag::setRawValue)

        .def("_getKey", &ExifTag::getKey)
        .def("_getType", &ExifTag::getType)
        .def("_getName", &ExifTag::getName)
        .def("_getLabel", &ExifTag::getLabel)
        .def("_getDescription", &ExifTag::getDescription)
        .def("_getSectionName", &ExifTag::getSectionName)
        .def("_getSectionDescription", &ExifTag::getSectionDescription)
        .def("_getRawValue", &ExifTag::getRawValue)
        .def("_getHumanValue", &ExifTag::getHumanValue)
    ;

    class_<IptcTag>("_IptcTag", init<std::string>())

        .def("_setRawValues", &IptcTag::setRawValues)

        .def("_getKey", &IptcTag::getKey)
        .def("_getType", &IptcTag::getType)
        .def("_getName", &IptcTag::getName)
        .def("_getTitle", &IptcTag::getTitle)
        .def("_getDescription", &IptcTag::getDescription)
        .def("_getPhotoshopName", &IptcTag::getPhotoshopName)
        .def("_isRepeatable", &IptcTag::isRepeatable)
        .def("_getRecordName", &IptcTag::getRecordName)
        .def("_getRecordDescription", &IptcTag::getRecordDescription)
        .def("_getRawValues", &IptcTag::getRawValues)
    ;

    class_<XmpTag>("_XmpTag", init<std::string>())

        .def("_setTextValue", &XmpTag::setTextValue)
        .def("_setArrayValue", &XmpTag::setArrayValue)
        .def("_setLangAltValue", &XmpTag::setLangAltValue)

        .def("_getKey", &XmpTag::getKey)
        .def("_getExiv2Type", &XmpTag::getExiv2Type)
        .def("_getType", &XmpTag::getType)
        .def("_getName", &XmpTag::getName)
        .def("_getTitle", &XmpTag::getTitle)
        .def("_getDescription", &XmpTag::getDescription)
        .def("_getTextValue", &XmpTag::getTextValue)
        .def("_getArrayValue", &XmpTag::getArrayValue)
        .def("_getLangAltValue", &XmpTag::getLangAltValue)
    ;

    class_<Preview>("Preview", init<Exiv2::PreviewImage>())

        .def_readonly("mime_type", &Preview::_mimeType)
        .def_readonly("extension", &Preview::_extension)
        .def_readonly("size", &Preview::_size)
        .def_readonly("dimensions", &Preview::_dimensions)
        .def_readonly("data", &Preview::_data)

        .def("write_to_file", &Preview::writeToFile)
    ;

    class_<Image>("_Image", init<std::string>())

        .def("_readMetadata", &Image::readMetadata)
        .def("_writeMetadata", &Image::writeMetadata)

        .def("_getPixelWidth", &Image::pixelWidth)
        .def("_getPixelHeight", &Image::pixelHeight)

        .def("_getMimeType", &Image::mimeType)

        .def("_exifKeys", &Image::exifKeys)
        .def("_getExifTag", &Image::getExifTag)
        .def("_setExifTagValue", &Image::setExifTagValue)
        .def("_deleteExifTag", &Image::deleteExifTag)

        .def("_iptcKeys", &Image::iptcKeys)
        .def("_getIptcTag", &Image::getIptcTag)
        .def("_setIptcTagValues", &Image::setIptcTagValues)
        .def("_deleteIptcTag", &Image::deleteIptcTag)

        .def("_xmpKeys", &Image::xmpKeys)
        .def("_getXmpTag", &Image::getXmpTag)
        .def("_setXmpTagTextValue", &Image::setXmpTagTextValue)
        .def("_setXmpTagArrayValue", &Image::setXmpTagArrayValue)
        .def("_setXmpTagLangAltValue", &Image::setXmpTagLangAltValue)
        .def("_deleteXmpTag", &Image::deleteXmpTag)

        .def("_previews", &Image::previews)

        .def("_copyMetadata", &Image::copyMetadata)
    ;
}

