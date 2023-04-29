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


import os
import sys


ID_ENV       = 'e002_general_research'
EXIT_SUCCESS = 0
EXIT_FAILURE = 1


# -----------------------------------------------------------------------------
def test():
    """
    Run all dm005 tests.

    """
    import da.test
    if (     (unit_test()      == EXIT_SUCCESS)
         and (component_test() == EXIT_SUCCESS)
         and (system_test()    == EXIT_SUCCESS)):
        return EXIT_SUCCESS
    else:
        return EXIT_FAILURE


# -----------------------------------------------------------------------------
def test_test():
    """
    Run dm005 unit level tests.

    """
    import da.test
    # return da.test.run(control_tier = 'h20_functionality',
    #                    relpath      = 'fl/stableflow',
    #                    id_env       = ID_ENV)
    return da.test.run(control_tier = 'h20_functionality',
                       relpath      = 'fl/test',
                       id_env       = ID_ENV)


# -----------------------------------------------------------------------------
def unit_test():
    """
    Run dm005 unit level tests.

    """
    import da.test
    return da.test.run(control_tier = 'h20_functionality',
                       relpath      = 'fl/net/openai',
                       id_env       = ID_ENV)


# -----------------------------------------------------------------------------
def component_test():
    """
    Run dm005 component level tests.

    """
    import da.test
    return da.test.run(control_tier = 'h40_component',
                       relpath      = 'cl/net/openai',
                       id_env       = ID_ENV)


# -----------------------------------------------------------------------------
def system_test():
    """
    Run dm005 system level tests.

    """
    import da.test
    return da.test.run(control_tier = 'h50_product',
                       relpath      = '.',
                       id_env       = ID_ENV)


# -----------------------------------------------------------------------------
def app():
    """
    Run dm005 UI.

    """
    import da.test
    sys.exit(da.env.run.python_module(module = 'gradio_demo',
                                      id_env = ID_ENV))

