# -*- coding: utf-8 -*-
"""
---

title:
    "dm001_workflow demo commands."

description:
    "This module defines commands for the 
    dm001_workflow demonstration."

id:
    "87df2f55-214e-40be-9330-53cf354817ef"

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
def test():
    """
    Run all dm001 tests.

    """
    import da.env
    import da.test

    _run   = da.test.run
    _path  = da.env.path
    ID_ENV = 'e002_general_research'

    return _run(id_env    = ID_ENV,
                iter_path = (_path(control_tier = 'h20_functionality',
                                   relpath      = 'fl/util',
                                   id_env       = ID_ENV),
                             _path(control_tier = 'h20_functionality',
                                   relpath      = 'fl/stableflow',
                                   id_env       = ID_ENV),
                             _path(control_tier = 'h20_functionality',
                                   relpath      = 'fl/test',
                                   id_env       = ID_ENV),
                             _path(control_tier = 'h20_functionality',
                                   relpath      = 'fl/net/openai',
                                   id_env       = ID_ENV),
                             _path(control_tier = 'h20_functionality',
                                   relpath      = 'fl/ui/gradio',
                                   id_env       = ID_ENV),
                             _path(control_tier = 'h30_platform',
                                   relpath      = 'pl/stableview',
                                   id_env       = ID_ENV),
                             _path(control_tier = 'h40_component',
                                   relpath      = 'cl/ctrl',
                                   id_env       = ID_ENV),
                             ## _path(control_tier = 'h40_component',
                             ##       relpath      = 'cl/db',
                             ##       id_env       = ID_ENV),
                             ## _path(control_tier = 'h40_component',
                             ##       relpath      = 'cl/eng',
                             ##       id_env       = ID_ENV),
                             ## _path(control_tier = 'h40_component',
                             ##       relpath      = 'cl/fs',
                             ##       id_env       = ID_ENV),
                             ## _path(control_tier = 'h40_component',
                             ##       relpath      = 'cl/gis',
                             ##       id_env       = ID_ENV),
                             ## _path(control_tier = 'h40_component',
                             ##       relpath      = 'cl/ml',
                             ##       id_env       = ID_ENV),
                             _path(control_tier = 'h40_component',
                                   relpath      = 'cl/net',
                                   id_env       = ID_ENV),
                             ## _path(control_tier = 'h40_component',
                             ##       relpath      = 'cl/nlp',
                             ##       id_env       = ID_ENV),
                             ## _path(control_tier = 'h40_component',
                             ##       relpath      = 'cl/ocr',
                             ##       id_env       = ID_ENV),
                             ## _path(control_tier = 'h40_component',
                             ##       relpath      = 'cl/pdf',
                             ##       id_env       = ID_ENV),
                             ## _path(control_tier = 'h40_component',
                             ##       relpath      = 'cl/rpa',
                             ##       id_env       = ID_ENV),
                             ## _path(control_tier = 'h40_component',
                             ##       relpath      = 'cl/sim',
                             ##       id_env       = ID_ENV),
                             ## _path(control_tier = 'h40_component',
                             ##       relpath      = 'cl/ui',
                             ##       id_env       = ID_ENV),
                             ## _path(control_tier = 'h40_component',
                             ##       relpath      = 'cl/util',
                             ##       id_env       = ID_ENV),
                             ## _path(control_tier = 'h40_component',
                             ##       relpath      = 'cl/vid',
                             ##       id_env       = ID_ENV),
                             _path(control_tier = 'h50_subsystem',
                                  relpath      = '.',
                                  id_env       = ID_ENV),
                             _path(control_tier = 'h60_system',
                                  relpath      = '.',
                                  id_env       = ID_ENV),
                             _path(control_tier = 'h70_bespoke',
                                   relpath      = '.',
                                   id_env       = ID_ENV)))


# -----------------------------------------------------------------------------
def editor():
    """
    Run the FlowForge editor.

    """
    import da.env.run

    dirpath_editor = da.env.path(
                            process_area = 'a3_src',
                            control_tier = 'h60_system',
                            relpath      = 'flowforge')
    sys.exit(da.env.run.python_function(
                            spec         = 'pl.stableview.main',
                            iter_args    = (dirpath_editor, 'main'),
                            id_env       = 'e002_general_research'))


# -----------------------------------------------------------------------------
def start():
    """
    Start dm001 system.

    """
    tup_overrides = ('host.localhost.dirpath_log',   _dirpath_log(),
                     'node.ace.config.filepath_env', _filepath_dotenv())

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

    reldir_cfg   = 'da/demo/dm001_workflow'
    filename_cfg = 'dm001_workflow.stableflow.cfg.yaml'
    relpath_cfg  = os.path.join(reldir_cfg, filename_cfg)

    return da.env.path(process_area = 'a3_src',
                       control_tier = 'h90_internal',
                       relpath      = relpath_cfg)

