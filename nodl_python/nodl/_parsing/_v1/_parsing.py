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

from typing import List

from lxml import etree
from nodl._parsing._qos import parse_qos
from nodl._parsing._schemas import get_schema
from nodl._util import get_bool_attribute
from nodl.exception import InvalidNoDLError, NoNodeInterfaceError
from nodl.types import Action, Node, Parameter, Service, Topic


_SCHEMA = get_schema('v1.xsd')


def _parse_action(element: etree._Element) -> Action:
    """Parse a NoDL action from an xml element."""
    name = element.get('name')
    action_type = element.get('type')

    server = get_bool_attribute(element, 'server')
    client = get_bool_attribute(element, 'client')
    if not (server or client):
        raise NoNodeInterfaceError(f'Action <{name}> is neither server nor client.', element)

    policy = parse_qos(element.find('qos'))

    return Action(name=name, action_type=action_type, server=server, client=client, qos=policy)


def _parse_parameter(element: etree._Element) -> Parameter:
    """Parse a NoDL parameter from an xml element."""
    return Parameter(name=element.get('name'), parameter_type=element.get('type'))


def _parse_service(element: etree._Element) -> Service:
    """Parse a NoDL service from an xml element."""
    name = element.get('name')
    service_type = element.get('type')

    server = get_bool_attribute(element, 'server')
    client = get_bool_attribute(element, 'client')
    if not (server or client):
        raise NoNodeInterfaceError(f'Service <{name}> is neither server nor client.', element)

    policy = parse_qos(element.find('qos'))

    return Service(name=name, service_type=service_type, server=server, client=client, qos=policy,)


def _parse_topic(element: etree._Element) -> Topic:
    """Parse a NoDL topic from an xml element."""
    name = element.get('name')
    message_type = element.get('type')

    publisher = get_bool_attribute(element, 'publisher')
    subscription = get_bool_attribute(element, 'subscription')
    if not (publisher or subscription):
        raise NoNodeInterfaceError(
            f'Topic <{name}> is neither publisher nor subscription.', element
        )

    policy = parse_qos(element.find('qos'))

    return Topic(
        name=name,
        message_type=message_type,
        publisher=publisher,
        subscription=subscription,
        qos=policy,
    )


def _parse_nodes(interface: etree._Element) -> List[Node]:
    """Parse the nodes contained in an interface element and return a list."""
    node_elements = [child for child in interface if child.tag == 'node']
    return [_parse_node(node) for node in node_elements]


def _parse_node(node: etree._Element) -> Node:
    """Parse a NoDL node and all the elements it contains from an xml element."""
    name = node.attrib['name']

    actions = []
    parameters = []
    services = []
    topics = []

    for child in node:
        if child.tag == 'action':
            actions.append(_parse_action(child))
        if child.tag == 'parameter':
            parameters.append(_parse_parameter(child))
        if child.tag == 'service':
            services.append(_parse_service(child))
        if child.tag == 'topic':
            topics.append(_parse_topic(child))
    return Node(
        name=name, actions=actions, parameters=parameters, services=services, topics=topics
    )


def _validate_and_parse(interface: etree._Element) -> List[Node]:
    """"""
    try:
        _SCHEMA.assertValid(interface)
    except etree.DocumentInvalid as e:
        raise InvalidNoDLError(e.error_log[0].message, e) from e
    return _parse_nodes(interface)
