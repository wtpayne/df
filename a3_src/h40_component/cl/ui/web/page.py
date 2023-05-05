# -*- coding: utf-8 -*-
"""
Bowyer component for web UI layout.

"""


import bower.lib.ui.web.util
import bower.lib.ui.web.markup.html
import bower.lib.web.util
import bower.util


# -----------------------------------------------------------------------------
def reset(runtime, cfg, inputs, state, outputs):
    """
    Reset the bowyer UI component.

    """
    state['page_title']       = cfg['page_title']
    state['id_resource_page'] = cfg['id_resource']
    state['id_topic']         = cfg['id_topic']


# -----------------------------------------------------------------------------
def step(inputs, state, outputs):
    """
    Step the bowyer UI component.

    """
    bowyer.util.clear_outputs(outputs             = outputs,
                              iter_name_output    = ('resources', ),
                              iter_field_to_clear = ('list', ))

    map_res = bowyer.lib.web.util.ResMap()
    if inputs['id_subs']['ena']:
        map_res.topic(**{state['id_topic']: inputs['id_subs']['list']})

    if inputs['id_ui']['ena']:
        map_res.htm(
            **{state['id_resource_page']: bowyer.lib.ui.web.util.page(
                                    title      = state['page_title'],
                                    id_topic   = state['id_topic'],
                                    list_id_ui = inputs['id_ui']['list'])})
        map_res.js(
            bowyer_htmx_extension = bowyer.lib.ui.web.util.bowyer_htmx_extension())

    if map_res:
        outputs['resources']['ena']  = True
        outputs['resources']['list'] = [dict(map_res)]


