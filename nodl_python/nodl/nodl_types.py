# Copyright 2020 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License version 3, as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranties of MERCHANTABILITY, SATISFACTORY QUALITY, or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.


from typing import List, Optional

from rclpy.qos import QoSPresetProfiles, QoSProfile


class Action:
    """Data structure for action entries in NoDL."""

    def __init__(
        self,
        *,
        name: str,
        action_type: str,
        server: bool = False,
        client: bool = False,
        qos: QoSProfile = QoSPresetProfiles.ACTION_STATUS_DEFAULT
    ) -> None:
        self.name = name
        self.action_type = action_type
        self.server = server
        self.client = client

        self.qos = qos


class Parameter:
    """Data structure for parameter entries in NoDL."""

    def __init__(self, *, name: str, parameter_type: str) -> None:
        self.name = name
        self.parameter_type = parameter_type


class Service:
    """Data structure for service entries in NoDL."""

    def __init__(
        self,
        *,
        name: str,
        service_type: str,
        server: bool = False,
        client: bool = False,
        qos: QoSProfile = QoSPresetProfiles.SERVICES_DEFAULT
    ) -> None:
        self.name = name
        self.service_type = service_type
        self.server = server
        self.client = client

        self.qos = qos


class Topic:
    """Data structure for topic entries in NoDL."""

    def __init__(
        self,
        *,
        name: str,
        message_type: str,
        publisher: bool = False,
        subscriber: bool = False,
        qos: QoSProfile = QoSPresetProfiles.SYSTEM_DEFAULT
    ) -> None:
        self.name = name
        self.message_type = message_type
        self.publisher = publisher
        self.subscriber = subscriber

        self.qos = qos


class Node:
    """Data structure containing all interfaces a node exposes."""

    def __init__(
        self,
        *,
        name: str,
        actions: Optional[List[Action]] = None,
        parameters: Optional[List[Parameter]] = None,
        services: Optional[List[Service]] = None,
        topics: Optional[List[Topic]] = None
    ) -> None:
        self.name = name

        self.actions = actions if actions else []
        self.parameters = parameters if parameters else []
        self.services = services if services else []
        self.topics = topics if topics else []
