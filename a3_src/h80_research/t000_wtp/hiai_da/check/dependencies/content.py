# -*- coding: utf-8 -*-
"""
Functions to support dependencies register content validation.

---
type:
    python_module

validation_level:
    v00_minimum

protection:
    k00_public

copyright:
    "Copyright 2023 William Payne"

license:
    "Licensed under the Apache License, Version 2.0 (the License);
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an AS IS BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License."

requirements:
    "This design document may contain any number of requirements
    items embedded in comment blocks. Each requirements item
    that is present shall have one formal requirement statement
    with one modal verb. The modal verb shall be interpreted
    in accordance with iso29148:2011

    SHALL indicates a mandatory binding provision, the fulfillment
    of which must be proven through an appropriate test.

    WILL indicates a statement of fact; futurity; a declaration
    of purpose; or to establish a context or a limitation of use.
    These statements are not manadatory and not binding.

    SHOULD indicates a preference; a goal or an advantageous
    quality. These statements are not mandatory and not binding.

    MAY is used to grant permission or to make a suggestion.
    These statements are not mandatory and not binding."
...
"""

import os
import os.path
import subprocess

import git
import redbaron
import baron

import da.lwc.discover
import da.lwc.env
import da.util


# -----------------------------------------------------------------------------
def get_reference_data(dirpath_lwc_root):
    """
    Return dependency configuration data inferred from local storage.

    This is used for consistency checking. Treating
    this as reference data and comparing it with
    the actual dependency configuration reveals
    inconsistencies that may need to be resolved.

    ---
    type:   function
    ...

    """
    rootpath_src = da.lwc.discover.path(
                                    key              = 'env_src',
                                    dirpath_lwc_root = dirpath_lwc_root)

    reference_data = dict()
    for (entry_name, dirpath_entry_src, policy_name) in _gen_entries(
                                                               rootpath_src):
        dirpath_policy_src   = os.path.join(dirpath_entry_src, policy_name)
        api_config_on_disk   = _api_config_on_disk(dirpath_policy_src)
        scm_config_on_disk   = _scm_config_on_disk(dirpath_policy_src)
        build_config_on_disk = _build_config_on_disk(dirpath_policy_src)

        reference_data[entry_name] = {
            "dirname":      entry_name,
            "policy":       policy_name,
            "api":          api_config_on_disk,
            "config":       scm_config_on_disk,
            "build":        build_config_on_disk
        }

    da.lwc.env.set_register_absolute_paths(
                                        register         = reference_data,
                                        dirpath_lwc_root = dirpath_lwc_root)

    return reference_data


# -----------------------------------------------------------------------------
def _gen_entries(rootpath):
    """
    Generate dependency entry information from the directory structure on disk.

    ---
    type:   function
    ...

    """
    for (dirname, dirpath) in da.util.iter_dirs(rootpath):
        subdir_list = [
                item.name for item in os.scandir(dirpath) if item.is_dir()]

        last_subdir       = sorted(subdir_list)[-1]
        entry_name        = dirname
        dirpath_entry_src = dirpath
        policy_name       = last_subdir
        yield (entry_name, dirpath_entry_src, policy_name)


# -----------------------------------------------------------------------------
def _api_config_on_disk(dirpath_entry_src):
    """
    Return configuration for the dependency API.

    Return a best guess at an appropriate configuration for the dependency
    APIs.

    ---
    type:   function
    ...

    """
    relpath_api = os.path.join('lib', 'python3')
    api_config  = dict()
    if os.path.isfile(os.path.join(dirpath_entry_src, 'setup.py')):
        api_config['lib_python3'] = {
            'relpath': relpath_api
        }
    return api_config


# -----------------------------------------------------------------------------
def _scm_config_on_disk(dirpath_entry_src):
    """
    Return configuration for the dependency SCM tool.

    Return a best guess at an appropriate configuration for the source code
    configuration management tool for the specified dependency repository.

    ---
    type:   function
    ...

    """
    # Git.
    if os.path.isdir(os.path.join(dirpath_entry_src, '.git')):
        url    = _git_origin_url(dirpath_entry_src)
        if url is not None:
            method = 'automatic'
            tool   = 'git'
        else:
            method = 'manual'
            tool   = 'n/a'
            url    = 'n/a'

    # Mercurial.
    elif os.path.isdir(os.path.join(dirpath_entry_src, '.hg')):
        method = 'automatic'
        tool   = 'hg'
        url    = _hg_default_path(dirpath_entry_src)

    # Subversion.
    elif os.path.isdir(os.path.join(dirpath_entry_src, '.svn')):
        method = 'automatic'
        tool   = 'svn'
        url    = _svn_url(dirpath_entry_src)

    # Bazaar.
    elif os.path.isdir(os.path.join(dirpath_entry_src, '.bzr')):
        method = 'automatic'
        tool   = 'bzr'
        url    = _bzr_url(dirpath_entry_src)

    # Manual download.
    else:
        method = 'manual'
        tool   = 'n/a'
        url    = 'n/a'

    return {
        'method':  method,
        'tool':    tool,
        'url':     url
    }


# -----------------------------------------------------------------------------
def _git_origin_url(dirpath_entry_src):
    """
    Return the origin URL for the specified git local working copy.

    ---
    type:   function
    ...

    """
    repo   = git.Repo(dirpath_entry_src)
    if len(repo.remotes) == 0:
        url = None
    else:
        url = repo.remotes.origin.url.strip()
    return url


# -----------------------------------------------------------------------------
def _hg_default_path(dirpath_entry_src):
    """
    Return the default path for the specified mercurial local working copy.

    ---
    type:   function
    ...

    """
    cmd    = ['hg', 'paths', 'default']
    result = subprocess.run(cmd,
                            cwd    = dirpath_entry_src,
                            stdout = subprocess.PIPE,
                            check  = True)
    url    = result.stdout.decode('utf-8').strip()
    return url


# -----------------------------------------------------------------------------
def _svn_url(dirpath_entry_src):
    """
    Return the remote url for the specified subversion local working copy.

    ---
    type:   function
    ...

    """
    cmd    = ['svn', 'info', '--show-item', 'url']
    result = subprocess.run(cmd,
                            cwd    = dirpath_entry_src,
                            stdout = subprocess.PIPE,
                            check  = True)
    url    = result.stdout.decode('utf-8').strip()
    return url


# -----------------------------------------------------------------------------
def _bzr_url(dirpath_entry_src):
    """
    Return the remote url for the specified bazaar local working copy.

    ---
    type:   function
    ...

    """
    cmd    = ['bzr', 'info']
    result = subprocess.run(cmd,
                            cwd    = dirpath_entry_src,
                            stdout = subprocess.PIPE,
                            check  = True)
    for line in result.stdout.splitlines():
        line = line.strip()
        if line.startswith(b'parent branch:'):
            url = line[len('parent branch:'):].decode('utf-8').strip()
            return url
    url = 'n/a'
    return url


# -----------------------------------------------------------------------------
def _build_config_on_disk(dirpath_entry_src):
    """
    Return the build tool for the specified local working copy.

    ---
    type:   function
    ...

    """
    filepath_python_setup = os.path.join(dirpath_entry_src, 'setup.py')
    is_python             = os.path.isfile(filepath_python_setup)
    if not is_python:
        return {
            'method':  'manual',
            'tool':    'TBD'
        }

    build_tool = _python_setup_tool(filepath_python_setup)
    return {
        'method':   'automatic',
        'tool':     build_tool
    }


# -----------------------------------------------------------------------------
def _python_setup_tool(filepath_python_setup):
    """
    Return the tool used by the specified python setup file.

    ---
    type:   function
    ...

    """
    with open(filepath_python_setup, 'rt') as file_python_setup:
        python_setup_logic = file_python_setup.read()

    try:
        red = redbaron.RedBaron(python_setup_logic)
        import_nodes      = (   red.find_all('import')
                              + red.find_all('from_import'))
        distutils_imports = import_nodes.find_all('name', 'distutils')
        has_distutils     = distutils_imports is not None

    # If redbaron parsing fails, then fall back to
    # simple string matching. The redbaron parsing
    # can fail when a setup script contains one or
    # more function definitions with PEP 3107 return
    # type annotations.
    #
    except baron.parser.ParsingError:
        has_distutils = 'distutils' in python_setup_logic

    tool = 'python_distutils' if has_distutils else 'python_setuptools'
    return tool
