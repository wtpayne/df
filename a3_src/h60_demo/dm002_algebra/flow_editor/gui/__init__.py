# -*- coding: utf-8 -*-
"""
"""


import collections
import contextlib
import copy
import importlib
import os.path

import dearpygui.dearpygui

import flow_editor.gui.util


# -----------------------------------------------------------------------------
def main(cfg):
    """
    Main update/event loop for the ui.

    The cfg data structure defines the basic
    layout and structure of the GUI.

    """
    ctx                = DotDict()
    ctx.ui             = dearpygui.dearpygui
    ctx.cfg            = cfg
    spec_app_coroutine = ctx.cfg['app_coroutine']
    app_coroutine_fcn  = _ensure_resolved(spec_app_coroutine)
    ctx.app_coroutine  = app_coroutine_fcn(ctx)

    next(ctx.app_coroutine)                       # app early setup.

    ctx.ui.create_context()
    try:

        _build_ui(ctx)
        ctx.ui.setup_dearpygui()

        next(ctx.app_coroutine)                   # app late setup.

        ctx.ui.show_viewport()
        while ctx.ui.is_dearpygui_running():

            next(ctx.app_coroutine)               # app runtime step.

            ctx.ui.render_dearpygui_frame()

    finally:
        ctx.ui.destroy_context()


# -----------------------------------------------------------------------------
def _build_ui(ctx):
    """
    Add widgets to the current context.

    """

    model = flow_editor.gui.util.ViewModel()

    for (tup_path, cfg_widget) in _iter_widget_cfg(ctx.cfg):

        name_fcn = cfg_widget['fcn']
        args     = cfg_widget['args']
        kwargs   = cfg_widget['kwargs']
        bindings = cfg_widget['bindings']
        misc     = cfg_widget['misc']
        fcn      = getattr(ctx.ui, name_fcn)

        # Resolve constants and
        # functions to their
        # actual values.
        #
        tup_key = tuple(kwargs.keys())
        for key in tup_key:

            kwargs[key] = _ensure_resolved(value = kwargs[key])

            if key.endswith('callback'):
                kwargs['user_data'] = ctx

        # Handle functions with
        # no tag parameter.
        #
        tup_no_tag = ('create_viewport',
                      'bind_item_handler_registry')
        if name_fcn in tup_no_tag:
            fcn(**kwargs)
            continue

        str_tag       = '.'.join(tup_path)
        kwargs['tag'] = str_tag

        # Handle functions with
        # no parent parameter.
        #
        tup_no_parent = ('add_window',
                         'add_handler_registry',
                         'add_item_handler_registry')
        if name_fcn in tup_no_parent:
            fcn(**kwargs)
            if 'set_primary_window' in misc and misc['set_primary_window']:
                ctx.ui.set_primary_window(str_tag, True)
            continue

        # Bind widgets to the view model.
        #
        # model.bind(str_tag)

        # Handle all other functions.
        #
        str_parent       = '.'.join(tup_path[:-1])
        kwargs['parent'] = str_parent
        if args:
            fcn(*args, **kwargs)
        else:
            fcn(**kwargs)


# -----------------------------------------------------------------------------
def _ensure_resolved(value):
    """
    Ensure that the provided value is fully resolved.

    If the provided value is a string starting
    with the prefix '_spec::' then resolve it
    to the actual value.

    """
    if is_string(value) and value.startswith('_spec::'):
        (module, func) = value.split('::')[1].split(':')
        return getattr(importlib.import_module(module), func)

    return value

# -----------------------------------------------------------------------------
def _resolve_callback_from_spec(str_spec):
    """
    Return a callable from a string specification.

    """
    return fcn


# -----------------------------------------------------------------------------
def _iter_widget_cfg(cfg):
    """
    Yield widget configuration from cfg.

    """
    for (tup_path, item) in walkobj(cfg,
                                    gen_leaf    = False,
                                    gen_nonleaf = True,
                                    gen_path    = True,
                                    gen_obj     = True):
        try:
            tup_key = tuple(item.keys())
        except AttributeError:
            continue

        # Widget config keys start with
        # an underscore.
        #
        tup_key_cfg_widget = (key for key in tup_key if key.startswith('_'))
        cfg_widget         = dict()
        for key in tup_key_cfg_widget:
            cfg_widget[key[1:]] = item[key]

        if not cfg_widget:
            continue

        if 'bindings' not in cfg_widget:
            cfg_widget['bindings'] = dict()

        if 'kwargs' not in cfg_widget:
            cfg_widget['kwargs'] = dict()

        if 'args' not in cfg_widget:
            cfg_widget['args'] = tuple()

        if 'misc' not in cfg_widget:
            cfg_widget['misc'] = dict()

        # Make sure we return a separate
        # instance of the widget config
        # so we don't accidentally mutate
        # it and screw up the walk.
        #
        yield (tup_path, copy.deepcopy(cfg_widget))


# -----------------------------------------------------------------------------
def walkobj(obj,                                  # pylint: disable=R0912,R0913
            gen_leaf    = False,
            gen_nonleaf = False,
            gen_path    = False,
            gen_obj     = False,
            path        = (),
            memo        = None):
    """
    Generate a walk over a treelike structure of mappings and other iterables.

    Adapted from:
    http:/code.activestate.com/recipes/577982-recursively-walk-python-objects/

    This function performs a (depth-first left to
    right recursive) traversal over the provided
    data structure, which we assume to consist of
    a finite; treelike arrangement of nested
    collections.Mapping and collections.Iterable
    types.

    This function can be configured to yield
    information about nodes in the tree: leaf
    nodes; non-leaf (internal) nodes or both.

    The information that is yielded may also be
    configured: the path to the node can be
    delivered as can the object at the node
    itself.

    ---
    type:   generator
    ...

    """
    # If the object is elemental, it cannot be
    # decomposed, so we must bottom out the
    # recursion and yield the object and its'
    # path before returning control back up
    # the stack.
    #
    is_itable    = isinstance(obj, collections.abc.Iterable)
    is_leaf      = (not is_itable) or is_string(obj)

    if is_leaf:
        if gen_leaf:
            if gen_path and gen_obj:
                yield (path, obj)
            elif gen_path:
                yield path
            elif gen_obj:
                yield obj
        return

    # Since this is a recursive function, we need
    # to be on our guard against any references
    # to objects back up the call stack (closer
    # to the root of the tree). Any such
    # references would be circular, leading to
    # an infinite tree, and causing us to blow
    # our stack in a fit of unbounded recursion.
    #
    # If we detect that we've already visited
    # this object (using identity not equality),
    # then the safe thing to do is to halt the
    # recursive descent and return control back
    # up the stack.
    #
    _id = id(obj)
    if memo is None:
        memo = set()
    if _id in memo:
        return
    memo.add(_id)

    # If the object is not elemental (i.e. it is
    # an Iterable), then it may be decomposed, so
    # we should recurse down into each component,
    # yielding the results as we go. Of course,
    # we need different iteration functions for
    # mappings vs. other iterables.
    #
    def mapiter(mapping):
        """
        Return an iterator over the specified mapping or other iterable.

        This function selects the appropriate
        iteration function to use.

        """
        return getattr(mapping, 'iteritems', mapping.items)()
    itfcn = mapiter if isinstance(obj, collections.abc.Mapping) else enumerate

    for pathpart, component in itfcn(obj):

        childpath = path + (pathpart,)
        if gen_nonleaf:
            if gen_path and gen_obj:
                yield (childpath, component)
            elif gen_path:
                yield childpath
            elif gen_obj:
                yield component

        for result in walkobj(obj         = component,
                              gen_leaf    = gen_leaf,
                              gen_nonleaf = gen_nonleaf,
                              gen_path    = gen_path,
                              gen_obj     = gen_obj,
                              path        = childpath,
                              memo        = memo):
            yield result

    # We only need to guard against infinite
    # recursion within a branch of the call-tree.
    # There is no danger in visiting the same item
    # instance in sibling branches, so we can
    # forget about objects once we are done
    # with them and about to pop the stack.
    #
    memo.remove(_id)
    return


# -----------------------------------------------------------------------------
def is_string(obj):
    """
    Return true if obj is a string. Works in Python 2 and Python 3.

    """
    return isinstance(obj, string_types())


# -----------------------------------------------------------------------------
def string_types():
    """
    Return the string types for the current Python version.

    """
    is_python_2 = str is bytes
    if is_python_2:  # pylint: disable=R1705
        return (str, unicode)  # pylint: disable=E0602
    else:
        return (str, bytes)


# -----------------------------------------------------------------------------
def coroutine(fun):
    """
    Return a decorator function that primes communications with a coroutine.

    """
    def primed(*args, **kwargs):
        """
        Wrapper for coroutines that 'primes' it by sending the first message.

        """
        coro = fun(*args, **kwargs)
        coro.send(None)
        return coro
    return primed


# =============================================================================
class DotDict(dict):
    """
    Custom dictionary with dot notation attribute access.

    """
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


