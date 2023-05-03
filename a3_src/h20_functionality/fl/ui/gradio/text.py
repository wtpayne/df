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

    daemon = multiprocessing.Process(target = _gradio_main,
                                     args   = (cfg,),
                                     name   = 'workflow-ui',
                                     daemon = True)
    daemon.start()

    list_workflow = list()
    list_param    = list()
    list_result   = list()
    list_error    = list()

    while True:

        list_result.clear()
        list_error.clear()
        (list_result, list_error) = yield (list_workflow, list_param)
        list_workflow.clear()
        list_param.clear()

        print('STEP')
        str_test = 'TEST TEXT'
        try:
            cfg['queue_in'].put(str_test, block = False)
        except queue.Full as err:
            pass


# -----------------------------------------------------------------------------
def _gradio_main(cfg):
    """
    Service the request queue, forwarding requests to the UI.

    """

    # -------------------------------------------------------------------------
    def _btn_submit_callback(txt_input, txt_prompt):
        """
        """
        try:
            cfg['queue_out'].put((txt_input, txt_prompt), block = False)
        except queue.Full as err:
            print('QUEUE FULL')
        return

    # -------------------------------------------------------------------------
    def _timer_callback():
        """
        """
        try:
            result = cfg['queue_in'].get(block = False)
            return result
        except queue.Empty:
            return

    # -------------------------------------------------------------------------
    with gradio.Blocks() as ui:
        with gradio.Row():
            with gradio.Column():

                txt_input  = gradio.TextArea(
                                        interactive = True,
                                        label       = 'Input',
                                        lines       = 10)
                txt_prompt = gradio.TextArea(
                                        interactive = True,
                                        label       = 'Template',
                                        lines       = 10)
                txt_output = gradio.TextArea(
                                        interactive = False,
                                        label       = 'Output',
                                        lines       = 10)
                btn_submit = gradio.Button(
                                        value       = 'Submit')

                btn_submit.click(
                            fn     = _btn_submit_callback,
                            inputs = [txt_input, txt_prompt])

        ui.load(
            fn      = _timer_callback,
            outputs = [txt_output],
            every   = 1)

    ui.queue(
        concurrency_count = 2,
        max_size          = 3)

    ui.launch(
        inbrowser           = True,
        share               = False,
        prevent_thread_lock = False)
