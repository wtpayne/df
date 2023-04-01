# -*- coding: utf-8 -*-
"""
---

title:
    "Virtual environment management package."

description:
    "This package is used to create and update
    virtual environments of various types."

id:
    "1535294d-eedc-4d08-8721-31be6ecbef43"

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


"""


# Be careful not to import anything that won't be
# present in the host system. We should be safe
# as long as we stick to python3 builtin libraries
# and functions only.
#
import json
import os.path
import subprocess


# -----------------------------------------------------------------------------
def ensure_updated(rootpath, id_env):
    """
    Ensure the specified environment is up to date with the latest envspec.

    """
    envspec       = _load_envspec(rootpath, id_env)
    filepath_reqs = _create_requirements_file(rootpath, id_env, envspec)
    _install_requirements(filepath_reqs)


# -----------------------------------------------------------------------------
def _load_envspec(rootpath, id_env):
    """
    Return the envspec data for the specified environment id.

    """
    dirpath  = os.path.join(rootpath, 'a3_src/h10_resource/envspec')
    filename = '.'.join((id_env, 'envspec.json'))
    filepath = os.path.join(dirpath, filename)
    with open(filepath, 'rt') as file:
        return json.load(file)


# -----------------------------------------------------------------------------
def _create_requirements_file(rootpath, id_env, envspec):
    """
    Return temporary requirements.txt filepath after writing envspec data to it.

    """

    filepath = _filepath_requirements(rootpath, id_env)
    dirpath  = os.path.dirname(filepath)
    if not os.path.exists(dirpath):
       os.makedirs(dirpath)

    with open(filepath, 'wt') as file_reqs:
        _write = lambda msg: print(msg, file = file_reqs)
        for item in envspec['list_item']:
            _process_requirement_item(rootpath, item, _write)
        _write('')

    return filepath


# -----------------------------------------------------------------------------
def _filepath_requirements(rootpath, id_env):
    """
    Return the filepath of the temp requirements file for the specified env.

    """
    return os.path.join(rootpath, 'a4_tmp', id_env, 'requirements.txt')


# -----------------------------------------------------------------------------
def _process_requirement_item(rootpath, item, _write):
    """
    Write a single lines to the requirements file.

    """
    if isinstance(item, str):

        _write(item)

    elif item['type'] == 'pep508':

        _write(item['spec'])

    elif item['type'] == 'local':


        _write('-e {dirpath_dep}'.format(
                    dirpath_dep = os.path.join(rootpath, item['relpath'])))

    elif item['type'] == 'github':

        _write('-e {dirpath_dep}'.format(
                    dirpath_dep = _ensure_cloned_fron_github(
                                                url_remote = item['remote'],
                                                tag        = item['tag'],
                                                rootpath   = rootpath)))


# -----------------------------------------------------------------------------
def _ensure_cloned_fron_github(url_remote, tag, rootpath):
    """
    Ensure that specified github repository is cloned to local storage.

    """
    (_, user_and_path) = url_remote.split(':')
    (user, repo_path)  = user_and_path.split('/', maxsplit = 1)
    (repo_name, _)     = repo_path.rsplit('.', maxsplit = 1)
    dirpath_env        = os.path.join(rootpath, 'a0_env/src')
    dirpath_dep        = os.path.join(dirpath_env, user, repo_name)
    is_already_cloned  = os.path.exists(dirpath_dep)

    if not is_already_cloned:
        os.makedirs(dirpath_dep)
        subprocess.run(['git', 'clone', url_remote, dirpath_dep])

    subprocess.run(['git', 'checkout', tag], cwd = dirpath_dep)

    return dirpath_dep


# -----------------------------------------------------------------------------
def _install_requirements(filepath_reqs):
    """
    Install the dependencies specified in the given requirements file.

    We also always ensure that the wheel package
    is installed first, as some of the other
    packages require it before they can be
    installed.

    """
    subprocess.run(['pip', 'install', 'wheel'])
    subprocess.run(['pip', 'install', '-r', filepath_reqs])
