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


import nodl.types
import pytest


@pytest.fixture
def topic_publisher():
    return nodl.types.Topic(name='foo', message_type='bar', role=nodl.types.PubSubRole.PUBLISHER)


def test_action():
    action_server = nodl.types.Action(
        name='foo', action_type='bar', role=nodl.types.ServerClientRole.SERVER
    )
    assert action_server.name == 'foo'
    assert action_server.type == 'bar'
    assert action_server.role == nodl.types.ServerClientRole.SERVER


def test_parameter():
    parameter = nodl.types.Parameter(name='foo', parameter_type='bar')
    assert parameter.name == 'foo'
    assert parameter.type == 'bar'


def test_service():
    service = nodl.types.Service(
        name='foo', service_type='bar', role=nodl.types.ServerClientRole.CLIENT
    )
    assert service.name == 'foo'
    assert service.type == 'bar'
    assert service.role == nodl.types.ServerClientRole.CLIENT

    service = nodl.types.Service(
        name='foo', service_type='bar', role=nodl.types.ServerClientRole.SERVER,
    )
    assert service.role == nodl.types.ServerClientRole.SERVER


def test_topic():
    topic = nodl.types.Topic(name='foo', message_type='bar', role=nodl.types.PubSubRole.PUBLISHER,)
    assert topic.name == 'foo'
    assert topic.type == 'bar'
    assert topic.role == nodl.types.PubSubRole.PUBLISHER

    topic = nodl.types.Topic(
        name='foo', message_type='bar', role=nodl.types.PubSubRole.SUBSCRIPTION,
    )
    assert topic.role == nodl.types.PubSubRole.SUBSCRIPTION


def test_representations(topic_publisher):
    assert 'foo' in repr(topic_publisher) and 'bar' in repr(topic_publisher)
    assert 'foo' in str(topic_publisher) and 'bar' in str(topic_publisher)


def test_equality(topic_publisher):
    also_topic_publisher = nodl.types.Topic(
        name='foo', message_type='bar', role=nodl.types.PubSubRole.PUBLISHER,
    )
    assert also_topic_publisher == topic_publisher

    not_same_topic_publisher = nodl.types.Topic(
        name='bar', message_type='bar', role=nodl.types.PubSubRole.PUBLISHER,
    )
    assert not_same_topic_publisher != topic_publisher

    # Test different roles cause inequality
    assert nodl.types.Action(
        name='foo', action_type='bar', role=nodl.types.ServerClientRole.CLIENT
    ) != nodl.types.Action(name='foo', action_type='bar', role=nodl.types.ServerClientRole.BOTH)


def test_same_name_different_interface_type():
    topic = nodl.types.Topic(name='foo', message_type='bar', role=nodl.types.PubSubRole.PUBLISHER,)
    service = nodl.types.Service(
        name='foo', service_type='bar', role=nodl.types.ServerClientRole.SERVER
    )
    assert topic != service


def test_node(topic_publisher):
    service = nodl.types.Service(
        name='baz', service_type='woo', role=nodl.types.ServerClientRole.SERVER
    )

    node = nodl.types.Node(
        name='test', executable='toast', topics=[topic_publisher], services=[service]
    )
    assert node.name == 'test'
    assert node.executable == 'toast'
    assert node.topics[topic_publisher.name] == topic_publisher
    assert node.services[service.name] == service
