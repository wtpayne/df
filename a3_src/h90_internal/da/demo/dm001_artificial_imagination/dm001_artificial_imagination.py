# -*- coding: utf-8 -*-
"""
---

title:
    "dm001_artificial_imagination demo commands."

description:
    "This module defines commands for the
    dm001_artificial_imagination demonstration."

id:
    "7b26801b-4f12-4102-9b4e-6bee29b73746"

type:
    dt003_python_module

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


"""


import os
import os.path
import sys

import da.env
import da.env.run


# -----------------------------------------------------------------------------
def start():
    """
    Start dm001 system.

    """
    dirpath_self      = os.path.dirname(os.path.realpath(__file__))
    filename_template = 'quadrotor.urdf.template'
    filepath_template = os.path.join(dirpath_self, filename_template)

    dirpath_tmp       = da.env.path(
                                process_area = 'a4_tmp',
                                control_tier = 'h90_internal',
                                relpath      = 'dm001_artificial_imagination')
    filename_urdf     = 'quadrotor.urdf'
    filepath_urdf     = os.path.join(dirpath_tmp, filename_urdf)

    if not os.path.exists(dirpath_tmp):
       os.makedirs(dirpath_tmp)

    with open(filepath_template, 'rt') as file_template:
        str_template = file_template.read()
        str_urdf     = str_template.format(dirpath_root = da.env.rootpath())

    with open(filepath_urdf, 'wt') as file_urdf:
        file_urdf.write(str_urdf)

    tup_overrides = (
        'host.localhost.dirpath_log',               _dirpath_log(),
        'node.simulator.config.filepath_quadrotor', filepath_urdf)

    sys.exit(da.env.run.stableflow_start(path_cfg      = _filepath_cfg(),
                                         tup_overrides = tup_overrides))


# -----------------------------------------------------------------------------
def stop():
    """
    Stop dm001 system.

    """
    import da.env.run
    sys.exit(da.env.run.stableflow_stop(path_cfg = _filepath_cfg()))


# -----------------------------------------------------------------------------
def _filepath_cfg():
    """
    Return the filepath to the system stableflow configuration file.

    """
    import da.env
    relpath_dir  = 'da/demo/dm001_artificial_imagination'
    filename_cfg = 'dm001_artificial_imagination.stableflow.cfg.yaml'
    relpath_cfg  = os.path.join(relpath_dir, filename_cfg)
    return da.env.path(
            process_area = 'a3_src',
            control_tier = 'h90_internal',
            relpath      = relpath_cfg)


# -----------------------------------------------------------------------------
def _dirpath_log():
    """
    Return the directory path to the logging directory for this system.

    """
    import da.env
    return da.env.path(process_area = 'a4_tmp',
                       control_tier = 'h90_internal',
                       relpath      = 'dm001_artificial_imagination')
