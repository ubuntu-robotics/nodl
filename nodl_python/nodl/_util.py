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

from distutils.util import strtobool
from typing import TYPE_CHECKING

from nodl.exception import InvalidNoDLException

if TYPE_CHECKING:  # pragma: no cover
    from lxml.etree import _Element


def get_bool_attribute(element: '_Element', attribute: str) -> bool:
    """Access attribute and bool conversion."""
    boolean_string = element.get(attribute, 'False')
    try:
        return bool(strtobool(boolean_string))
    except ValueError as excinfo:
        raise InvalidNoDLException(
            f'Attribute {attribute} has invalid value {boolean_string}', element
        ) from excinfo
