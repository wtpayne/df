# -*- coding: utf-8 -*-
"""
Package containing test fixtures for schema validation tests.

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


import pytest


# -----------------------------------------------------------------------------
# W0621 redefined-outer-name is disabled. The parameter dirpath_lwc_root is
# not actually redefining the function definition of the same name (above) but
# rather calling it (the function) via the magic of py.test fixtures.
@pytest.fixture(scope = 'module')
def idclass_tab(dirpath_lwc_root):                      # pylint: disable=W0621
    """
    Return a mapping from identifier-class-name to validating schema.

    """
    import da.check.schema.common
    return da.check.schema.common.idclass_schema(dirpath_lwc_root)


# -----------------------------------------------------------------------------
@pytest.fixture(scope = 'module')
def load():
    """
    Return a mapping from identifier-class-name to validating schema.

    """
    import io
    import textwrap
    import yaml

    def _load(raw_text):
        """
        Return data deserialised from the provided YAML format text.

        """
        return yaml.load(io.BytesIO(textwrap.dedent(raw_text).encode()))

    return _load
