# -*- coding: utf-8 -*-
"""
Package containing a data validation schema for the dependencies register.

---
type:
    python_package

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

from good import (Any,
                  Extra,
                  Reject,
                  Schema)

import da.check.schema.common


# -----------------------------------------------------------------------------
def get():
    """
    Return the data validation schema for the dependencies register.

    """
    common = da.check.schema.common

    # ---
    # i00082_each_dependency_will_offer_zero_or_more_interfaces:
    #   - "Each dependency WILL offer zero or more interfaces."
    #   - notes: "Some dependencies offer multiple
    #            interfaces through which they can
    #            be used. For example, OpenCV offers
    #            a Python 2 API, a Python 3 API, a
    #            C++ API and a vanilla C API. Most
    #            dependencies will have at least
    #            one interface defined, although
    #            it is possible for no interface
    #            to be defined if a dependency is
    #            being used manually, or if the
    #            integration is not complete."
    #   - type: information
    #   - state: draft
    #
    # i00088_configure_location_of_interface_in_each_dependency:
    #   - "The dependencies_register_data_structure
    #      SHALL provide the dependencies_management_logic
    #      with the ability to determine the location
    #      of multiple interfaces for each dependency."
    #   - notes: "Some dependencies offer multiple
    #            interfaces through which we may
    #            interact with them. We shall support
    #            this by allowing access to more
    #            than one API per dependency. The
    #            relevant documents for each API will
    #            be located in different locations
    #            in the dependency build output, so
    #            we shall provide a mapping from api
    #            name to a relative path to provide
    #            the dependencies management logic
    #            with the information that it needs."
    #   - type: mandate
    #   - state: draft
    # ...
    #
    # The API config is a map from interface name to relpath.
    #
    built_item_config = Schema({
        'relpath':  common.LOWERCASE_PATH
    })
    api_iface_name = Any('include',
                         'lib_native',
                         'lib_javascript',
                         'lib_python2',
                         'lib_python3')
    api_config = Any({}, {api_iface_name:        built_item_config})
    cli_config = Any({}, {common.LOWERCASE_NAME: built_item_config})
    gui_config = Any({}, {common.LOWERCASE_NAME: built_item_config})

    scm_tool   = Any('bzr', 'git', 'hg', 'svn', 'darcs',
                     'ftp', 'manual', 'n/a', 'TBD')

    build_tool = Any('python_setuptools', 'python_distutils', 'make',
                     'n/a', 'TBD')

    return Schema({
        'title':                common.TITLE_TEXT,

        'introduction':         common.PARAGRAPH_TEXT,

        'register': {

            common.LOWERCASE_NAME: {
                'desc':         Any('TBD', common.SUMMARY_TEXT),
                'notes':        Any('TBD', common.PARAGRAPH_TEXT),
                'labels':       Any([], [common.LOWERCASE_NAME]),
                'dirname':      common.LOWERCASE_NAME,
                'policy':       common.LOWERCASE_NAME,
                'api':          api_config,
                'cli':          cli_config,
                'gui':          gui_config,
                'tgt':          Any([], [common.LOWERCASE_NAME]),
                'config': {
                    'method':   Any('automatic',
                                    'manual',
                                    'n/a'),
                    'tool':     scm_tool,
                    'url':      common.URL
                },
                'build': {
                    'method':   Any('automatic',
                                    'manual',
                                    'n/a'),
                    'tool':     build_tool
                }
            }

        },
        Extra:                  Reject
    })
