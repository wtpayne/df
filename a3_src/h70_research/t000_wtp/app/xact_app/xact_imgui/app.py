# -*- coding: utf-8 -*-
"""
Top level UI service for the IMGUI demo app.

"""


import dill

import xact.lib.ui.imgui.widget


SPEC = ('imgui', 'toplevel', '*')


# -----------------------------------------------------------------------------
def coro(id_node):  # pylint: disable=W0613
    """
    Filesystem service coroutine.

    """
    widget       = xact.lib.ui.imgui.widget
    list_msg_out = list()

    while True:

        list_msg_in = yield (list_msg_out)
        list_msg_out.clear()

        list_msg_out.append({
            '_spec':        ('imgui', 'toplevel', 'menu'),
            '_node':        id_node,
            'type':         'ui_component',
            'is_top_level': True,
            'is_enabled':   True,
            'coro':         dill.dumps(widget.main_menu_bar.coro)})
