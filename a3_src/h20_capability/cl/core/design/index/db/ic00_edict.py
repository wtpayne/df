# -*- coding: utf-8 -*-
"""
---

title:
    "Design index database stableflow-edict component."

description:
    "Stores design information in the design
    index database."

id:
    "4823e97f-bae0-46e9-b34b-e7fdf65178a6"

type:
    dt004_python_stableflow_edict_component

dependencies:
    - pycozo[embedded,pandas]
    - pandas

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
    WIT HOUT WARRANTIES OR CONDITIONS OF ANY KIND,
    either express or implied. See the License
    for the specific language governing
    permissions and limitations under the
    License."

...
"""


import collections
import pprint

import pycozo.client
import cl.core.design.index.db.trace as trace




# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Design index component coroutine.

    """


    filepath_db = '/media/wtp/Data/dev/df/ws00_pri/a4_tmp/main/design_index.db'
    db_trace    = trace.DataBase(filepath_db = filepath_db)

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

        #
        if inputs['data']['ena']:
            try:
                db_trace.bulk_upsert(iter_tup_trace = inputs['data']['list'])
            except Exception as err:
                print(repr(err))  # TODO: Logging / Error handling?

        list_out = list()
        if list_out:
            map_ts = inputs[id_in]['ts']
            for id_out in outputs.keys():
                outputs[id_out]['ena'] = True
                outputs[id_out]['ts'].update(map_ts)
                outputs[id_out]['list'][:] = list_out

    client.close()
