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

import fl.rule
import fl.util

try:
    __version__ = importlib.metadata.version('stableview')
except importlib.metadata.PackageNotFoundError:
    __version__ = '0.0.1'


# -----------------------------------------------------------------------------
def main(dirpath_cfg, name_view):
    """
    Main update/event loop for the ui.

    We use an MVVM architecture with an
    application model (ctx.app), a view
    model (ctx.view) and a view (ctx.ui).

    ctx.app --> ctx.view --> ctx.ui

    """

    # Initialize the various component parts of
    # the UI architecture:-
    #
    #   1. The application model (ctx.app).
    #   2. The view model (ctx.view)
    #   3. The view API (ctx.ui)
    #
    ctx     = fl.util.Bureau()
    batch   = ctx.batch_init()
    ctx.app = fl.util.Bureau()
    ctx.view.from_file(filepath = _filepath_cfg_view(dirpath_cfg, name_view))
    ctx.ui  = dearpygui.dearpygui

    # Add rules for responding to changes in the
    # view model. Rules for responding to changes
    # in the application model will be by their
    # nature application-specific and therefore
    # are colocated with application specific
    # design elements.
    #
    ctx.view.rule(cond = fl.rule.is_leaf_at(('_fcn',)),
                  act  = _update_dearpygui_widgets)

    # Application coroutine
    #
    ctx.coro = fl.util.resolve(ctx.view.coro)(ctx)
    next(ctx.coro)                                # app early setup.

    ctx.ui.create_context()

    try:
        ctx.batch_finalize(batch)                 # Trigger rules, create view.

        ctx.ui.setup_dearpygui()

        with ctx.batch_context():
            next(ctx.coro)                        # app late setup.

        ctx.ui.show_viewport()
        while ctx.ui.is_dearpygui_running():

            with ctx.batch_context():
                next(ctx.coro)                    # app runtime step.
                ctx.ui.render_dearpygui_frame()
    finally:
        ctx.ui.destroy_context()


# -----------------------------------------------------------------------------
def _filepath_cfg_view(dirpath_cfg, name_view):
    """
    Load configuration for the UI from the specified view.

    """
    filename_cfg = '{name}.stableview.cfg.yaml'.format(name = name_view)
    filepath_cfg = os.path.join(dirpath_cfg, name_view, filename_cfg)
    return filepath_cfg


# -----------------------------------------------------------------------------
def update_bound_values(sender, app_data, ctx):
    """
    Update bound values with app_data.

    This function is intended to be registered as
    a callback handler on various widgets in the
    view, allowing any number of bound values to
    be updated in response to user input or other
    UI events.

    We have arranged things so that the dearpygui
    tag for each widget is also the dot delimited
    string path of the corresponding item in the
    view model data structure.

    This means that we are able to easily look
    up the configured bindings for each widget
    just by using the 'sender' tag as an index
    into the context data structure.

    Similarly, the bindings themselves are just
    lists of dot-delimited bound paths that
    need to be updated with the callback
    app_Data value.

    """

    if '_bind' in ctx[sender]:
        for bound_path in ctx[sender]._bind:
            ctx[bound_path] = app_data
    return None


# -----------------------------------------------------------------------------
def _update_dearpygui_widgets(ctx, tup_cmd):
    """
    Update widgets corresponding to the specified commands.

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
def widget(cfg, fcn, *args, **kwargs):
    """
    Add the specfied widget to the view model.

    """
    cfg._fcn = fcn

    if args:
        cfg.args = list()
        for item in args:
            cfg._args.append(item)

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
    for key in tuple(kwargs.keys()):  # Keys change, so iterate over a copy.

        kwargs[key] = fl.util.resolve(value = kwargs[key])

        if key.endswith('callback'):
            kwargs['user_data'] = ctx

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

    # Handle functions known to have
    # no parent parameter.
    #
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

    if '_fcn' in cfg_item:
        name_fcn = cfg_item._fcn

    if '_args' in cfg_item:
        args = cfg_item._args

    if '_kwargs' in cfg_item:
        kwargs = cfg_item._kwargs.to_dict()

    if '_bindings' in cfg_item:
        bindings = cfg_item._bindings.to_dict()

    if '_misc' in cfg_item:
        misc = cfg_item._misc.to_dict()

    return (name_fcn, args, kwargs, bindings, misc)
