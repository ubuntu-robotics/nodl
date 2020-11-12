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

import nodl._index
import nodl.errors
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


def test__get_nodl_files_from_package_share(mocker, tmp_share):
    # Test gets all files recursively
    mock = mocker.patch('nodl._index.get_package_share_directory', return_value=tmp_share)
    assert (tmp_share / 'a.nodl.xml') in nodl._index._get_nodl_files_from_package_share(
        package_name='foo'
    )

    mock.return_value = tmp_share / 'no_nodl'
    with pytest.raises(nodl.errors.NoNoDLFilesError):
        nodl._index._get_nodl_files_from_package_share(package_name='foo')


def test__get_nodes_from_package(mocker):
    mock_package = mocker.patch('nodl._index._get_nodl_files_from_package_share')
    mock_parse = mocker.patch('nodl._index._parse_multiple')

    res = nodl._index._get_nodes_from_package(package_name='foo')
    mock_package.assert_called_with(package_name='foo')
    assert res == mock_parse.return_value


@pytest.fixture
def test_nodes(mocker) -> List[nodl.types.Node]:
    return [
        mocker.MagicMock(spec=nodl.types.Node, executable=executable)
        for executable in ['foo', 'bar', 'baz']
    ]


def test_get_node_by_executable(mocker, test_nodes):
    mocker.patch('nodl._index._get_nodes_from_package', return_value=test_nodes)

    assert (
        nodl._index.get_node_by_executable(package_name='', executable_name='bar').executable
        == 'bar'
    )

    with pytest.raises(nodl.errors.ExecutableNotFoundError):
        nodl._index.get_node_by_executable(package_name='', executable_name='fizz')


def test_get_nodes_by_executables(mocker, test_nodes):
    mocker.patch('nodl._index._get_nodes_from_package', autospec=True, return_value=test_nodes)

    nodes, missing = nodl._index._get_nodes_by_executables(
        package_name='', executable_names=['foo', 'bar', 'fizz']
    )
    nodes = {node.executable: node for node in nodes}

    assert 'foo' in nodes and 'bar' in nodes and len(nodes.keys()) == 2
    assert missing[0] == 'fizz'
