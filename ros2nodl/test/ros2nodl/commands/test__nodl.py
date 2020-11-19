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

import pytest
import ros2nodl._command._nodl


@pytest.fixture
def command():
    return ros2nodl._command._nodl._NoDLCommand()


def test_add_arguments_sets_subparser(mocker, command):
    mocker.patch('ros2nodl._command._nodl.add_subparsers_on_demand')
    parser = mocker.MagicMock(spec=argparse.ArgumentParser)

    command.add_arguments(parser, '')
    assert command._subparser == parser


def test_main(mocker, command):
    parser = mocker.MagicMock()
    args = mocker.MagicMock()

    # Test returns extension.main(args=args) when a verb is provided
    assert command.main(parser=parser, args=args) == args._verb.main(args=args)

    # Test prints help when no verb specified
    del args._verb
    command._subparser = mocker.MagicMock()
    assert command.main(parser=parser, args=args) == 0

    command._subparser.print_help.assert_called_once()
