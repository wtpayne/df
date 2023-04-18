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
import shutil
import sys


# -----------------------------------------------------------------------------
def app():
    """
    Run dm004 frontend mobile app.

    """
    import da.env.run
    sys.exit(da.env.run.python_module(module = 'forever.library.main',
                                      id_env = 'e002_general_research'))


# -----------------------------------------------------------------------------
def server_start():
    """
    Start dm004 backend server.

    """
    import da.env
    import da.env.run
    dirpath_cfg  = da.env.path(process_area = 'a3_src',
                               control_tier = 'h70_research',
                               relpath      = 'forever/library')
    filepath_cfg = os.path.join(dirpath_cfg, 'forever.stableflow.cfg.yaml')
    sys.exit(da.env.run.stableflow_start(path_cfg = filepath_cfg))


# -----------------------------------------------------------------------------
def server_stop():
    """
    Stop dm004 backend server.

    """
    import da.env
    import da.env.run
    dirpath_cfg  = da.env.path(process_area = 'a3_src',
                               control_tier = 'h70_research',
                               relpath      = 'forever/library')
    filepath_cfg = os.path.join(dirpath_cfg, 'forever.stableflow.cfg.yaml')
    sys.exit(da.env.run.stableflow_stop(path_cfg = filepath_cfg))


# -----------------------------------------------------------------------------
def build_android():
    """
    Build dm004 for Android.

    """
    import da.env
    import da.env.run

    # Recursively copy the source design
    # documents to the temporary build
    # area.
    #
    dirpath_src = da.env.path(process_area = 'a3_src',
                              control_tier = 'h70_research',
                              relpath      = 'forever/library')
    dirpath_tmp = da.env.path(process_area = 'a4_tmp',
                              control_tier = 'h70_research',
                              relpath      = 'forever/library')
    shutil.copytree(dirpath_src, dirpath_tmp, dirs_exist_ok = True)

    # Now build from the temporary build area.
    #
    command = 'cd {dir} && buildozer android debug deploy run'.format(
                                                            dir = dirpath_tmp)
    sys.exit(da.env.run.shell_command(command = command,
                                      id_env  = 'e002_general_research'))


# -----------------------------------------------------------------------------
def test():
    """
    Run dm004 tests.

    """
    import da.env
    dirpath = da.env.path(process_area = 'a3_src',
                          control_tier = 'h70_research')
    print(dirpath)
