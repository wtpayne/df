# -*- coding: utf-8 -*-
"""
---

title:
    "Python design document style checking stableflow-edict component."

description:
    "Design document style checking component"

id:
    "fe27f0f1-cb13-4aff-bbec-471d51f143a5"

type:
    dt004_python_stableflow_edict_component

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


import pycodestyle

import cl.design.nonconformity


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Design document style checking component coroutine.

    """
    signal = None

    list_ignore = cfg['list_ignore']

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

        # Attempt to check each
        # fileinfo item provided.
        #
        list_fileinfo = list()
        for (id_in, msg) in inputs.items():
            if msg['ena']:
                map_ts = msg['ts']
                for fileinfo in msg['list']:
                    _run_check_and_update(list_ignore = list_ignore,
                                          fileinfo    = fileinfo)
                    list_fileinfo.append(fileinfo)

        # If any fileinfo objects were
        # processed succesfully, then
        # output them.
        #
        if list_fileinfo:
            for id_out in outputs.keys():
                outputs[id_out]['ena'] = True
                outputs[id_out]['ts'].update(map_ts)
                outputs[id_out]['list'][:] = list_fileinfo


# --------------------------------------------------------------------------
def _run_check_and_update(list_ignore, fileinfo):
    """
    Update fileinfo with the results of the design document style check.

    """

    list_nonconformity = list()
    nc = cl.design.nonconformity

    # =========================================================================
    class ReportAdapter(pycodestyle.StandardReport):
        """
        Reporting Adapter class for pycodestyle (pep8) checks.

        """

        def get_file_results(self):
            """
            Redirect error messages to list_nonconformity.

            """
            for (line, col, msg_id, msg, doc) in self._deferred_print:
                id_nc = nc.ID.nc003_python_code_style_nonconformity
                doc   = '    ' + doc.strip()  # Fixup indentation
                nonconformity = { 'reporter': __name__,
                                  'id_nc':    id_nc,
                                  'str_msg':  doc,
                                  'filepath': filepath,
                                  'line':     None,
                                  'col':      None }
                list_nonconformity.append(nonconformity)

    style = pycodestyle.StyleGuide(quiet  = False,
                                   ignore = list_ignore)
    style.init_report(reporter = ReportAdapter)  # Inject custom reporting.

    filepath = fileinfo['filepath']
    list_nonconformity.clear()
    style.check_files((filepath,))
    if list_nonconformity:
        fileinfo['list_nonconformity'].extend(list_nonconformity)
