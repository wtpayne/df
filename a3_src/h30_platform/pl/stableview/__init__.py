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


import copy
import importlib.metadata
import os.path

import dearpygui.dearpygui
import ruamel.yaml

import fl.util


try:
    __version__ = importlib.metadata.version('stableview')
except importlib.metadata.PackageNotFoundError:
    __version__ = '0.0.1'


# -----------------------------------------------------------------------------
def main(dirpath_cfg, name_view):
    """
    Main update/event loop for the ui.

    The cfg data structure defines the basic
    layout and structure of the GUI.

    TODO: HOW DO I MODIFY PATHS IN THE CONFIG
          SO THAT THEY POINT TO THE RIGHT ASSET
          DIRECTORY? (cfg.font.fira_code._kwargs.file)

    """

    ctx = fl.util.Bureau()
    ctx.rule(cond = fl.util.is_leaf_at(('_fcn',)),
             act  = _update_widget)

    ctx.ui                     = dearpygui.dearpygui
    batch                      = ctx.batch_init()
    ctx.cfg.from_file(filepath = _filepath_cfg(dirpath_cfg, name_view))
    ctx.coro_view              = fl.util.resolve(ctx.cfg.coro_view)(ctx)

    next(ctx.coro_view)                           # app early setup.

    ctx.ui.create_context()

    try:
        ctx.batch_finalize(batch)                 # Create widgets.

        ctx.ui.setup_dearpygui()

        with ctx.batch_context():
            next(ctx.coro_view)                   # app late setup.

        ctx.ui.show_viewport()
        while ctx.ui.is_dearpygui_running():

            with ctx.batch_context():
                next(ctx.coro_view)               # app runtime step.
                ctx.ui.render_dearpygui_frame()
    finally:
        ctx.ui.destroy_context()


# -----------------------------------------------------------------------------
def _filepath_cfg(dirpath_cfg, name_view):
    """
    Load configuration for the UI from the specified view.

    """
    filename_cfg = '{name}.stableview.cfg.yaml'.format(name = name_view)
    filepath_cfg = os.path.join(dirpath_cfg, name_view, filename_cfg)
    return filepath_cfg


# -----------------------------------------------------------------------------
def _update_widget(ctx, tup_cmd):
    """
    Delete corresponding to the specified commands.

    """

    for cmd in tup_cmd:

        if cmd.operation == 'del':
            _del_widget(ctx, cmd)

        if cmd.operation == 'add':
            _add_widget(ctx, cmd)

        if cmd.operation == 'edit':
            print('EDIT')
            print(cmd)


# -----------------------------------------------------------------------------
def _del_widget(ctx, cmd):
    """
    Delete the widget being referenced by the specified command.

    """

    tup_path = cmd.path[:-1]
    tag      = '.'.join(tup_path)
    ctx.ui.delete_item(tag)


# -------------------------------------------------------------------------
def fcn(cfg, fcn, *args, **kwargs):
    """
    """
    cfg._fcn = fcn

    if args:
        cfg.args = list()
        for item in args:
            cfg.args.append(item)

    if kwargs:
        for (key, value) in kwargs.items():
            cfg._kwargs[key] = value

    return cfg


# -----------------------------------------------------------------------------
def _add_widget(ctx, cmd):
    """
    Add the widget being referenced by the specified command.

    """

    tup_path = cmd.path[:-1]
    cfg_item = ctx[tup_path]

    (name_fcn, args, kwargs, bindings, misc) = _get_widget_params(cfg_item)

    fcn = getattr(ctx.ui, name_fcn)

    # Resolve functions (and sometimes also
    # constants) from specification strings
    # to their actual (e.g. callable) values.
    #
    tup_key = tuple(kwargs.keys())
    for key in tup_key:

        kwargs[key] = fl.util.resolve(value = kwargs[key])

        if key.endswith('callback'):
            kwargs['user_data'] = ctx

        #######################################################
        #######################################################
        # TODO: IN SOME CASES, WE WANT THE CALLBACK TO SIMPLY #
        #       MUTATE THE CONFIG. WE CAN POSSIBLY DO THIS    #
        #       WITH A SIMPLE LAMBDA AT THIS POINT.           #
        #######################################################
        #######################################################

    # Handle nodes where the associated
    # DearPyGui function does not expect
    # either a tag parameter or a parent
    # parameter.
    #
    tup_no_tag = ('create_viewport',
                  'bind_item_font',
                  'bind_item_handler_registry')
    if name_fcn in tup_no_tag:
        fcn(**kwargs)
        return
    tag_item      = '.'.join(tup_path)
    kwargs['tag'] = tag_item

    # Handle functions with
    # no parent parameter.

    tup_no_parent = ('add_file_dialog',
                     'add_font_registry',
                     'add_handler_registry',
                     'add_item_handler_registry',
                     'add_texture_registry',
                     'add_window')
    if name_fcn in tup_no_parent:
        fcn(**kwargs)
        if 'set_primary_window' in misc and misc['set_primary_window']:
            ctx.ui.set_primary_window(tag_item, True)
        return
    tag_parent       = '.'.join(tup_path[:-1])
    kwargs['parent'] = tag_parent

    # Handle all other functions.
    #
    if args:
        fcn(*args, **kwargs)
    else:
        fcn(**kwargs)


# -----------------------------------------------------------------------------
def _get_widget_params(cfg_item):
    """
    Return widget parameters from the specified config.

    """

    name_fcn = ''
    args     = tuple()
    kwargs   = dict()
    bindings = dict()
    misc     = dict()

    tup_keys = tuple(cfg_item.keys())

    if '_fcn' in tup_keys:
        name_fcn = cfg_item._fcn

    if '_args' in tup_keys:
        args = cfg_item._args

    if '_kwargs' in tup_keys:
        kwargs = cfg_item._kwargs.to_dict()

    if '_bindings' in tup_keys:
        bindings = cfg_item._bindings.to_dict()

    if '_misc' in tup_keys:
        misc = cfg_item._misc.to_dict()

    return (name_fcn, args, kwargs, bindings, misc)
