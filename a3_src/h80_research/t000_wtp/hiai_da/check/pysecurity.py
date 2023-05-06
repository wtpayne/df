# -*- coding: utf-8 -*-
"""
Module containing pysecurity (bandit) checking coroutines.

Bandit is a security linter from openstack.

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


# import bandit

import da.lwc.file
import da.util


# -----------------------------------------------------------------------------
@da.util.coroutine
def coro(_):
    """
    Send errors to build_monitor if supplied files not compliant with bandit.

    ---
    type:   coroutine
    ...

    """
    # filepath_bandit = da.lwc.env.cli_path(
    #                         dependency_id    = 'bandit',
    #                         application_name = 'bandit',
    #                         dirpath_lwc_root = dirpath_lwc_root)
    # Run main file-processing loop: recieve file
    # paths from outside the coroutine and send
    # them one at a time to the bandit module.
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

        # TODO: Call bandit to lint current file...
        # bandit_command = [
        #     filepath_bandit,
        #     filepath]

        # process  = subprocess.Popen(bandit_command,
        #                             stdout = subprocess.PIPE,
        #                             stderr = subprocess.PIPE)
        # out, err = process.communicate()
        # exitcode = process.returncode
        # isok     = exitcode == 0
        # if isok:
        #     continue

        # # Any text output to stderr indicates that
        # # a fatal error has occurred in MyPy.
        # #
        # if err:
        #     err_str = err.decode('utf8')
        #     raise RuntimeError(
        #                 'Error in Bandit: {err}'.format(err = err_str))

        # for line_of_output in out.decode('utf8').splitlines():

        #     build_monitor.report_nonconformity(
        #                                 tool    = 'da.check.pysecurity',
        #                                 msg_id  = 'TBD',
        #                                 msg     = line_of_output,
        #                                 path    = filepath)
