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

from lxml import etree
from nodl._util import get_bool_attribute


def test_get_bool_attribute_except(mocker):
    foo = etree.Element('foo', {'bar': 'true'})
    assert get_bool_attribute(foo, 'bar')
    foo.set('bar', 'false')
    assert not get_bool_attribute(foo, 'bar')
