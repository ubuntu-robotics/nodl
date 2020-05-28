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
import pprint
import shutil
import sys

from argcomplete.completers import FilesCompleter
import nodl
from nodl._index import _FILE_EXTENSION
from ros2cli.verb import VerbExtension


class _ValidateVerb(VerbExtension):
    """Validate NoDL XML documents."""

    def add_arguments(self, parser: argparse.ArgumentParser, cli_name: None = None):
        # Ignoring type because of https://github.com/python/typeshed/issues/1878
        parser.add_argument(  # type: ignore
            'files',
            nargs='*',
            default=[],
            metavar='file',
            help=f'Specific {_FILE_EXTENSION} file(s) to validate.',
        ).completer = FilesCompleter(allowednames=[_FILE_EXTENSION], directories=False)

        parser.add_argument('-p', '--print', action='store_true', help='Print parsed output.')

    def main(self, args: argparse.Namespace) -> int:
        if args.files:
            paths = [Path(filename) for filename in args.files]
        else:
            paths = list(Path.cwd().glob('*' + _FILE_EXTENSION))
        if not paths:
            print('No files to validate', file=sys.stderr)
            return 1

        for path in paths:
            if not path.is_file():
                print(f'{path.name} is not a file')
                return 1

            print(f'Validating {path}...')
            try:
                nodes = nodl.parse(path=path)
            except nodl.errors.NoDLError as e:
                print(f'Failed to parse {path}', file=sys.stderr)
                print(e, file=sys.stderr)
                return 1
            print('  Success')
            if args.print:
                for node in nodes:
                    pprint.pprint(node._as_dict, width=shutil.get_terminal_size()[0])

        print('All files validated')
        return 0
