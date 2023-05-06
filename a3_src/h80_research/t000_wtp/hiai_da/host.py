# -*- coding: utf-8 -*-
"""
Build host environment.

This module contains logic to configure the host
environment and install a minimal set of third
party dependencies (if required) such that the
isolated build can run.

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


import os.path

import da.lwc.discover
import da.lwc.env


# -----------------------------------------------------------------------------
def ensure_configured(dirpath_lwc_root):
    """
    Ensure that the host environment is configured.

    pyrun requires:-
        OpenSSL 1.0.0 or later
        zlib 1.2 or later
        SQLite 3.4 or later
        bzip2 1.0 or later

    These will be installed with the package manager.

    git
    download pyrun... which means we need an artifact server...

    ---
    type:   function
    ...

    """
    register = da.lwc.env.dependencies_register(
                                        dirpath_lwc_root = dirpath_lwc_root)
    for dependency_data in register.values():

        if 'w000_bootstrap' not in dependency_data['labels']:
            continue

        if not os.path.isdir(dependency_data['dirpath_policy_bin']):

            # TODO: Install missing dependencies here so we
            #       can bootstrap from a clean environment...
            #
            pass
