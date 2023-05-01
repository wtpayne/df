# -*- coding: utf-8 -*-
"""
---

title:
    "dm005_workflow_engine demo commands."

description:
    "This module defines commands for the 
    dm005_workflow_engine demonstration."

id:
    "87df2f55-214e-40be-9330-53cf354817ef"

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
def test():
    """
    Run all dm005 tests.

    """
    import da.env
    import da.test

    _run   = da.test.run
    _path  = da.env.path
    ID_ENV = 'e002_general_research'

    return _run(id_env    = ID_ENV,
                iter_path = (_path(control_tier = 'h20_functionality',
                                   relpath      = 'fl/stableflow',
                                   id_env       = ID_ENV),
                             _path(control_tier = 'h20_functionality',
                                   relpath      = 'fl/test',
                                   id_env       = ID_ENV),
                             _path(control_tier = 'h20_functionality',
                                   relpath      = 'fl/net/openai',
                                   id_env       = ID_ENV),
                             _path(control_tier = 'h40_component',
                                   relpath      = 'cl/net/openai',
                                   id_env       = ID_ENV),
                             _path(control_tier = 'h50_product',
                                   relpath      = '.',
                                   id_env       = ID_ENV)))


# -----------------------------------------------------------------------------
def start():
    """
    Start dm005 system.

    """
    # tup_overrides = ('host.localhost.dirpath_log',      _dirpath_log_server(),
    #                  'node.client.config.filepath_env', _filepath_dotenv())
    tup_overrides = None

    import da.env.run
    sys.exit(da.env.run.stableflow_start(path_cfg      = _filepath_cfg(),
                                         tup_overrides = tup_overrides))


# -----------------------------------------------------------------------------
def stop():
    """
    Stop dm005 system.

    """
    import da.env.run
    sys.exit(da.env.run.stableflow_stop(path_cfg = _filepath_cfg()))


# -----------------------------------------------------------------------------
def _dirpath_log_server():
    """
    Return the directory path to the logging directory for this system.

    """
    import da.env
    return da.env.path(process_area = 'a4_tmp',
                       control_tier = 'h70_research',
                       relpath      = 'workflow_engine')


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
def _filepath_cfg():
    """
    Return the filepath to the backend server stableflow configuration file.

    """
    import da.env

    reldir_cfg   = 'dm005_workflow_engine'
    filename_cfg = 'dm005_workflow_engine.stableflow.cfg.yaml'
    relpath_cfg  = os.path.join(reldir_cfg, filename_cfg)

    return da.env.path(process_area = 'a3_src',
                       control_tier = 'h80_demonstration',
                       relpath      = relpath_cfg)

