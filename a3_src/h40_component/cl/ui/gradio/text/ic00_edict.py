# -*- coding: utf-8 -*-
"""
---

title:
    "Gradio text input stableflow-edict component."

description:
    "Placeholder no-op component. Does nothing"

id:
    "c917c7be-064d-43b0-adfd-2a057834d51e"

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


import fl.ui.gradio.text


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    OpenAI agent coroutine.

    """

    ui = fl.ui.gradio.text.coro_ui(cfg)

    # Initialize outputs.
    #
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

        # Grab any new result inputs.
        #
        map_ts      = dict()
        list_result = list()
        if inputs['result']['ena']:
            map_ts      = inputs['result']['ts']
            list_result = inputs['result']['list']

        # Grab any new error inputs.
        #
        map_ts     = dict()
        list_error = list()
        if inputs['error']['ena']:
            map_ts     = inputs['error']['ts']
            list_error = inputs['error']['list']

        # Communicate with the UI.
        #
        (list_workflow,
         list_param) = ui.send((list_result,
                                list_error))

        # Update workflow outputs.
        #
        if ('workflow' in outputs) and list_workflow:
            outputs['workflow']['ena'] = True
            outputs['workflow']['ts'].update(map_ts)
            outputs['workflow']['list'][:] = list_workflow

        # Update param outputs.
        #
        if ('param' in outputs) and list_param:
            outputs['param']['ena'] = True
            outputs['param']['ts'].update(map_ts)
            outputs['param']['list'][:] = list_param



# -----------------------------------------------------------------------------
def _daemon_main(cfg):
    """
    Service the request queue, forwarding requests to the OpenAI API.

    Each request in the queue is processed,
    pausing for secs_interval if no request
    is available at that time.

    Results and errors are enqueued onto
    their respective queues for further
    processing by the controlling process.

    This is intended to be a minimal daemon
    that sits in a separate process and
    handles communication with the OpenAI
    API.

    """

    import gradio as gr

    # while True:

    #     try:
    #         request = cfg['queue_request'].get(block = False)
    #     except queue.Empty:
    #         time.sleep(cfg['secs_interval'])
    #         continue

    #     # result = _process_one_request(request_raw = request,
    #     #                               default     = cfg['default'],
    #     #                               is_bit      = cfg['is_bit'])

    #     if result['error'] is not None:
    #         cfg['queue_error'].put(result['error'], block = False)

    #     try:
    #         cfg['queue_result'].put(result, block = False)
    #     except queue.Full as error:
    #         cfg['queue_error'].put(error, block = False)


    # -------------------------------------------------------------------------
    def process(input,
                proc_01,
                proc_02,
                proc_03,
                proc_04):

        return 'echo', 'foo', 'bar', 'baz', 'splat'


    list_inputs  = [gr.Textbox(lines = 3, placeholder = "Input")]
    list_outputs = [gr.Textbox(lines = 3, placeholder = "")]

    num_steps = 4;
    for idx in range(num_steps):
        list_inputs.append(gr.Textbox(lines = 3, placeholder = "Process step #"))
        list_outputs.append(gr.Textbox(lines = 3, placeholder = "Process step #"))

    demo = gr.Interface(
        fn      = process,
        inputs  = list_inputs,
        outputs = list_outputs,
    )
    demo.launch()


    while True:

        time.sleep(1)

        # TODO: Pump queues and update stuff.