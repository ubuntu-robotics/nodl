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

from typing import TYPE_CHECKING

from lxml import etree

if TYPE_CHECKING:  # pragma: no cover
    import rclpy.qos


class NoDLError(Exception):
    """Base class for all NoDL exceptions."""

    pass


class InvalidNoDLError(NoDLError):
    """Exception class representing most errors in parsing the NoDL tree."""

    pass


class InvalidNoDLDocumentError(InvalidNoDLError):
    """"""

    def __init__(self, invalid: etree.DocumentInvalid) -> None:
        self.invalid = invalid
        e = invalid.error_log[0]
        super().__init__(
            f'Error parsing NoDL from {e.filename}, line {e.line}, col {e.column}: {e.message}'
        )


class InvalidElementError(InvalidNoDLError):
    """"""

    def __init__(self, message: str, element: etree._Element) -> None:
        super().__init__(
            f'Error parsing {element.tag} from {element.base}, line {element.sourceline}: '
            + message
        )


class InvalidQoSError(InvalidElementError):
    """Exception class for value out of enum in QoS."""

    pass


class InvalidQosProfileError(InvalidQoSError):
    """"""

    def __init__(
        self, error: 'rclpy.qos.InvalidQoSProfileException', element: etree._Element
    ) -> None:
        super().__init__(str(error), element)


class InvalidQOSAttributeValueError(InvalidQoSError):
    """Exception class for value out of enum in QoS."""

    def __init__(self, attribute: str, element: etree._Element) -> None:
        super().__init__(
            f'Value: {element.get(attribute)} is not valid for attribute {attribute}', element
        )


class InvalidActionError(InvalidElementError):
    """"""

    pass


class AmbiguousActionInterfaceError(InvalidActionError):
    """"""

    def __init__(self, element: etree._Element) -> None:
        super().__init__(
            f'Action <{element.get("name")}> is neither server nor client', element=element
        )


class InvalidParameterError(InvalidElementError):
    """"""

    pass


class InvalidTopicError(InvalidElementError):
    """"""

    pass


class AmbiguousTopicInterfaceError(InvalidTopicError):
    """"""

    def __init__(self, element: etree._Element) -> None:
        super().__init__(
            f'Topic <{element.get("name")}> is neither publisher nor subscription', element=element
        )


class InvalidServiceError(InvalidElementError):
    """"""

    pass


class AmbiguousServiceInterfaceError(InvalidServiceError):
    """"""

    def __init__(self, element: etree._Element) -> None:
        super().__init__(
            f'Service <{element.get("name")}> is neither server nor client', element=element
        )


class UnsupportedInterfaceError(InvalidNoDLError):
    """Exception thrown when an interface has a future or invalid version."""

    def __init__(self, version: int, max_version: int) -> None:
        super().__init__(f'Unsupported interface version: {version} must be <= {max_version}')
