# -*- coding: utf-8 -*-
"""
Unit tests for the da.monitor.console_reporter module.

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
import textwrap


# =============================================================================
class SpecifyCoro:
    """
    Specify the da.monitor.console_reporter.coro() function.

    """

    def it_prints_a_progress_bar_to_the_console(self, tmpdir, capsys):
        """
        The coro() function prints a progress bar to the console.

        """
        import da.monitor.console_reporter
        reporter = da.monitor.console_reporter.coro(
                        cfg = {
                            'build_id':             'TEST_BUILD_ID',
                            'cfg_name':             'TEST_CFG_NAME',
                            'relpath_cfg':          'TEST_CONFIG_FILE',
                            'safe_branch_name':     'TEST_SAFE_BRANCH_NAME',
                            'defined_baseline': {
                                'commit_summary':   'TEST_COMMIT_SUMMARY'
                            },
                            'paths': {
                                'rootpath_tmp':     str(tmpdir)
                            },
                            'timestamp': {
                                'datetime_utc':     datetime.datetime.utcnow()
                            }
                        },
                        url_build_report = 'TEST_URL_BUILD_REPORT')
        (out, err) = capsys.readouterr()
        assert err == ''
        assert out == textwrap.dedent("""\
                        Build id:       TEST_BUILD_ID
                        Config file:    TEST_CONFIG_FILE
                        Last commit:    TEST_COMMIT_SUMMARY
                        Report:         TEST_URL_BUILD_REPORT
                        """)
        reporter.send({
                    'relpath':  'TEST_RELPATH'
                      })
        (out, err) = capsys.readouterr()
        assert err == ''
        assert out == 'Progress:     \n'

        reporter.send(da.constants.BUILD_COMPLETED)
        (out, err) = capsys.readouterr()
        assert err == ''
        assert len(out) > 0  # TODO: CHECK MORE STRICTLY


# =============================================================================
class SpecifyPrintAllNonconformities:
    """
    Specify da.monitor.console_reporter.print_all_nonconformities() function.

    """

    def it_prints_a_message_to_stdout(self, capsys):
        """
        print_all_nonconformities() prints all nonconformities to the console.

        """
        import da.monitor.console_reporter
        nonconformity_list = [{
            'path':   'TEST_FILE',
            'line':   1,
            'tool':   'TEST_TOOL',
            'msg_id': 'TEST_MSG_ID',
            'msg':    'TEST_MSG'
        }]
        da.monitor.console_reporter.print_all_nonconformities(
                                    nonconformity_list   = nonconformity_list)
        (out, err) = capsys.readouterr()
        assert err == ''
        assert len(out) > 0  # TODO: CHECK MORE STRICTLY


# =============================================================================
class Specify_Msg:
    """
    Specify the da.monitor.console_reporter._msg() function.

    """

    def it_prints_a_message_to_stdout(self, capsys):
        """
        The _msg() function prints a key-value pair to stdout.

        """
        import da.monitor.console_reporter
        da.monitor.console_reporter._msg(
                                    key = 'TEST_KEY', value = 'TEST_VALUE')
        (out, err) = capsys.readouterr()
        assert out == 'TEST_KEY        TEST_VALUE\n'
        assert err == ''


# =============================================================================
class Specify_PadKey:
    """
    Specify the da.monitor.console_reporter._pad_key() function.

    """

    def it_returns_a_string_padded_to_14_characters(self):
        """
        The _pad_key() returns the input string with whitespace padding.

        """
        import da.monitor.console_reporter
        assert da.monitor.console_reporter._pad_key('A') == 'A             '
        assert da.monitor.console_reporter._pad_key('AB') == 'AB            '
        assert da.monitor.console_reporter._pad_key(
                                        'ABCDEFGHIJKLMNO') == 'ABCDEFGHIJKLMNO'
