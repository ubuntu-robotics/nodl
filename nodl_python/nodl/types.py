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

from typing import Any, Dict, List, Optional

from nodl._util import qos_to_dict
import rclpy.qos


class NoDLData:
    """Data structure base class for NoDL objects."""

    def __repr__(self) -> str:
        return str(self._as_dict)

    def __str__(self) -> str:
        return str(self._as_dict)

    @property
    def _as_dict(self) -> Dict:
        self_dict = self.__dict__.copy()
        for key in self_dict.keys():
            if 'qos_profile' in key:
                self_dict[key] = qos_to_dict(self_dict[key])
        return self_dict


class NoDLInterface(NoDLData):
    """Abstract base class for NoDL communication interfaces."""

    def __init__(self, *, name: str, value_type: str) -> None:
        self.name = name
        self.type = value_type

    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, type(self)) or isinstance(self, type(other))
        ) and self.__dict__ == other.__dict__


class Action(NoDLInterface):
    """Data structure for action entries in NoDL."""

    def __init__(
        self,
        *,
        name: str,
        action_type: str,
        server: bool = False,
        client: bool = False,
        goal_service_qos_profile: rclpy.qos.QoSProfile = rclpy.qos.qos_profile_services_default,
        result_service_qos_profile: rclpy.qos.QoSProfile = rclpy.qos.qos_profile_services_default,
        cancel_service_qos_profile: rclpy.qos.QoSProfile = rclpy.qos.qos_profile_services_default,
        feedback_qos_profile: rclpy.qos.QoSProfile = rclpy.qos.QoSProfile(depth=10),
        status_qos_profile: rclpy.qos.QoSProfile = rclpy.qos.qos_profile_action_status_default
    ) -> None:
        super().__init__(name=name, value_type=action_type)
        self.server = server
        self.client = client

        self.goal_service_qos_profile = goal_service_qos_profile
        self.result_service_qos_profile = result_service_qos_profile
        self.cancel_service_qos_profile = cancel_service_qos_profile
        self.feedback_qos_profile = feedback_qos_profile
        self.status_qos_profile = status_qos_profile


class Parameter(NoDLInterface):
    """Data structure for parameter entries in NoDL."""

    def __init__(self, *, name: str, parameter_type: str) -> None:
        super().__init__(name=name, value_type=parameter_type)


class Service(NoDLInterface):
    """Data structure for service entries in NoDL."""

    def __init__(
        self,
        *,
        name: str,
        service_type: str,
        server: bool = False,
        client: bool = False,
        qos_profile: rclpy.qos.QoSProfile = rclpy.qos.qos_profile_services_default
    ) -> None:
        super().__init__(name=name, value_type=service_type)
        self.server = server
        self.client = client

        self.qos_profile = qos_profile


class Topic(NoDLInterface):
    """Data structure for topic entries in NoDL."""

    def __init__(
        self,
        *,
        name: str,
        message_type: str,
        qos_profile: rclpy.qos.QoSProfile,
        publisher: bool = False,
        subscription: bool = False,
    ) -> None:
        super().__init__(name=name, value_type=message_type)
        self.publisher = publisher
        self.subscription = subscription

        self.qos_profile = qos_profile


class Node(NoDLData):
    """Data structure containing all interfaces a node exposes."""

    def __init__(
        self,
        *,
        name: str,
        executable: str,
        actions: Optional[List[Action]] = None,
        parameters: Optional[List[Parameter]] = None,
        services: Optional[List[Service]] = None,
        topics: Optional[List[Topic]] = None
    ) -> None:
        self.name = name
        self.executable = executable

        self.actions = {action.name: action for action in actions} if actions else {}
        self.parameters = (
            {parameter.name: parameter for parameter in parameters} if parameters else {}
        )
        self.services = {service.name: service for service in services} if services else {}
        self.topics = {topic.name: topic for topic in topics} if topics else {}

    @property
    def _as_dict(self):
        return {
            'name': self.name,
            'executable': self.executable,
            'actions': [action._as_dict for action in self.actions.values()],
            'parameters': [parameter._as_dict for parameter in self.parameters.values()],
            'services': [service._as_dict for service in self.services.values()],
            'topics': [topic._as_dict for topic in self.topics.values()],
        }
