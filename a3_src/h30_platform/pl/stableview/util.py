# -*- coding: utf-8 -*-
"""
---

title:
    "Stableview platform utility function module."

description:
    "This python module contains assorted utility
    functions used by the stableview platform."

id:
    "dc479ba2-6702-4fb1-91d8-5eb3f17a9cea"

type:
    dt003_python_module

validation_level:
    v00_minimum

protection:
    k00_general

copyright:
    "Copyright 2023 William Payne"

license:
    "Licensed under the Apache License, Version
    2.0 (the License); you may not use this file
    except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed
    to in writing, software distributed under
    the License is distributed on an AS IS BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
    either express or implied. See the License
    for the specific language governing
    permissions and limitations under the
    License."

...
"""



import importlib

import fl.util


# -----------------------------------------------------------------------------
def resolve(value):
    """
    Ensure that the provided value is fully resolved.

    If the provided value is a string starting
    with the prefix '_spec::' then resolve it
    to the actual value.

    """
    if fl.util.is_string(value) and value.startswith('_spec::'):
        (module, func) = value.split('::')[1].split(':')
        return getattr(importlib.import_module(module), func)

    return value
