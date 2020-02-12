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
from typing import List

from lxml import etree
from nodl._parsing import _v1 as parse_v1
from nodl.exception import InvalidNoDLException, UnsupportedInterfaceException
from nodl.types import Node


NODL_MAX_SUPPORTED_VERSION = 1


def parse_interface(interface: etree._Element) -> List[Node]:
    """Parse out all nodes from an interface element."""
    try:
        version = interface.attrib['version']
    except KeyError:
        raise InvalidNoDLException(f'Missing version attribute in "interface".', interface)

    if version == '1':
        return parse_v1.parse_nodes(interface)
    else:
        raise UnsupportedInterfaceException(NODL_MAX_SUPPORTED_VERSION, interface)


def parse_element_tree(element_tree: etree._ElementTree) -> List[Node]:
    """Extract an interface element from an ElementTree if present."""
    interface = element_tree.getroot()
    if interface.tag != 'interface':
        interface = next(interface.iter('interface'), None)
        if interface is None:
            raise InvalidNoDLException(f'No interface tag in {element_tree.docinfo.URL}')
    return parse_interface(interface)


def parse_nodl_file(path: Path) -> List[Node]:
    """Parse the nodes out of a given NoDL file."""
    full_path = path.resolve()
    element_tree = etree.parse(str(full_path))
    interface = parse_element_tree(element_tree)

    return parse_element_tree(interface)
