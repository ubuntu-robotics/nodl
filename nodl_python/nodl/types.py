# Copyright 2020 Canonical, Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from enum import Enum, unique
from typing import Any, List, Optional, Union


@unique
class PubSubRole(Enum):
    PUBLISHER = 'publisher'
    SUBSCRIPTION = 'subscription'
    BOTH = 'both'


@unique
class ServerClientRole(Enum):
    SERVER = 'server'
    CLIENT = 'client'
    BOTH = 'both'


class NoDLData:
    """Data structure base class for NoDL objects."""

    def __repr__(self) -> str:
        return str(self.__dict__)

    def __str__(self) -> str:
        return str(self.__dict__)


class NoDLInterface(NoDLData):
    """Abstract base class for NoDL communication interfaces."""

    def __init__(self, *, name: str, value_type: str) -> None:
        self.name = name
        self.type = value_type

    def __eq__(self, other: Any) -> bool:
        return (
            (isinstance(other, type(self)) and isinstance(self, type(other)))
            and self.name == other.name
            and self.type == other.type
        )


class _NoDLInterfaceWithRole(NoDLInterface):
    """ABC providing role to interfaces."""

    def __init__(self, *, name: str, value_type: str, role: Union[PubSubRole, ServerClientRole]):
        super().__init__(name=name, value_type=value_type)
        self.role = role

    def __eq__(self, other: Any):
        return super().__eq__(other) and self.role == other.role


class Action(_NoDLInterfaceWithRole):
    """Data structure for action entries in NoDL."""

    def __init__(self, *, name: str, action_type: str, role: ServerClientRole) -> None:
        super().__init__(name=name, value_type=action_type, role=role)


class Parameter(NoDLInterface):
    """Data structure for parameter entries in NoDL."""

    def __init__(self, *, name: str, parameter_type: str):
        super().__init__(name=name, value_type=parameter_type)


class Service(_NoDLInterfaceWithRole):
    """Data structure for service entries in NoDL."""

    def __init__(self, *, name: str, service_type: str, role: ServerClientRole,) -> None:
        super().__init__(name=name, value_type=service_type, role=role)


class Topic(_NoDLInterfaceWithRole):
    """Data structure for topic entries in NoDL."""

    def __init__(self, *, name: str, message_type: str, role: PubSubRole,) -> None:
        super().__init__(name=name, value_type=message_type, role=role)


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
        topics: Optional[List[Topic]] = None,
    ) -> None:
        self.name = name
        self.executable = executable

        self.actions = {action.name: action for action in actions} if actions else {}
        self.parameters = (
            {parameter.name: parameter for parameter in parameters} if parameters else {}
        )
        self.services = {service.name: service for service in services} if services else {}
        self.topics = {topic.name: topic for topic in topics} if topics else {}
