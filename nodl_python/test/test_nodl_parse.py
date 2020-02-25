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

from lxml.builder import E
import lxml.etree as etree
from nodl import errors
import nodl._parsing
import nodl.types
import pytest
from rclpy import qos


@pytest.fixture()
def valid_nodl() -> etree._ElementTree:
    return etree.parse(str(Path('test/nodl.xml')))


def test__parse_element_tree(mocker):
    not_interface = E.notinterface()
    # Test that fails when no interface tag is included
    with pytest.raises(errors.InvalidNoDLError):
        nodl._parsing._parsing._parse_element_tree(etree.ElementTree(not_interface))

    # Test that fails when no version is specified
    with pytest.raises(errors.InvalidNoDLError):
        nodl._parsing._parsing._parse_element_tree(E.interface(E.node()))

    # Test that succeeds when interface is top level
    interface = E.interface(E.node(), version='1')
    mocker.patch('nodl._parsing._parsing._parse_interface')
    assert nodl._parsing._parsing._parse_element_tree(etree.ElementTree(interface))


def test_parse_nodl_file_valid(mocker):
    mocker.patch('nodl._parsing._parsing._parse_element_tree')

    # Test if accepts a valid xml file
    assert nodl._parsing._parsing._parse_nodl_file(Path('test/nodl.xml')) is not None


def test_parse_interface(mocker):
    mocker.patch('nodl._parsing._parsing.parse_v1._validate_and_parse')
    # Test that unversioned interfaces aren't accepted
    interface_no_version = E.interface()
    with pytest.raises(errors.InvalidNoDLError):
        nodl._parsing._parsing._parse_interface(interface_no_version)

    # Test that unsupported versions aren't accepted
    interface_future_version = E.interface(
        E.node(), version=str(nodl._parsing._parsing.NODL_MAX_SUPPORTED_VERSION + 1)
    )
    with pytest.raises(errors.UnsupportedInterfaceError):
        nodl._parsing._parsing._parse_interface(interface_future_version)

    # Test that all versions <= max version are supported
    interface_versions = [
        E.interface(E.node(), version=str(version))
        for version in range(1, nodl._parsing._parsing.NODL_MAX_SUPPORTED_VERSION + 1)
    ]
    for version, interface in enumerate(interface_versions):
        assert (
            nodl._parsing._parsing._parse_interface(interface) is not None
        ), f'Missing version {version}'


def test__parse_qos():
    # Test that qos requires at minimum history or depth
    element = etree.Element('qos')
    with pytest.raises(errors.InvalidQoSError):
        nodl._parsing._qos._parse_qos(element)

    # Test that each attribute can be set
    # History
    element.set('history', 'system_default')
    qos_profile = nodl._parsing._qos._parse_qos(element)
    assert qos_profile.history == qos.HistoryPolicy.SYSTEM_DEFAULT
    element.set('history', 'keep_all')
    qos_profile = nodl._parsing._qos._parse_qos(element)
    assert qos_profile.history == qos.HistoryPolicy.KEEP_ALL

    # Reliability
    element.set('reliability', 'system_default')
    qos_profile = nodl._parsing._qos._parse_qos(element)
    assert qos_profile.reliability == qos.ReliabilityPolicy.SYSTEM_DEFAULT
    element.set('reliability', 'best_effort')
    qos_profile = nodl._parsing._qos._parse_qos(element)
    assert qos_profile.reliability == qos.ReliabilityPolicy.BEST_EFFORT

    # Durability
    element.set('durability', 'system_default')
    qos_profile = nodl._parsing._qos._parse_qos(element)
    assert qos_profile.durability == qos.DurabilityPolicy.SYSTEM_DEFAULT
    element.set('durability', 'transient_local')
    qos_profile = nodl._parsing._qos._parse_qos(element)
    assert qos_profile.durability == qos.DurabilityPolicy.TRANSIENT_LOCAL

    # Lifespan
    element.set('lifespan', '451')
    qos_profile = nodl._parsing._qos._parse_qos(element)
    assert qos_profile.lifespan.nanoseconds == 451

    # Liveliness
    element.set('liveliness', 'system_default')
    qos_profile = nodl._parsing._qos._parse_qos(element)
    assert qos_profile.liveliness == qos.LivelinessPolicy.SYSTEM_DEFAULT
    element.set('liveliness', 'manual_by_node')
    qos_profile = nodl._parsing._qos._parse_qos(element)
    assert qos_profile.liveliness == qos.LivelinessPolicy.MANUAL_BY_NODE

    # Liveliness Lease Duration
    element.set('liveliness_lease_duration', '451')
    qos_profile = nodl._parsing._qos._parse_qos(element)
    assert qos_profile.liveliness_lease_duration.nanoseconds == 451

    # Avoid ROS namespace conventions
    element.set('avoid_ros_namespace_conventions', 'True')
    qos_profile = nodl._parsing._qos._parse_qos(element)
    assert qos_profile.avoid_ros_namespace_conventions
    element.set('avoid_ros_namespace_conventions', 'False')
    qos_profile = nodl._parsing._qos._parse_qos(element)
    assert not qos_profile.avoid_ros_namespace_conventions

    # Test that parser errors on out of enum values
    element.set('liveliness', 'foobar')
    with pytest.raises(errors.InvalidQoSError):
        nodl._parsing._qos._parse_qos(element)


class TestInterface_v1:
    """Test suite for v1 of NoDL."""

    def test__validate_and_parse(self, valid_nodl):
        # Assert a minimal example passes validation
        element = E.interface(
            E.node(E.action(E.qos(depth='10'), name='bar', type='baz', server='true'), name='foo'),
            version='1',
        )
        assert nodl._parsing._v1._validate_and_parse(element)

        # Assert example nodl passes validation
        assert nodl._parsing._v1._validate_and_parse(valid_nodl.getroot())

        # Assert empty interface does not pass
        element = E.interface(version='1')
        with pytest.raises(errors.InvalidNoDLError):
            nodl._parsing._v1._validate_and_parse(element)

    def test__parse_action(self):
        element = E.action(E.qos(depth='10'), name='foo', type='bar', server='true')

        # Test that actions get parsed
        action = nodl._parsing._v1._parse_action(element)
        assert type(action) is nodl.types.Action
        assert action.server
        # Test that bools have default values
        assert not action.client

        # Test that warning is emitted when both bools are false
        element.attrib['server'] = 'False'
        with pytest.raises(errors.AmbiguousActionInterfaceError):
            nodl._parsing._v1._parse_action(element)

    def test__parse_parameter(self):
        element = E.parameter()

        # Test that parse is successful
        element.set('name', 'foo')
        element.set('type', 'bar')
        assert type(nodl._parsing._v1._parse_parameter(element)) is nodl.types.Parameter
        assert element.get('name') == 'foo'
        assert element.get('type') == 'bar'

    def test__parse_service(self):
        # Test that parse fails when missing name/type
        element = E.service(E.qos(depth='10'), name='foo', type='bar', server='true')

        # Test that services get parsed
        service = nodl._parsing._v1._parse_service(element)
        assert type(service) is nodl.types.Service
        assert service.server
        # Test that bools have default values
        assert not service.client

        # Test that warning is emitted when both bools are false
        element.attrib['server'] = 'False'
        with pytest.raises(errors.AmbiguousServiceInterfaceError):
            nodl._parsing._v1._parse_service(element)

    def test__parse_topic(self):
        # Test that parse fails when missing name/type
        element = E.topic(E.qos(depth='10'), name='foo', type='bar', publisher='true')

        topic = nodl._parsing._v1._parse_topic(element)
        assert topic.publisher
        # Test that bools have default values
        assert not topic.subscription

        # Test that warning is emitted when both bools are false
        element.set('publisher', 'false')
        with pytest.raises(errors.AmbiguousTopicInterfaceError):
            nodl._parsing._v1._parse_topic(element)

    def test__parse_node(self, valid_nodl: etree._ElementTree):
        nodes = valid_nodl.findall('node')
        node = nodl._parsing._v1._parse_node(nodes[1])
        assert node.actions and node.parameters and node.services and node.topics

    def test__parse_nodes(self, valid_nodl: etree._ElementTree):
        nodes = nodl._parsing._v1._parse_nodes(valid_nodl.getroot())
        assert len(nodes) == 2
