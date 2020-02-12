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

from typing import Optional

from lxml import etree
from nodl._util import get_bool_attribute
from nodl.exception import InvalidNoDLException
from rclpy import qos
from rclpy.duration import Duration


def parse_qos(element: Optional[etree._Element]) -> qos.QoSProfile:
    """Populate a QoS Profile from a qos NoDL element."""
    profile: qos.QoSProfile = qos.QoSProfile(
        **qos.QoSProfile._QoSProfile__qos_profile_default_dict
    )

    if element is not None:
        try:
            if element.get('history'):
                profile.history = qos.HistoryPolicy.get_from_short_key(element.get('history'))
            if element.get('reliability'):
                profile.reliability = qos.ReliabilityPolicy.get_from_short_key(
                    element.get('reliability')
                )
            if element.get('durability'):
                profile.durability = qos.DurabilityPolicy.get_from_short_key(
                    element.get('durability')
                )
            if element.get('lifespan'):
                profile.lifespan = Duration(nanoseconds=float(element.get('lifespan')))
            if element.get('liveliness'):
                profile.liveliness = qos.LivelinessPolicy.get_from_short_key(
                    element.get('liveliness')
                )
            if element.get('liveliness_lease_duration'):
                profile.liveliness_lease_duration = Duration(
                    nanoseconds=float(
                        element.get('liveliness_lease_duration', profile.liveliness_lease_duration)
                    )
                )
            if element.get('avoid_ros_namespace_conventions'):
                profile.avoid_ros_namespace_conventions = get_bool_attribute(
                    element, 'avoid_ros_namespace_conventions'
                )
        except KeyError as excinfo:
            raise InvalidNoDLException(
                f"Couldn't parse QoS, {excinfo.args[0]} is not a valid policy", element
            ) from excinfo

    return profile
