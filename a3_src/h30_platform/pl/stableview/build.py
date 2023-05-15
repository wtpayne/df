# -*- coding: utf-8 -*-
"""
---

title:
    "Stableview GUI building module."

description:
    "This module provides functions for
    building the user interface widgets
    from supplied configuration data."

id:
    "0298490d-41be-4d04-a404-2ec1637190f7"

type:
    dt003_python_module

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

import fl.util
import pl.stableview.util


# -----------------------------------------------------------------------------
def ui(ctx):
    """
    Add widgets to the current context.

    """
    for (tup_path, cfg_widget) in _iter_widget_cfg(ctx.cfg):

        name_fcn = cfg_widget['fcn']
        args     = cfg_widget['args']
        kwargs   = cfg_widget['kwargs']
        bindings = cfg_widget['bindings']
        misc     = cfg_widget['misc']
        fcn      = getattr(ctx.ui, name_fcn)

        # Resolve functions (and sometimes also
        # constants) from specification strings
        # to their actual (e.g. callable) values.
        #
        tup_key = tuple(kwargs.keys())
        for key in tup_key:

            kwargs[key] = pl.stableview.util.resolve(value = kwargs[key])

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

        # Handle all other functions.
        #
        str_parent       = '.'.join(tup_path[:-1])
        kwargs['parent'] = str_parent
        if args:
            fcn(*args, **kwargs)
        else:
            fcn(**kwargs)

        # Bind widgets to the view model.
        #
        # if name_fcn == 'add_menu_item':
        print('')
        print('')
        print('-' * 60)
        print(str_tag)
        print('=' * len(str_tag))
        print('')
        import pprint
        pprint.pprint(ctx.ui.get_item_configuration(str_tag))
        print('')

        # model.bind(
        #         tag         = str_tag,
        #         ui_property = 'value',
        #         ui_callback = 'callback')


# -----------------------------------------------------------------------------
def _iter_widget_cfg(cfg):
    """
    Yield widget configuration items from the given configuration object.

    This function iterates through the given
    configuration object, extracting widget
    configurations based on specific keys
    starting with an underscore.

    It also ensures that the widget configuration
    contains 'bindings', 'kwargs', 'args', and
    'misc' keys with default values if they are
    not present.

    Parameters:

        cfg (dict): The configuration object containing
                    widget configurations.

    Yields:

        tuple:  A tuple containing the path to the widget
                configuration and the widget configuration
                itself as a dictionary.

    Example:

        Given a configuration object `cfg` containing
        widget configurations, the function can be
        used as follows:

            >>> for path, widget_config in _iter_widget_cfg(cfg):
            ...     print(path, widget_config)

    """
    for (tup_path, item) in fl.util.walkobj(cfg,
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
