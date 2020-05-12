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

from ament_index_python.packages import get_package_share_directory

from nodl._parsing._parsing import _parse_multiple
from nodl.errors import ExecutableNotFoundError, NoNoDLFilesError

from .types import Node


def _get_nodl_xml_files_in_path(*, path: Path) -> List[Path]:
    """Return all files with NoDL extension (.nodl.xml) in a path."""
    return sorted(path.rglob('*.nodl.xml'))


def _get_nodl_files_from_package_share(*, package_name: str) -> List[Path]:
    """Return all .nodl.xml files from the share directory of a package.

    :raises PackageNotFoundError: if package is not found
    :raises NoNoDLFilesError: if no .nodl.xml files are in package share directory
    """
    package_share_directory = Path(get_package_share_directory(package_name))
    nodl_paths = _get_nodl_xml_files_in_path(path=package_share_directory)
    if not nodl_paths:
        raise NoNoDLFilesError(package_name)
    return nodl_paths


def _get_nodes_from_package(*, package_name: str) -> List[Node]:
    """Return results of parsing all nodl.xml files of a package.

    :param package_name: name of the package
    :type package_name: str
    :return: combined list of all `nodl.Node`'s a package contains
    :rtype: List[Node]
    """
    nodl_files = _get_nodl_files_from_package_share(package_name=package_name)
    return _parse_multiple(paths=nodl_files)


def get_node_by_executable(*, package_name: str, executable_name: str) -> Node:
    """Return node associated with given executable from a package's exported nodl.

    :param package_name: name of the package to search in
    :type package_name: str
    :param executable_name: the name of the executable the node is associated with
    :type executable_name: str
    :raises ExecutableNotFoundError: if no node in the package is associated with executable_name
    :return: Node with matching executable field
    :rtype: Node
    """
    try:
        nodes = _get_nodes_from_package(package_name=package_name)
        result = next(node for node in nodes if node.executable == executable_name)
    except StopIteration:
        raise ExecutableNotFoundError(package_name=package_name, executable_name=executable_name)
    return result
