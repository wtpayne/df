# -*- coding: utf-8 -*-
"""
Unit tests for the da.lwc.run module.

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


import pytest

import da.lwc.run


# -----------------------------------------------------------------------------
@pytest.fixture
def patch_subprocess_call(monkeypatch):
    """
    Replace subprocess.call with a dummy noop function call.

    """
    def noop(_):
        return 0

    monkeypatch.setattr(da.lwc.run, '_subprocess_call', noop)


# =============================================================================
class SpecifyPython2:
    """
    Specify the da.lwc.run.python2() function.

    """

    def it_is_callable(self):
        """
        The python2() function is callable.

        """
        assert callable(da.lwc.run.python2)


# =============================================================================
class SpecifyPython3:
    """
    Specify the da.lwc.run.python3() function.

    """

    def it_is_callable(self):
        """
        The python3() function is callable.

        """
        assert callable(da.lwc.run.python3)


# =============================================================================
class SpecifyPythonInterpreter:
    """
    Specify the da.lwc.run.python_interpreter() function.

    """

    def it_returns_a_string(self):
        """
        The python_interpreter() function returns a string.

        """
        assert isinstance(da.lwc.run.python_interpreter(), str)


# =============================================================================
class SpecifyBash:
    """
    Specify the da.lwc.run.bash() function.

    """

    def it_is_callable(self):
        """
        The bash() function is callable.

        """
        assert callable(da.lwc.run.bash)


# =============================================================================
class SpecifySubl:
    """
    Specify the da.lwc.run.subl() function.

    """

    def it_is_callable(self, patch_subprocess_call):    # pylint: disable=W0613
        """
        The subl() function is callable.

        """
        assert da.lwc.run.subl() == 0
