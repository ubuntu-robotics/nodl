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


from pathlib import Path

from lxml.builder import E
import lxml.etree as etree
from nodl import errors
import nodl._parsing
import nodl.types
import pytest


def test__parse_element_tree(mocker):
    not_interface = E.notinterface()
    # Test that fails when no interface tag is included
    with pytest.raises(errors.InvalidNoDLDocumentError):
        nodl._parsing._parsing._parse_element_tree(etree.ElementTree(not_interface))

    # Test that fails when no version is specified
    with pytest.raises(errors.InvalidNoDLDocumentError):
        nodl._parsing._parsing._parse_element_tree(E.interface(E.node()))

    # Test that succeeds when interface is top level
    interface = E.interface(E.node(), version='1')
    mocker.patch('nodl._parsing._parsing._parse_interface')
    assert nodl._parsing._parsing._parse_element_tree(etree.ElementTree(interface))


def test_parse_nodl_file_valid(mocker):
    mocker.patch('nodl._parsing._parsing._parse_element_tree')

    # Test if accepts a valid xml file
    assert nodl._parsing._parsing.parse(path=Path('test/nodl/test.nodl.xml')) is not None

    # Test if accepts file name as string
    assert nodl._parsing._parsing.parse(path='test/nodl/test.nodl.xml') is not None

    # Test if accepts file object
    with open('test/nodl/test.nodl.xml', 'rb') as fd:
        assert nodl._parsing._parsing.parse(path=fd) is not None


def test_parse_interface(mocker):
    mocker.patch('nodl._parsing._parsing.parse_v1.parse')

    # Test that unsupported versions aren't accepted
    interface_future_version = E.interface(
        E.node(), version=str(nodl._parsing._parsing.NODL_MAX_SUPPORTED_VERSION + 1)
    )
    with pytest.raises(errors.UnsupportedInterfaceError):
        nodl._parsing._parsing._parse_interface(interface_future_version)

    # Test that all versions <= max version are supported
    interface_versions = [
        E.interface(E.node(), version=str(version))
        for version in range(1, nodl._parsing._parsing.NODL_MAX_SUPPORTED_VERSION + 1)
    ]
    for version, interface in enumerate(interface_versions):
        assert (
            nodl._parsing._parsing._parse_interface(interface) is not None
        ), f'Missing version {version}'
