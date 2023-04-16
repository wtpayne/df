# -*- coding: utf-8 -*-
"""
---

title:
    "Virtual environment run utilities module."

description:
    "This module contains functions to run
    various different programs in virtual
    environments of various types."

id:
    "cb568718-71d7-443d-b2ce-918faf27bd99"

type:
    dt003_python_module

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


"""


# Since this module is called during the bootstrap
# process, we need to be careful not to depend on
# too many things that won't be present in the
# host environment. (i.e. before any of our
# managed environments get activated).
#
# We make an exception for the shell commands
# pip3 and git, which we require to be installed
# beforehand -- but other than that we should
# seek to stick to python3 builtin libraries
# and unix coreutils only.
#
import os.path
import subprocess


# -----------------------------------------------------------------------------
def shell_command(command, id_env, id_env_boot, acct, host):
    """
    Run a shell command in the specified environment.

    """
    dirpath_self      = os.path.dirname(os.path.realpath(__file__))
    relpath_root      = '../../../..'
    mixpath_root      = os.path.join(dirpath_self, relpath_root)
    dirpath_root      = os.path.normpath(mixpath_root)
    rootpath_venv     = os.path.join(dirpath_root, 'a0_env', 'venv')

    relpath_py        = os.path.join('bin', 'python3')
    relpath_act       = os.path.join('bin', 'activate')

    filepath_py_boot  = os.path.join(rootpath_venv, id_env_boot, relpath_py)
    filepath_act_boot = os.path.join(rootpath_venv, id_env_boot, relpath_act)
    filepath_act      = os.path.join(rootpath_venv, id_env,      relpath_act)

    ssh               = 'ssh -X'
    module_update     = 'da.env.ensure_updated'

    cmd_update_env    = '. {act} && {py3} -m {module} {root} {env}'.format(
                                            act     = filepath_act_boot,
                                            py3     = filepath_py_boot,
                                            module  = module_update,
                                            root    = dirpath_root,
                                            env     = id_env)
    cmd_run_shell     = '. {act} && {command}'.format(
                                            act     = filepath_act,
                                            command = command)

    ssh_update_env    = '{ssh} {acct}@{host} "{cmd}"'.format(
                                            ssh     = ssh,
                                            acct    = acct,
                                            host    = host,
                                            cmd     = cmd_update_env)
    ssh_run_shell     = '{ssh} {acct}@{host} "{cmd}"'.format(
                                            ssh     = ssh,
                                            acct    = acct,
                                            host    = host,
                                            cmd     = cmd_run_shell)

    subprocess.run(ssh_update_env, shell = True, check = True)
    subprocess.run(ssh_run_shell,  shell = True, check = True)


# -----------------------------------------------------------------------------
def python_module(module, id_env, id_env_boot, acct, host):
    """
    Run a python module in the specified environment.

    """
    dirpath_self      = os.path.dirname(os.path.realpath(__file__))
    relpath_root      = '../../../..'
    mixpath_root      = os.path.join(dirpath_self, relpath_root)
    dirpath_root      = os.path.normpath(mixpath_root)
    rootpath_venv     = os.path.join(dirpath_root, 'a0_env', 'venv')

    relpath_py        = os.path.join('bin', 'python3')
    relpath_act       = os.path.join('bin', 'activate')

    filepath_py_boot  = os.path.join(rootpath_venv, id_env_boot, relpath_py)
    filepath_py_env   = os.path.join(rootpath_venv, id_env,      relpath_py)

    filepath_act_boot = os.path.join(rootpath_venv, id_env_boot, relpath_act)
    filepath_act      = os.path.join(rootpath_venv, id_env,      relpath_act)

    ssh               = 'ssh -X'
    module_update     = 'da.env.ensure_updated'

    cmd_update_env    = '. {act} && {py3} -m {module} {root} {env}'.format(
                                            act    = filepath_act_boot,
                                            py3    = filepath_py_boot,
                                            module = module_update,
                                            root   = dirpath_root,
                                            env    = id_env)
    cmd_run_module    = '. {act} && {py3} -m {module}'.format(
                                            act    = filepath_act,
                                            py3    = filepath_py_env,
                                            module = module)

    ssh_update_env    = '{ssh} {acct}@{host} "{cmd}"'.format(
                                            ssh    = ssh,
                                            acct   = acct,
                                            host   = host,
                                            cmd    = cmd_update_env)
    ssh_run_module    = '{ssh} {acct}@{host} "{cmd}"'.format(
                                            ssh    = ssh,
                                            acct   = acct,
                                            host   = host,
                                            cmd    = cmd_run_module)

    subprocess.run(ssh_update_env, shell = True, check = True)
    subprocess.run(ssh_run_module, shell = True, check = True)


