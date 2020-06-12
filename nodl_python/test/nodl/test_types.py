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


from itertools import chain, combinations

import nodl.types
import pytest
import rclpy.qos


@pytest.fixture
def qos_mock(mocker):
    mocker.MagicMock(spec=rclpy.qos.QoSProfile)


@pytest.fixture
def profile_keys():
    return [
        'goal_service_qos_profile',
        'result_service_qos_profile',
        'cancel_service_qos_profile',
        'feedback_sub_qos_profile',
        'status_sub_qos_profile',
    ]


@pytest.fixture
def topic_publisher(qos_mock):
    return nodl.types.Topic(name='foo', message_type='bar', publisher=True, qos_profile=qos_mock)


def test_action(qos_mock, profile_keys):
    action_server = nodl.types.Action(name='foo', action_type='bar', server=True)
    assert action_server.name == 'foo'
    assert action_server.type == 'bar'
    assert action_server.server

    # Test that every combination of keys is settable
    p_set = chain.from_iterable(
        combinations(profile_keys, r) for r in range(len(profile_keys) + 1)
    )
    for comb in p_set:
        args = {'name': 'foo', 'action_type': 'bar', 'client': True}
        args.update({key: qos_mock for key in comb})
        action_server = nodl.types.Action(**args)

        for key in comb:
            assert (
                getattr(action_server, key) == qos_mock
            ), f'Setting combination of {comb} failed!'


def test_parameter():
    parameter = nodl.types.Parameter(name='foo', parameter_type='bar')
    assert parameter.name == 'foo'
    assert parameter.type == 'bar'


def test_service(qos_mock):
    service = nodl.types.Service(name='foo', service_type='bar', client=True)
    assert service.name == 'foo'
    assert service.type == 'bar'
    assert not service.server
    assert service.client
    assert service.qos_profile is not None

    service = nodl.types.Service(name='foo', service_type='bar', server=True, qos_profile=qos_mock)
    assert service.qos_profile == qos_mock
    assert service.server
    assert not service.client


def test_topic(qos_mock):
    topic = nodl.types.Topic(name='foo', message_type='bar', publisher=True, qos_profile=qos_mock)
    assert topic.name == 'foo'
    assert topic.type == 'bar'
    assert topic.publisher

    topic = nodl.types.Topic(
        name='foo', message_type='bar', subscription=True, qos_profile=qos_mock
    )
    assert topic.subscription


def test_representations(topic_publisher):
    topic_publisher.qos_profile = rclpy.qos.QoSProfile(depth=10)
    assert 'foo' in repr(topic_publisher) and 'bar' in repr(topic_publisher)
    assert 'foo' in str(topic_publisher) and 'bar' in str(topic_publisher)


def test__as_dict(topic_publisher):
    topic_publisher.qos_profile = rclpy.qos.qos_profile_system_default
    assert topic_publisher._as_dict['name'] == 'foo'
    assert topic_publisher._as_dict['type'] == 'bar'
    assert isinstance(topic_publisher._as_dict['qos_profile'], dict)

    parameter = nodl.types.Parameter(name='foo', parameter_type='bar')
    assert 'qos_profile' not in parameter._as_dict


def test__as_dict_action(profile_keys):
    action = nodl.types.Action(name='foo', action_type='bar', server=True)
    assert action._as_dict['name'] == 'foo'
    assert action._as_dict['type'] == 'bar'

    for key in profile_keys:
        assert isinstance(action._as_dict[key], dict)


def test_equality(topic_publisher, qos_mock):
    also_topic_publisher = nodl.types.Topic(
        name='foo', message_type='bar', publisher=True, qos_profile=qos_mock
    )
    assert also_topic_publisher == topic_publisher

    not_same_topic_publisher = nodl.types.Topic(
        name='foo', message_type='bar', publisher=True, qos_profile=rclpy.qos.QoSProfile(depth=1)
    )
    assert not_same_topic_publisher != topic_publisher


def test_same_name_different_interface_type(qos_mock):
    topic = nodl.types.Topic(name='foo', message_type='bar', publisher=True, qos_profile=qos_mock)
    service = nodl.types.Service(name='foo', service_type='bar', server=True)
    assert topic != service


def test_node(topic_publisher):
    service = nodl.types.Service(name='baz', service_type='woo', server=True)

    node = nodl.types.Node(
        name='test', executable='toast', topics=[topic_publisher], services=[service]
    )
    assert node.name == 'test'
    assert node.executable == 'toast'
    assert node.topics[topic_publisher.name] == topic_publisher
    assert node.services[service.name] == service


def test_node__as_dict(topic_publisher):
    topic_publisher.qos_profile = rclpy.qos.QoSProfile(depth=10)
    service = nodl.types.Service(name='baz', service_type='woo')

    node = nodl.types.Node(
        name='test', executable='toast', topics=[topic_publisher], services=[service]
    )
    assert node._as_dict['name'] == node.name
    assert node._as_dict['executable'] == node.executable
    assert topic_publisher._as_dict in node._as_dict['topics']
