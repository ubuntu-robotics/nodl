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
from nodl._util import get_bool_attribute, str_to_bool
from nodl.exception import InvalidNoDLException
import pytest


def test_str_to_bool():
    true_strs = ['true', 'True', 'TrUe', '1']
    false_strs = ['false', 'False', 'FaLsE', '0']
    for val in true_strs:
        assert str_to_bool(val)
    for val in false_strs:
        assert not str_to_bool(val)
    with pytest.raises(ValueError) as excinfo:
        str_to_bool('bar')
    assert 'bar' in str(excinfo.value)


def test_get_bool_attribute_except(mocker):
    mock_et = mocker.patch('nodl._util.str_to_bool', return_value=True)
    foo = etree.Element('foo', {'bar': 'true'})
    assert get_bool_attribute(foo, 'bar')
    mock_et.side_effect = ValueError

    foo.set('bar', 'baz')
    with pytest.raises(InvalidNoDLException) as excinfo:
        get_bool_attribute(foo, 'bar')
    assert 'bar' in str(excinfo.value)
    assert 'baz' in str(excinfo.value)
