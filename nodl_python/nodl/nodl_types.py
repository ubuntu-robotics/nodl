# Copyright 2020 Canonical, Ltd.
#
# This program is free software: you can redistribute it and/or modify it under the terms of the
# GNU Limited General Public License version 3, as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranties of MERCHANTABILITY, SATISFACTORY QUALITY,
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Limited General Public License for more details.
#
# You should have received a copy of the GNU Limited General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.


from typing import List, Optional

from rclpy.qos import QoSProfile, QoSPresetProfiles


class NoDLAction:
    """Data structure for action entries in NoDL."""

    def __init__(self,
                 *,
                 name: str,
                 msg_type: str,
                 server: bool = False,
                 client: bool = False,
                 qos: QoSProfile = QoSPresetProfiles.ACTION_STATUS_DEFAULT):
        self.name = name
        self.type = msg_type
        self.server = server
        self.client = client

        self.qos = qos


class NoDLParameter:
    def __init__(self,
                 *,
                 name: str,
                 param_type: str):
        self.name = name
        self.type = param_type


class NoDLService:
    """Data structure for service entries in NoDL."""

    def __init__(self,
                 *,
                 name: str,
                 service: str,
                 server: bool = False,
                 client: bool = False,
                 qos: QoSProfile = QoSPresetProfiles.SERVICES_DEFAULT):
        self.name = name
        self.type = service
        self.server = server
        self.client = client

        self.qos = qos


class NoDLTopic:
    """Data structure for topic entries in NoDL."""

    def __init__(self,
                 *,
                 name: str,
                 message: str,
                 server: bool = False,
                 client: bool = False,
                 qos: QoSProfile = QoSPresetProfiles.SYSTEM_DEFAULT):
        self.name = name
        self.type = message
        self.server = server
        self.client = client

        self.qos = qos


class NoDLNode:
    """"""

    def __init__(self, *,
                 name: str,
                 actions: Optional[List[NoDLAction]] = None,
                 parameters: Optional[List[NoDLParameter]] = None,
                 services: Optional[List[NoDLService]] = None,
                 topics: Optional[List[NoDLTopic]] = None):
        self.name = name

        self.actions = actions if actions else []
        self.parameters = parameters if parameters else []
        self.services = services if services else []
        self.topics = topics if topics else []
