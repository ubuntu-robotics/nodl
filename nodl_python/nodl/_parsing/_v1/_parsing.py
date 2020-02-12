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
import warnings

from lxml import etree
from nodl._parsing._qos import parse_qos
from nodl._util import str_to_bool
from nodl.exception import InvalidNoDLException
from nodl.types import Action, Node, Parameter, Service, Topic
from nodl.warning import NoNodeInterfaceWarning


def parse_action(element: etree._Element) -> Action:
    """Parse a NoDL action from an xml element."""
    # ETree.Element contains a `get()` feature that can be used to avoid
    # a potential dict creation from accessing `element.attrib`. We don't use
    # this because we want a KeyError if the required fields aren't there.
    attribs = element.attrib
    name = attribs['name']
    action_type = attribs['type']

    server = str_to_bool(attribs.get('server', 'False'))
    client = str_to_bool(attribs.get('client', 'False'))
    if not (server or client):
        warnings.warn(
            f'{element.base}:{element.sourceline}: {name} is neither server or client',
            NoNodeInterfaceWarning,
        )

    policy = element.find('qos')

    return Action(
        name=name, action_type=action_type, server=server, client=client, qos=parse_qos(policy)
    )


def parse_parameter(element: etree._Element) -> Parameter:
    """Parse a NoDL parameter from an xml element."""
    return Parameter(name=element.attrib['name'], parameter_type=element.attrib['type'])


def parse_service(element: etree._Element) -> Service:
    """Parse a NoDL service from an xml element."""
    attribs = element.attrib
    name = attribs['name']
    service_type = attribs['type']

    server = str_to_bool(attribs.get('server', 'False'))
    client = str_to_bool(attribs.get('client', 'False'))

    if not (server or client):
        warnings.warn(
            f'{element.base}:{element.sourceline}: {name} is neither server or client',
            NoNodeInterfaceWarning,
        )

    policy = element.find('qos')

    return Service(
        name=name, service_type=service_type, server=server, client=client, qos=parse_qos(policy),
    )


def parse_topic(element: etree._Element) -> Topic:
    """Parse a NoDL topic from an xml element."""
    attribs = element.attrib
    name = attribs['name']
    message_type = attribs['type']

    publisher = str_to_bool(attribs.get('publisher', 'False'))
    subscriber = str_to_bool(attribs.get('subscriber', 'False'))
    if not (publisher or subscriber):
        warnings.warn(
            f'{element.base}:{element.sourceline}: {name} is neither publisher or subscriber',
            NoNodeInterfaceWarning,
        )

    policy = element.find('qos')

    return Topic(
        name=name,
        message_type=message_type,
        publisher=publisher,
        subscriber=subscriber,
        qos=parse_qos(policy),
    )


def parse_nodes(interface) -> List[Node]:
    """Parse the nodes contained in an interface element and return a list."""
    node_elements = [child for child in interface if child.tag == 'node']
    return [parse_node(node) for node in node_elements]


def parse_node(node: etree._Element) -> Node:
    """Parse a NoDL node and all the elements it contains from an xml element."""
    name = node.attrib['name']

    actions = []
    parameters = []
    services = []
    topics = []

    for child in node:
        try:
            if child.tag == 'action':
                actions.append(parse_action(child))
            if child.tag == 'parameter':
                parameters.append(parse_parameter(child))
            if child.tag == 'service':
                services.append(parse_service(child))
            if child.tag == 'topic':
                topics.append(parse_topic(child))
        except KeyError as excinfo:
            raise InvalidNoDLException(
                f'{child.tag} is missing required attribute "{excinfo.args[0]}"', child
            ) from excinfo

    return Node(
        name=name, actions=actions, parameters=parameters, services=services, topics=topics
    )
