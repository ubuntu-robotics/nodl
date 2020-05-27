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
from typing import Any, List, Optional

from ros2cli.command import add_subparsers_on_demand, CommandExtension


class _NoDLCommand(CommandExtension):
    """Access node interface descriptions exported from packages."""

    def add_arguments(
        self, parser: argparse.ArgumentParser, cli_name: str, *, argv: Optional[List] = None
    ):
        self._subparser = parser
        add_subparsers_on_demand(
            parser=parser,
            cli_name=cli_name,
            dest='_verb',
            group_name='ros2nodl.verb',
            required=False,
            argv=argv,
        )

    def main(self, *, parser: argparse.ArgumentParser, args: Any) -> int:
        if not hasattr(args, '_verb'):
            self._subparser.print_help()
            return 0
        extension = args._verb

        return extension.main(args=args)
