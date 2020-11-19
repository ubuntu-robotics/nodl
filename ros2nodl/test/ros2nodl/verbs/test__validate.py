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
