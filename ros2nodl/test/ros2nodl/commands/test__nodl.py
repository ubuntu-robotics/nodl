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
