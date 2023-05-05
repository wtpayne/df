# -*- coding: utf-8 -*-
"""
Unit tests for the da.monitor.desktop_reporter module.

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
...
"""


# =============================================================================
class Specify_Env:
    """
    Specify the da.monitor.desktop_reporter._env() function.

    """
    def it_returns_env_for_python_2_and_3(self):
        """
        The _env() function is reuturns a bash environment for python 2 and 3.

        """
        import da.monitor.desktop_reporter
        py3env = da.monitor.desktop_reporter._env(iface_name = 'lib_python3')
        assert isinstance(py3env, dict)
        assert 'PYTHONPATH' in py3env

        py2env = da.monitor.desktop_reporter._env(iface_name = 'lib_python2')
        assert isinstance(py2env, dict)
        assert 'PYTHONPATH' in py2env

        assert py2env['PYTHONPATH'] != py3env['PYTHONPATH']


# =============================================================================
class SpecifyCoro:
    """
    Specify the da.monitor.desktop_reporter.coro() function.

    """

    def it_is_callable(self):
        """
        The coro() function is callable

        """
        import da.monitor.desktop_reporter
        assert callable(da.monitor.desktop_reporter.coro)
