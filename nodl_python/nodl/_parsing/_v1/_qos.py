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
from nodl import errors
from nodl._util import get_bool_attribute
from rclpy import qos
from rclpy.duration import Duration


def _parse_qos(element: etree._Element) -> qos.QoSProfile:
    """Populate a QoS Profile from a qos NoDL element."""
    kwargs = {}

    if element.get('history'):
        try:
            kwargs['history'] = qos.HistoryPolicy.get_from_short_key(element.get('history'))
        except KeyError:
            raise errors.InvalidQOSAttributeValueError('history', element)

    if element.get('reliability'):
        try:
            kwargs['reliability'] = qos.ReliabilityPolicy.get_from_short_key(
                element.get('reliability')
            )
        except KeyError:
            raise errors.InvalidQOSAttributeValueError('reliability', element)

    if element.get('durability'):
        try:
            kwargs['durability'] = qos.DurabilityPolicy.get_from_short_key(
                element.get('durability', element)
            )
        except KeyError:
            raise errors.InvalidQOSAttributeValueError('durability', element)

    if element.get('depth'):
        kwargs['depth'] = int(element.get('depth'))

    if element.get('lifespan'):
        kwargs['lifespan'] = Duration(nanoseconds=float(element.get('lifespan')))

    if element.get('deadline'):
        kwargs['deadline'] = Duration(nanoseconds=float(element.get('lifespan')))

    if element.get('liveliness'):
        try:
            kwargs['liveliness'] = qos.LivelinessPolicy.get_from_short_key(
                element.get('liveliness')
            )
        except KeyError:
            raise errors.InvalidQOSAttributeValueError('liveliness', element)

    if element.get('liveliness_lease_duration'):
        kwargs['liveliness_lease_duration'] = Duration(
            nanoseconds=float(
                element.get('liveliness_lease_duration')
            )
        )
    if element.get('avoid_ros_namespace_conventions'):
        kwargs['avoid_ros_namespace_conventions'] = get_bool_attribute(
            element, 'avoid_ros_namespace_conventions'
        )
    try:
        return qos.QoSProfile(**kwargs)
    except qos.InvalidQoSProfileException as e:
        raise errors.InvalidQosProfileError(e, element) from e
