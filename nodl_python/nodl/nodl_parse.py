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


from pathlib import Path
from typing import List, Optional
import warnings

from lxml import etree
from nodl.nodl_types import Action, Node, Parameter, Service, Topic
from rclpy import qos
from rclpy.duration import Duration


NODL_MAX_SUPPORTED_VERSION: int = 1


def str_to_bool(boolean_string: str) -> bool:
    """Convert xml boolean entries to `bool`."""
    return boolean_string.lower() in ['true', '1']


class InvalidNoDLException(Exception):
    """Exception class representing most errors in parsing the NoDL tree."""

    def __init__(self, message: str, element: Optional[etree._Element] = None) -> None:
        if element is not None:
            super().__init__(f'{element.base}:{element.sourceline}  ' + message)
        else:
            super().__init__(message)


class UnsupportedInterfaceException(InvalidNoDLException):
    """Exception thrown when an interface has a future or invalid version."""

    def __init__(self, element: etree._Element) -> None:
        super().__init__(
            f'{element.base}:{element.sourceline}  Unsupported interface version: '
            f'{element.attrib["version"]} (must be <={NODL_MAX_SUPPORTED_VERSION})'
        )


class NoNodeInterfaceWarning(UserWarning):
    """Warning raised when not marked as either server/client or pub/sub."""

    pass


def parse_element_tree(element_tree: etree._ElementTree) -> etree._Element:
    """Extract an interface element from an ElementTree if present."""
    interface = element_tree.getroot()
    if interface.tag != 'interface':
        interface = next(interface.iter('interface'), None)
        if interface is None:
            raise InvalidNoDLException(f'No interface tag in {element_tree.docinfo.URL}')
    return interface


def parse_nodl_file(path: Path) -> List[Node]:
    """Parse the nodes out of a given NoDL file."""
    full_path = path.resolve()
    element_tree = etree.parse(str(full_path))
    interface = parse_element_tree(element_tree)

    try:
        version = interface.attrib['version']
    except KeyError:
        raise InvalidNoDLException(f'Missing version attribute in "interface".', interface)

    if version == '1':
        return Interface_v1.parse_nodes(interface)
    else:
        raise UnsupportedInterfaceException(interface)


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
                profile.avoid_ros_namespace_conventions = str_to_bool(
                    str(element.get('avoid_ros_namespace_conventions'))
                )
        except KeyError as excinfo:
            raise InvalidNoDLException(
                f'Couldn"t parse QoS, {excinfo.args[0]} is not a valid policy', element
            ) from excinfo

    return profile


class Interface_v1:
    """Parser methods for v1."""

    @classmethod
    def parse_action(cls, element: etree._Element) -> Action:
        """Parse a NoDL action from an xml element."""
        # ETree.Element contains a `get()` feature that can be used to avoid
        # a potential dict creation from accessing `element.attrib`. We don"t use
        # this because we want a KeyError if the required fields aren"t there.
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

    @classmethod
    def parse_parameter(cls, element: etree._Element) -> Parameter:
        """Parse a NoDL parameter from an xml element."""
        return Parameter(name=element.attrib['name'], parameter_type=element.attrib['type'])

    @classmethod
    def parse_service(cls, element: etree._Element) -> Service:
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
            name=name,
            service_type=service_type,
            server=server,
            client=client,
            qos=parse_qos(policy),
        )

    @classmethod
    def parse_topic(cls, element: etree._Element) -> Topic:
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

    @classmethod
    def parse_nodes(cls, interface) -> List[Node]:
        """Parse the nodes contained in an interface element and return a list."""
        node_elements = [child for child in interface if child.tag == 'node']
        return [cls.parse_node(node) for node in node_elements]

    @classmethod
    def parse_node(cls, node: etree._Element) -> Node:
        """Parse a NoDL node and all the elements it contains from an xml element."""
        name = node.attrib['name']

        actions = []
        parameters = []
        services = []
        topics = []

        for child in node:
            try:
                if child.tag == 'action':
                    actions.append(cls.parse_action(child))
                if child.tag == 'parameter':
                    parameters.append(cls.parse_parameter(child))
                if child.tag == 'service':
                    services.append(cls.parse_service(child))
                if child.tag == 'topic':
                    topics.append(cls.parse_topic(child))
            except KeyError as excinfo:
                raise InvalidNoDLException(
                    f'{child.tag} is missing required attribute "{excinfo.args[0]}"', child
                ) from excinfo

        return Node(
            name=name, actions=actions, parameters=parameters, services=services, topics=topics
        )
