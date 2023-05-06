# -*- coding: utf-8 -*-
"""
---

title:
    "Server debug printer."

description:
    "Server debug printer."

id:
    ""

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


import pprint


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Parameter generator coroutine

    """

    # Initialize outputs.
    #
    signal = None
    for id_out in outputs.keys():
        outputs[id_out]['ena']  = False
        outputs[id_out]['ts']   = dict()
        outputs[id_out]['list'] = list()

    # Loop forever
    #
    while True:

        inputs = yield (outputs, signal)

        # Reset outputs.
        #
        for id_out in outputs.keys():
            outputs[id_out]['ena'] = False
            outputs[id_out]['ts'].clear()
            outputs[id_out]['list'].clear()

        if not inputs['request']['ena']:
            continue

        print('')
        print('')
        print('#' * 80)
        print('SERVER DEBUG PRINT:-')
        pprint.pprint(inputs['request'])
        print('#' * 80)
        print('')
        print('')

        # {'request': {'ena': True,
        #              'list': [{'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        #                        'accept_encoding': 'gzip, deflate, br',
        #                        'accept_language': 'en-US,en;q=0.9,en-GB;q=0.8',
        #                        'client_ip': '127.0.0.1',
        #                        'id_resource': 'test_url2',
        #                        'id_session': '6fb5f77a-4fa1-46e6-92bd-1edf9361139b',
        #                        'id_user': '040c2b05-8330-4705-9b2c-89789dd7cccf',
        #                        'url': 'http://localhost:8080/test_url2',
        #                        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; '
        #                                      'x64) AppleWebKit/537.36 (KHTML, like '
        #                                      'Gecko) Chrome/112.0.0.0 Safari/537.36'},
        #                       {'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        #                        'accept_encoding': 'gzip, deflate, br',
        #                        'accept_language': 'en-US,en;q=0.9,en-GB;q=0.8',
        #                        'client_ip': '127.0.0.1',
        #                        'id_resource': 'favicon.ico',
        #                        'id_session': '6fb5f77a-4fa1-46e6-92bd-1edf9361139b',
        #                        'id_user': '040c2b05-8330-4705-9b2c-89789dd7cccf',
        #                        'url': 'http://localhost:8080/favicon.ico',
        #                        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; '
        #                                      'x64) AppleWebKit/537.36 (KHTML, like '
        #                                      'Gecko) Chrome/112.0.0.0 Safari/537.36'}],
        #              'ts': {}}}
