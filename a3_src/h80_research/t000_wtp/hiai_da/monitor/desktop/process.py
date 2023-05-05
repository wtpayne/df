# -*- coding: utf-8 -*-
"""
The process module supports control over the notification server process.

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


import ctypes
import ctypes.util
import os
import signal

import psutil


# -----------------------------------------------------------------------------
def ensure_one_instance(name):
    """
    Ensure that we have only one process with the specified name.

    Kills any other process with the specified name,
    then renames the current process with that name.

    AKA the 'Highlander' function: 'There can be only one'.

    """
    _kill(name)
    _rename(name)


# -----------------------------------------------------------------------------
def _kill(name):
    """
    Kill the process with the specified name.

    """
    for proc in psutil.process_iter():
        if proc.name() == name:
            os.kill(proc.pid, signal.SIGKILL)


# -----------------------------------------------------------------------------
def _rename(short_name):
    """
    Rename the current process using the prctl function from libc.

    """
    # Only the first 15 characters of a process
    # name are significant, so we enforce a limit
    # to discourage e.g. long module paths being
    # used.
    max_name_length = 15
    if len(short_name) > max_name_length:
        raise ValueError('Short name must be <= 15 characters in length.')

    # Create a C buffer containing the name as a null-terminated ASCII string.
    bytes_name = short_name.encode('ascii')
    len_buff   = len(short_name) + 1
    buff       = ctypes.create_string_buffer(len_buff)
    buff.value = bytes_name  # Null terminated

    # Call the prctl function to set the process name.
    name_libc   = ctypes.util.find_library('c')
    libc        = ctypes.cdll.LoadLibrary(name_libc)
    pr_set_name = 15
    libc.prctl(pr_set_name, ctypes.byref(buff), 0, 0, 0)
