from pathlib import Path

from lxml.builder import E
import lxml.etree as etree
from nodl.api import errors
import nodl.api._parsing
import nodl.api._parsing._v1._parsing
import nodl.api.types
import pytest


@pytest.fixture()
def valid_nodl() -> etree._ElementTree:
    return etree.parse(str(Path('test/nodl.xml')))


def test_parse(valid_nodl):
    # Assert a minimal example passes validation
    element = E.interface(
        E.node(E.action(E.qos(depth='10'), name='bar', type='baz', server='true'), name='foo'),
        version='1',
    )
    assert nodl.api._parsing._v1.parse(element)

    # Assert example nodl passes validation
    assert nodl.api._parsing._v1.parse(valid_nodl.getroot())

    # Assert empty interface does not pass
    element = E.interface(version='1')
    with pytest.raises(errors.InvalidNoDLDocumentError):
        nodl.api._parsing._v1.parse(element)


def test__parse_action():
    element = E.action(E.qos(depth='10'), name='foo', type='bar', server='true')

    # Test that actions get parsed
    action = nodl.api._parsing._v1._parsing._parse_action(element)
    assert type(action) is nodl.api.types.Action
    assert action.server
    # Test that bools have default values
    assert not action.client

    # Test that warning is emitted when both bools are false
    element.attrib['server'] = 'False'
    with pytest.raises(errors.AmbiguousActionInterfaceError):
        nodl.api._parsing._v1._parsing._parse_action(element)


def test__parse_parameter():
    element = E.parameter()

    # Test that parse is successful
    element.set('name', 'foo')
    element.set('type', 'bar')
    assert isinstance(
        nodl.api._parsing._v1._parsing._parse_parameter(element), nodl.api.types.Parameter
    )
    assert element.get('name') == 'foo'
    assert element.get('type') == 'bar'


def test__parse_service():
    # Test that parse fails when missing name/type
    element = E.service(E.qos(depth='10'), name='foo', type='bar', server='true')

    # Test that services get parsed
    service = nodl.api._parsing._v1._parsing._parse_service(element)
    assert type(service) is nodl.api.types.Service
    assert service.server
    # Test that bools have default values
    assert not service.client

    # Test that warning is emitted when both bools are false
    element.attrib['server'] = 'False'
    with pytest.raises(errors.AmbiguousServiceInterfaceError):
        nodl.api._parsing._v1._parsing._parse_service(element)


def test__parse_topic():
    # Test that parse fails when missing name/type
    element = E.topic(E.qos(depth='10'), name='foo', type='bar', publisher='true')

    topic = nodl.api._parsing._v1._parsing._parse_topic(element)
    assert topic.publisher
    # Test that bools have default values
    assert not topic.subscription

    # Test that warning is emitted when both bools are false
    element.set('publisher', 'false')
    with pytest.raises(errors.AmbiguousTopicInterfaceError):
        nodl.api._parsing._v1._parsing._parse_topic(element)


def test__parse_node(valid_nodl: etree._ElementTree):
    nodes = valid_nodl.findall('node')
    node = nodl.api._parsing._v1._parsing._parse_node(nodes[1])
    assert node.actions and node.parameters and node.services and node.topics


def test__parse_nodes(valid_nodl: etree._ElementTree):
    nodes = nodl.api._parsing._v1._parsing._parse_nodes(valid_nodl.getroot())
    assert len(nodes) == 2
