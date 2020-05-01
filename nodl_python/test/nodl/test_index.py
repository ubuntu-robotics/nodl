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


import nodl.errors
import nodl.index
import pytest


@pytest.fixture
def tmp_share(tmp_path):
    for fname in ['a.nodl.xml', 'anodl.xml', 'b.nodl', 'bar.xml']:
        (tmp_path / fname).touch()
    (tmp_path / 'no_nodl').mkdir()
    (tmp_path / 'no_nodl/baz.xml').touch()
    (tmp_path / 'has_nodl').mkdir()
    (tmp_path / 'has_nodl/b.nodl.xml').touch()

    return tmp_path


def test_get_nodl_xml_files_in_path(tmp_share):
    assert all(
        fname in nodl.index.get_nodl_xml_files_in_path(path=tmp_share)
        for fname in [tmp_share / 'a.nodl.xml', tmp_share / 'has_nodl/b.nodl.xml']
    )


def test_get_nodl_files_from_package_share(mocker, tmp_share):
    # Test gets all files recursively
    mock = mocker.patch('nodl.index.get_package_share_directory', return_value=tmp_share)
    assert all(
        fname in nodl.index.get_nodl_files_from_package_share(package_name='foo')
        for fname in [tmp_share / 'a.nodl.xml', tmp_share / 'has_nodl/b.nodl.xml']
    )

    mock.return_value = tmp_share / 'no_nodl'
    with pytest.raises(nodl.errors.NoNoDLFilesError):
        nodl.index.get_nodl_files_from_package_share(package_name='foo')


def test_get_nodes_from_package(mocker):
    mock_package = mocker.patch('nodl.index.get_nodl_files_from_package_share')
    mock_parse = mocker.patch('nodl.index.parse_multiple')

    res = nodl.index.get_nodes_from_package(package_name='foo')
    mock_package.assert_called_with(package_name='foo')
    assert res == mock_parse.return_value
