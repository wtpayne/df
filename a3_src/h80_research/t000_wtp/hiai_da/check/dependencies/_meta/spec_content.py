# -*- coding: utf-8 -*-
"""
Unit tests for the da.check.dependencies.content module.

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


import contextlib
import os

import da.check.pytest.fixtures


dirpath_testdata = da.check.pytest.fixtures.dirpath_testdata


# =============================================================================
class SpecifyGetReferenceData:
    """
    Specify the da.check.dependencies.content.get_reference_data() function.

    """

    # -------------------------------------------------------------------------
    def it_returns_indented_string(self, dirpath_testdata):
        """
        get_reference_data() returns a string with the correct indentation.

        """
        import da.machine
        env_name           = da.machine.env_id()
        dirname_depend     = 'test_dependency'
        policy             = 'ver_versionid'

        rootpath_test_wc   = os.path.join(dirpath_testdata, 'working_copy')
        rootpath_test_env  = os.path.join(rootpath_test_wc, 'a0_env')
        rootpath_src       = os.path.join(rootpath_test_env, 'src')
        rootpath_dst       = os.path.join(rootpath_test_env, env_name)

        dirpath_src        = os.path.join(rootpath_src, dirname_depend, policy)
        rootpath_dep_bin   = os.path.join(rootpath_dst, dirname_depend)
        dirpath_policy_bin = os.path.join(rootpath_dep_bin, policy)
        relpath_api        = os.path.join('lib', 'python3')
        dirpath_api        = os.path.join(dirpath_policy_bin, relpath_api)

        # ---------------------------------------------------------------------
        @contextlib.contextmanager
        def monkeypatch_env_path():
            """
            Context manager for monkeypatching the da.lwc.path function.

            This context manager temporarily replaces
            the real da.lwc.path function with one
            that uses the path to the test environment
            directory.

            ---
            type:   coroutine
            ...

            """
            import da.lwc.discover
            original_pathfcn     = da.lwc.discover.path
            original_env_root    = original_pathfcn(
                                        key              = 'env',
                                        dirpath_lwc_root = rootpath_test_wc)

            original_current_env = original_pathfcn(
                                        key              = 'current_env',
                                        dirpath_lwc_root = rootpath_test_wc)

            relpath_current_env  = os.path.relpath(original_current_env,
                                                   start = original_env_root)

            patched_current_env  = os.path.join(rootpath_test_env,
                                                relpath_current_env)

            original_env_src     = original_pathfcn(
                                        key              = 'env_src',
                                        dirpath_lwc_root = rootpath_test_wc)

            relpath_env_src      = os.path.relpath(original_env_src,
                                                   start = original_env_root)

            patched_env_src      = os.path.join(rootpath_test_env,
                                                relpath_env_src)

            patched_paths = {
                'env':          rootpath_test_env,
                'current_env':  patched_current_env,
                'env_src':      patched_env_src
            }

            # -----------------------------------------------------------------
            def patched_env_path(key, dirpath_lwc_root = None):
                """
                Modifies the behaviour of da.lwc.function for testing.

                """
                if key in patched_paths:
                    return patched_paths[key]
                else:
                    return original_pathfcn(key, dirpath_lwc_root)

            da.lwc.discover.path = patched_env_path
            try:
                (yield)
            finally:
                da.lwc.discover.path = original_pathfcn

        expected_output  = {
            'test_dependency': {
                'api': {
                    'lib_python3': {
                        'relpath': relpath_api,
                        'dirpath': dirpath_api
                    }
                },
                'build': {
                    'method': 'automatic',
                    'tool':   'python_distutils'
                },
                'config': {
                    'method': 'manual',
                    'tool':   'n/a',
                    'url':    'n/a'
                },
                'name':               dirname_depend,
                'policy':             policy,
                'dirname':            dirname_depend,
                'dirpath_src':        dirpath_src,
                'rootpath_dep_bin':   rootpath_dep_bin,
                'dirpath_policy_bin': dirpath_policy_bin,
            }
        }

        import da.check.dependencies.content as check_content
        with monkeypatch_env_path():
            reference_data = check_content.get_reference_data(
                                        dirpath_lwc_root = rootpath_test_wc)
        assert reference_data == expected_output
