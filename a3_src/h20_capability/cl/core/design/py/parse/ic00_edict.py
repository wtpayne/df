# -*- coding: utf-8 -*-
"""
---

title:
    "Design document parsing stableflow-edict component."

description:
    "Design document parsing component."

id:
    "be7445bd-f048-4b14-b35b-5a0896c7a441"

type:
    dt004_python_stableflow_edict_component

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


import ast
import io
import os.path

import cl.core.design.nonconformity
import cl.core.design.py.parse._impl


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Design document parsing component coroutine.

    """
    signal = None

    for id_out in outputs.keys():
        outputs[id_out]['ena']  = False
        outputs[id_out]['ts']   = dict()
        outputs[id_out]['list'] = list()

    while True:

        inputs = yield (outputs, signal)

        # Reset outputs.
        #
        for id_out in outputs.keys():
            outputs[id_out]['ena'] = False
            outputs[id_out]['ts'].clear()
            outputs[id_out]['list'].clear()

        # Attempt to parse each
        # fileinfo item provided.
        #
        list_fileinfo = list()
        for (id_in, msg) in inputs.items():
            if msg['ena']:
                map_ts = msg['ts']
                for fileinfo in msg['list']:
                    list_fileinfo.append(_update_fileinfo(fileinfo))

        # If any fileinfo objects were
        # processed succesfully, then
        # output them.
        #
        if list_fileinfo:
            for id_out in outputs.keys():
                outputs[id_out]['ena'] = True
                outputs[id_out]['ts'].update(map_ts)
                outputs[id_out]['list'][:] = list_fileinfo


# -----------------------------------------------------------------------------
def _update_fileinfo(fileinfo):
    """
    Update the specified fileinfo structure with parse data.

    """
    impl     = cl.core.design.py.parse._impl
    filepath = fileinfo['filepath']
    str_text = fileinfo['text']
    tup_ast  = impl.parse(filepath, str_text)

    (ast_root, nonconformity) = tup_ast

    if nonconformity:

        fileinfo['list_nonconformity'].append(nonconformity)

    if ast_root:


        list_class  = [it for it in impl.iter_name_class(ast_root)]
        list_func   = [it for it in impl.iter_name_func(ast_root)]
        list_method = [it for it in impl.iter_name_method(ast_root)]
        bytes_text  = str_text.encode('utf-8')
        io_text     = io.BytesIO(bytes_text)
        name_mop    = impl.get_module_or_package_name(filepath)
        list_embed  = [tup for tup in impl.iter_tup_embed(
                                                        module_name = name_mop,
                                                        ast_root    = ast_root,
                                                        file        = io_text)]

        fileinfo['ast']   = ast_root
        fileinfo['embed'] = dict(list_func   = list_func,
                                 list_class  = list_class,
                                 list_method = list_method,
                                 list_embed  = list_embed)

        # TODO: Validate embedded metadata.
        # TODO: Check for required metadata fields.

    return fileinfo
