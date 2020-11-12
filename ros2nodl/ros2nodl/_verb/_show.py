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
import pprint
import shutil
import sys

import nodl
from ros2cli.verb import VerbExtension
from ros2pkg.api import package_name_completer, PackageNotFoundError
from ros2run.api import ExecutableNameCompleter


class _ShowVerb(VerbExtension):
    """Show NoDL data."""

    def add_arguments(self, parser: argparse.ArgumentParser, cli_name: None = None):
        # Ignoring type because of https://github.com/python/typeshed/issues/1878
        parser.add_argument(  # type: ignore
            'package_name', help='Name of the package to show.'
        ).completer = package_name_completer

        # Ignoring type because of https://github.com/python/typeshed/issues/1878
        parser.add_argument(  # type: ignore
            'executables',
            nargs='*',
            default=[],
            metavar='executable',
            help='Specific Executable to display.',
        ).completer = ExecutableNameCompleter(package_name_key='package_name')

    def main(self, args: argparse.Namespace) -> int:
        package = args.package_name

        nodes_to_show = []

        if args.executables:
            nodes_to_show, missing = nodl._index._get_nodes_by_executables(
                package_name=package, executable_names=args.executables
            )
            for name in missing:
                print(
                    nodl.errors.ExecutableNotFoundError(
                        package_name=package, executable_name=name
                    ),
                    file=sys.stderr,
                )
        else:
            try:
                nodes_to_show = nodl._index._get_nodes_from_package(package_name=package)
            except (PackageNotFoundError, nodl.errors.NoDLError) as e:
                print(e, file=sys.stderr)
                return 1

        for node in nodes_to_show:
            pprint.pprint(node, width=shutil.get_terminal_size()[0])
        return 0
