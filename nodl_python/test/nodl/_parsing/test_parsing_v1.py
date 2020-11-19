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


def test_parse_minimal():
    # Assert a minimal example passes validation
    element = E.interface(
        E.node(
            E.action(name='bar', type='baz', role='server'), name='foo', executable='row',
        ),
        version='1',
    )
    assert nodl._parsing._v1.parse(element)


def test_parse_valid_example(valid_nodl):
    # Assert example nodl passes validation
    assert nodl._parsing._v1.parse(valid_nodl.getroot())


def test_parse_fail_on_empty():
    # Assert empty interface does not pass
    element = E.interface(version='1')
    with pytest.raises(errors.InvalidNoDLDocumentError):
        nodl._parsing._v1.parse(element)


def test__parse_action():
    element = E.action(name='foo', value_type='bar', role='server')

    # Test that actions get parsed
    action = nodl._parsing._v1._parsing._parse_action(element)
    assert type(action) is nodl.types.Action
    assert action.role == nodl.types.ServerClientRole.SERVER


def test__parse_parameter():
    element = E.parameter(name='foo', type='bar')

    # Test that parse is successful
    assert type(nodl._parsing._v1._parsing._parse_parameter(element)) is nodl.types.Parameter
    assert element.get('name') == 'foo'
    assert element.get('type') == 'bar'


def test__parse_service():
    element = E.service(name='foo', value_type='bar', role='server')

    # Test that services get parsed
    service = nodl._parsing._v1._parsing._parse_service(element)
    assert type(service) is nodl.types.Service
    assert service.role == nodl.types.ServerClientRole.SERVER


def test__parse_topic():
    element = E.topic(name='foo', value_type='bar', role='publisher')

    topic = nodl._parsing._v1._parsing._parse_topic(element)
    assert topic.role == nodl.types.PubSubRole.PUBLISHER


def test__parse_node(valid_nodl: etree._ElementTree):
    nodes = valid_nodl.findall('node')
    node = nodl._parsing._v1._parsing._parse_node(nodes[1])
    assert node.actions and node.parameters and node.services and node.topics


def test__parse_node_invalid_child():
    node = E.node(E.baz(), name='foo', executable='bar')
    with pytest.raises(errors.InvalidNodeChildError):
        nodl._parsing._v1._parsing._parse_node(node)


def test__parse_nodes(valid_nodl: etree._ElementTree):
    nodes = nodl._parsing._v1._parsing._parse_nodes(valid_nodl.getroot())
    assert len(nodes) == 2
