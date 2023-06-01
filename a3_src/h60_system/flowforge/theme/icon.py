# -*- coding: utf-8 -*-
"""
---

title:
    "Stableflow theme icon module."

description:
    "Provides functions for preparing and
    loading icon assets."

id:
    "3cfe0496-9a1c-49e6-b25a-96316b08071a"

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
def build(filepath_icon_src, id_theme, id_icon, color_fg, color_bg):
    """
    Create an icon file.

    """
    import PIL.Image
    import numpy

    rgba = PIL.Image.open(filepath).convert("RGBA")
    return numpy.array(rgba).flatten()

    filepath_icon_src


# -----------------------------------------------------------------------------
def load(id_theme, id_icon):
    """
    TODO: MOVE THIS INTO A BUILD STEP WHERE WE COMPILE ASSETS.

    """
    import da.env
    filepath = da.env.path(
        control_tier = 'h10_resource',
        relpath      = 'icon/dark/solid/{id}/16x16.png'.format(id = id_icon),
        id_env       = 'e002_general_research')
