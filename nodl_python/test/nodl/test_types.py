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


import nodl.types
import pytest
import rclpy.qos


@pytest.fixture
def topic_publisher():
    return nodl.types.Topic(name='foo', message_type='bar', publisher=True)


def test_action():
    action_server = nodl.types.Action(name='foo', action_type='bar', server=True)
    assert action_server.name == 'foo'
    assert action_server.type == 'bar'
    assert action_server.server
    assert action_server.qos is not None


def test_parameter():
    parameter = nodl.types.Parameter(name='foo', parameter_type='bar')
    assert parameter.name == 'foo'
    assert parameter.type == 'bar'


def test_service():
    service_client = nodl.types.Service(name='foo', service_type='bar', client=True)
    assert service_client.name == 'foo'
    assert service_client.type == 'bar'
    assert service_client.client
    assert service_client.qos is not None


def test_topic(topic_publisher):
    assert topic_publisher.name == 'foo'
    assert topic_publisher.type == 'bar'
    assert topic_publisher.publisher


def test_representations(topic_publisher):
    assert 'foo' in repr(topic_publisher) and 'bar' in repr(topic_publisher)
    assert 'foo' in str(topic_publisher) and 'bar' in str(topic_publisher)


def test__as_dict(topic_publisher):
    assert topic_publisher._as_dict['name'] == 'foo'
    assert topic_publisher._as_dict['type'] == 'bar'
    assert isinstance(topic_publisher._as_dict['qos'], dict)

    parameter = nodl.types.Parameter(name='foo', parameter_type='bar')
    assert 'qos' not in parameter._as_dict


def test_equality(topic_publisher):
    also_topic_publisher = nodl.types.Topic(name='foo', message_type='bar', publisher=True)
    assert also_topic_publisher == topic_publisher

    not_same_topic_publisher = nodl.types.Topic(
        name='foo', message_type='bar', publisher=True, qos=rclpy.qos.QoSProfile(depth=1)
    )
    assert not_same_topic_publisher != topic_publisher


def test_same_name_different_interface_type():
    topic = nodl.types.Topic(name='foo', message_type='bar')
    service = nodl.types.Service(name='foo', service_type='bar')
    assert topic != service


def test_node():
    topic = nodl.types.Topic(name='foo', message_type='bar')
    service = nodl.types.Service(name='baz', service_type='woo')

    node = nodl.types.Node(name='test', executable='toast', topics=[topic], services=[service])
    assert node.name == 'test'
    assert node.executable == 'toast'
    assert node.topics[topic.name] == topic
    assert node.services[service.name] == service


def test_node__as_dict():
    topic = nodl.types.Topic(name='foo', message_type='bar')
    service = nodl.types.Service(name='baz', service_type='woo')

    node = nodl.types.Node(name='test', executable='toast', topics=[topic], services=[service])
    assert node._as_dict['name'] == node.name
    assert node._as_dict['executable'] == node.executable
    assert topic._as_dict in node._as_dict['topics']
