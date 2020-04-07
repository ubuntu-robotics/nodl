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

from pathlib import Path
from typing import IO, List, Union

from lxml import etree
from nodl import errors
from nodl._parsing import _v1 as parse_v1
from nodl._parsing._schemas import interface_schema
from nodl.types import Node


NODL_MAX_SUPPORTED_VERSION = 1


def _parse_interface(interface: etree._Element) -> List[Node]:
    """Parse out all nodes from an interface element."""
    if interface.get('version') == '1':
        return parse_v1.parse(interface)
    else:
        raise errors.UnsupportedInterfaceError(
            interface.get('version'), NODL_MAX_SUPPORTED_VERSION
        )


def _parse_element_tree(element_tree: etree._ElementTree) -> List[Node]:
    """Extract an interface element from an ElementTree if present.

    :param element_tree: parsed xml tree to operate on
    :type element_tree: etree._ElementTree
    :raises errors.InvalidNoDLDocumentError: raised if tree does not adhere to schema
    :return: List of NoDL nodes present in the xml tree.
    :rtype: List[Node]
    """
    try:
        interface_schema().assertValid(element_tree)
    except etree.DocumentInvalid as e:
        raise errors.InvalidNoDLDocumentError(e)
    return _parse_interface(element_tree.getroot())


def parse(path: Union[str, Path, IO]) -> List[Node]:
    """Parse the nodes out of a given NoDL file.

    :param path: location of file, or opened file object
    :type path: Union[str, Path, IO]
    :raises errors.InvalidNoDLDocumentError: raised if tree does not adhere to schema
    :return: List of NoDL nodes present in the file
    :rtype: List[Node]
    """
    if isinstance(path, str):
        path = Path(path)
    if isinstance(path, Path):
        path = str(path.resolve())
    element_tree = etree.parse(path)

    return _parse_element_tree(element_tree)
