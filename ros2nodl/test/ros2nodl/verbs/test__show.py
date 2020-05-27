# Copyright (C) 2020 Canonical Ltd.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License Version 3 as published by
# the Free Software Foundation.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
