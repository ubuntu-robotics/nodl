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
import nodl
from nodl import errors
import pytest
from rclpy import qos


def test__parse_qos():
    # Test that qos requires at minimum history or depth
    element = etree.Element('qos')
    with pytest.raises(errors.InvalidQosProfileError):
        nodl._parsing._v1._qos._parse_qos(element)

    # Test that each attribute can be set
    # History
    element.set('history', 'system_default')
    qos_profile = nodl._parsing._v1._qos._parse_qos(element)
    assert qos_profile.history == qos.HistoryPolicy.SYSTEM_DEFAULT
    element.set('history', 'keep_all')
    qos_profile = nodl._parsing._v1._qos._parse_qos(element)
    assert qos_profile.history == qos.HistoryPolicy.KEEP_ALL

    # Reliability
    element.set('reliability', 'system_default')
    qos_profile = nodl._parsing._v1._qos._parse_qos(element)
    assert qos_profile.reliability == qos.ReliabilityPolicy.SYSTEM_DEFAULT
    element.set('reliability', 'best_effort')
    qos_profile = nodl._parsing._v1._qos._parse_qos(element)
    assert qos_profile.reliability == qos.ReliabilityPolicy.BEST_EFFORT

    # Durability
    element.set('durability', 'system_default')
    qos_profile = nodl._parsing._v1._qos._parse_qos(element)
    assert qos_profile.durability == qos.DurabilityPolicy.SYSTEM_DEFAULT
    element.set('durability', 'transient_local')
    qos_profile = nodl._parsing._v1._qos._parse_qos(element)
    assert qos_profile.durability == qos.DurabilityPolicy.TRANSIENT_LOCAL

    # Lifespan
    element.set('lifespan', '451')
    qos_profile = nodl._parsing._v1._qos._parse_qos(element)
    assert qos_profile.lifespan.nanoseconds == 451

    # Liveliness
    element.set('liveliness', 'system_default')
    qos_profile = nodl._parsing._v1._qos._parse_qos(element)
    assert qos_profile.liveliness == qos.LivelinessPolicy.SYSTEM_DEFAULT
    element.set('liveliness', 'manual_by_node')
    qos_profile = nodl._parsing._v1._qos._parse_qos(element)
    assert qos_profile.liveliness == qos.LivelinessPolicy.MANUAL_BY_NODE

    # Liveliness Lease Duration
    element.set('liveliness_lease_duration', '451')
    qos_profile = nodl._parsing._v1._qos._parse_qos(element)
    assert qos_profile.liveliness_lease_duration.nanoseconds == 451

    # Avoid ROS namespace conventions
    element.set('avoid_ros_namespace_conventions', 'True')
    qos_profile = nodl._parsing._v1._qos._parse_qos(element)
    assert qos_profile.avoid_ros_namespace_conventions
    element.set('avoid_ros_namespace_conventions', 'False')
    qos_profile = nodl._parsing._v1._qos._parse_qos(element)
    assert not qos_profile.avoid_ros_namespace_conventions

    # Test that parser errors on out of enum values
    element.set('history', 'foobar')
    with pytest.raises(errors.InvalidQOSAttributeValueError):
        nodl._parsing._v1._qos._parse_qos(element)
    element.set('history', 'system_default')

    element.set('reliability', 'foobar')
    with pytest.raises(errors.InvalidQOSAttributeValueError):
        nodl._parsing._v1._qos._parse_qos(element)
    element.set('reliability', 'system_default')

    element.set('durability', 'foobar')
    with pytest.raises(errors.InvalidQOSAttributeValueError):
        nodl._parsing._v1._qos._parse_qos(element)
    element.set('durability', 'system_default')

    element.set('liveliness', 'foobar')
    with pytest.raises(errors.InvalidQOSAttributeValueError):
        nodl._parsing._v1._qos._parse_qos(element)
    element.set('liveliness', 'system_default')
