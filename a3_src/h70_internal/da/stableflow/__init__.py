# -*- coding: utf-8 -*-
"""
---

title:
    "Design factory stableflow support package."

description:
    "This package provides commands to start
    and stop stableflow systems within design
    factory managed environments."

id:
    "f411b031-321e-44b7-8c21-470491382524"

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
import sys

import stableflow.cfg
import stableflow.cfg.exception
import stableflow.log
import stableflow.sys

import da.env


# -----------------------------------------------------------------------------
def start(path_cfg, tup_overrides):
    """
    Start the specified system.

    """
    with stableflow.log.logger.catch(onerror = lambda _: sys.exit(1)):

        try:

            cfg = stableflow.cfg.prepare(
                                    path_cfg      = path_cfg,
                                    tup_overrides = tup_overrides)

            _update_all_environments(cfg)
            _configure_all_launch_commands(cfg)

        except stableflow.cfg.exception.CfgError as err:
            print(err, file = sys.stderr)  # Custom message (no stack trace)
            return 1

        else:
            try:
                return stableflow.sys.start(cfg)
            except Exception as err:
                # An exception will be thrown
                # when we need to display either
                # a custom error message, or no
                # error message at all.
                #
                err_msg = str(err)
                if err_msg != '':
                    print(err_msg, file = sys.stderr)
                return 1


# -----------------------------------------------------------------------------
def stop(path_cfg):
    """
    Stop monitoring.

    """
    with stableflow.log.logger.catch(onerror = lambda _: sys.exit(1)):

        try:
            cfg = stableflow.cfg.prepare(path_cfg = path_cfg)
        except stableflow.cfg.exception.CfgError as err:
            print(err, file = sys.stderr)  # Custom message (no stack trace)
            return 1

        else:
            try:
                return stableflow.sys.stop(cfg)
            except Exception as err:
                # An exception will be thrown
                # when we need to display either
                # a custom error message, or no
                # error message at all.
                #
                err_msg = str(err)
                if err_msg != '':
                    print(err_msg, file = sys.stderr)
                return 1


# -----------------------------------------------------------------------------
def _update_all_environments(cfg):
    """
    Update all environments used by the specified cfg.

    TODO: Run these on remote hosts also.

    """
    dirpath_root = _dirpath_root()
    for cfg_host in cfg['host'].values():
        try:
            da.env.ensure_updated(rootpath = dirpath_root,
                                  id_env   = cfg_host['environment'])
        except KeyError:
            pass


# -----------------------------------------------------------------------------
def _configure_all_launch_commands(cfg):
    """
    Set each launch command as required for each host environment.

    """
    for cfg_host in cfg['host'].values():

        try:
            id_env       = cfg_host['environment']
            dirpath_env  = os.path.join(_dirpath_env(), 'venv', id_env)
            filepath_py3 = os.path.join(dirpath_env, 'bin', 'python3')
            launch_cmd   = '{python} -m stableflow.cli.command'.format(
                                                        python = filepath_py3)
            cfg_host['launch_cmd'] = launch_cmd
        except KeyError:
            pass


# -----------------------------------------------------------------------------
def _dirpath_env():
    """
    Return the path of the root directory of the environment filesystem.

    """
    return os.path.join(_dirpath_root(), 'a0_env')


# -----------------------------------------------------------------------------
def _dirpath_root():
    """
    Return the path of the root directory of the design factory filesystem.

    """
    return os.path.normpath(os.path.join(_dirpath_self(), '../../../..'))


# -----------------------------------------------------------------------------
def _dirpath_self():
    """
    Return the directory path to the current module.

    """
    return os.path.dirname(os.path.realpath(__file__))
