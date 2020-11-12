# Copyright 2020 Canonical, Ltd.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from lxml import etree

from .types import Node


class NoDLError(Exception):
    """Base class for all NoDL exceptions."""


class NoNoDLFilesError(NoDLError):
    """Exception raised when a package has no NoDL files in the ament index."""

    def __init__(self, package_name: str):
        super().__init__(f'{package_name} has no NoDL files in its ament index.')


class DuplicateNodeError(NoDLError):
    """Exception raised when a node is redefined."""

    def __init__(self, node: 'Node'):
        super().__init__(f'Error: Multiple definitions of {node.name} found in {node.executable}!')


class ExecutableNotFoundError(NoDLError):
    """Exception raised when a package is queried for an executable with no NoDL entry attached."""

    def __init__(self, package_name: str, executable_name: str):
        super().__init__(
            f'{package_name} has no matching nodl entries for executable "{executable_name}"'
        )


class InvalidNoDLError(NoDLError):
    """Exception class representing most errors in parsing the NoDL tree."""


class InvalidXMLError(InvalidNoDLError):
    """Error raised when unable to parse XML."""

    def __init__(self, err: etree.XMLSyntaxError):
        super().__init__(f'XML syntax error: {err.filename}: {err.msg}')


class InvalidNoDLDocumentError(InvalidNoDLError):
    """Error raised when schema validation fails."""

    def __init__(self, invalid: etree.DocumentInvalid):
        self.invalid = invalid
        e = invalid.error_log[0]
        super().__init__(
            f'Error parsing NoDL from {e.filename}, line {e.line}, col {e.column}: {e.message}'
        )


class InvalidElementError(InvalidNoDLError):
    """Base class for all bad NoDL elements."""

    def __init__(self, message: str, element: etree._Element):
        super().__init__(
            f'Error parsing {element.tag} from {element.base}, line {element.sourceline}: '
            + message
        )
        self.element = element


class InvalidActionError(InvalidElementError):
    """Base class for all errors in parsing an action."""


class InvalidParameterError(InvalidElementError):
    """Base class for all errors in parsing a parameter."""


class InvalidTopicError(InvalidElementError):
    """Base class for all errors in parsing a topic."""


class InvalidServiceError(InvalidElementError):
    """Base class for all errors in parsing a service."""


class InvalidNodeChildError(InvalidElementError):
    """Error raised when a node has a child with an unsupported tag."""

    def __init__(self, element: etree._Element) -> None:
        super().__init__(
            (
                f'Nodes cannot contain {element.tag},'
                'must be one of (Action, Parameter, Service, Topic)'
            ),
            element,
        )


class UnsupportedInterfaceError(InvalidNoDLError):
    """Error raised when an interface has a future or invalid version."""

    def __init__(self, version: int, max_version: int) -> None:
        super().__init__(f'Unsupported interface version: {version} must be <= {max_version}')
