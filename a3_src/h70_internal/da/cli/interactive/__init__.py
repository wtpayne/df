# -*- coding: utf-8 -*-
"""
---

title:
    "Interactive commands package."

description:
    "This package provides commands to start
    various interactive tools."

id:
    "8e9fc059-9dcc-441a-b3f8-d00809153ac6"

type:
    dt002_python_package

validation_level:
    v00_minimum

protection:
    k00_general

copyright:
    "Copyright 2015-2022 William Payne"

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
def bash():
    """
    Start a bash repl.

    """
    import da.cli.interactive.bash_shell
    return da.cli.interactive.bash_shell.run()


# -----------------------------------------------------------------------------
def bpython():
    """
    Start a bpython repl.

    """
    import bpython
    return bpython.embed()


# -----------------------------------------------------------------------------
def cpython():
    """
    Start a cpython repl.

    """
    import code
    code.interact()
    return 0


# -----------------------------------------------------------------------------
def ipython():
    """
    Start a ipython repl.

    """
    import ptpython.ipython
    ptpython.ipython.embed()
    return 0


# -----------------------------------------------------------------------------
def ptpython():
    """
    Start a ptpython repl.

    """
    import ptpython.repl
    ptpython.repl.embed(globals(), locals())
    return 0


# -----------------------------------------------------------------------------
def browser():
    """
    Start a design index browser.

    """
    import os
    import da.cli.interactive.browser
    da.cli.interactive.browser.run()


# -----------------------------------------------------------------------------
def direpl():
    """
    Start a design index repl.

    """
    import os
    import da.cli.interactive.direpl
    da.cli.interactive.direpl.run()
