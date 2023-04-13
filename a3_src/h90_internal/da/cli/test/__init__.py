# -*- coding: utf-8 -*-
"""
---

title:
    "Test commands package."

description:
    "This package provides commands to run
    various build system processes and
    operations."

id:
    "f47fdf01-e6eb-4c4b-ae69-3f55a7090794"

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
import subprocess


# -----------------------------------------------------------------------------
def all(dirpath_src):
    """
    Run all tests.

    """
    import pytest

    relpath_ini  = 'h90_internal/da/cli/test/pytest.ini'
    filepath_ini = os.path.join(dirpath_src, relpath_ini)

    # os.chdir(dirpath_lwc_root)
    print(dirpath_src)
    exit_code = pytest.main([
        dirpath_src,
        # '-vvv',
        # '-k=' + 'it_supports_feedback_loops',
        '-c=' + filepath_ini])

    print(exit_code)

    # # Define test result files.
    # filepath_pytest_log   = os.path.join(dirpath_log, 'pytest.log')
    # filepath_pytest_out   = os.path.join(dirpath_log, 'pytest_out.log')
    # filepath_pytest_err   = os.path.join(dirpath_log, 'pytest_err.log')
    # filepath_junit_xml    = os.path.join(dirpath_log, 'pytest.junit.xml')
    # filepath_pytest_json  = os.path.join(dirpath_log, 'pytest.json')
    # filepath_cover_pickle = os.path.join(dirpath_log, 'test_cover.pickle')
    # filepath_cover_json   = os.path.join(dirpath_log, 'test_cover.json')

    # # Run a py.test session for the current module's test cases.
    # with da.util.cwd_context(dirpath_cwd = dirpath_src):
    #     with da.util.stdio_context(filepath_stdout = filepath_pytest_out,
    #                                filepath_stderr = filepath_pytest_err,
    #                                enable = True):
    #         exit_code = pytest.main(
    #                         [filepath_test,
    #                          '-p', 'da.check.pytest.plugin',
    #                          # '-m', 'ci'
    #                          '--capture=no',
    #                          '-vv',
    #                          '-c='             + filepath_ini,
    #                          '--result-log='   + filepath_pytest_log,
    #                          '--junit-xml='    + filepath_junit_xml,
    #                          '--json='         + filepath_pytest_json,
    #                          '--coverage-log=' + filepath_cover_pickle])