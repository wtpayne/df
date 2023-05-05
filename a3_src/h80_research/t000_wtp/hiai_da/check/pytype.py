# -*- coding: utf-8 -*-
"""
Module containing mypy type checking coroutines.

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


import os
import subprocess

import da.check.constants
import da.lwc.file
import da.util


# -----------------------------------------------------------------------------
@da.util.coroutine
def coro(dirpath_lwc_root, build_monitor):
    """
    Send errors to build_monitor if supplied files not compliant with pep8.

    ---
    type:   coroutine
    ...

    """
    filepath_mypy = da.lwc.env.cli_path(
                                dependency_id    = 'mypy',
                                application_name = 'mypy',
                                dirpath_lwc_root = dirpath_lwc_root)

    # TODO: Figure out a way of correctly
    #       installing MyPy so that we do
    #       not need this typeshed path
    #       hack business.
    dirpath_typeshed = os.path.abspath(
                            os.path.join(
                                os.path.dirname(filepath_mypy),
                                '../lib/mypy/typeshed'))

    # Run main file-processing loop: recieve file
    # paths from outside the coroutine and send
    # them one at a time to mypy.
    #
    while True:

        build_unit = (yield)
        filepath   = build_unit['filepath']

        # Ignore non-python design documents.
        if not da.lwc.file.is_python_file(filepath):
            continue

        # Ignore experimental design documents.
        if da.lwc.file.is_experimental(filepath):
            continue

        # Ensure the test results dir exists.
        dirpath_log = build_unit['dirpath_log']
        da.util.ensure_dir_exists(dirpath_log)

        filepath_junit_xml = os.path.join(dirpath_log, 'pytype.junit.xml')

        # Call mypy as a subprocess.
        # As of 20161213 the MyPy API is waiting
        # to be merged.
        #
        #   https://github.com/python/mypy/pull/2439
        #
        # Until this is merged, we have to invoke
        # MyPy as a separate process. :-(
        #
        mypy_command = [
            filepath_mypy,
            '--silent-imports',
            '--show-column-numbers',
            '--junit-xml={file}'.format(file = filepath_junit_xml),
            '--custom-typeshed-dir={dir}'.format(dir = dirpath_typeshed),
            filepath]

        process  = subprocess.Popen(mypy_command,
                                    stdout = subprocess.PIPE,
                                    stderr = subprocess.PIPE)
        out, err = process.communicate()
        exitcode = process.returncode
        isok     = exitcode == 0
        if isok:
            continue

        # Any text output to stderr indicates that
        # a fatal error has occurred in MyPy.
        #
        if err:
            err_str = err.decode('utf8')
            raise RuntimeError('Error in MyPy: {err}'.format(err = err_str))

        # Regular nonconformities are reported
        # via messages on stdout. Fields are
        # colon-delimited, but a variable number
        # of fields may be present.
        #
        # ref: mypy.errors.Errors.messages, lines 238-260
        #
        for line_of_output in out.decode('utf8').splitlines():

            (message, reported_path, line_num, col_num) = _parse_line(
                                                    line_of_output, filepath)

            build_monitor.report_nonconformity(
                tool    = 'da.check.pytype',
                msg_id  = da.check.constants.MYPY_NONCONFORMITY,
                msg     = message,
                path    = reported_path,
                line    = line_num,
                col     = col_num)


# -----------------------------------------------------------------------------
def _parse_line(line_of_output, filepath):
    """
    Return values parsed from one line of MyPy output.

    ---
    type:   function
    ...

    """
    # Parse one line of MyPy output.
    line_parts = ':'.split(line_of_output)
    num_parts  = len(line_parts)

    # Set default values
    reported_path = filepath
    severity      = 'Error'
    line_num      = 1
    col_num       = 0

    if num_parts == 5:
        (reported_path,
         line_num,
         col_num,
         severity,
         reported_msg) = line_parts

    elif num_parts == 4:
        (reported_path,
         line_num,
         severity,
         reported_msg) = line_parts

    elif num_parts == 3:
        (reported_path,
         severity,
         reported_msg) = line_parts

    elif num_parts == 2:
        (severity,
         reported_msg) = line_parts

    else:
        reported_msg = line_of_output

    message = '{sev}: {msg}'.format(
                                sev = severity,
                                msg = reported_msg)

    return (message, reported_path, line_num, col_num)
