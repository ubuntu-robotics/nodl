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

import nodl
import pytest

from ros2nodl._verb import _validate


@pytest.fixture
def verb() -> _validate._ValidateVerb:
    return _validate._ValidateVerb()


@pytest.fixture
def parser(verb):
    parser = argparse.ArgumentParser()

    verb.add_arguments(parser)
    return parser


def test_accepts_valid_path(mocker, parser, test_nodl, verb):
    mocker.patch('ros2nodl._verb._validate.nodl.parse')

    args = parser.parse_args([str(test_nodl)])
    assert not verb.main(args=args)


def test_finds_all(mocker, parser, sample_package, verb):
    mocker.patch('ros2nodl._verb._validate.Path.cwd', return_value=sample_package)
    mock = mocker.patch('ros2nodl._verb._validate.nodl.parse')

    args = parser.parse_args([])
    assert not verb.main(args=args)
    assert len(mock.mock_calls) == 2


def test_fails_no_file(mocker, parser, tmp_path, verb):
    mocker.patch('ros2nodl._verb._validate.Path.cwd', return_value=tmp_path)

    args = parser.parse_args([])
    assert verb.main(args=args)


def test_fails_sneaky_dir(mocker, parser, tmp_path, verb):
    sneakydir = tmp_path / 'test.nodl.xml'
    sneakydir.mkdir()

    args = parser.parse_args([str(tmp_path.resolve())])
    assert verb.main(args=args)


def test_validates_valid_file(mocker, parser, test_nodl, verb):
    args = parser.parse_args([str(test_nodl)])

    assert not verb.main(args=args)


def test_fails_invalid_nodl(mocker, parser, test_nodl, verb):
    mocker.patch(
        'ros2nodl._verb._validate.nodl.parse',
        side_effect=nodl.errors.InvalidNoDLDocumentError(mocker.MagicMock()),
    )
    args = parser.parse_args([str(test_nodl)])

    assert verb.main(args=args)


def test_pprints_to_console(mocker, parser, test_nodl, verb):
    print_mock = mocker.patch('ros2nodl._verb._validate.pprint.pprint', autospec=True)

    args = parser.parse_args([str(test_nodl), '-p'])

    verb.main(args=args)
    assert len(print_mock.mock_calls) == 2
