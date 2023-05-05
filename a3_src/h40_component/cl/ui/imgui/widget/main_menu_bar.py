# -*- coding: utf-8 -*-
"""
Imgui main menu bar UI component.

"""


import collections
import contextlib

import imgui

import xact.signal




# -----------------------------------------------------------------------------
def coro(id_node):
    """
    Imgui main menu bar UI component frontend.

    """

    coro_menu_dynamic = _coro_menu_dynamic()
    coro_menu_dynamic.send(None)

    list_msg_out = list()

    while True:

        (ctx_ui, ctx_frame, list_msg_in) = yield (list_msg_out)
        list_msg_out.clear()

        with main_menu_bar_context() as bar:

            add_file_menu(      ctx_ui, list_msg_in, list_msg_out )
            add_component_menu( ctx_ui, list_msg_in, list_msg_out )

            _step(coroutine    = coro_menu_dynamic,
                  ctx_ui       = ctx_ui,
                  ctx_frame    = ctx_frame,
                  list_msg_in  = list_msg_in,
                  list_msg_out = list_msg_out)


# -----------------------------------------------------------------------------
def _step(coroutine, ctx_ui, ctx_frame, list_msg_in, list_msg_out):
    """
    Step the specified coroutine.

    """
    list_msg_out_part = []
    try:
        list_msg_out_part = coroutine.send((ctx_ui, ctx_frame, list_msg_in))
    except StopIteration:
        raise xact.signal.Halt(0)
    if list_msg_out_part:
        list_msg_out.extend(list_msg_out_part)


# -----------------------------------------------------------------------------
def _coro_menu_dynamic():
    """
    """
    map_item     = dict()
    list_msg_out = list()

    while True:

        (ctx_ui, ctx_frame, list_msg_in) = yield (list_msg_out)
        list_msg_out.clear()

        with menu_context('Dynamic') as menu:
            if not menu:
                continue

        #     if list_msg_in:
        #         import pprint
        #         pprint.pprint(list_msg_in)

            imgui.menu_item('pending - [x]')
            list_msg_out.append({
                '_node':  ctx_ui.id_node,
                '_type':  'request',
                '_spec':  ('fs', 'media', 'wtp', 'Data', 'dev'),
            })



# -----------------------------------------------------------------------------
@contextlib.contextmanager
def main_menu_bar_context():
    """
    Context manager for drawing the main window menu.

    """
    is_open = imgui.begin_main_menu_bar()

    (yield is_open)

    if is_open:
        imgui.end_main_menu_bar()


# -----------------------------------------------------------------------------
@contextlib.contextmanager
def menu_context(label, is_enabled = True):
    """
    Context manager for drawing a menu.

    """
    is_open = imgui.begin_menu(label, is_enabled)

    (yield is_open)

    if is_open:
        imgui.end_menu()


# -----------------------------------------------------------------------------
def add_file_menu(ctx_ui, list_msg_in, list_msg_out):
    """
    Main file menu.

    """
    with menu_context('File') as menu:

        if not menu:
            return

        (clicked_quit, selected_quit) = imgui.menu_item('Quit', 'Cmd+Q')
        if clicked_quit:
            raise xact.signal.Halt(0)


# -----------------------------------------------------------------------------
def add_component_menu(ctx_ui, list_msg_in, list_msg_out):
    """
    Component menu.

    """
    map_component = ctx_ui.ui_state['map_coro']
    if not map_component:
        return

    with menu_context('Component') as component_menu:
        if not component_menu:
            return

        for path in map_component.keys():
            (clicked, selected) = imgui.menu_item('.'.join(path))
            if not clicked:
                continue

            if path not in ctx_ui.ui_state['set_enabled']:
                ctx_ui.ui_state['set_enabled'].add(path)
            else:
                ctx_ui.ui_state['set_enabled'].remove(path)




# # -----------------------------------------------------------------------------
# def _ply(cursor):
#     """
#     """
#     for (key, value) in cursor.items():
#         if imgui.core.tree_node(key, 0):
#             if isinstance(value, str):
#                 imgui.text(value)
#             else:
#                 _ply(cursor = value)
#             imgui.tree_pop()

# # -----------------------------------------------------------------------------
# def menu_item_component(inputs, context, id_ui_source, id_component, cfg_ui):
#     """
#     """
#     (ctx_ui, ctx_frame) = context
#     (clicked, selected) = imgui.menu_item(id_component)
#     if clicked:
#         key = (id_ui_source, id_component)

