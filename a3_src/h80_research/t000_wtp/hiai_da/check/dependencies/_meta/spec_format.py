# -*- coding: utf-8 -*-
"""
Unit tests for the da.check.dependencies.format module.

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


import json
import textwrap

import pytest


# -----------------------------------------------------------------------------
@pytest.fixture()
def mock_dependencies_register():
    """
    Return a mock system dependencies register as a string.

    """
    return textwrap.dedent("""\
    {

        "title":                    "Mock system dependencies register.",

        "introduction":             "A fake dependencies register for testing.",

        "register": {

            "entry_key": {
                "desc":             "A dummy dependencies register entry.",
                "notes":            "Used to help test registery functions.",
                "labels":           [],
                "dirname":          "directory_name",
                "policy":           "configuration_policy",
                "api": {
                    "api_name_one": "one/api/path",
                    "api_name_two": "another/api/path"
                },
                "cli": {
                    "cli_name_one": "one/cli/path",
                    "cli_name_two": "another/cli/path"
                },
                "gui": {
                    "gui_name_one": "one/gui/path",
                    "gui_name_two": "another/gui/path"
                },
                "tgt":              ["e00_x86_64_linux_ubuntu_xenial"],
                "config": {
                    "method":       "automatic",
                    "tool":         "git",
                    "url":          "http://some.git.url"
                },
                "build": {
                    "method":       "automatic",
                    "tool":         "some/bash/script.sh"
                }
            }
        }
    }
    """)


# =============================================================================
class SpecifyGetReferenceText:
    """
    Specify the da.check.dependencies.format_register_data() function.

    """

    # -------------------------------------------------------------------------
    def it_returns_a_formatted_system_dependencies_register(
                                            self, mock_dependencies_register):
        """
        get_reference_text() returns a string with the correct indentation.

        """
        import da.check.dependencies.format
        returned_string = da.check.dependencies.format.get_reference_text(
                                        json.loads(mock_dependencies_register))
        assert returned_string == mock_dependencies_register
