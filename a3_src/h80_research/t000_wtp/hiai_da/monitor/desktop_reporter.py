# -*- coding: utf-8 -*-
"""
The desktop_reporter module reports build progress using desktop notifications.

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
import subprocess

import da.constants
import da.monitor
import da.monitor.desktop.notification_server
import da.lwc.run
import da.util


# -----------------------------------------------------------------------------
def _env(iface_name = 'lib_python3'):
    """
    Return a shell environment suitable for the specified interface.

    """
    python_import_path = da.lwc.env.python_import_path(iface_name = iface_name)
    env = os.environ.copy()
    env['PYTHONPATH'] = os.pathsep.join(python_import_path)
    env['BROWSER'] = 'google-chrome'  # Suppress GPU warning message.
    return env


# -----------------------------------------------------------------------------
def _dir(module):
    """
    Return the directory path to the specified module.

    """
    return os.path.dirname(module.__file__)


# -----------------------------------------------------------------------------
@da.util.coroutine
def coro(cfg, url_build_report):
    """
    Coroutine for reporting build progress using desktop integration.

    """
    server_module = da.monitor.desktop.notification_server
    module_name   = server_module.__name__
    short_name    = 'da_notify'
    interpreter   = da.lwc.run.python_interpreter(dependency_id = 'pyrun3')
    args          = [short_name, '-m', module_name, short_name]

    assert interpreter is not None
    assert args is not None
    assert subprocess is not None

    server = subprocess.Popen(
                    executable         = interpreter,
                    args               = args,
                    env                = _env('lib_python3'),
                    cwd                = _dir(server_module),
                    stdin              = subprocess.PIPE,
                    stdout             = subprocess.DEVNULL,
                    universal_newlines = True,      # Text mode.
                    bufsize            = 1,         # Line buffered.
                    start_new_session  = True)      # Detach.

    msg = {
        'build_id':         cfg['build_id'],
        'dirpath_log':      cfg['paths']['dirpath_branch_dst'],
        'url_build_report': url_build_report,
        'is_conforming':    True
    }
    server_module.write(server.stdin, msg)

    while True:
        signal = (yield)

        if signal == da.constants.BUILD_COMPLETED:
            pass

        elif signal['type'] == 'nonconformity':
            server_module.write(server.stdin, {
                'build_id':         cfg['build_id'],
                'dirpath_log':      cfg['paths']['dirpath_branch_dst'],
                'url_build_report': url_build_report,
                'is_conforming':    False
            })

        elif signal['type'] == 'build_unit':
            pass
            # build-unit (progress)
