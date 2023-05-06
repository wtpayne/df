# -*- coding: utf-8 -*-
"""
---

title:
    "dm004_forever_library demo commands."

description:
    "This module defines commands for the 
    dm004_forever_library demonstration."

id:
    "b1e5f9e5-0626-4900-968f-c300006c074e"

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
import shutil
import sys


ID_ENV       = 'e002_general_research'
ID_ENV_BUILD = ID_ENV


# -----------------------------------------------------------------------------
def app():
    """
    Run dm004 frontend mobile app.

    """
    import da.env.run
    sys.exit(da.env.run.python_module(module = 'forever.library.main',
                                      id_env = ID_ENV))


# -----------------------------------------------------------------------------
def server_start():
    """
    Start dm004 backend server.

    """
    tup_overrides = ('host.localhost.dirpath_log',      _dirpath_log_server(),
                     'node.client.config.filepath_env', _filepath_dotenv())

    import da.env.run
    sys.exit(da.env.run.stableflow_start(
                                    path_cfg      = _filepath_cfg_server(),
                                    tup_overrides = tup_overrides))


# -----------------------------------------------------------------------------
def server_stop():
    """
    Stop dm004 backend server.

    """
    import da.env.run
    sys.exit(da.env.run.stableflow_stop(path_cfg = _filepath_cfg_server()))


# -----------------------------------------------------------------------------
def build_android():
    """
    Build dm004 for Android.

    """
    import da.build
    sys.exit(da.build.kivy(control_tier   = 'h80_research',
                           relpath        = 'forever/library',
                           target         = 'android',
                           build          = 'debug',
                           do_deploy      = False,
                           id_env_build   = ID_ENV_BUILD))


# -----------------------------------------------------------------------------
def test():
    """
    Run dm004 tests.

    """
    import da.test
    sys.exit(da.test.run(control_tier = 'h80_research',
                         relpath      = 'forever/library',
                         id_env       = ID_ENV))


# -----------------------------------------------------------------------------
def _dirpath_log_server():
    """
    Return the directory path to the logging directory for this system.

    """
    import da.env
    return da.env.path(process_area = 'a4_tmp',
                       control_tier = 'h80_research',
                       relpath      = 'forever/library')


# -----------------------------------------------------------------------------
def _filepath_dotenv():
    """
    Return the filepath to the dotenv .env file containing the API key.

    """
    import da.env
    return da.env.path(
                process_area = 'a3_src',
                control_tier = 'h10_resource',
                relpath      = 'keys/openai.env')


# -----------------------------------------------------------------------------
def _filepath_cfg_server():
    """
    Return the filepath to the backend server stableflow configuration file.

    """
    import da.env
    return da.env.path(
                process_area = 'a3_src',
                control_tier = 'h80_research',
                relpath      = 'forever/library/forever.stableflow.cfg.yaml')
