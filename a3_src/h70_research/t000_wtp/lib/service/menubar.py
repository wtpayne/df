# -*- coding: utf-8 -*-
"""
Imgui main menu bar UI component.

"""


import collections
import contextlib

import imgui

import xact.signal


SPEC = ('imgui', 'toplevel', '*')


# -----------------------------------------------------------------------------
def coro():
    """
    Imgui main menu bar UI component frontend.

    """

    map_menu     = dict()
    list_msg_out = list()

    while True:

        (ctx_ui, ctx_frame, list_msg_in) = yield (list_msg_out)
        list_msg_out.clear()

        with main_menu_bar_context() as bar:

            add_file_menu()
            add_component_menu(ctx_ui)
            add_dynamic_menu(list_msg_in, list_msg_out)


# -----------------------------------------------------------------------------
def add_dynamic_menu(list_msg_in, list_msg_out):
    """
    """
    with menu_context('Dynamic') as menu:
        if not menu:
            return

        imgui.menu_item('pending2')
        list_msg_out.append({
            '_type':  'request',
            '_spec':  ('main_menu_bar', 'dynamic'),
        })


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


# -----------------------------------------------------------------------------
def add_file_menu():
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
def add_component_menu(ctx_ui):
    """
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


# -----------------------------------------------------------------------------
def menu_item_component(inputs, context, id_ui_source, id_component, cfg_ui):
    """
    """
    (ctx_ui, ctx_frame) = context
    (clicked, selected) = imgui.menu_item(id_component)
    if clicked:
        key = (id_ui_source, id_component)


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
