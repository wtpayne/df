# -*- coding: utf-8 -*-
"""
---

title:
    "dm005_routine demo commands."

description:
    "This module defines commands for the 
    dm005_routine demonstration."

id:
    "d90a16a3-f522-4e98-ab67-35ff9136be21"

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
import sys


# -----------------------------------------------------------------------------
def start():
    """
    Start dm001 system.

    """
    tup_overrides = ('host.localhost.dirpath_log',          _dirpath_log(),
                     'node.discord.config.filepath_dotenv', _filepath_dotenv())

    import da.env.run
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
def _dirpath_log():
    """
    Return the directory path to the logging directory for this system.

    """
    import da.env
    return da.env.path(process_area = 'a4_tmp',
                       control_tier = 'h80_research',
                       relpath      = 'dm005_routine')


# -----------------------------------------------------------------------------
def _filepath_dotenv():
    """
    Return the filepath to the dotenv .env file containing the API key.

    """
    import da.env
    return da.env.path(
                process_area = 'a3_src',
                control_tier = 'h10_resource',
                relpath      = 'key/default.env')


# -----------------------------------------------------------------------------
def _filepath_cfg():
    """
    Return the filepath to the backend server stableflow configuration file.

    """
    import da.env
    return da.env.path(
                process_area = 'a3_src',
                control_tier = 'h60_system',
                relpath      = 'routine/routine.stableflow.cfg.yaml')
