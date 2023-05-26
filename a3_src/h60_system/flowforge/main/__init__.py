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

import fl.util
import fl.stableflow.cfg
import fl.stableflow.cfg.edge
import fl.stableflow.cfg.layout

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
    """
    filepath = da.env.path(
                    control_tier = 'h10_resource',
                    relpath      = 'icon/png/{name}.png'.format(name = name),
                    id_env       = 'e002_general_research')
    rgba = PIL.Image.open(filepath).convert("RGBA")
    return numpy.array(rgba).flatten()


ICON_PLAY_24X24  = _load_icon('play-solid')
ICON_PAUSE_24X24 = _load_icon('pause-solid')
ICON_STOP_24X24  = _load_icon('stop-solid')


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

    yield  # Context is created and widgets are added in gui.main().

    _load_file(ctx = ctx, filepath = FILEPATH_DEFAULT_LOAD)
    _save_file(ctx = ctx, filepath = FILEPATH_DEFAULT_SAVE)

    #ctx.pm.host.set_count(1)
    #ctx.pm.proc.set_count(1)

    # import pprint
    # pprint.pprint(ctx.ui.get_item_configuration('cfg.vp.win'))
    # ctx.ui.configure_item('cfg.vp.win.main.toolbar', vertical_spacing = -1)

    yield  # Viewport is shown, main loop starts in gui.main().

    while True:

        # print('A')

        #ctx.pm.node.update_selected_nodes()
        #ctx.pm.edge.update_selected_edges()

        yield  # Frame is rendered, is_dearpygui_running check in gui.main().

        # print('B')


# -----------------------------------------------------------------------------
def menu_file_open(sender, app_data, ctx):
    """
    Callback for the 'Open' button in the 'File' menu.

    """

    fcn = pl.stableview.fcn
    open_file = fcn(
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

    extension = fcn(
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

    _load_file(ctx, filepath = app_data['file_path_name'])
    del ctx.vp.open_file


# -----------------------------------------------------------------------------
def menu_file_save(sender, app_data, ctx):
    """
    Callback for the 'Save' button in the 'File' menu.

    """

    fcn = pl.stableview.fcn
    save_file = fcn(
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

    extension = fcn(
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

    _save_file(ctx, filepath = app_data['file_path_name'])
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
    nodeeditor    = ctx.cfg.vp.win.main.nodeeditor
    list_selected = ctx.ui.get_selected_nodes(nodeeditor._str_path())

    if len(list_selected) == 0:
        ctx.ui.configure_item('cfg.vp.win.ctx.node_add',  show = True)
        ctx.ui.configure_item('cfg.vp.win.ctx.node_edit', show = False)
        ctx.ui.configure_item('cfg.vp.win.ctx.node_del',  show = False)
    elif len(list_selected) == 1:
        ctx.ui.configure_item('cfg.vp.win.ctx.node_add',  show = False)
        ctx.ui.configure_item('cfg.vp.win.ctx.node_edit', show = True)
        ctx.ui.configure_item('cfg.vp.win.ctx.node_del',  show = True)
    else:
        ctx.ui.configure_item('cfg.vp.win.ctx.node_add',  show = False)
        ctx.ui.configure_item('cfg.vp.win.ctx.node_edit', show = False)
        ctx.ui.configure_item('cfg.vp.win.ctx.node_del',  show = True)

    width  = ctx.cfg.vp.win.ctx._kwargs.width
    height = ctx.cfg.vp.win.ctx._kwargs.height
    ctx.ui.configure_item('cfg.vp.win.ctx',
                          min_size = [width, height],
                          pos      = ctx.ui.get_mouse_pos(local = False),
                          show     = True)


# -----------------------------------------------------------------------------
def ctx_node_add(sender, app_data, ctx):
    """
    Add button on right click context menu.

    """
    ctx.ui.configure_item(ctx.cfg.vp.win.ctx._str_path(), show = False)
    pos    = ctx.ui.get_item_pos('cfg.vp.win.ctx')
    pos[0] = pos[0] - 40
    pos[1] = pos[1] - 20

    idx_node_max = 0
    for name in ctx.cfg.vp.win.main.nodeeditor.keys():
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
    nodeeditor = ctx.cfg.vp.win.main.nodeeditor
    node       = pl.stableview.fcn(nodeeditor['node_' + id_node],
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
    ctx.ui.configure_item('cfg.vp.win.ctx',
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


# # -----------------------------------------------------------------------------
# def menu_edit_addnode(sender, app_data, ctx):
#     """
#     Callback for the vp.win.menu.edit.addnode menu_item widget.

#     """
#     ctx.pm.node.add(pos = None)


# # -----------------------------------------------------------------------------
# def side_cfg_sys_id(sender, app_data, ctx):
#     """
#     Set the system id.

#     """
#     ctx.pm.sys.set_id(id_system = app_data)


# # -----------------------------------------------------------------------------
# def side_cfg_host_count(sender, app_data, ctx):
#     """
#     Set the number of process hosts in the system.

#     """
#     ctx.pm.host.set_count(count_new = app_data)


# # -----------------------------------------------------------------------------
# def side_cfg_proc_count(sender, app_data, ctx):
#     """
#     Set the number of processes in the system.

#     """
#     ctx.pm.proc.set_count(count_new = app_data)


# # -----------------------------------------------------------------------------
# def side_cfg_node_id(sender, app_data, ctx):
#     """
#     Callback for the vp.win.main.side.tab.cfg.node.id input_text widget.

#     """
#     ctx.pm.node.selected().set_id(app_data)


# # -----------------------------------------------------------------------------
# def side_cfg_node_proc(sender, app_data, ctx):
#     """
#     Callback for the vp.win.main.side.tab.cfg.node.proc combo widget.

#     """
#     ctx.pm.node.selected().set_proc(app_data)


# # -----------------------------------------------------------------------------
# def side_cfg_node_input_count(sender, app_data, ctx):
#     """
#     Callback for the vp.win.main.side.tab.cfg.node.countin input_int widget.

#     """
#     ctx.pm.node.selected().set_input_count(count_new = app_data)


# # -----------------------------------------------------------------------------
# def side_cfg_node_output_count(sender, app_data, ctx):
#     """
#     Callback for the vp.win.main.side.tab.cfg.node.countout input_int widget.

#     """
#     ctx.pm.node.selected().set_output_count(app_data)









































# -----------------------------------------------------------------------------
def _load_file(ctx, filepath):
    """
    Load file.

    """

    WIDTH_NODE     = 160

    nodeeditor     = ctx.cfg.vp.win.main.nodeeditor
    sfcfg          = fl.stableflow.cfg
    fcn            = pl.stableview.fcn
    map_cfg_norm   = sfcfg.prepare(path_cfg = filepath)
    map_cfg_denorm = sfcfg.denormalize(copy.deepcopy(map_cfg_norm))
    map_cfg_layout = sfcfg.layout.horizontal(map_cfg_denorm  = map_cfg_denorm,
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
    map_link = collections.defaultdict(dict)
    for (id_node, cfg_node) in map_cfg_layout['node'].items():

        node = fcn(nodeeditor['node_' + id_node],
                   'add_node',
                   label = id_node,
                   pos   = [cfg_node['pos_x'], cfg_node['pos_y']])

        # Keep a record of node config.
        #
        node._id  = id_node
        node._cfg = map_cfg_norm['node'][id_node]

        for (id_input, id_edge) in sorted(cfg_node['input'].items()):

            attr = fcn(node['input_' + id_input],
                       'add_node_attribute',
                       label          = id_input,
                       attribute_type = ctx.ui.mvNode_Attr_Input)

            map_link[id_edge]['input'] = attr._str_path()

            text = fcn(attr.text,
                       'add_input_text',
                       width         = WIDTH_NODE,
                       default_value = id_input)

        for (id_output, id_edge) in sorted(cfg_node['output'].items()):

            attr = fcn(node['output_' + id_output],
                       'add_node_attribute',
                       label          = id_output,
                       attribute_type = ctx.ui.mvNode_Attr_Output)

            map_link[id_edge]['output'] = attr._str_path()

            text = fcn(attr.text,
                       'add_input_text',
                       width         = WIDTH_NODE,
                       default_value = id_output)

    # Build lookup table for edge configuration.
    #
    map_edge = dict()
    for cfg_edge in map_cfg_norm['edge']:
        id_edge = sfcfg.edge.id_edge(cfg_edge)
        map_edge[id_edge] = cfg_edge

    # Add edges to the view model.
    #
    for (idx_edge, (id_edge, link)) in enumerate(map_link.items()):
        edge = fcn(nodeeditor['edge_{:04d}'.format(idx_edge)],
                   'add_node_link',
                   show     = True,
                   attr_1   = link['input'],
                   attr_2   = link['output'])
        edge._id  = id_edge
        edge._cfg = map_edge[id_edge]



# -----------------------------------------------------------------------------
def _save_file(ctx, filepath):
    """
    Save file.

    """
    cfg_save = {
        'node': dict(),
        'edge': list()
    }

    # Extract node and edge config from the view model
    #
    for (key, value) in ctx.cfg.vp.win.main.nodeeditor.items():
        if key.startswith('node_'):
            cfg_save['node'][value._id] = value._cfg
        if key.startswith('edge_'):
            cfg_save['edge'].append(value._cfg)

    # import pprint
    # pprint.pprint(cfg_save)

    ##################################################
    # TODO: WHAT METADATA DO I NEED?                 #
    #       WHERE WILL IT BE STORED?                 #
    #       APPLICATION MODEL TO VIEW MODEL MAPPING? #
    ##################################################

    # THINK ABOUT DATA FLOW BETWEEN APPLICATION MODEL AND VIEW MODEL

