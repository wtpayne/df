# -*- coding: utf-8 -*-
"""
---

title:
    "dm004_legend demo commands."

description:
    "This module defines commands for the 
    dm004_legend demonstration."

id:
    "b1e5f9e5-0626-4900-968f-c300006c074e"

type:
    dt003_python_module

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


"""


import os
import sys


# -----------------------------------------------------------------------------
def app():
    """
    Run dm004 frontend mobile app.

    """
    import da.env.run
    sys.exit(da.env.run.python_module(
                            module      = 'forever.library.main',
                            id_env      = 'e002_general_research',
                            id_env_boot = 'e000_design_automation_core',
                            acct        = 'wtp',
                            host        = 'localhost'))


# -----------------------------------------------------------------------------
def server_start():
    """
    Start dm004 backend server.

    """
    dirpath_self = os.path.dirname(os.path.realpath(__file__))
    relpath_root = '../../..'
    mixpath_root = os.path.join(dirpath_self, relpath_root)
    dirpath_root = os.path.normpath(mixpath_root)
    relpath_cfg  = 'a3_src/h70_research/forever/library'
    filename_cfg = 'forever.stableflow.cfg.yaml'
    filepath_cfg = os.path.join(dirpath_root, relpath_cfg, filename_cfg)
    import da.stableflow
    sys.exit(da.stableflow.start(path_cfg = filepath_cfg))


# -----------------------------------------------------------------------------
def server_stop():
    """
    Stop dm004 backend server.

    """
    dirpath_self = os.path.dirname(os.path.realpath(__file__))
    relpath_root = '../../..'
    mixpath_root = os.path.join(dirpath_self, relpath_root)
    dirpath_root = os.path.normpath(mixpath_root)
    relpath_cfg  = 'a3_src/h70_research/forever/library'
    filename_cfg = 'forever.stableflow.cfg.yaml'
    filepath_cfg = os.path.join(dirpath_root, relpath_cfg, filename_cfg)
    import da.stableflow
    sys.exit(da.stableflow.stop(path_cfg = filepath_cfg))


# -----------------------------------------------------------------------------
def build_android():
    """
    Build dm004 for Android.

    """
    dirpath_self = os.path.dirname(os.path.realpath(__file__))
    relpath_root = '../../..'
    mixpath_root = os.path.join(dirpath_self, relpath_root)
    dirpath_root = os.path.normpath(mixpath_root)
    relpath_src  = 'a3_src/h70_research/forever/library'
    dirpath_src  = os.path.join(dirpath_root, relpath_src)
    relpath_tmp  = 'a4_tmp/h70_research/forever/library'
    dirpath_tmp  = os.path.join(dirpath_root, relpath_tmp)
    
    # Recursively copy the source design documents
    # to the temporary build area.
    #
    import shutil
    shutil.copytree(dirpath_src, 
                    dirpath_tmp,
                    dirs_exist_ok = True)

    command = 'cd {dir} && buildozer android debug deploy run'.format(
                                                            dir = dirpath_tmp)
    import da.env.run
    sys.exit(da.env.run.shell_command(
                            command     = command,
                            id_env      = 'e002_general_research',
                            id_env_boot = 'e000_design_automation_core',
                            acct        = 'wtp',
                            host        = 'localhost'))



