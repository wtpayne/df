# -*- coding: utf-8 -*-
"""
Unit tests for the da.check.dependencies package.

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


# =============================================================================
class SpecifyCoro:
    """
    Specify the da.check.dependencies.coro() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The coro() function is callabe.

        """
        import da.check.dependencies
        assert callable(da.check.dependencies.coro)


# =============================================================================
class Specify_LoadRegister:
    """
    Specify the da.check.dependencies._load_register() function.

    """

    # -------------------------------------------------------------------------
    def it_returns_a_dict(self, dirpath_lwc_root):
        """
        The _load_register() function returns a dict.

        """
        import da.check.dependencies
        register = da.check.dependencies._load_register(dirpath_lwc_root)
        assert isinstance(register, dict)


# =============================================================================
class Specify_CheckRegisterFormat:
    """
    Specify the da.check.dependencies._check_register_format() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The _check_register_format() function is callabe.

        """
        import da.check.dependencies
        assert callable(da.check.dependencies._check_register_format)


# =============================================================================
class Specify_CheckMissingSources:
    """
    Specify the da.check.dependencies._check_missing_from_disk() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The _check_missing_sources() function is callabe.

        """
        import da.check.dependencies
        assert callable(da.check.dependencies._check_missing_sources)


# =============================================================================
class Specify_CheckMissingFromRegister:
    """
    Specify the da.check.dependencies._check_missing_from_register() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The _check_missing_from_register() function is callabe.

        """
        import da.check.dependencies
        assert callable(da.check.dependencies._check_missing_from_register)


# =============================================================================
class Specify_CheckContentConsistency:
    """
    Specify the da.check.dependencies._check_content_consistency() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The _check_content_consistency() function is callabe.

        """
        import da.check.dependencies
        assert callable(da.check.dependencies._check_content_consistency)


# =============================================================================
class Specify_CheckRegisteredConfigMethod:
    """
    Specify the _check_registered_config_method() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The _check_registered_config_method() function is callabe.

        """
        import da.check.dependencies
        assert callable(da.check.dependencies._check_registered_config_method)


# =============================================================================
class Specify_CheckRegisteredBuildMethod:
    """
    Specify the _check_registered_build_method() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The _check_registered_build_method() function is callabe.

        """
        import da.check.dependencies
        assert callable(da.check.dependencies._check_registered_build_method)
