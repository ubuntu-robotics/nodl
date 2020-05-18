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

from lxml.builder import E
import lxml.etree as etree
from nodl import errors
import nodl._parsing
import nodl._parsing._v1._parsing
import nodl.types
import pytest


@pytest.fixture()
def valid_nodl(test_nodl_path) -> etree._ElementTree:
    return etree.parse(str(test_nodl_path))


def test_parse(valid_nodl):
    # Assert a minimal example passes validation
    element = E.interface(
        E.node(
            E.action(E.qos(depth='10'), name='bar', type='baz', server='true'),
            name='foo',
            executable='row',
        ),
        version='1',
    )
    assert nodl._parsing._v1.parse(element)

    # Assert example nodl passes validation
    assert nodl._parsing._v1.parse(valid_nodl.getroot())

    # Assert empty interface does not pass
    element = E.interface(version='1')
    with pytest.raises(errors.InvalidNoDLDocumentError):
        nodl._parsing._v1.parse(element)


def test__parse_action():
    element = E.action(E.qos(depth='10'), name='foo', value_type='bar', server='true')

    # Test that actions get parsed
    action = nodl._parsing._v1._parsing._parse_action(element)
    assert type(action) is nodl.types.Action
    assert action.server
    # Test that bools have default values
    assert not action.client

    # Test that warning is emitted when both bools are false
    element.attrib['server'] = 'False'
    with pytest.raises(errors.AmbiguousActionInterfaceError):
        nodl._parsing._v1._parsing._parse_action(element)


def test__parse_parameter():
    element = E.parameter()

    # Test that parse is successful
    element.set('name', 'foo')
    element.set('type', 'bar')
    assert type(nodl._parsing._v1._parsing._parse_parameter(element)) is nodl.types.Parameter
    assert element.get('name') == 'foo'
    assert element.get('type') == 'bar'


def test__parse_service():
    # Test that parse fails when missing name/type
    element = E.service(E.qos(depth='10'), name='foo', value_type='bar', server='true')

    # Test that services get parsed
    service = nodl._parsing._v1._parsing._parse_service(element)
    assert type(service) is nodl.types.Service
    assert service.server
    # Test that bools have default values
    assert not service.client

    # Test that warning is emitted when both bools are false
    element.attrib['server'] = 'False'
    with pytest.raises(errors.AmbiguousServiceInterfaceError):
        nodl._parsing._v1._parsing._parse_service(element)


def test__parse_topic():
    # Test that parse fails when missing name/type
    element = E.topic(E.qos(depth='10'), name='foo', value_type='bar', publisher='true')

    topic = nodl._parsing._v1._parsing._parse_topic(element)
    assert topic.publisher
    # Test that bools have default values
    assert not topic.subscription

    # Test that warning is emitted when both bools are false
    element.set('publisher', 'false')
    with pytest.raises(errors.AmbiguousTopicInterfaceError):
        nodl._parsing._v1._parsing._parse_topic(element)


def test__parse_node(valid_nodl: etree._ElementTree):
    nodes = valid_nodl.findall('node')
    node = nodl._parsing._v1._parsing._parse_node(nodes[1])
    assert node.actions and node.parameters and node.services and node.topics


def test__parse_nodes(valid_nodl: etree._ElementTree):
    nodes = nodl._parsing._v1._parsing._parse_nodes(valid_nodl.getroot())
    assert len(nodes) == 2
