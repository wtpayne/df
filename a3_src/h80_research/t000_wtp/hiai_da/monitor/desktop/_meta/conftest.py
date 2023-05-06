# -*- coding: utf-8 -*-
"""
Package containing test fixtures for build monitor desktop integration tests.

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
@pytest.fixture(scope = 'function')
def mock_callable():
    """
    Return a mock callable to test if a particular function has been called.

    """

    # =========================================================================
    class MockCallable(object):
        """
        Mock callable functor.

        """
        call_count = 0
        call_args  = []

        # ---------------------------------------------------------------------
        def __call__(self, *args):
            """
            Record call statistics.

            """
            self.call_count += 1
            self.call_args.append(list(args))

    return MockCallable()


