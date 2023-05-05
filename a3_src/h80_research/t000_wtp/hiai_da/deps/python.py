# -*- coding: utf-8 -*-
"""
Functions to support preparing python libraries for use.

---
type:
    python_module

validation_level:
    v00_minimum

protection:
    k00_public

copyright:
    "Copyright 2019 High Integrity Artificial Intelligence Systems"

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

import contextlib
import copy
import logging
import os
import shutil
import subprocess

import da.exception
import da.log
import da.lwc
import da.lwc.discover
import da.lwc.env
import da.lwc.run
import da.util


# -----------------------------------------------------------------------------
@da.log.trace
def build(extra_args,
          register_entry,
          dep_build_cfg,
          dirpath_lwc_root):
    """
    Build the specified application or library using distutils. (Python 2 & 3).

    It is possible for a single dependency to offer
    multiple interfaces through which clients may
    interact with it.

    For example, a library such as OpenCV offers a
    C API; a C++ API; a Python 2 API and a Python 3
    API.

    This function is supports building Python 2
    and Python 3 APIs and will build both if the
    dependency offers them.

    ---
    type:   function
    ...

    """
    dependency_apis = set(register_entry['api'].keys())    # Offered by dep.
    supported_apis  = set(('lib_python2', 'lib_python3'))  # Supported by us.
    apis_to_build   = dependency_apis & supported_apis     # Set intersection.

    for api_name in apis_to_build:
        _build_api(api_name         = api_name,
                   extra_args       = extra_args,
                   register_entry   = register_entry,
                   dep_build_cfg    = dep_build_cfg,
                   dirpath_lwc_root = dirpath_lwc_root)


# -----------------------------------------------------------------------------
@da.log.trace
def _build_api(api_name,
               extra_args,
               register_entry,
               dep_build_cfg,
               dirpath_lwc_root):
    """
    Call the python build command.

    TODO: Spend some more time thinking about how
          the concept of interfaces intersects with
          setuptools concepts like entrypoints.

    ---
    type:   function
    ...

    """
    # Which python binary do we need to call to generate this api?
    #
    python_fcn = _select_python_binary(api_name)

    # Which setuptools or distutils setup script do we use?
    #
    dependency_name = register_entry['name']
    dirpath_src     = register_entry['dirpath_src']
    filepath_setup  = _filepath_setup_or_throw(dependency_name, dirpath_src)

    # Temporary directory for build output.
    #
    policy_name       = register_entry['policy']
    relpath_api       = register_entry['api'][api_name]['relpath']
    dirpath_build_tmp = os.path.join(register_entry['rootpath_dep_bin'],
                                     'build',
                                     policy_name,
                                     dep_build_cfg['build_id'],
                                     relpath_api)

    # Final install directory for build output.
    #
    dirpath_build_out = os.path.join(register_entry['dirpath_policy_bin'],
                                     relpath_api)

    # PYTHONPATH and other environment variables needed by the build.
    #
    env = _environment_vars(api_name, dirpath_build_tmp, dirpath_lwc_root)

    # Log directory.
    #
    dirpath_log  = os.path.join(dep_build_cfg['rootpath_log'],
                                dependency_name,
                                policy_name,
                                relpath_api)

    with _open_log_files(dirpath_log) as log_files:

        (fp_log_stderr,
         fp_log_stdout,
         filepath_log_files,
         filepath_log_stderr) = log_files

        build_command = _build_command(
                                filepath_setup     = filepath_setup,
                                filepath_log_files = filepath_log_files,
                                dirpath_build_tmp  = dirpath_build_tmp,
                                extra_args         = extra_args)

        logging.debug('Dependency         = %s.', dependency_name)
        logging.debug('API name           = %s.', api_name)
        logging.debug('Temp build path    = %s.', dirpath_build_tmp)
        logging.debug('Final install path = %s.', dirpath_build_out)
        logging.debug('Build command      = %s.', ' '.join(build_command))

        with _clean_build_dirs(dirpath_src, dirpath_build_tmp):
            try:

                python_fcn(
                        build_command,
                        cwd              = dirpath_src,
                        stdout           = fp_log_stdout,
                        stderr           = fp_log_stderr,
                        env              = env,
                        dirpath_lwc_root = dirpath_lwc_root)

            except subprocess.CalledProcessError as err:

                # If there was an error, tell the developer.
                #
                raise da.exception.AbortWithoutStackTrace(
                    message     = 'Dependency build failed:\n{msg}'.format(
                                                        msg = str(err)),
                    filepath    = filepath_log_stderr,
                    line_number = -1)

            else:

                # If there was no error, install.
                #
                _install(dirpath_build_tmp, dirpath_build_out)


# -----------------------------------------------------------------------------
def _environment_vars(api_name, dirpath_bak, dirpath_lwc_root):
    """
    Return the environment variables suitable for the specified build.

    ---
    type:   function
    ...

    """
    python_import_path = da.lwc.env.python_import_path(
                                        iface_name       = api_name,
                                        dirpath_lwc_root = dirpath_lwc_root)

    # Add the intermediate output directory to the PYTHONPATH
    # because setuptools/distutils will not install to a directory
    # that is not on the PYTHONPATH.
    #
    python_import_path.append(dirpath_bak)

    env = copy.copy(os.environ)
    env['PYTHONPATH']           = os.pathsep.join(python_import_path)
    env['KIVY_USE_SETUPTOOLS']  = '1'

    return env


# -----------------------------------------------------------------------------
def _select_python_binary(api_name):
    """
    Return the correct python binary to use for the specified api.

    ---
    type:   function
    ...

    """
    if api_name == 'lib_python2':
        python_fcn = da.lwc.run.python2
    elif api_name == 'lib_python3':
        python_fcn = da.lwc.run.python3
    else:
        raise da.exception.DesignNonconformity('api_name not recognised.')

    return python_fcn


# -----------------------------------------------------------------------------
def _filepath_setup_or_throw(dependency_name, dirpath_src):
    """
    Return the path of the setup.py script or throw if does not exist.

    ---
    type:   function
    ...

    """
    filepath_setup_script = os.path.join(dirpath_src, 'setup.py')
    if not os.path.isfile(filepath_setup_script):
        raise RuntimeError(
                'Could not find setup script for {dep}: {path}'.format(
                                        dep  = dependency_name,
                                        path = filepath_setup_script))
    return filepath_setup_script


# -----------------------------------------------------------------------------
@contextlib.contextmanager
def _clean_build_dirs(dirpath_src, dirpath_bak):
    """
    Ensure the build directories are clean before and after the build.

    ---
    type:   context_manager
    ...

    """
    dirpath_tmp = os.path.join(dirpath_src, 'build')

    # Ensure that we are performing a clean build
    # by removing the temporary in-source build
    # directory that is created by distutils by
    # default.
    #
    if os.path.isdir(dirpath_tmp):
        logging.debug('Remove previous temporary build directory.')
        shutil.rmtree(dirpath_tmp)

    # If we already have files in the output
    # directory, remove them so that we may
    # reduce the risk of unwanted files
    # contaminating our output.
    #
    if os.path.isdir(dirpath_bak):
        logging.debug('Remove previous installation directory.')
        shutil.rmtree(dirpath_bak)

    if os.path.isdir(dirpath_bak):
        raise RuntimeError(
            'Failed to remove previous installation dir: {dir}'.format(
                                                            dir = dirpath_bak))

    os.makedirs(dirpath_bak)

    (yield)

    # Once we are finished, we remove the (temporary)
    # build sub-directory in order that we may return
    # the source tree back to the state in which we
    # found it.
    #
    if os.path.isdir(dirpath_tmp):
        shutil.rmtree(dirpath_tmp)

    # If the temporary directoy still exists, then
    # something has gone wrong.
    #
    if os.path.isdir(dirpath_tmp):
        raise RuntimeError(
            'Failed to delete temporary directory: {dir}'.format(
                                                        dir = dirpath_tmp))


# -----------------------------------------------------------------------------
@contextlib.contextmanager
def _open_log_files(dirpath_log):
    """
    Return a tuple of build log filepaths.

    Ensure that the files don't exist (to prevent
    confusion with previous builds).

    ---
    type:   context_manager
    ...

    """
    # Ensure that the log directory exists
    #
    if not os.path.isdir(dirpath_log):
        os.makedirs(dirpath_log, exist_ok = True)

    # Delete old log-files (if any exist) so we
    # won't be confused or misled by them.
    #
    filepath_log_stderr = os.path.join(dirpath_log, 'stderr.log')
    if os.path.isfile(filepath_log_stderr):
        os.unlink(filepath_log_stderr)

    filepath_log_stdout = os.path.join(dirpath_log, 'stdout.log')
    if os.path.isfile(filepath_log_stdout):
        os.unlink(filepath_log_stdout)

    filepath_log_files  = os.path.join(dirpath_log, 'install_files.log')
    if os.path.isfile(filepath_log_files):
        os.unlink(filepath_log_files)

    with open(filepath_log_stderr, 'w') as fp_log_stderr:
        with open(filepath_log_stdout, 'w') as fp_log_stdout:

            yield (fp_log_stderr,
                   fp_log_stdout,
                   filepath_log_files,
                   filepath_log_stderr)


# -----------------------------------------------------------------------------
def _build_command(
            filepath_setup, filepath_log_files, dirpath_build_tmp, extra_args):
    """
    Return the build command.

    ---
    type:   function
    ...

    """
    build_command = [
        filepath_setup,
        'install',
        '--record='           + filepath_log_files,
        '--install-base='     + dirpath_build_tmp,
        '--install-platbase=' + dirpath_build_tmp,
        '--install-purelib='  + dirpath_build_tmp,
        '--install-platlib='  + dirpath_build_tmp,
        '--install-scripts='  + dirpath_build_tmp,
        '--install-headers='  + dirpath_build_tmp,
        '--install-data='     + dirpath_build_tmp]
    if extra_args is not None:
        build_command = build_command + extra_args
    return build_command


# -----------------------------------------------------------------------------
def _install(dirpath_build_tmp, dirpath_build_out):
    """
    Copy files from intermediate/backup location to final install destination.

    ---
    type:   function
    ...

    """
    if not os.path.isdir(dirpath_build_tmp):
        raise da.exception.UnitPreconditionViolation(
                                         'Cannot locate build output folder.')

    if os.path.isdir(dirpath_build_out):
        shutil.rmtree(dirpath_build_out)

    shutil.copytree(src = dirpath_build_tmp,
                    dst = dirpath_build_out)

    if not os.path.isdir(dirpath_build_out):
        raise da.exception.UnitPreconditionViolation(
                                         'Cannot locate install folder.')
