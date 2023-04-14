
# -*- coding: utf-8 -*-
"""
Planner prototype command line interface logic.

"""

import click
import os

import da.lwc.discover


# -----------------------------------------------------------------------------
@click.group(name = 'docmatic')
def main():
    """
    Docmatic documentation generation prototype.

    """
    pass


# -----------------------------------------------------------------------------
@main.command()
@click.pass_context
def run(ctx):
    """
    Run docmatic documentation generation prototype.

    """
    from . import dashex
    dashex.run()
    # dirpath_lwc_root = ctx.obj['dirpath_lwc_root']
    # dirpath_src      = da.lwc.discover.path('src', dirpath_lwc_root)
    # for dirpath_doc in _gen_doc_dirs(dirpath_src):
    #     print(dirpath_doc)


# -----------------------------------------------------------------------------
def _gen_doc_dirs(dirpath_lwc_root):
    """
    Generate all directories that require documentation.

    """
    direxcl = da.lwc.discover.LWC_DIR_EXCLUDE_EXPR_LIST
    direxcl += [r'^_meta$']
    return da.lwc.search.filtered_dirpath_generator(
                        root     = dirpath_lwc_root,
                        direxcl  = direxcl,
                        pathincl = None,
                        pathexcl = None)

