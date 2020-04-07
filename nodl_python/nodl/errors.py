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


class InvalidNoDLError(NoDLError):
    """Exception class representing most errors in parsing the NoDL tree."""


class InvalidNoDLDocumentError(InvalidNoDLError):
    """Error raised when schema validation fails."""

    def __init__(self, invalid: etree.DocumentInvalid) -> None:
        self.invalid = invalid
        e = invalid.error_log[0]
        super().__init__(
            f'Error parsing NoDL from {e.filename}, line {e.line}, col {e.column}: {e.message}'
        )


class InvalidElementError(InvalidNoDLError):
    """Base class for all bad NoDL elements."""

    def __init__(self, message: str, element: etree._Element) -> None:
        super().__init__(
            f'Error parsing {element.tag} from {element.base}, line {element.sourceline}: '
            + message
        )
        self.element = element


class InvalidQoSError(InvalidElementError):
    """Base class for all errors in parsing a QoS element."""


class InvalidQosProfileError(InvalidQoSError):
    """Error raised when rclpy does not accept QoSProfile constructor arguments."""

    def __init__(
        self, error: 'rclpy.qos.InvalidQoSProfileException', element: etree._Element
    ) -> None:
        super().__init__(str(error), element)


class InvalidQOSAttributeValueError(InvalidQoSError):
    """Error raised for values out of enum in QoS."""

    def __init__(self, attribute: str, element: etree._Element) -> None:
        super().__init__(
            f'Value: {element.get(attribute)} is not valid for attribute {attribute}', element
        )
        self.attribute = attribute


class InvalidActionError(InvalidElementError):
    """Base class for all errors in parsing an action."""


class AmbiguousActionInterfaceError(InvalidActionError):
    """Error raised when an action has no interface exposed."""

    def __init__(self, element: etree._Element) -> None:
        super().__init__(
            f'Action <{element.get("name")}> is neither server nor client', element=element
        )


class InvalidParameterError(InvalidElementError):
    """Base class for all errors in parsing a parameter."""


class InvalidTopicError(InvalidElementError):
    """Base class for all errors in parsing a topic."""


class AmbiguousTopicInterfaceError(InvalidTopicError):
    """Error raised when a topic has no interface exposed."""

    def __init__(self, element: etree._Element) -> None:
        super().__init__(
            f'Topic <{element.get("name")}> is neither publisher nor subscription', element=element
        )


class InvalidServiceError(InvalidElementError):
    """Base class for all errors in parsing a service."""


class AmbiguousServiceInterfaceError(InvalidServiceError):
    """Error raised when a topic has no interface exposed."""

    def __init__(self, element: etree._Element) -> None:
        super().__init__(
            f'Service <{element.get("name")}> is neither server nor client', element=element
        )


class UnsupportedInterfaceError(InvalidNoDLError):
    """Error raised when an interface has a future or invalid version."""

    def __init__(self, version: int, max_version: int) -> None:
        super().__init__(f'Unsupported interface version: {version} must be <= {max_version}')
