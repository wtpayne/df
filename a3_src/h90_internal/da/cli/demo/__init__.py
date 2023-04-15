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
import functools

import click

import da.cli.group
import da.stableflow
import stableflow.cfg
import stableflow.cfg.exception
import stableflow.log
import stableflow.sys


# -----------------------------------------------------------------------------
def add_demos(grp_parent):
    """
    """
    rootpath_demo = os.path.join(
                            _dirpath_root(), 'a3_src', 'h80_demonstration')

    for name in sorted(os.listdir(rootpath_demo)):

        path    = os.path.join(rootpath_demo, name)
        is_demo = os.path.isdir(path) and name.startswith('dm')
        if not is_demo:
            continue

        id_demo      = name
        dirpath_demo = path

        str_help     = 'Demo {id}.'.format(id = id_demo)
        grp_demo     = da.cli.group.Ordered(id_demo, help = str_help)
        num_demo     = id_demo.split(sep = '_', maxsplit = 1)[0]
        grp_parent.add_command(grp_demo, name = num_demo)

        filename_cfg = '{id}.stableflow.cfg.yaml'.format(id = id_demo)
        filepath_cfg = os.path.join(dirpath_demo, filename_cfg)
        filename_py  = '{id}.py'.format(id = id_demo)
        filepath_py  = os.path.join(dirpath_demo, filename_py)

        # Add start command for a standalone (or wrapper) script.
        #
        if os.path.exists(filepath_py):
            callback = functools.partial(_run_script, filepath_py)
            grp_demo.add_command(
                name = 'start',
                cmd  = click.Command(
                        name     = 'start',
                        callback = callback,
                        help     = 'Start {id}.'.format(id = id_demo)))

        # Add start command for a stableflow configuration file.
        #
        elif os.path.exists(filepath_cfg):
            callback = functools.partial(da.stableflow.start,
                                         path_cfg = filepath_cfg)
            grp_demo.add_command(
                name = 'start',
                cmd  = click.Command(
                        name     = 'start',
                        callback = callback,
                        help     = 'Start {id}.'.format(id = id_demo)))

        # Add stop command for a stableflow configuration file.
        #
        if os.path.exists(filepath_cfg):
            callback = functools.partial(da.stableflow.stop,
                                         path_cfg = filepath_cfg)
            grp_demo.add_command(
                name = 'stop',
                cmd  = click.Command(
                        name     = 'stop',
                        callback = callback,
                        help     = 'Stop {id}.'.format(id = id_demo)))


# -----------------------------------------------------------------------------
def _dirpath_root():
    """
    Return the directory path of the root of the repository.

    """
    dirpath_self = os.path.dirname(os.path.realpath(__file__))
    relpath_root = '../../../../..'
    dirpath_root = os.path.normpath(os.path.join(dirpath_self, relpath_root))
    return dirpath_root


# -----------------------------------------------------------------------------
def _run_script(filepath_py):
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
