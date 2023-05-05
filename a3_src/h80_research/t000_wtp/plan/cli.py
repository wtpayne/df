# -*- coding: utf-8 -*-
"""
Planner prototype command line interface logic.

"""


import click
import os

import da.lwc.discover


# -----------------------------------------------------------------------------
@click.group(name = 'plan')
def main():
    """
    Planner prototype.

    """
    pass


# -----------------------------------------------------------------------------
@main.command()
@click.pass_context
def run(ctx):
    """
    Run openpyxl planner.

    """
    import plan.main
    dirpath_lwc_root = ctx.obj['dirpath_lwc_root']
    dirpath_tmp      = da.lwc.discover.path(
                                        key = 'tmp',
                                        dirpath_lwc_root = dirpath_lwc_root)
    filepath_out     = os.path.join(dirpath_tmp, 'tmp.xlsx')
    return plan.main.run(filepath_out)
