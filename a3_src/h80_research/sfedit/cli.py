#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
---

title:
    "Stableflow editor command line interface."

description:
    "This script is used to launch the
    stableflow editor GUI."

id:
    "fac2efd1-a12f-4726-8a19-3410c306dfd1"

type:
    dt001_python_script

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


"""


import click

import sfedit


# -----------------------------------------------------------------------------
@click.command()
@click.version_option(version = sfedit.__version__)
def main():
    """
    Run the main view of the stableflow editor GUI.

    """
    sfedit.main(cfg = sfedit.get_view_cfg('main'))


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    sys.argv.pop(0)
    main(prog_name = sys.argv[0])
