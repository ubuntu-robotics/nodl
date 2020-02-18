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

from lxml import etree
import pkg_resources


def get_schema(name: str) -> etree.XMLSchema:
    file_name = pkg_resources.resource_filename(
        package_or_requirement='nodl', resource_name=str(Path(f'schemas/{name}'))
    )
    return etree.XMLSchema(file=file_name)
