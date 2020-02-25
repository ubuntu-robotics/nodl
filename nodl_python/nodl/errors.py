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


class NoDLError(Exception):
    """Base class for all NoDL exceptions."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class InvalidNoDLError(NoDLError):
    """Exception class representing most errors in parsing the NoDL tree."""

    def __init__(self, message: str, invalid: Optional[etree.DocumentInvalid] = None) -> None:
        self.invalid = invalid
        if invalid is not None:
            e = invalid.error_log[0]
            super().__init__(
                f'Error parsing NoDL from {e.filename}, line {e.line}, col {e.column}: {message}'
            )
        else:
            super().__init__(message)


class InvalidQoSError(InvalidNoDLError):
    """Exception class for value out of enum in QoS."""

    def __init__(self, message: str, element: etree._Element) -> None:
        super().__init__(
            f'Error parsing NoDL from {element.base}, line {element.sourceline}: {message}'
        )


class InvalidQOSAttributeValueError(InvalidQoSError):
    """Exception class for value out of enum in QoS."""

    def __init__(self, attribute: str, element: etree._Element) -> None:
        super().__init__(
            f'Value: {element.get(attribute)} is not valid for attribute {attribute}', element
        )


class InvalidActionError(InvalidNoDLError):
    """"""

    def __init__(self, message: str, element: etree._Element) -> None:
        super().__init__(
            f'Error parsing action from {element.base}, line {element.sourceline}: {message}'
        )


class AmbiguousActionInterfaceError(InvalidActionError):
    """"""

    def __init__(self, element: etree._Element) -> None:
        super().__init__(
            f'Action <{element.get("name")}> is neither server nor client', element=element
        )


class InvalidParameterError(InvalidNoDLError):
    """"""

    def __init__(self, message: str, element: etree._Element) -> None:
        super().__init__(
            f'Error parsing parameter from {element.base}, line {element.sourceline}: {message}'
        )


class InvalidTopicError(InvalidNoDLError):
    """"""

    def __init__(self, message: str, element: etree._Element) -> None:
        super().__init__(
            f'Error parsing topic from {element.base}, line {element.sourceline}: {message}'
        )


class AmbiguousTopicInterfaceError(InvalidTopicError):
    """"""

    def __init__(self, element: etree._Element) -> None:
        super().__init__(
            f'Topic <{element.get("name")}> is neither publisher nor subscription', element=element
        )


class InvalidServiceError(InvalidNoDLError):
    """"""

    def __init__(self, message: str, element: etree._Element) -> None:
        super().__init__(
            f'Error parsing service from {element.base}, line {element.sourceline}: {message}'
        )


class AmbiguousServiceInterfaceError(InvalidServiceError):
    """"""

    def __init__(self, element: etree._Element) -> None:
        super().__init__(
            f'Service <{element.get("name")}> is neither server nor client', element=element
        )


class UnsupportedInterfaceError(InvalidNoDLError):
    """Exception thrown when an interface has a future or invalid version."""

    def __init__(self, version: int, max_version: int) -> None:
        super().__init__('Unsupported interface version: {version} must be <= {max_version}')
