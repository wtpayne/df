# -*- coding: utf-8 -*-
"""
---

title:
    "Gradio NLP demo support module."

description:
    "This Python module is designed to
    interact with a Gradio UI that is
    running in a separate process."

id:
    "f42feb22-a8dd-4c66-9968-475cb4c78e94"

type:
    dt004_python_stableflow_edict_component

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

...
"""


import multiprocessing
import queue

import gradio

import fl.util


# -----------------------------------------------------------------------------
@fl.util.coroutine
def coro_ui(cfg):
    """
    """
    cfg['queue_in']  = multiprocessing.Queue()  # coro   --> daemon
    cfg['queue_out'] = multiprocessing.Queue()  # daemon --> coro

    daemon = multiprocessing.Process(target = _daemon_main,
                                     args   = (cfg,),
                                     name   = 'workflow-ui',
                                     daemon = True)
    daemon.start()

    list_result   = list()
    list_error    = list()
    list_workflow = list()
    list_param    = list()

    # Loop forever
    #
    while True:

        (list_result, list_error) = yield (list_workflow, list_param)
        try:

            cfg['queue_in'].put((list_result, list_error), block = False)

        except queue.Full as err:
            # TODO: LOGGING
            pass

        list_result.clear()
        list_error.clear()

        list_workflow.clear()
        list_param.clear()

        while True:
            try:

                (list_workflow_part,
                 list_param_part) = cfg['queue_out'].get(block = False)

                list_workflow.extend(list_workflow_part)queue_out
                list_param.extend(list_param_part)

            except queue.Empty:
                # TODO: LOGGING
                break


# -----------------------------------------------------------------------------
def _daemon_main(cfg):
    """
    Service the request queue, forwarding requests to the UI.

    """

    list_fields = ['Field 1',
                   'Field 2',
                   'Field 3',
                   'Field 4',
                   'Field 5']

    # -------------------------------------------------------------------------
    def _ui_callback(input,
                     proc_01,
                     proc_02,
                     proc_03,
                     proc_04):

        return tuple(list_fields)

    # -------------------------------------------------------------------------
    def _system_callback(result):
        """
        """
        # Update list_fields from result.

        return ([], [])

    # MAIN
    # ====

    list_inputs  = [gr.Textbox(lines = 3, placeholder = "Input")]
    list_outputs = [gr.Textbox(lines = 3, placeholder = "")]

    num_steps = 4;
    for idx in range(num_steps):
        list_inputs.append(gr.Textbox(lines = 3, placeholder = "Process step #"))
        list_outputs.append(gr.Textbox(lines = 3, placeholder = "Process step #"))

    demo = gr.Interface(
        fn      = _ui_callback,
        inputs  = list_inputs,
        outputs = list_outputs,
    )
    demo.launch()

    while True:

        try:
            (list_result, list_error) = cfg['queue_in'].get(block = False)
        except queue.Empty:
            time.sleep(cfg['secs_interval'])
            continue

        for result in list_result:
            (list_workflow, list_param) = _system_callback(result)

        # for error in list_error:
        #     _process_one_error(error)

        try:
            cfg['queue_out'].put((list_workflow, list_param),
                                 block = False)
        except queue.Full as exc:
            pass

