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

from collections import defaultdict
from pathlib import Path
from typing import Dict, IO, List, Sequence, Union

from lxml import etree
from nodl._parsing import _v1 as parse_v1
from nodl._parsing._schemas import interface_schema
from nodl.errors import DuplicateNodeError, InvalidNoDLDocumentError, UnsupportedInterfaceError
from nodl.types import Node


NODL_MAX_SUPPORTED_VERSION = 1


def _parse_interface(interface: etree._Element) -> List[Node]:
    """Parse out all nodes from an interface element."""
    if interface.get('version') == '1':
        return parse_v1.parse(interface)
    else:
        raise UnsupportedInterfaceError(interface.get('version'), NODL_MAX_SUPPORTED_VERSION)


def _parse_element_tree(element_tree: etree._ElementTree) -> List[Node]:
    """Extract an interface element from an ElementTree if present.

    :param element_tree: parsed xml tree to operate on
    :type element_tree: etree._ElementTree
    :raises InvalidNoDLDocumentError: if tree does not adhere to schema
    :return: List of NoDL nodes present in the xml tree.
    :rtype: List[Node]
    """
    try:
        interface_schema().assertValid(element_tree)
    except etree.DocumentInvalid as e:
        raise InvalidNoDLDocumentError(e)
    return _parse_interface(element_tree.getroot())


def parse(path: Union[str, Path, IO]) -> List[Node]:
    """Parse the nodes out of a given NoDL file.

    :param path: location of file, or opened file object
    :type path: Union[str, Path, IO]
    :raises InvalidNoDLDocumentError: raised if tree does not adhere to schema
    :return: List of NoDL nodes present in the file
    :rtype: List[Node]
    """
    if isinstance(path, str):
        path = Path(path)
    if isinstance(path, Path):
        path = str(path.resolve())
    element_tree = etree.parse(path)

    return _parse_element_tree(element_tree)


def parse_multiple(paths: Sequence[Union[str, Path, IO]]) -> List[Node]:
    """Merge nodl files into one large node list.

    :param paths: List of nodl files to parse
    :type paths: Sequence[Union[str, Path, IO]]
    :raises DuplicateNodeError: if node is defined multiple times
    :raises InvalidNoDLDocumentError: if doc does not adhere to schema
    :return: flat list of nodes provided by the documents
    :rtype: List[Node]
    """
    node_lists = [parse(path) for path in paths]
    combined = []
    combined_dict: Dict[str, List] = defaultdict(list)
    for node_list in node_lists:
        for node in node_list:
            if node.name in combined_dict:
                if node.executable in combined_dict[node.name]:
                    raise DuplicateNodeError(node=node)
            combined_dict[node.name].append(node.executable)
            combined.append(node)
    return combined
