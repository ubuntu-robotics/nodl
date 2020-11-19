# Copyright 2020 Canonical, Ltd.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import List

from lxml import etree
from nodl import errors
from nodl._parsing._schemas import v1_schema
from nodl.types import (
    Action,
    Node,
    Parameter,
    PubSubRole,
    ServerClientRole,
    Service,
    Topic,
)


def _parse_action(element: etree._Element) -> Action:
    """Parse a NoDL action from an xml element."""
    name = element.get('name')
    action_type = element.get('type')

    role = ServerClientRole(element.get('role'))

    return Action(name=name, action_type=action_type, role=role)


def _parse_parameter(element: etree._Element) -> Parameter:
    """Parse a NoDL parameter from an xml element."""
    return Parameter(name=element.get('name'), parameter_type=element.get('type'))


def _parse_service(element: etree._Element) -> Service:
    """Parse a NoDL service from an xml element."""
    name = element.get('name')
    service_type = element.get('type')

    role = ServerClientRole(element.get('role'))

    return Service(name=name, service_type=service_type, role=role)


def _parse_topic(element: etree._Element) -> Topic:
    """Parse a NoDL topic from an xml element."""
    name = element.get('name')
    message_type = element.get('type')

    role = PubSubRole(element.get('role'))

    return Topic(name=name, message_type=message_type, role=role)


def _parse_nodes(interface: etree._Element) -> List[Node]:
    """Parse the nodes contained in an interface element and return a list."""
    node_elements = [child for child in interface if child.tag == 'node']
    return [_parse_node(node) for node in node_elements]


def _parse_node(node: etree._Element) -> Node:
    """Parse a NoDL node and all the elements it contains from an xml element."""
    name = node.attrib['name']
    executable = node.attrib['executable']

    actions = []
    parameters = []
    services = []
    topics = []

    for child in node:
        if child.tag == 'action':
            actions.append(_parse_action(child))
        elif child.tag == 'parameter':
            parameters.append(_parse_parameter(child))
        elif child.tag == 'service':
            services.append(_parse_service(child))
        elif child.tag == 'topic':
            topics.append(_parse_topic(child))
        else:
            raise errors.InvalidNodeChildError(child)
    return Node(
        name=name,
        executable=executable,
        actions=actions,
        parameters=parameters,
        services=services,
        topics=topics,
    )


def parse(interface: etree._Element) -> List[Node]:
    """"""
    try:
        v1_schema().assertValid(interface)
    except etree.DocumentInvalid as e:
        raise errors.InvalidNoDLDocumentError(e) from e
    return _parse_nodes(interface)
