# -*- coding: utf-8 -*-
"""
Unit tests for the da.monitor module.

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


import datetime
import os
import textwrap

import pytest


# -----------------------------------------------------------------------------
@pytest.fixture
def cfg(tmpdir):
    """
    Return a mock build configuration.

    """
    return {
            'build_id':                 'TEST_BUILD_ID',
            'cfg_name':                 'TEST_CFG_NAME',
            'relpath_cfg':              'TEST_CONFIG_FILE',
            'safe_branch_name':         'TEST_SAFE_BRANCH_NAME',
            'defined_baseline': {
                'commit_summary':       'TEST_COMMIT_SUMMARY'
            },
            'paths': {
                'rootpath_tmp':         os.path.join(str(tmpdir), 'tmp'),
                'dirpath_branch_dst':   os.path.join(str(tmpdir), 'dst'),
                'dirpath_isolated_src': os.path.join(str(tmpdir), 'iso'),
                'dirpath_lwc_root':     os.path.join(str(tmpdir), 'src')
            },
            'timestamp': {
                'datetime_utc':         datetime.datetime.utcnow()
            }
        }


# -----------------------------------------------------------------------------
@pytest.fixture
def build_unit():
    """
    Return a mock build unit.

    """
    return {
        'type':     'build_unit',
        'relpath':  'TEST_RELPATH'
    }


# -----------------------------------------------------------------------------
@pytest.fixture
def patch_progressbar(monkeypatch):
    """
    Monkeypatch the click.progress bar so it can run without a real tty.

    render_progress has a bug that manifests when we call it without a
    real tty. As a quick fix we simply disable the method here...

    """
    import click._termui_impl
    monkeypatch.setattr(
            click._termui_impl.ProgressBar, 'render_progress', lambda: None)


# =============================================================================
class SpecifyBuildMonitorReportProgress:
    """
    Specify the da.monitor.BuildMonitor.report_progress() function.

    """
    def it_reports_progress_to_console_and_to_file(
                        self, cfg, build_unit, capsys):
        """
        The report_progress() method prints reports to console and to file.

        """
        import da.monitor

        mon = da.monitor.BuildMonitor(cfg)

        # The BuildMonitor class constructor writes a header to the console.
        filepath_report = os.path.join(
                            cfg['paths']['dirpath_branch_dst'], 'build.html')
        (out, err) = capsys.readouterr()
        assert err == ''
        assert out == textwrap.dedent("""\
        Build id:       TEST_BUILD_ID
        Config file:    TEST_CONFIG_FILE
        Last commit:    TEST_COMMIT_SUMMARY
        Report:         file://{filepath_report}
        """.format(filepath_report = filepath_report))

        # The BuildMonitor class constructor writes a header to the file.
        assert os.path.isfile(filepath_report)
        with open(filepath_report, 'rt') as file:
            report_header = file.read()
        assert report_header == textwrap.dedent(
            """\
            <html>
            <head>
            </head>
            <body>
            """)

        mon.report_progress(build_unit)

        (out, err) = capsys.readouterr()
        assert err == ''
        assert out != ''


# =============================================================================
class SpecifyBuildMonitorReportNonconformity:
    """
    Specify the da.monitor.BuildMonitor.report_nonconformity() function.

    """

    def it_is_callable(self):
        """
        The report_nonconformity() method is callable.

        """
        import da.monitor
        assert callable(da.monitor.BuildMonitor.report_nonconformity)


# =============================================================================
class SpecifyBuildMonitorNotifyBuildEnd:
    """
    Specify the da.monitor.BuildMonitor.notify_build_end() function.

    """

    def it_is_callable(self):
        """
        The notify_build_end() method is callable.

        """
        import da.monitor
        assert callable(da.monitor.BuildMonitor.notify_build_end)
