# -*- coding: utf-8 -*-
"""
---

title:
    "Build system commands package."

description:
    "This package provides commands to run
    various build system processes and
    operations."

id:
    "4edea1be-2fb8-42f4-aae2-aaeea56a3997"

type:
    dt002_python_package

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


import os
import os.path

import stableflow.cfg
import stableflow.cfg.exception
import stableflow.log
import stableflow.sys


# -----------------------------------------------------------------------------
def _dirpath_demo(dirpath_src, name_demo):
    """
    Return the path to demos.

    """
    return os.path.join(dirpath_src, 'h60_demo', name_demo)


# -----------------------------------------------------------------------------
def _filepath_cfg(dirpath_src, name_demo):
    """
    Return the file path of the configuration data for the demo.

    """
    dirpath_demo  = _dirpath_demo(dirpath_src, name_demo)
    filename_cfg  = '{name}.stableflow.cfg.yaml'.format(name = name_demo)
    return os.path.join(dirpath_demo, filename_cfg)


# -----------------------------------------------------------------------------
def _filepath_entrypoint(dirpath_src, name_demo):
    """
    Return the file path of the entrypoint script for the demo.

    """
    dirpath_demo        = _dirpath_demo(dirpath_src, name_demo)
    filename_entrypoint = '{name}.py'.format(name = name_demo)
    return os.path.join(dirpath_demo, filename_entrypoint)


# -----------------------------------------------------------------------------
def start(dirpath_src, name_demo):
    """
    Start the specified demo.

    """
    filepath_cfg = _filepath_cfg(dirpath_src, name_demo)
    if os.path.exists(filepath_cfg):
        return da.stableflow.start(path_cfg = filepath_cfg)

    filepath_py = _filepath_entrypoint(dirpath_src, name_demo)
    if os.path.exists(filepath_py):
        _start_entrypoint_script(filepath_py)


# -----------------------------------------------------------------------------
def _start_entrypoint_script(filepath_py):
    """
    Run the specified entrypoint script in the current process.

    """
    import importlib
    import os
    import sys

    (dirpath, filename_py) = os.path.split(filepath_py)
    (modulename, _) = os.path.splitext(filename_py)
    sys.path.append(dirpath)
    module = importlib.import_module(modulename)
    sys.argv[:] = [filepath_py]
    return module.main()


# -----------------------------------------------------------------------------
def stop(dirpath_src, name_demo):
    """
    Stop the specified demo stableflow system.

    """
    filepath_cfg = _filepath_cfg(dirpath_src, name_demo)
    if os.path.exists(filepath_cfg):
        return da.stableflow.stop(path_cfg = filepath_cfg)
