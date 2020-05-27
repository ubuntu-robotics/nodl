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

from pathlib import Path

import pytest


@pytest.fixture
def sample_package(tmp_path) -> Path:
    shortnames = [
        'foo.nodl.xml',
        'bar.nodl.xml',
        'baz.xml.nodl',
        'fizz.nodl',
        'buzz.xml',
        'jonodl.xml',
    ]
    names = [(tmp_path / name) for name in shortnames]
    for name in names:
        name.touch()
    return tmp_path


@pytest.fixture
def test_nodl():
    return Path(__file__).parents[1] / 'test.nodl.xml'
