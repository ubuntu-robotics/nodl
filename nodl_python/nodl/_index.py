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
from typing import Iterable, List, Tuple

from ament_index_python.packages import get_package_share_directory

from nodl._parsing._parsing import _parse_multiple
from nodl.errors import ExecutableNotFoundError, NoNoDLFilesError

from .types import Node


_FILE_EXTENSION = '.nodl.xml'


def _get_nodl_files_from_package_share(*, package_name: str) -> List[Path]:
    """Return all .nodl.xml files from the share directory of a package.

    :raises PackageNotFoundError: if package is not found
    :raises NoNoDLFilesError: if no .nodl.xml files are in package share directory
    """
    package_share_directory = Path(get_package_share_directory(package_name))
    nodl_paths = [
        path for path in package_share_directory.glob('*' + _FILE_EXTENSION) if path.is_file()
    ]
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
    nodes = _get_nodes_from_package(package_name=package_name)
    try:
        return next(node for node in nodes if node.executable == executable_name)
    except StopIteration:
        raise ExecutableNotFoundError(package_name=package_name, executable_name=executable_name)


def _get_nodes_by_executables(
    *, package_name: str, executable_names: Iterable[str]
) -> Tuple[List[Node], List[str]]:
    """Return nodes associated with given executables from a package's exported nodl.

    :param package_name: name of the package to search in
    :type package_name: str
    :param executable_names: the names of the executables the nodes are associated with
    :type executable_names: Iterable[str]
    :return: Tuple containing nodes with matching executable field, unmatched nodes
    :rtype: Tuple[List[Node], List[Node]]
    """
    nodes = _get_nodes_from_package(package_name=package_name)
    result = {node.executable: node for node in nodes if node.executable in executable_names}
    missing = list(set(executable_names) - result.keys())
    return list(result.values()), missing
