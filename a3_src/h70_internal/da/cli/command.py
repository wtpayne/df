# -*- coding: utf-8 -*-
"""
---

title:
    "Design automation command line interface command module."

description:
    "This module provides a set of commands
    which may be invoked from the design
    automation command line interface.

    This module uses the excellent click
    library from the Pallets organization
    to parse commands, argument and
    parameters.

    The actual implementation of the commands
    themselves is delegated to their respective
    modules."

id:
    "b9236f11-1078-4209-9b6b-a634ad37a2ca"

type:
    dt003_python_module

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


import importlib.metadata
import sys

import click

import da.cli.group


# -----------------------------------------------------------------------------
@click.group(
        name             = 'main',
        cls              = da.cli.group.Ordered,
        context_settings = { 'max_content_width': 50 })
@click.version_option(
        version          = importlib.metadata.version("h70_internal"))
def grp_main():
    """
    Design automation command line interface.

    The design automation command line interface
    provides the user with the ability to issue
    design automation commands.

    """
    pass


# -----------------------------------------------------------------------------
@grp_main.group(name = 'util',
                cls  = da.cli.group.Ordered)
def grp_utility():
    """
    Utility commands.

    """
    pass


# -----------------------------------------------------------------------------
@grp_utility.command()
def uuid():
    """
    Generate a UUID4.

    """
    import da.cli.utility
    sys.exit(da.cli.utility.uuid())


# -----------------------------------------------------------------------------
@grp_main.group(name = 'interact',
                cls  = da.cli.group.Ordered)
def grp_interactive():
    """
    Interactive tools, repls and shells.

    """
    pass


# -----------------------------------------------------------------------------
@grp_interactive.command()
def bash():
    """
    Start a bash shell.

    """
    import da.cli.interactive
    sys.exit(da.cli.interactive.bash())


# -----------------------------------------------------------------------------
@grp_interactive.command()
def bpy():
    """
    Start a bpython repl.

    """
    import da.cli.interactive
    sys.exit(da.cli.interactive.bpython())


# -----------------------------------------------------------------------------
@grp_interactive.command()
def cpy():
    """
    Start a cpython repl.

    """
    import da.cli.interactive
    sys.exit(da.cli.interactive.cpython())


# -----------------------------------------------------------------------------
@grp_interactive.command()
def ipy():
    """
    Start a ipython repl.

    """
    import da.cli.interactive
    sys.exit(da.cli.interactive.ipython())


# -----------------------------------------------------------------------------
@grp_interactive.command()
def ptpy():
    """
    Start a ptpython repl.

    """
    import da.cli.interactive
    sys.exit(da.cli.interactive.ptpython())


# -----------------------------------------------------------------------------
@grp_interactive.command()
def direpl():
    """
    Start a design index repl.

    """
    import da.cli.interactive
    sys.exit(da.cli.interactive.direpl())


# -----------------------------------------------------------------------------
@grp_interactive.command()
def browse():
    """
    Start a design index browser.

    """
    import da.cli.interactive
    sys.exit(da.cli.interactive.browser())


# -----------------------------------------------------------------------------
@grp_main.group(name = 'service',
                cls  = da.cli.group.Ordered)
def grp_service():
    """
    Background services.

    """
    pass


# -----------------------------------------------------------------------------
@grp_service.group(name = 'process_assistant',
                   cls  = da.cli.group.Ordered)
def grp_process_assistant():
    """
    Process assistant service.

    """
    pass


# -----------------------------------------------------------------------------
@grp_process_assistant.command()
def start():
    """
    Start the process assistant service.

    """
    import da.cli.service.process_assistant
    sys.exit(da.cli.service.process_assistant.start())


# -----------------------------------------------------------------------------
@grp_process_assistant.command()
def stop():
    """
    Stop the process assistant service.

    """
    import da.cli.service.process_assistant
    sys.exit(da.cli.service.process_assistant.stop())


# -----------------------------------------------------------------------------
@grp_main.group(name = 'build',
                cls  = da.cli.group.Ordered)
def grp_build():
    """
    Build system.

    """
    pass


# -----------------------------------------------------------------------------
@grp_build.command()
def docs():
    """
    Build documentation.

    """
    import da.cli.build
    sys.exit(da.cli.build.docs())


# -----------------------------------------------------------------------------
@grp_main.group(name = 'release',
                cls  = da.cli.group.Ordered)
def grp_cms():
    """
    Configuration management system.

    """
    pass


# -----------------------------------------------------------------------------
@grp_build.command()
def release():
    """
    Make a public release.

    """
    import da.cli.cms
    sys.exit(da.cli.cms.release())


# -----------------------------------------------------------------------------
@grp_main.group(name = 'demo',
                cls  = da.cli.group.Ordered)
def grp_demo():
    """
    Demonstrations.

    """
    pass


# -----------------------------------------------------------------------------
@grp_demo.command()
@click.argument(
    'name',
    required = True,
    type     = click.STRING)
def start(name):
    """
    Start the named demonstration.

    """
    import da.cli.demo
    sys.exit(da.cli.demo.start(name_demo = name))


# -----------------------------------------------------------------------------
@grp_demo.command()
@click.argument(
    'name',
    required = True,
    type     = click.STRING)
def stop(name):
    """
    Stop the named demonstration.

    """
    import da.cli.demo
    sys.exit(da.cli.demo.stop(name_demo = name))


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    sys.argv.pop(0)
    grp_main(prog_name = sys.argv[0])
