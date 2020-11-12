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

import argparse
from pathlib import Path
from typing import List

from ament_index_python import PackageNotFoundError
import nodl
import pytest
from ros2nodl._verb import _show


@pytest.fixture
def verb() -> _show._ShowVerb:
    return _show._ShowVerb()


@pytest.fixture(scope='session')
def nodl_fixture() -> List[nodl.types.Node]:
    return nodl.parse(Path(__file__).parents[1] / 'test.nodl.xml')


@pytest.fixture
def mock_nodl(mocker, nodl_fixture):
    return mocker.patch(
        'ros2nodl._verb._show.nodl._index._get_nodes_from_package', return_value=nodl_fixture
    )


@pytest.fixture
def parser(verb) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    verb.add_arguments(parser, None)
    return parser


def test_parse_can_read_valid_packages(mocker, parser):
    """Test if can read valid package names per REP 144."""
    valid_names = ['foo', 'bar_', 'baz_', 'fizz_buzz']

    for name in valid_names:
        assert parser.parse_args([name]).package_name == name


def test_errors_on_invalid_package(mock_nodl, parser, verb):
    mock_nodl.side_effect = nodl.errors.NoNoDLFilesError('foo')

    args = parser.parse_args(['foo'])
    assert verb.main(args=args)

    mock_nodl.side_effect = PackageNotFoundError()
    assert verb.main(args=args)


def test_accepts_valid_package(mock_nodl, parser, verb):
    args = parser.parse_args(['foo'])
    assert not verb.main(args=args)


def test_accepts_valid_file(mock_nodl, parser, verb):
    args = parser.parse_args(['foo', 'first'])
    assert not verb.main(args=args)


def test_continue_on_missing_file(mocker, mock_nodl, parser, verb):
    args = parser.parse_args(['foo', 'bar'])
    assert not verb.main(args=args)


def test_show_parsed_fail_on_duplicate(mocker, mock_nodl, parser, verb):
    mock_nodl.side_effect = nodl.errors.DuplicateNodeError(mocker.MagicMock())
    args = parser.parse_args(['foo'])
    assert verb.main(args=args)
