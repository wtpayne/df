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
    __version__ = importlib.metadata.version('sfedit')
except importlib.metadata.PackageNotFoundError:
    __version__ = '0.0.1'


# -----------------------------------------------------------------------------
def main(dirpath_cfg, name_view):
    """
    Main update/event loop for the ui.

    The cfg data structure defines the basic
    layout and structure of the GUI.

    """

    ctx    = fl.util.Bureau()
    ctx.add_rule(fl.util.Rule(condition = fl.util.condition.always,
                              action    = _build_widget))

    ctx.ui = dearpygui.dearpygui

    _load_configuration(ctx, dirpath_cfg, name_view)

    ctx.coro_view = fl.util.resolve(ctx.cfg.coro_view)(ctx)

    next(ctx.coro_view)                           # app early setup.

    ctx.ui.create_context()
    try:

        _add_all_widgets_from_configuration(ctx)

        ctx.ui.setup_dearpygui()

        next(ctx.coro_view)                       # app late setup.

        ctx.ui.show_viewport()
        while ctx.ui.is_dearpygui_running():

            next(ctx.coro_view)                   # app runtime step.

            ctx.ui.render_dearpygui_frame()

    finally:
        ctx.ui.destroy_context()


# -----------------------------------------------------------------------------
def _load_configuration(ctx, dirpath_cfg, name_view):
    """
    """
    ctx.cfg.from_file(filepath = _filepath_cfg(dirpath_cfg, name_view))

# -----------------------------------------------------------------------------
def _filepath_cfg(dirpath_cfg, name_view):
    """
    Load configuration for the UI from the specified view.

    """
    filename_cfg = '{name}.stableview.cfg.yaml'.format(name = name_view)
    filepath_cfg = os.path.join(dirpath_cfg, name_view, filename_cfg)
    return filepath_cfg


# -----------------------------------------------------------------------------
def _add_all_widgets_from_configuration(ctx):
    """
    Add all widgets from the specified configuration data.

    """
    for (tup_path, cfg_item) in _select_internal_data_structures(
                                        fl.util.walkobj(ctx.cfg,
                                                        gen_leaf    = False,
                                                        gen_nonleaf = True,
                                                        gen_path    = True,
                                                        gen_obj     = True)):

        add_widget(ctx      = ctx,
                   tup_path = tup_path,
                   cfg_item = cfg_item)


# -----------------------------------------------------------------------------
def add_widget(ctx, tup_path, cfg_item)
    """

    """

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

    # Handle nodes where the associated
    # DearPyGui function does not expect
    # either a tag parameter or a parent
    # parameter.
    #
    tup_no_tag = ('create_viewport',
                  'bind_item_handler_registry')
    if name_fcn in tup_no_tag:
        fcn(**kwargs)
        return
    tag_item      = '.'.join(tup_path),
    kwargs['tag'] = tag_item

    # Handle functions with
    # no parent parameter.
    #
    tup_no_parent = ('add_window',
                     'add_handler_registry',
                     'add_item_handler_registry')
    if name_fcn in tup_no_parent:
        fcn(**kwargs)
        if 'set_primary_window' in misc and misc['set_primary_window']:
            ctx.ui.set_primary_window(tag_item, True)
        return
    tag_parent       = '.'.join(tup_path[:-1]
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


# -----------------------------------------------------------------------------
def _select_internal_data_structures(iter_items):
    """
    Yield all items inthe specified iterator that posess internal fields.

    """
    for (tup_path, item) in iter_items:
        if _has_internal_fields(tup_path, item):
            yield (tup_path, item)


# -----------------------------------------------------------------------------
def _has_internal_fields(tup_path, item):
    """
    Return true if tup_path has no leading underscores but item.keys does.

    This indicates that it is a data item at a
    public location that contains internal
    implementation-specific fields. (I.e. those
    that begin with an underscore.)

    """
    is_container = isinstance(item, fl.util.Bureau)
    if not is_container:
        return False

    is_internal = _has_internal_element(tup_path)
    if is_internal:
        return False

    tup_fields          = tuple(item.keys())
    has_internal_fields = _has_internal_element(tup_fields)

    return has_internal_fields


# -----------------------------------------------------------------------------
def _has_internal_element(tup_str):
    """
    Return true if any element in tup_str starts with an underscore.

    """
    return any(_select_internal_elemnets(tup_str))


# -----------------------------------------------------------------------------
def _select_internal_elemnets(tup_str):
    """
    Yield each element in tup_str that starts with an underscore.

    """
    for str_element in tup_str:
        if str_element.startswith('_'):
            yield str_element

