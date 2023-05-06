# -*- coding: utf-8 -*-
"""
---

title:
    "Video debug display stableflow-edict component."

description:
    "Video debug display component."

id:
    "f45a3154-6dd6-489a-9a64-efd8a4f8c7ed"

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


import cv2


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Video capture coroutine.

    """
    signal = None
    state['window_name'] = cfg.get('window_name', 'lib.video.display')

    # If this component is running on a
    # remote host, then the X server on
    # the remote host needs to be running.
    #
    # The user we are logged in as needs
    # to have the authorization to use the
    # X server. On most distros (but not all),
    # this is done by having a "magic cookie"
    # in $HOME/.Xauthority.
    #
    # You can accomplish this for example by
    # logging in as the same user you are
    # using for ssh onto the remote host from
    # the keyboard.
    #
    # If this has been done, you can set export
    # DISPLAY=:0 after you log in with ssh to
    # the remote host, and then any X programs
    # spawned from this shell will use the
    # display on the remote host.
    #
    while True:

        inputs = yield (outputs, signal)

        if not inputs['img']['ena']:
            continue

        cv2.imshow(state['window_name'], inputs['img']['buff'])
        cv2.waitKey(1)


# -----------------------------------------------------------------------------
def finalize(runtime, config, inputs, state, outputs):
    """
    Clean up resources.

    """
    try:
        cv2.destroyWindow(state['window_name'])
    except cv2.error as err:
        pass
