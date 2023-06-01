# -*- coding: utf-8 -*-
"""
---

title:
    "Theme selection for FlowForge."

description:
    "This python module defines the theme
    selection for the FlowForge system."

id:
    "b11b1992-3e03-4a40-930f-8501774f755a"

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


from . import light
from . import dark


id_theme = 'light'

if id_theme == 'light':
     globals().update(light.theme())

elif id_theme == 'dark':
     globals().update(dark.theme())

else:
     globals().update(light.theme())
