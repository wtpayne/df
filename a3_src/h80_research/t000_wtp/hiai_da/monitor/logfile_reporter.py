# -*- coding: utf-8 -*-
"""
The logfile_reporter module reports nonconformities to a text log file.

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


import da.util


# -----------------------------------------------------------------------------
@da.util.coroutine
def coro(filepath_nonconformity_log):
    """
    Coroutine for reporting nonconformities to a textual log file.

    TODO: We want to record all not-yet-rectified nonconformities,
          not just the ones that were encountered in the last
          build. I.e. we need to refactor the way that this function
          is called so we can erase file-paths from this log if the
          file no longer exists or if the nonconformity is fixed.

    ---
    type:   coroutine
    ...

    """
    with open(filepath_nonconformity_log, 'wt') as file:
        while True:
            nonconformity = (yield)
            file.write('{path}\n'.format(path = nonconformity['path']))
            file.flush()
