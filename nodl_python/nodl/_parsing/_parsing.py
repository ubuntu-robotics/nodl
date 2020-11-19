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

from pathlib import Path
from typing import Dict, IO, Iterable, List, Union

from lxml import etree
from nodl._parsing import _v1 as parse_v1
from nodl._parsing._schemas import interface_schema
from nodl.errors import (
    DuplicateNodeError,
    InvalidNoDLDocumentError,
    InvalidXMLError,
    UnsupportedInterfaceError,
)
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
    try:
        element_tree = etree.parse(path)
    except etree.XMLSyntaxError as e:
        raise InvalidXMLError(e)

    return _parse_element_tree(element_tree)


def _parse_multiple(paths: Iterable[Union[str, Path, IO]]) -> List[Node]:
    """Merge nodl files into one large node list.

    :param paths: List of nodl files to parse
    :type paths: Iterable[Union[str, Path, IO]]
    :raises DuplicateNodeError: if node is defined multiple times
    :raises InvalidNoDLDocumentError: if doc does not adhere to schema
    :return: flat list of nodes provided by the documents
    :rtype: List[Node]
    """
    node_lists = [parse(path) for path in paths]
    combined_dict: Dict[str, Node] = {}
    for node_list in node_lists:
        for node in node_list:
            if node.executable in combined_dict:
                raise DuplicateNodeError(node=node)
            combined_dict[node.executable] = node
    return list(combined_dict.values())
