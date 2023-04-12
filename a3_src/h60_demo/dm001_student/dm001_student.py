#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
---

title:
    "dm001_student demonstration launcher script."

description:
    "This script is used to launch the
    dm001_student demonstration."

id:
    "7b26801b-4f12-4102-9b4e-6bee29b73746"

type:
    dt001_python_script

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


"""


import os
import sys

import da.env


# -----------------------------------------------------------------------------
def main():
    """
    Run the dm001_student demonstration.

    """
    dirpath_self       = os.path.dirname(os.path.realpath(__file__))
    filename_cfg       = 'dm001_student.stableflow.cfg.yaml'
    filepath_cfg       = os.path.join(dirpath_self, filename_cfg)
    filename_quadrotor = 'quadrotor.urdf'
    filepath_quadrotor = os.path.join(dirpath_self, filename_quadrotor)
    tup_overrides      = (
        'node.simulator.config.filepath_quadrotor', filepath_quadrotor)

    da.stableflow.start(path_cfg      = filepath_cfg,
                        tup_overrides = tup_overrides)


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    main()
