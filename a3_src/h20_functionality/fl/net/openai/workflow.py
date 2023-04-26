# -*- coding: utf-8 -*-
"""
---

title:
    "OpenAI workflow engine module."

description:
    "This python module is designed to automate
    and continuously improve workflows for
    OpenAI ChatGPT agents."

id:
    "2fdd7113-1e2d-40df-81dc-7c4511f8e627"

type:
    dt003_python_module

validation_level:
    v00_minimum

protection:
    k00_general

copyright:
    "Copyright 2022-2023 William Payne"

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


import fl.util


# -----------------------------------------------------------------------------
@fl.util.coroutine
def coro(cfg):
    """
    OpenAI workflow engine coroutine.

    """

    list_template = list()
    list_param    = list()
    list_resource = list()

    while True:

        (result, param) = yield (list_template, list_param, list_resource)

        list_template.clear()
        list_param.clear()
        list_resource.clear()

        # Default templates.
        #
        if list_template_default:
            list_template.extend(list_template_default)
            list_template_default.clear()

        # Parameters from outside (e.g. user)
        #
        if param is not None:
            list_param.append(param)

        # Parameters from OpenAI result (i.e. prev step)
        #
        if result is not None:
            (param_new, final_text) = _get_next_outputs(result)
            if param_new is not None:
                list_param.append(param_new)
            if final_text is not None:
                list_resource.append(final_text)


