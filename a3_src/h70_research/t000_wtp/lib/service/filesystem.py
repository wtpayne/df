# -*- coding: utf-8 -*-
"""
Filesystem service.

"""


import os


SPEC = ('fs', '*')


# -----------------------------------------------------------------------------
def coro(id_node):  # pylint: disable=W0613
    """
    Filesystem service coroutine.

    """
    list_msg_out = list()

    while True:

        list_msg_in = yield (list_msg_out)
        list_msg_out.clear()

        for msg_in in list_msg_in:

            msg_out = {
                '_node':   id_node,
                '_spec':   msg_in['_spec'],
                'listdir': []
            }

            str_path = os.sep + os.sep.join(msg_in['_spec'][1:])
            for str_item in os.listdir(str_path):
                msg_out['listdir'].append({
                    'name': str_item,
                    'spec': (*msg_in['_spec'], str_item)
                })

            list_msg_out.append(msg_out)

