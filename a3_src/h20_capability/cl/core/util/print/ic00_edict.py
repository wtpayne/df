# -*- coding: utf-8 -*-
"""
---

title:
    "Diagnostic print utility steadyflow-edict component."

description:
    "Diagnostic print utility component."

id:
    "f3581a3e-bcfd-4c99-b7e3-015da68a71f1"

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


import os.path
import pprint
import sys


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Debug print coroutine.

    """
    signal = None

    # Read config.
    #
    spec_ostream   = cfg.get('output',   'stdout')
    list_delimpath = cfg.get('path',     list())
    do_prettyprint = cfg.get('pretty',   True)
    do_enabledonly = cfg.get('only_ena', True)

    # Select the output stream.
    #
    ostream = None
    if spec_ostream == 'stdout':
        ostream = sys.stdout
    elif spec_ostream == 'stderr':
        ostream = sys.stderr
    else:
        os.makedirs(os.path.dirname(spec_ostream), exist_ok = True)
        ostream = open(spec_ostream, 'wt')

    # Define which inputs
    # we are going to read.
    #
    list_tup_path = list(list())
    if not list_delimpath:
        for key in inputs.keys():
            list_tup_path.append((key,))
    else:
        for path in list_delimpath:
            list_tup_path.append(tuple(path.split('.')))

    while True:

        inputs = yield (outputs, signal)

        for tup_path in list_tup_path:

            # Check enable flag on selected input.
            #
            id_input = tup_path[0]
            selected = inputs[id_input]
            if do_enabledonly and 'ena' in selected and not selected['ena']:
                continue

            # Drill down to selected data item.
            #
            cursor = inputs
            for name in tup_path:
                cursor = cursor[name]

            # Print it.
            #
            if do_prettyprint:
                pprint.pprint(cursor, stream = ostream)
            else:
                print(cursor, file = ostream)
