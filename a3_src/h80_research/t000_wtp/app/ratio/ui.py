# -*- coding: utf-8 -*-
"""
Generate diagram UI.

"""

import bowyer.lib.ui.web.markup.html
import bowyer.lib.ui.web.util
import bowyer.lib.web.util


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Generate diagram UI component coroutine.

    """
    signal = None

    # Initialize outputs.
    #
    for id_out in outputs.keys():
        outputs[id_out]['ena']  = False
        outputs[id_out]['ts']   = dict()
        outputs[id_out]['list'] = list()

    while True:

        inputs = yield (outputs, signal)

        # Reset outputs.
        #
        for id_out in outputs.keys():
            outputs[id_out]['ena'] = False
            outputs[id_out]['ts'].clear()
            outputs[id_out]['list'].clear()

        map_res = dict()

        # Create a page for each
        # supplied SVG diagram.
        #
        if 'svg' in inputs and (inputs['svg']['ena']):
            map_ts = inputs['svg']['ts']
            for (id_system, str_svg) in inputs['svg']['map'].items():
                map_res.update(_generate_web_resources_svg(id_system, str_svg))

        # Create a page for each
        # supplied A-Frame scene.
        #
        if 'aframe' in inputs and (inputs['aframe']['ena']):
            map_ts = inputs['aframe']['ts']
            for (id_system, str_aframe) in inputs['aframe']['map'].items():
                map_res.update(_generate_web_resources_aframe(
                                                        id_system, str_aframe))

        # If any HTML has been rendered,
        # then output it.
        #
        if map_res:
            for id_out in outputs.keys():
                outputs[id_out]['ena'] = True
                outputs[id_out]['ts'].update(map_ts)
                outputs[id_out]['list'].append(map_res)


# -----------------------------------------------------------------------------
def _generate_web_resources_svg(id_system, str_svg):
    """
    Return the web resources needed to display the specified diagram.

    """
    id_res_sse = '{id_system}.2d.sse'.format(    id_system = id_system )
    id_res_htm = '{id_system}.2d.ui.htm'.format( id_system = id_system )
    id_res_svg = '{id_system}.2d.svg'.format(    id_system = id_system )

    str_html = _render_html(id_system   = id_system,
                            id_res_sse  = id_res_sse,
                            id_res_svg  = id_res_svg,
                            str_diagram = str_svg)

    map_res = bowyer.lib.web.util.ResMap()
    map_res.htm(   **{id_res_htm: str_html})
    map_res.svg(   **{id_res_svg: str_svg})
    map_res.topic( **{id_res_sse: [id_res_svg]})
    return dict(map_res)


# -----------------------------------------------------------------------------
def _generate_web_resources_aframe(id_system, str_aframe):
    """
    Return the web resources needed to display the specified diagram.

    """
    id_res_sse = '{id_system}.3d.sse'.format(    id_system = id_system )
    id_res_htm = '{id_system}.3d.ui.htm'.format( id_system = id_system )
    id_res_svg = '{id_system}.3d.htm'.format(    id_system = id_system )

    str_html = _render_html(id_system   = id_system,
                            id_res_sse  = id_res_sse,
                            id_res_svg  = id_res_svg,
                            str_diagram = str_aframe)

    map_res = bowyer.lib.web.util.ResMap()
    map_res.htm(   **{id_res_htm: str_html})
    map_res.htm(   **{id_res_svg: str_aframe})
    map_res.topic( **{id_res_sse: [id_res_svg]})
    return dict(map_res)


# -----------------------------------------------------------------------------
def _render_html(id_system, id_res_sse, id_res_svg, str_diagram):
    """
    Return the html for displaying the diagram.

    """
    str_title = 'System: {id_system}'.format(id_system = id_system)
    html      = bowyer.lib.ui.web.markup.html
    page      = html.document(title = str_title)

    with page.head:

        html.meta(charset = 'utf-8')

        html.meta(name    = 'viewport',
                  content = 'width=device-width, initial-scale=1.0')

        html.link(rel     = 'stylesheet',
                  href    = 'tailwind.css')

        html.script(type  = 'text/javascript',
                    src   = 'htmx.js')

        html.script(type  = 'text/javascript',
                    src   = 'sse.js')

        html.script(type  = 'text/javascript',
                    src   = 'aframe.js')

        html.script(type  = 'text/javascript',
                    src   = 'sse.js')

    use_htmx_sse_ext = False  # Doesn't seem to work yet.
    if use_htmx_sse_ext:

        with page:
            with html.div(data_hx_ext = 'sse',
                          sse_connect = '/' + id_res_sse,
                          sse_swap    = id_res_svg):
                html.raw(str_diagram)

    else:  # Legacy htm SSE.

        with page:
            with html.div(data_hx_sse = 'connect:/{id}'.format(id = id_res_sse)):
                with html.div(data_hx_trigger = 'sse:{id}'.format(id = id_res_svg),
                              data_hx_get     = '/{id}'.format(id = id_res_svg)):
                    html.raw(str_diagram)

    str_htm = page.render()
    return str_htm
