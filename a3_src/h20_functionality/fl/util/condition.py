# -*- coding: utf-8 -*-
"""
---

title:
    "Utility conditions module."

description:
    "This module contains various general
    purpose rule condition indicator functions."

id:
    "83bb959c-738d-4e85-9470-ce2b05565203"

type:
    dt003_python_module

validation_level:
    v00_minimum

protection:
    k00_general

copyright:
    "Copyright 2023 William Payne"

license:
    "Licensed under the Apache License, Version
    2.0 (the License); you may not use this file
    except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed
    to in writing, software distributed under
    the License is distributed on an AS IS BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
    either express or implied. See the License
    for the specific language governing
    permissions and limitations under the
    License."

...
"""


# -----------------------------------------------------------------------------
def always():
    """
    Return an always-true indicator function.

    """
    def _always(cmd):
        """
        Return True.

        """
        return True
    return _always


# -----------------------------------------------------------------------------
def never():
    """
    Return a never-true indicator function.

    """
    def _never(cmd):
        """
        Return False.

        """
        return False
    return _never


# -----------------------------------------------------------------------------
def root_in(tup_path_root):
    """
    Return indicator that checks cmd.path is rooted in the specified location.

    """
    def _root_in(cmd):
        """
        Return True iff cmd.path is rooted in the specified location.

        """
        return cmd.path[:len(tup_path_root)] == tup_path_root
    return _root_in


# -----------------------------------------------------------------------------
def root_not_in(tup_path_root):
    """
    Return indicator that checks cmd.path not rooted in the specified location.

    """
    def _root_not_in(cmd):
        """
        Return True iff cmd.path is not rooted in the specified location.

        """
        return not cmd.path[:len(tup_path_root)] == tup_path_root
    return _root_not_in
