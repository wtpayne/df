# -*- coding: utf-8 -*-
"""
---

title:
    "Stableflow theme font module."

description:
    "Provides functions for preparing and
    locating font assets."

id:
    "0e457d79-3f2e-457f-a69c-7be2c2f6c017"

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


# -----------------------------------------------------------------------------
def build(filepath_font, name):
    """
    """
    pass

# -----------------------------------------------------------------------------
def path(id_theme, id_font):
    """
    """
    import da.env
    return da.env.path(
        control_tier = 'h10_resource',
        relpath      = 'font/tecnico/fino.ttf',
        id_env       = 'e002_general_research')