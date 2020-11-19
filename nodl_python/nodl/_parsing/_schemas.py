# Copyright 2020 Canonical, Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import importlib.resources

from lxml import etree


__interface_schema: etree.XMLSchema = None
__v1_schema: etree.XMLSchema = None


def interface_schema() -> etree.XMLSchema:
    global __interface_schema
    if not __interface_schema:
        __interface_schema = _get_schema('interface.xsd')
    return __interface_schema


def v1_schema() -> etree.XMLSchema:
    global __v1_schema
    if not __v1_schema:
        __v1_schema = _get_schema('v1.xsd')
    return __v1_schema


def _get_schema(name: str) -> etree.XMLSchema:
    with importlib.resources.path('nodl._schemas', name) as path:
        return etree.XMLSchema(file=str(path))
