# -*- coding: utf-8 -*-
"""
---

title:
    "Design document nonconformity report aggregator steadyflow component."

description:
    "Design document nonconformity report aggregator component."

id:
    "5d824805-88e2-4d7c-a1cb-c9a4e23052a8"

type:
    dt004_python_steadyflow_edict_component

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


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Design document nonconformity report component coroutine.

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

        # Merge fileinfo items that
        # refer to the same files.
        #
        map_fileinfo = dict()
        for (id_in, pkt_in) in inputs.items():
            if pkt_in['ena']:
                map_ts = pkt_in['ts']
                for fileinfo in pkt_in['list']:
                    map_fileinfo = _update_map_fileinfo(map_fileinfo,
                                                        fileinfo)

        # If any fileinfo objects were
        # processed succesfully, then
        # output them.
        #
        if map_fileinfo:
            for id_out in outputs.keys():
                outputs[id_out]['ena'] = True
                outputs[id_out]['ts'].update(map_ts)
                outputs[id_out]['list'][:] = map_fileinfo.values()


# -----------------------------------------------------------------------------
def _update_map_fileinfo(map_fileinfo, fileinfo):
    """
    Update map_fileinfo with the new fileinfo object.

    This mainly means merging in the list of
    nonconformities.

    """
    filepath           = fileinfo['filepath']
    list_nonconformity = fileinfo['list_nonconformity']
    if filepath in map_fileinfo:
        map_fileinfo[filepath]['list_nonconformity'].extend(
                                                        list_nonconformity)
    else:
        map_fileinfo[filepath] = fileinfo
    return map_fileinfo
