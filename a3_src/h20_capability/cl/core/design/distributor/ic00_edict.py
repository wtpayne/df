# -*- coding: utf-8 -*-
"""
---

title:
    "File information distributor stableflow-edict component."

description:
    "File information distributor component.
    Sends file information to a different
    output depending on the file path."

id:
    "845c6440-bda4-413d-966d-a004b2d56eab"

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


import re


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    File information distributor component coroutine.

    """
    signal = None

    for id_out in outputs.keys():
        outputs[id_out]['ena']  = False
        outputs[id_out]['ts']   = dict()
        outputs[id_out]['list'] = list()

    map_str_output = cfg.get('output', dict())
    map_re_output  = dict()
    for (id_out, iter_regex) in map_str_output.items():
        map_re_output[id_out] = _combine_regex(iter_regex, op = '|')

    while True:

        inputs = yield (outputs, signal)

        # Reset outputs.
        #
        for id_out in outputs.keys():
            outputs[id_out]['ena'] = False
            outputs[id_out]['ts'].clear()
            outputs[id_out]['list'].clear()

        # Distribute inputs according
        # to the configured regexes.
        #
        map_ts = dict()
        for (id_out, regex) in map_re_output.items():

            assert id_out in outputs.keys()

            for id_in in inputs.keys():

                if not inputs[id_in]['ena']:
                    continue

                for fileinfo in inputs[id_in]['list']:
                    if regex.match(fileinfo['filepath']) is None:
                        continue
                    outputs[id_out]['list'].append(fileinfo)

                if outputs[id_out]['list']:
                    outputs[id_out]['ena'] = True
                    outputs[id_out]['ts'].update(inputs[id_in]['ts'])


# --------------------------------------------------------------------------
def _combine_regex(iter_regex, op = '|'):
    """
    Return a regular expression compiled from an iterable of strings.

    The supplied strings are combined using the
    supplied operator and then compiled into a
    single regular expression object and
    returned.

    """
    if iter_regex is None:
        return re.compile('(?!x)x')  # Will never match anything

    str_delim = '){op}('.format(op = op)
    str_inner = str_delim.join(iter_regex)
    str_regex = '({inner})'.format(inner = str_inner)
    obj_regex = re.compile(str_regex)
    return obj_regex
