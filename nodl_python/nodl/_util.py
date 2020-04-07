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

import distutils.util
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from lxml import etree
    from rclpy.qos import QoSProfile


def get_bool_attribute(element: 'etree._Element', attribute: str) -> bool:
    """Access attribute and bool conversion."""
    boolean_string = element.get(attribute, 'False')
    return bool(distutils.util.strtobool(boolean_string))


def qos_to_dict(qos: 'QoSProfile') -> Dict[str, str]:
    return {
            'history': qos.history.short_key,
            'depth': qos.depth,
            'reliability': qos.reliability.short_key,
            'durability': qos.durability.short_key,
            'lifespan': qos.lifespan.nanoseconds,
            'deadline': qos.deadline.nanoseconds,
            'liveliness': qos.liveliness.short_key,
            'liveliness_lease_duration': qos.liveliness_lease_duration.nanoseconds,
            'avoid_ros_namespace_conventions': qos.avoid_ros_namespace_conventions,
    }
