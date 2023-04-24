# -*- coding: utf-8 -*-
"""
---

title:
    "dm005_chicago demo commands."

description:
    "This module defines commands for the 
    dm005_chicago demonstration."

id:
    "87df2f55-214e-40be-9330-53cf354817ef"

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


# -----------------------------------------------------------------------------
def test():
    """
    Run dm005 tests.

    """
    import da.env
    dirpath = da.env.path(process_area = 'a3_src',
                          control_tier = 'h70_research')
    print(dirpath)
