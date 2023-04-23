# -*- coding: utf-8 -*-
"""
---

title:
    "dm003_poetic demo commands."

description:
    "This module defines commands for the
    dm003_poetic demonstration."

id:
    "b6506820-b3f9-42ea-8ff1-582139be96c8"

type:
    dt003_python_module

validation_level:
    v00_minimum

protection:
    k00_general

copyright:
    "Copyright 2015-2023 William Payne"

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


"""


import sys


# -----------------------------------------------------------------------------
def app():
    """
    Run dm002 app.

    """
    import da.env.run
    sys.exit(da.env.run.python_module(module = 'flow_editor.cli.main',
                                      id_env = 'e002_general_research'))
