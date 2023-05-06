# -*- coding: utf-8 -*-
"""
"""


import os.path

import click

import flow_editor


# -----------------------------------------------------------------------------
@click.command()
@click.version_option(
        version = flow_editor.__version__)
def main():
    """
    Load configuration for the UI.

    """

    filename = 'flow_editor.uicfg.yaml'
    dirname  = 'gui'
    dirpath  = os.path.dirname(os.path.realpath(__file__))
    filepath = os.path.join(dirpath, dirname, filename)
    cfg      = _read_cfg_file(filepath)

    import flow_editor.gui
    flow_editor.gui.main(cfg)


# -----------------------------------------------------------------------------
def _read_cfg_file(filepath):
    """
    Load configuration for the UI.

    """

    import ruamel.yaml
    loader = ruamel.yaml.YAML(typ = 'safe')
    with open(filepath, 'rt') as file:
        cfg = loader.load(file)
    return cfg
