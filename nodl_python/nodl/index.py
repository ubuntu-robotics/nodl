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
from typing import List, TYPE_CHECKING

from ament_index_python.packages import get_package_share_directory

from ._parsing import parse_multiple
from .errors import NoNoDLFilesError

if TYPE_CHECKING:
    from .types import Node  # noqa: F401


def get_nodl_xml_files_in_path(*, path: Path) -> List[Path]:
    """Return all files with NoDL extension (.nodl.xml) in a path."""
    return sorted(path.rglob('*.nodl.xml'))


def get_nodl_files_from_package_share(*, package_name: str) -> List[Path]:
    """Return all .nodl.xml files from the share directory of a package.

    :raises PackageNotFoundError: if package is not found
    :raises NoNoDLFilesError: if no .nodl.xml files are in package share directory
    """
    package_share_directory = Path(get_package_share_directory(package_name))
    nodl_paths = get_nodl_xml_files_in_path(path=package_share_directory)
    if not nodl_paths:
        raise NoNoDLFilesError(package_name)
    return nodl_paths


def get_nodes_from_package(*, package_name: str) -> List['Node']:
    """Return results of parsing all nodl.xml files of a package.

    :param package_name: name of the package
    :type package_name: str
    :return: combined list of all `nodl.Node`'s a package contains
    :rtype: List[Node]
    """
    nodl_files: List[Path] = get_nodl_files_from_package_share(package_name=package_name)
    return parse_multiple(paths=nodl_files)
