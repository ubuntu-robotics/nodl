# Copyright 2020 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify it under the terms of the
# GNU Limited General Public License version 3, as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranties of MERCHANTABILITY, SATISFACTORY QUALITY, or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Limited General Public License for more details.
#
# You should have received a copy of the GNU Limited General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

from typing import Optional

from lxml import etree


class NoDLException(Exception):
    """Base class for all NoDL exceptions."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class InvalidNoDLException(NoDLException):
    """Exception class representing most errors in parsing the NoDL tree."""

    def __init__(self, message: str, element: Optional[etree._Element] = None) -> None:
        if element is not None:
            super().__init__(f'{element.base}:{element.sourceline}  ' + message)
        else:
            super().__init__(message)


class UnsupportedInterfaceException(InvalidNoDLException):
    """Exception thrown when an interface has a future or invalid version."""

    def __init__(self, max_version: int, element: etree._Element) -> None:
        super().__init__(
            f'{element.base}:{element.sourceline}  Unsupported interface version: '
            f'{element.attrib["version"]} (must be <={max_version})'
        )
