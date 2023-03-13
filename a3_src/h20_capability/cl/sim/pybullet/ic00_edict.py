# -*- coding: utf-8 -*-
"""
---

title:
    "PyBullet simulation stableflow-edict component."

description:
    "PyBullet simulation stableflow-edict component.
    Runs."

id:
    "8fb922d3-a661-4da5-b2f8-75d75d5457cc"

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


import time

import pybullet
import pybullet_data


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Noop component coroutine.

    """
    signal = None

    for id_out in outputs.keys():
        outputs[id_out]['ena']  = False
        outputs[id_out]['ts']   = dict()
        outputs[id_out]['list'] = list()

# https://docs.google.com/document/d/10sXEhzFRSnvFcl3XxNGhnD4N2SedqwdAvK3dsihxVUA/edit#
# https://github.com/utiasDSL/gym-pybullet-drones

    physicsClient = pybullet.connect(pybullet.GUI)
    pybullet.setAdditionalSearchPath(pybullet_data.getDataPath())
    pybullet.setGravity(0,0,-10)
    planeId          = pybullet.loadURDF("plane.urdf")
    startPos         = [0,0,1]
    startOrientation = pybullet.getQuaternionFromEuler([0,0,0])
    boxId            = pybullet.loadURDF("data/quadrotor.urdf")

    while True:

        inputs = yield (outputs, signal)

        # Reset outputs.
        #
        for id_out in outputs.keys():
            outputs[id_out]['ena'] = False
            outputs[id_out]['ts'].clear()
            outputs[id_out]['list'].clear()

        pybullet.stepSimulation()

        cubePos, cubeOrn = pybullet.getBasePositionAndOrientation(boxId)
        print(cubePos,cubeOrn)

        if any((val['ena'] for val in inputs.values())):
            continue

        list_out = list()

        # If any filepaths are ready for
        # processing, then output them.
        #
        if list_out:
            map_ts = inputs[id_in]['ts']
            for id_out in outputs.keys():
                outputs[id_out]['ena'] = True
                outputs[id_out]['ts'].update(map_ts)
                outputs[id_out]['list'][:] = list_out

    pybullet.disconnect()


# -----------------------------------------------------------------------------
def _foo():
    """
    """
    pass

