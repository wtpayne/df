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


import os.path

import fl.util

from . import model


SIDEBAR_WIDTH        = model.SIDEBAR_WIDTH
SIDEBAR_WIDGET_WIDTH = model.SIDEBAR_WIDGET_WIDTH
INDENT               = model.INDENT


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

    _load_file(
        ctx      = ctx,
        filepath = '/media/wtp/Data1/dev/df/ws00_pri/a3_src/h90_internal/da/demo/dm001_workflow/dm001_workflow.stableflow.cfg.yaml')

    #ctx.pm.host.set_count(1)
    #ctx.pm.proc.set_count(1)

    yield  # Viewport is shown, main loop starts in gui.main().

    while True:

        # print('A')

        #ctx.pm.node.update_selected_nodes()
        #ctx.pm.edge.update_selected_edges()

        yield  # Frame is rendered, is_dearpygui_running check in gui.main().

        # print('B')


# -----------------------------------------------------------------------------
def _load_file(ctx, filepath):
    """
    Load file.

    """
    stableflow_cfg = fl.util.Bureau(filepath = filepath)


    node          = ctx.cfg.vp.win.main.nodeeditor.node
    node._fcn     = 'add_node'
    kwargs        = node._kwargs
    kwargs.label  = 'Foo'
    kwargs.id     = 'FooNode'
    kwargs.pos    = [100.0, 100.0]

    print('LOADED')
    print(repr(kwargs.pos))
    print(type(kwargs.pos))
    print(str(kwargs.pos))

    # for (id_node, cfg_node) in stableflow_cfg.node.items():

        # import pprint
        # pprint.pprint(cfg_node.to_dict())


# -----------------------------------------------------------------------------
def menu_file_open(sender, app_data, ctx):
    """
    Callback for the file-open menu item.

    """
    open_file                 = ctx.vp.open_file
    open_file._fcn            = 'add_file_dialog'
    kwargs                    = open_file._kwargs
    kwargs.directory_selector = False
    kwargs.modal              = True
    kwargs.show               = True
    kwargs.label              = 'Open file'
    kwargs.callback           = '_spec::flowforge.main.menu_file_open_ok'
    kwargs.cancel_callback    = '_spec::flowforge.main.menu_file_open_cancel'
    kwargs.width              = 700
    kwargs.height             = 500
    kwargs.default_path       = os.path.expanduser('~')
    kwargs.file_count         = 1
    # dialog_kwargs.max_size - seems to cause segfault
    # dialog_kwargs.min_size - seems to cause segfault

    extension = open_file.extension
    extension._fcn = 'add_file_extension'
    ext_kwargs               = extension._kwargs
    ext_kwargs.label         = 'yaml'
    ext_kwargs.extension     = '.yaml'
    ext_kwargs.width         = 200
    ext_kwargs.height        = 100


# -----------------------------------------------------------------------------
def menu_file_open_ok(sender, app_data, ctx):
    """
    Callback for the 'ok' button on the file-open dialog.

    """
    _load_file(ctx, filepath = app_data['file_path_name'])


# -----------------------------------------------------------------------------
def menu_file_open_cancel(sender, app_data, ctx):
    """
    """
    del ctx.vp.open_file


# -----------------------------------------------------------------------------
def node_link(sender, app_data, ctx):
    """
    """
    pass
    # ctx.ui.add_node_link(app_data[0], app_data[1], parent=sender)


# -----------------------------------------------------------------------------
def node_delink(sender, app_data, ctx):
    """
    """
    pass
    # ctx.ui.delete_item(app_data)


# -----------------------------------------------------------------------------
def menu_tools_itemreg(sender, app_data, ctx):
    """
    """
    ctx.ui.show_tool(ctx.ui.mvTool_ItemRegistry)



# # -----------------------------------------------------------------------------
# def mouseright(sender, app_data, ctx):
#     """
#     Mouse right click handler.

#     Displays the right click context menu.

#     """
#     ctx.ui.configure_item('vp.win.ctx',
#                           pos  = ctx.ui.get_mouse_pos(local = False),
#                           show = True)


# # -----------------------------------------------------------------------------
# def ctx_addnode(sender, app_data, ctx):
#     """
#     Add Node button callback from the right click context menu.

#     """
#     pos    = ctx.ui.get_item_pos('vp.win.ctx')
#     pos[0] = pos[0] - 40
#     pos[1] = pos[1] - 20
#     ctx.pm.node.add(pos)
#     ctx.ui.configure_item("vp.win.ctx", show = False)


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







# # -----------------------------------------------------------------------------
# def menu_file_save(sender, app_data, ctx):
#     """
#     """
#     pass


# # -----------------------------------------------------------------------------
# def menu_file_save(sender, app_data, ctx):
#     """
#     """
#     pass


# # -----------------------------------------------------------------------------
# def menu_tools_about(sender, app_data, ctx):
#     """
#     """
#     ctx.ui.show_tool(ctx.ui.mvTool_About)


# # -----------------------------------------------------------------------------
# def menu_tools_metrics(sender, app_data, ctx):
#     """
#     """
#     ctx.ui.show_tool(ctx.ui.mvTool_Metrics)


# # -----------------------------------------------------------------------------
# def menu_tools_doc(sender, app_data, ctx):
#     """
#     """
#     ctx.ui.show_tool(ctx.ui.mvTool_Doc)


# # -----------------------------------------------------------------------------
# def menu_tools_debug(sender, app_data, ctx):
#     """
#     """
#     ctx.ui.show_tool(ctx.ui.mvTool_Debug)


# # -----------------------------------------------------------------------------
# def menu_tools_style(sender, app_data, ctx):
#     """
#     """
#     ctx.ui.show_tool(ctx.ui.mvTool_Style)


# # -----------------------------------------------------------------------------
# def menu_tools_font(sender, app_data, ctx):
#     """
#     """
#     ctx.ui.show_tool(ctx.ui.mvTool_Font)


# # -----------------------------------------------------------------------------
# def menu_tools_demo(sender, app_data, ctx):
#     """
#     """
#     pass


# # -----------------------------------------------------------------------------
# def menu_help_about(sender, app_data, ctx):
#     """
#     """
#     pass
