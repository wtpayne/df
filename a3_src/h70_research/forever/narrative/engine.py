# -*- coding: utf-8 -*-
"""
---

title:
    "Placeholder no-op stableflow-edict component."

description:
    "Placeholder no-op component. Does nothing"

id:
    "8747de1c-76ac-4f63-a88d-f67a60515571"

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

# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Engine coro

    """

    # Initialize outputs.
    #
    signal = None
    for id_out in outputs.keys():
        outputs[id_out]['ena']  = False
        outputs[id_out]['ts']   = dict()
        outputs[id_out]['list'] = list()

    # Loop forever, sending messages
    # to and from the discord client
    # via the two message queues.
    #
    while True:

        inputs = yield (outputs, signal)

        print('HELLO ENGINE')

        # # Reset outputs.
        # #
        # for id_out in outputs.keys():
        #     outputs[id_out]['ena'] = False
        #     outputs[id_out]['ts'].clear()
        #     outputs[id_out]['list'].clear()

        # # Take any messages that
        # # we recieve from the rest
        # # of the stableflow system
        # # and forward them on to
        # # the discord client so that
        # # they can be printed in
        # # the specified channel.
        # #
        # map_ts = dict()
        # for (id_in, pkt_in) in inputs.items():
        #     if pkt_in['ena']:
        #         map_ts = pkt_in['ts']
        #         for tup_msg in pkt_in['list']:
        #             try:
        #                 queue_to_client.put(tup_msg, block = False)
        #             except queue.Full:
        #                 pass  # TODO: LOG SOME SORT OF ERROR?

        # # Retrieve any messages that
        # # a user has input into the
        # # discord client and forward
        # # them to the rest of the
        # # stableflow system for
        # # further processing.
        # #
        # list_msg = list()
        # while True:
        #     try:
        #         list_msg.append(queue_from_client.get(block = False))
        #     except queue.Empty:
        #         break

        # # If any messages have been
        # # received from the discord
        # # client, then place them
        # # in the component output.
        # #
        # if list_msg:
        #     for id_out in outputs.keys():
        #         outputs[id_out]['ena'] = True
        #         outputs[id_out]['ts'].update(map_ts)
        #         outputs[id_out]['list'][:] = list_msg

