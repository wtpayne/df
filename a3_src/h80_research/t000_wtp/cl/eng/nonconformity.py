# -*- coding: utf-8 -*-
"""
---

title:
    "Nonconformity identifier module."

description:
    "This module contains constants to
    indicate the type of nonconformity
    that has been identified."

id:
    "24660efd-f770-498d-a63f-a40c698e4368"

type:
    dt003_python_module

validation_level:
    v00_minimum

protection:
    k00_general

copyright:
    "Copyright 2015-2022 William Payne"

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

import enum


# =============================================================================
class ID(enum.Enum):
    """
    Nonconformity Id enum.

    """
    nc000_file_not_readable               = 0
    nc001_file_not_decodable              = 1
    nc002_file_not_parseable              = 2
    nc003_python_code_style_nonconformity = 3
