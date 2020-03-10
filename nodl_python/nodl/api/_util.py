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

import distutils.util
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from lxml import etree


def get_bool_attribute(element: 'etree._Element', attribute: str) -> bool:
    """Access attribute and bool conversion."""
    boolean_string = element.get(attribute, 'False')
    return bool(distutils.util.strtobool(boolean_string))
