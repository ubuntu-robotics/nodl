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
from typing import List

import lxml.etree as etree
import nodl._parsing
from nodl.exception import InvalidNoDLException, UnsupportedInterfaceException
import nodl.types
from nodl.warning import NoNodeInterfaceWarning
import pytest
from rclpy import qos


@pytest.fixture()
def valid_nodl() -> etree._ElementTree:
    return etree.parse(str(Path('test/nodl.xml')))


def test_parse_element_tree(mocker):
    not_interface = etree.Element('notinterface')
    not_interface.append(etree.Element('stillnotelement'))
    # Test that fails when no interface tag is included
    with pytest.raises(InvalidNoDLException) as excinfo:
        nodl._parsing.parse_element_tree(etree.ElementTree(not_interface))
    assert 'No interface tag in' in str(excinfo.value)

    # Test that succeeds when interface isn't top level
    not_interface[0].append(etree.Element('interface'))
    mocker.patch('nodl._parsing._parsing.parse_interface')
    assert nodl._parsing.parse_element_tree(etree.ElementTree(not_interface)) is not None

    # Test that succeeds when interface is top level
    assert nodl._parsing.parse_element_tree(etree.ElementTree(etree.Element('interface')))


def test_parse_nodl_file_valid(mocker):
    mocker.patch('nodl._parsing._parsing.parse_element_tree')

    # Test if accepts a valid xml file
    assert nodl._parsing.parse_nodl_file(Path('test/nodl.xml')) is not None


def test_parse_interface():

    # Test that unversioned interfaces aren't accepted
    interface_no_version = etree.Element('interface')
    with pytest.raises(InvalidNoDLException) as excinfo:
        nodl._parsing.parse_interface(interface_no_version)
    assert 'Missing version attribute in "interface"' in str(excinfo.value)

    # Test that unsupported versions aren't accepted
    interface_future_version = etree.Element(
        'interface', {'version': str(nodl._parsing._parsing.NODL_MAX_SUPPORTED_VERSION + 1)}
    )
    with pytest.raises(UnsupportedInterfaceException) as excinfo:
        nodl._parsing.parse_interface(interface_future_version)
    assert 'Unsupported interface version' in str(excinfo)

    # Test that all versions <= max version are supported
    interface_versions = [
        etree.Element('interface', {'version': str(version)})
        for version in range(1, nodl._parsing._parsing.NODL_MAX_SUPPORTED_VERSION + 1)
    ]
    for version, interface in enumerate(interface_versions):
        assert nodl._parsing.parse_interface(interface) is not None, f'Missing version {version}'


def test_parse_qos():
    # Test that there is a default value for all qos entries
    element: etree._Element = etree.Element('qos')
    assert nodl._parsing.parse_qos(element)

    # Test that each attribute can be set
    # History
    element.set('history', 'system_default')
    qos_profile = nodl._parsing.parse_qos(element)
    assert qos_profile.history == qos.HistoryPolicy.SYSTEM_DEFAULT
    element.set('history', 'keep_all')
    qos_profile = nodl._parsing.parse_qos(element)
    assert qos_profile.history == qos.HistoryPolicy.KEEP_ALL

    # Reliability
    element.set('reliability', 'system_default')
    qos_profile = nodl._parsing.parse_qos(element)
    assert qos_profile.reliability == qos.ReliabilityPolicy.SYSTEM_DEFAULT
    element.set('reliability', 'best_effort')
    qos_profile = nodl._parsing.parse_qos(element)
    assert qos_profile.reliability == qos.ReliabilityPolicy.BEST_EFFORT

    # Durability
    element.set('durability', 'system_default')
    qos_profile = nodl._parsing.parse_qos(element)
    assert qos_profile.durability == qos.DurabilityPolicy.SYSTEM_DEFAULT
    element.set('durability', 'transient_local')
    qos_profile = nodl._parsing.parse_qos(element)
    assert qos_profile.durability == qos.DurabilityPolicy.TRANSIENT_LOCAL

    # Lifespan
    element.set('lifespan', '451')
    qos_profile = nodl._parsing.parse_qos(element)
    assert qos_profile.lifespan.nanoseconds == 451

    # Liveliness
    element.set('liveliness', 'system_default')
    qos_profile = nodl._parsing.parse_qos(element)
    assert qos_profile.liveliness == qos.LivelinessPolicy.SYSTEM_DEFAULT
    element.set('liveliness', 'manual_by_node')
    qos_profile = nodl._parsing.parse_qos(element)
    assert qos_profile.liveliness == qos.LivelinessPolicy.MANUAL_BY_NODE

    # Liveliness Lease Duration
    element.set('liveliness_lease_duration', '451')
    qos_profile = nodl._parsing.parse_qos(element)
    assert qos_profile.liveliness_lease_duration.nanoseconds == 451

    # Avoid ROS namespace conventions
    element.set('avoid_ros_namespace_conventions', 'True')
    qos_profile = nodl._parsing.parse_qos(element)
    assert qos_profile.avoid_ros_namespace_conventions
    element.set('avoid_ros_namespace_conventions', 'False')
    qos_profile = nodl._parsing.parse_qos(element)
    assert not qos_profile.avoid_ros_namespace_conventions

    # Test that parser errors on out of enum values
    element.set('liveliness', 'foobar')
    with pytest.raises(InvalidNoDLException):
        nodl._parsing.parse_qos(element)


class TestInterface_v1:
    """Test suite for v1 of NoDL."""

    @pytest.mark.filterwarnings('error')
    def test_parse_action(self):
        # Test that parse fails when missing name/type
        element: etree._Element = etree.Element('service')
        with pytest.raises(KeyError):
            nodl._parsing._v1.parse_action(element)

        element.set('name', 'foo')
        element.set('type', 'bar')
        element.set('server', 'True')

        # Test that actions get parsed
        action = nodl._parsing._v1.parse_action(element)
        assert type(action) is nodl.types.Action
        assert action.server
        # Test that bools have default values
        assert not action.client

        # Test that warning is emitted when both bools are false
        element.attrib['server'] = 'False'
        with pytest.warns(NoNodeInterfaceWarning):
            assert type(nodl._parsing._v1.parse_action(element)) is nodl.types.Action

    def test_parse_parameter(self):
        # Test that parse fails when missing name/type
        element: etree._Element = etree.Element('parameter')
        with pytest.raises(KeyError):
            nodl._parsing._v1.parse_action(element)

        # Test that parse is successful
        element.set('name', 'foo')
        element.set('type', 'bar')
        assert type(nodl._parsing._v1.parse_parameter(element)) is nodl.types.Parameter

    @pytest.mark.filterwarnings('error')
    def test_parse_service(self):
        # Test that parse fails when missing name/type
        element: etree._Element = etree.Element('service')
        with pytest.raises(KeyError):
            nodl._parsing._v1.parse_service(element)

        element.set('name', 'foo')
        element.set('type', 'bar')
        element.set('server', 'True')

        # Test that actions get parsed
        service = nodl._parsing._v1.parse_service(element)
        assert type(service) is nodl.types.Service
        assert service.server
        # Test that bools have default values
        assert not service.client

        # Test that warning is emitted when both bools are false
        element.attrib['server'] = 'False'
        with pytest.warns(NoNodeInterfaceWarning):
            service = nodl._parsing._v1.parse_service(element)

        assert not service.server

    @pytest.mark.filterwarnings('error')
    def test_parse_topic(self):
        # Test that parse fails when missing name/type
        element: etree._Element = etree.Element('topic')
        with pytest.raises(KeyError):
            nodl._parsing._v1.parse_topic(element)

        element.set('name', 'foo')
        element.set('type', 'bar')
        element.set('publisher', 'True')
        topic = nodl._parsing._v1.parse_topic(element)
        assert topic.publisher
        # Test that bools have default values
        assert not topic.subscriber

        # Test that warning is emitted when both bools are false
        element.set('publisher', 'False')
        with pytest.warns(NoNodeInterfaceWarning):
            topic = nodl._parsing._v1.parse_topic(element)
        assert not topic.publisher

    @pytest.mark.filterwarnings('ignore::nodl.warning.NoNodeInterfaceWarning')
    def test_parse_node(self, valid_nodl: etree._ElementTree):
        nodes: List[etree._Element] = valid_nodl.findall('node')
        node = nodl._parsing._v1.parse_node(nodes[1])
        assert node.actions and node.parameters and node.services and node.topics

        nodes[0].find('topic').attrib.pop('name')
        with pytest.raises(InvalidNoDLException):
            nodl._parsing._v1.parse_node(nodes[0])

    @pytest.mark.filterwarnings('ignore::nodl.warning.NoNodeInterfaceWarning')
    def test_parse_nodes(self, valid_nodl: etree._ElementTree):
        nodes = nodl._parsing._v1.parse_nodes(valid_nodl.getroot())
        assert len(nodes) == 2
        next(valid_nodl.iter('parameter')).attrib.pop('name')
        with pytest.raises(InvalidNoDLException) as excinfo:
            nodl._parsing._v1.parse_nodes(valid_nodl.getroot())
        assert 'parameter is missing required attribute "name"' in excinfo.value.args[0]
