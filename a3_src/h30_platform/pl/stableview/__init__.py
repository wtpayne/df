# -*- coding: utf-8 -*-
"""
---

title:
    "Stableview GUI platform package."

description:
    "This package provides functions for
    running user interfaces that are based
    ont the stableview platform."

id:
    "9fa93a78-fd12-44c4-9122-05b35e272340"

type:
    dt002_python_package

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

import importlib.metadata
import os.path

import dearpygui.dearpygui
import ruamel.yaml

import fl.util
import pl.stableview.build
import pl.stableview.util


try:
    __version__ = importlib.metadata.version('sfedit')
except importlib.metadata.PackageNotFoundError:
    __version__ = '0.0.1'


# -----------------------------------------------------------------------------
def _load_cfg(dirpath_cfg, name_view):
    """
    Load configuration for the UI from the specified view.

    """
    filename_cfg = '{name}.stableview.cfg.yaml'.format(name = name_view)
    filepath_cfg = os.path.join(dirpath_cfg, name_view, filename_cfg)

    with open(filepath_cfg, 'rt') as file:
        return ruamel.yaml.YAML(typ = 'safe').load(file)


# -----------------------------------------------------------------------------
def main(dirpath_cfg, name_view):
    """
    Main update/event loop for the ui.

    The cfg data structure defines the basic
    layout and structure of the GUI.

    """

    ctx           = fl.util.DotDict
    ctx.ui        = dearpygui.dearpygui
    ctx.cfg       = _load_cfg(dirpath_cfg, name_view)
    ctx.coro_view = pl.stableview.util.resolve(ctx.cfg['coro_view'])(ctx)

    next(ctx.coro_view)                           # app early setup.

    ctx.ui.create_context()
    try:

        pl.stableview.build.ui(ctx)
        ctx.ui.setup_dearpygui()

        next(ctx.coro_view)                       # app late setup.

        ctx.ui.show_viewport()
        while ctx.ui.is_dearpygui_running():

            next(ctx.coro_view)                   # app runtime step.

            ctx.ui.render_dearpygui_frame()

    finally:
        ctx.ui.destroy_context()
