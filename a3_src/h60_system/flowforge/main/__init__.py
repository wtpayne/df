# -*- coding: utf-8 -*-
"""
---

title:
    "Workflow editor main view."

description:
    "This python module contains functions
    for running the workflow editor."

id:
    "555345dc-41c5-4810-a4fc-7ccbcde432af"

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


import collections
import copy
import os.path

import dearpygui
import PIL.Image
import numpy

import fl.rule
import fl.stableflow.cfg
import fl.stableflow.cfg.edge
import fl.stableflow.cfg.layout
import fl.util

import pl.stableview

import da.env

from . import model


SIDEBAR_WIDTH        = model.SIDEBAR_WIDTH
SIDEBAR_WIDGET_WIDTH = model.SIDEBAR_WIDGET_WIDTH
INDENT               = model.INDENT

# TODO: USE SOME OTHER NON-INTERNAL-SPECIFIC
#       WAY OF GETTING RESOURCES.
#
FILEPATH_FONT_FIRA_CODE = da.env.path(
        control_tier = 'h10_resource',
        relpath      = 'font/FiraCodeNerdFontMono-Light.ttf',
        id_env       = 'e002_general_research')

FILEPATH_DEFAULT_LOAD = da.env.path(
        control_tier = 'h90_internal',
        relpath      = 'da/cli/service/process_assistant/process_assistant.stableflow.cfg.yaml',
        # relpath    = 'da/demo/dm001_workflow/dm001_workflow.stableflow.cfg.yaml'
        id_env       = 'e002_general_research')

FILEPATH_DEFAULT_SAVE = da.env.path(
        control_tier = 'h90_internal',
        relpath      = '/da/demo/dm001_workflow/dm001_workflow_saved.stableflow.cfg.yaml',
        id_env       = 'e002_general_research')


BOTTOM_RIGHT = dearpygui.dearpygui.mvNodeMiniMap_Location_BottomRight
NO_PADDING   = [0, 0]


# -----------------------------------------------------------------------------
def _load_icon(name):
    """
    TODO: MOVE THIS INTO A BUILD STEP WHERE WE COMPILE ASSETS.

    """
    filepath = da.env.path(
        control_tier = 'h10_resource',
        relpath      = 'icon/dark/solid/{name}/16x16.png'.format(name = name),
        id_env       = 'e002_general_research')
    rgba = PIL.Image.open(filepath).convert("RGBA")
    return numpy.array(rgba).flatten()


ICON_PLAY_16X16  = _load_icon('play')
ICON_PAUSE_16X16 = _load_icon('pause')
ICON_STOP_16X16  = _load_icon('stop')

#####################################
# TODO: MOVE THIS INTO A BUILD STEP #
#####################################

# -----------------------------------------------------------------------------
def coro(ctx):
    """
    Main coroutine for the app.

    """
    # We set up the presentation model here
    # because it does not require the dearpygui
    # context and is required by the callbacks
    # that are bound to the widgets during their
    # creation.
    #
    #ctx.pm = model.Model(ctx)

    ctx.app.rule(cond = fl.rule.always(),
                 act  = _update_from_application_model)  # TODO: ctx.app.update FROM CONFIGURATION?

    yield  # Context is created and widgets are added in gui.main().

    #######################################
    # AUTO LOAD FILE FOR EASIER DEBUGGING #
    #######################################

    with ctx.batch_context():
        ctx.app.from_dict(fl.stableflow.cfg.prepare(FILEPATH_DEFAULT_LOAD))
    # ctx.app.to_file(filepath = FILEPATH_DEFAULT_SAVE)

    #ctx.pm.host.set_count(1)
    #ctx.pm.proc.set_count(1)

    # import pprint
    # pprint.pprint(ctx.app.to_dict())

    # pprint.pprint(ctx.ui.get_item_configuration('view.vp.win'))
    # ctx.ui.configure_item('view.vp.win.main.toolbar', vertical_spacing = -1)

    yield  # Viewport is shown, main loop starts in gui.main().

    while True:

        # print('A')

        #ctx.pm.node.update_selected_nodes()
        #ctx.pm.edge.update_selected_edges()

        yield  # Frame is rendered, is_dearpygui_running check in gui.main().

        # print('B')


# -----------------------------------------------------------------------------
def _update_from_application_model(ctx, tup_cmd):
    """
    TBD

    """

    WIDTH_NODE     = 160
    widget         = pl.stableview.widget

    nodeeditor     = ctx.view.vp.win.main.nodeeditor
    map_cfg_norm   = copy.deepcopy(ctx.app.to_dict())
    map_cfg_denorm = fl.stableflow.cfg.denormalize(map_cfg_norm)
    map_cfg_layout = fl.stableflow.cfg.layout.horizontal(
                                            map_cfg_denorm  = map_cfg_denorm,
                                            diagram_border  = 10,
                                            swimlane_title  = 0,
                                            longbus_u       = 0,
                                            crossbus_v      = 0,
                                            node_size_x     = WIDTH_NODE,
                                            node_size_y     = 70,
                                            node_margin_x   = 40,
                                            node_margin_y   = 40)

    # Add nodes to the view model.
    #
    with ctx.batch_context():
        map_link = collections.defaultdict(dict)
        for (id_node, cfg_node) in map_cfg_layout['node'].items():

            node = widget(nodeeditor['node_' + id_node],
                          'add_node',
                          label = id_node,
                          pos   = [cfg_node['pos_x'], cfg_node['pos_y']])

            # Keep a record of node config.
            #
            node._id  = id_node
            node._cfg = map_cfg_norm['node'][id_node]

            for (id_input, id_edge) in sorted(cfg_node['input'].items()):
                attr = widget(node['input_' + id_input],
                              'add_node_attribute',
                              label          = id_input,
                              attribute_type = ctx.ui.mvNode_Attr_Input)

                map_link[id_edge]['input'] = attr._str_path()

                text = widget(attr.text,
                              'add_input_text',
                              width         = WIDTH_NODE,
                              default_value = id_input)

            for (id_output, id_edge) in sorted(cfg_node['output'].items()):

                attr = widget(node['output_' + id_output],
                              'add_node_attribute',
                              label          = id_output,
                              attribute_type = ctx.ui.mvNode_Attr_Output)

                map_link[id_edge]['output'] = attr._str_path()

                text = widget(attr.text,
                              'add_input_text',
                              width         = WIDTH_NODE,
                              default_value = id_output)

        # Build lookup table for edge configuration.
        #
        map_edge = dict()
        for cfg_edge in map_cfg_norm['edge']:
            id_edge = fl.stableflow.cfg.edge.id_edge(cfg_edge)
            map_edge[id_edge] = cfg_edge

        # Add edges to the view model.
        #
        for (idx_edge, (id_edge, link)) in enumerate(map_link.items()):
            edge = widget(nodeeditor['edge_{:04d}'.format(idx_edge)],
                          'add_node_link',
                          show     = True,
                          attr_1   = link['input'],
                          attr_2   = link['output'])
            edge._id  = id_edge
            edge._cfg = map_edge[id_edge]


# -----------------------------------------------------------------------------
def menu_file_open(sender, app_data, ctx):
    """
    Callback for the 'Open' button in the 'File' menu.

    """

    widget    = pl.stableview.widget
    open_file = widget(
            ctx.vp.open_file,
            'add_file_dialog',
            directory_selector = False,
            modal              = True,
            show               = True,
            label              = 'Open file',
            callback           = '_spec::flowforge.main.menu_file_open_ok',
            cancel_callback    = '_spec::flowforge.main.menu_file_open_cancel',
            width              = 700,
            height             = 500,
            default_path       = os.path.expanduser('~'),
            file_count         = 1)

    extension = widget(
            open_file.extension,
            'add_file_extension',
            label         = 'yaml',
            extension     = '.yaml',
            width         = 200,
            height        = 100)


# -----------------------------------------------------------------------------
def menu_file_open_cancel(sender, app_data, ctx):
    """
    Callback for the 'cancel' button on the file-open dialog.

    """

    del ctx.vp.open_file


# -----------------------------------------------------------------------------
def menu_file_open_ok(sender, app_data, ctx):
    """
    Callback for the 'ok' button on the file-open dialog.

    """

    ctx.app.from_dict(fl.stableflow.cfg.prepare(app_data['file_path_name']))
    del ctx.vp.open_file


# -----------------------------------------------------------------------------
def menu_file_save(sender, app_data, ctx):
    """
    Callback for the 'Save' button in the 'File' menu.

    """

    widget    = pl.stableview.widget
    save_file = widget(
            ctx.vp.save_file,
            'add_file_dialog',
            directory_selector = False,
            modal              = True,
            show               = True,
            label              = 'Save file',
            callback           = '_spec::flowforge.main.menu_file_save_ok',
            cancel_callback    = '_spec::flowforge.main.menu_file_save_cancel',
            width              = 700,
            height             = 500,
            default_path       = os.path.expanduser('~'),
            file_count         = 1)

    extension = widget(
            save_file.extension,
            'add_file_extension',
            label     = 'yaml',
            extension = '.yaml',
            width     = 200,
            height    = 100)


# -----------------------------------------------------------------------------
def menu_file_save_cancel(sender, app_data, ctx):
    """
    Callback for the 'Cancel' button on the file-save dialog.

    """

    del ctx.vp.save_file


# -----------------------------------------------------------------------------
def menu_file_save_ok(sender, app_data, ctx):
    """
    Callback for the 'OK' button on the file-save dialog.

    """

    ctx.app.to_file(filepath = app_data['file_path_name'])
    del ctx.vp.save_file


# -----------------------------------------------------------------------------
def menu_edit_undo(sender, app_data, ctx):
    """
    Callback for the 'Undo' button in the 'Edit' menu.

    """

    raise NotImplementedError('edit.undo')


# -----------------------------------------------------------------------------
def menu_edit_redo(sender, app_data, ctx):
    """
    Callback for the 'Redo' button in the 'Edit' menu.

    """

    raise NotImplementedError('edit.redo')


# -----------------------------------------------------------------------------
def menu_run_start(sender, app_data, ctx):
    """
    Callback for the 'Start' button in the 'Run' menu.

    """

    raise NotImplementedError('run.start')


# -----------------------------------------------------------------------------
def menu_run_pause(sender, app_data, ctx):
    """
    Callback for the 'Pause' button in the 'Run' menu.

    """

    raise NotImplementedError('run.pause')


# -----------------------------------------------------------------------------
def menu_run_stop(sender, app_data, ctx):
    """
    Callback for the 'Stop' button in the 'Run' menu.

    """

    raise NotImplementedError('run.stop')


# -----------------------------------------------------------------------------
def menu_tools_about(sender, app_data, ctx):
    """
    Callback for the 'Show About' button in the 'Tools' menu.

    """

    ctx.ui.show_tool(ctx.ui.mvTool_About)


# -----------------------------------------------------------------------------
def menu_tools_metrics(sender, app_data, ctx):
    """
    Callback for the 'Show Metrics' button in the 'Tools' menu.

    """

    ctx.ui.show_tool(ctx.ui.mvTool_Metrics)


# -----------------------------------------------------------------------------
def menu_tools_doc(sender, app_data, ctx):
    """
    Callback for the 'Show Documentation' button in the 'Tools' menu.

    """

    ctx.ui.show_tool(ctx.ui.mvTool_Doc)


# -----------------------------------------------------------------------------
def menu_tools_debug(sender, app_data, ctx):
    """
    Callback for the 'Show Debug Tool' button in the 'Tools' menu.

    """

    ctx.ui.show_tool(ctx.ui.mvTool_Debug)


# -----------------------------------------------------------------------------
def menu_tools_style(sender, app_data, ctx):
    """
    Callback for the 'Show Style Editor' button in the 'Tools' menu.

    """

    ctx.ui.show_tool(ctx.ui.mvTool_Style)


# -----------------------------------------------------------------------------
def menu_tools_font(sender, app_data, ctx):
    """
    Callback for the 'Show Font Editor' button in the 'Tools' menu.

    """

    ctx.ui.show_tool(ctx.ui.mvTool_Font)


# -----------------------------------------------------------------------------
def menu_tools_itemreg(sender, app_data, ctx):
    """
    Callback for the 'Show Item Registry' button in the 'Tools' menu.

    """

    ctx.ui.show_tool(ctx.ui.mvTool_ItemRegistry)


# -----------------------------------------------------------------------------
def menu_help_doc(sender, app_data, ctx):
    """
    Callback for the 'Documentation' button in the 'Help' menu.

    """

    raise NotImplementedError('help.doc')


# -----------------------------------------------------------------------------
def menu_help_about(sender, app_data, ctx):
    """
    Callback for the 'About' button in the 'Help' menu.

    """

    raise NotImplementedError('help.about')


# -----------------------------------------------------------------------------
def mouseright(sender, app_data, ctx):
    """
    Mouse right click handler.

    Displays the right click context menu.

    """

    nodeeditor     = ctx.view.vp.win.main.nodeeditor
    configure      = ctx.ui.configure_item
    path           = 'view.vp.win.ctx'
    list_selected  = ctx.ui.get_selected_nodes(nodeeditor._str_path())
    count_selected = len(list_selected)
    str_title      = 'Edit ({count})'.format(count = count_selected)

    if count_selected == 0:
        configure(path + '.title',     default_value = 'Create')
        configure(path + '.node_add',  show          = True)
        configure(path + '.node_edit', show          = False)
        configure(path + '.node_del',  show          = False)
    elif count_selected == 1:
        configure(path + '.title',     default_value = str_title)
        configure(path + '.node_add',  show          = False)
        configure(path + '.node_edit', show          = True)
        configure(path + '.node_del',  show          = True)
    else:
        configure(path + '.title',     default_value = str_title)
        configure(path + '.node_add',  show          = False)
        configure(path + '.node_edit', show          = False)
        configure(path + '.node_del',  show          = True)

    configure(path, pos  = ctx.ui.get_mouse_pos(local = False),
                    show = True)


# -----------------------------------------------------------------------------
def ctx_node_add(sender, app_data, ctx):
    """
    Add button on right click context menu.

    """

    ctx.ui.configure_item(ctx.view.vp.win.ctx._str_path(), show = False)
    pos    = ctx.ui.get_item_pos('view.vp.win.ctx')
    pos[0] = pos[0] - 40
    pos[1] = pos[1] - 20

    idx_node_max = 0
    for name in ctx.view.vp.win.main.nodeeditor.keys():
        prefix = 'node_'
        if not name.startswith(prefix):
            continue
        suffix = name[len(prefix):]
        try:
            idx_node = int(suffix)
        except ValueError:
            continue
        else:
            idx_node_max = max(idx_node_max, idx_node)

    id_node    = '{:04d}'.format(idx_node_max + 1)
    nodeeditor = ctx.view.vp.win.main.nodeeditor
    widget     = pl.stableview.widget
    node       = widget(nodeeditor['node_' + id_node],
                        'add_node',
                        label = id_node,
                        pos   = pos)


# -----------------------------------------------------------------------------
def ctx_node_edit(sender, app_data, ctx):
    """
    Edit button on right click context menu.

    """

    print('EDIT NODE')


# -----------------------------------------------------------------------------
def ctx_node_del(sender, app_data, ctx):
    """
    Delete button on right click context menu.

    """

    print('DEL NODE')


# -----------------------------------------------------------------------------
def ctx_node_cancel(sender, app_data, ctx):
    """
    Cancel button on right click context menu.

    """

    ctx.ui.configure_item('view.vp.win.ctx',
                          pos  = ctx.ui.get_mouse_pos(local = False),
                          show = False)


# -----------------------------------------------------------------------------
def node_link(sender, app_data):
    """
    """

    print('LINK CALLBACK')
    # ctx.ui.add_node_link(app_data[0], app_data[1], parent=sender)


# -----------------------------------------------------------------------------
def node_delink(sender, app_data):
    """
    """

    print('DELINK CALLBACK')
    # ctx.ui.delete_item(app_data)


# -----------------------------------------------------------------------------
# def _save_file(ctx, filepath):
#     """
#     Save file.

#     """
#     cfg_save = {
#         'node': dict(),
#         'edge': list()
#     }

    # Extract node and edge config from the view model
    #
    # for (key, value) in ctx.view.vp.win.main.nodeeditor.items():
    #     if key.startswith('node_'):
    #         cfg_save['node'][value._id] = value._cfg
    #     if key.startswith('edge_'):
    #         cfg_save['edge'].append(value._cfg)

    # import pprint
    # pprint.pprint(cfg_save)

    ##################################################
    # TODO: WHAT METADATA DO I NEED?                 #
    #       WHERE WILL IT BE STORED?                 #
    #       APPLICATION MODEL TO VIEW MODEL MAPPING? #
    ##################################################

    # THINK ABOUT DATA FLOW BETWEEN APPLICATION MODEL AND VIEW MODEL

