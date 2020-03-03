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

from lxml import etree
from nodl._util import get_bool_attribute


def test_get_bool_attribute_except(mocker):
    foo = etree.Element('foo', {'bar': 'true'})
    assert get_bool_attribute(foo, 'bar')
    foo.set('bar', 'false')
    assert not get_bool_attribute(foo, 'bar')
