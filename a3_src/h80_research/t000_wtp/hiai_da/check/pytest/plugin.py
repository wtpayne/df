# -*- coding: utf-8 -*-
"""
Plugin to adapt and configure py.test for use with development automation.

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


import figleaf
import pytest


# -----------------------------------------------------------------------------
def pytest_addoption(parser):
    """
    Add DA options to the pytest command line.

    """
    group = parser.getgroup('DA', 'Development Automation options.')
    group.addoption('--coverage-log', action = 'store',
                                       type   = 'string')


# -----------------------------------------------------------------------------
def pytest_sessionstart(session):                       # pylint: disable=W0613
    """
    Start figleaf coverage reporting.

    """
    figleaf.start()


# -----------------------------------------------------------------------------
def pytest_runtest_setup(item):
    """
    Notify figleaf that a new testcase/section is about to start.

    """
    figleaf.start_section(item.nodeid)


# -----------------------------------------------------------------------------
def pytest_runtest_teardown(item, nextitem):            # pylint: disable=W0613
    """
    Notify figleaf that the current testcase/section has just ended.

    """
    figleaf.stop_section()


# -----------------------------------------------------------------------------
def pytest_sessionfinish(session, exitstatus):          # pylint: disable=W0613
    """
    Write out figleaf coverage report for the test session.

    """
    figleaf.stop()
    filepath_coverage_log = session.config.known_args_namespace.coverage_log
    with open(filepath_coverage_log, 'wb') as file:
        figleaf.dump_pickled_coverage(file)


# -----------------------------------------------------------------------------
@pytest.fixture(scope = 'session')
def dirpath_lwc_root():
    """
    Return the directory path to the root of the local working copy.

    """
    import da.lwc.discover
    return da.lwc.discover.path(key = 'root')
