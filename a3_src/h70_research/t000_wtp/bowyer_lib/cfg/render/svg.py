# -*- coding: utf-8 -*-
"""
Bowyer component for rendering a bowyer configuration file to SVG markup.

"""


import collections
import copy
import dataclasses
import typing

import bowyer.lib.ui.web.markup.svg
import bowyer.proc
import bowyer.util


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Render provided config to SVG.

    """
    signal = None

    # Initialize outputs.
    #
    for id_out in outputs.keys():
        outputs[id_out]['ena'] = True
        outputs[id_out]['ts']  = dict()
        outputs[id_out]['map'] = dict()

    while True:

        inputs = yield (outputs, signal)

        # Reset outputs.
        #
        for id_out in outputs.keys():
            outputs[id_out]['ena'] = False
            outputs[id_out]['ts'].clear()
            outputs[id_out]['map'].clear()

        # Construct an ECS model of the system
        # using the supplied configuration data.
        # This means that the ECS model will be
        # rebuilt from scratch each time the
        # configuration file is read.
        #
        map_ts  = dict()
        map_svg = dict()
        for id_in in inputs.keys():
            if inputs[id_in]['ena']:
                map_ts = inputs[id_in]['ts']  # Get a ts for this sim step.
                for (filepath, map_cfg_layout) in inputs[id_in]['map'].items():
                    id_system          = map_cfg_layout['system']['id_system']
                    map_cfg_pos        = _calculate_position(map_cfg_layout)
                    map_svg[id_system] = _render_svg(map_cfg_pos)

        # Set outputs.
        #
        if map_svg:
            for id_out in outputs.keys():
                outputs[id_out]['ena'] = True
                outputs[id_out]['ts'].update(map_ts)
                outputs[id_out]['map'].update(map_svg)


# -------------------------------------------------------------------------
def _calculate_position(map_cfg_layout):
    """
    Convert abstract layout in map_cfg_layout to concrete positions.

    """
    map_cfg_pos    = copy.deepcopy(map_cfg_layout)

    diagram_border = 10
    swimlane_title = 30
    longbus_x      = 60  # Longitudinal bus width (top to bottom swimlanes)
    crossbus_y     = 30  # Cross bus height (top to bottom swimlanes)

    node_size_x    = 200
    node_size_y    = 30
    node_margin_x  = 10
    node_margin_y  = 10

    node_stride_x  = (node_size_x + node_margin_x)
    node_stride_y  = (node_size_y + node_margin_y + crossbus_y)

    # Layout nodes in the grid.
    #
    for (id_node, cfg_node) in map_cfg_pos['node'].items():

        cfg_node['size_x'] = node_size_x
        cfg_node['size_y'] = node_size_y
        cfg_node['pos_x']  = (   diagram_border
                               + longbus_x
                               + node_margin_x
                               + (node_stride_x * cfg_node['idx_x']))
        cfg_node['pos_y']  = (   diagram_border
                               + swimlane_title
                               + (node_stride_y * cfg_node['idx_y']))

    # Layout process swimlanes.
    #
    for (id_proc, cfg_proc) in map_cfg_pos['process'].items():

        idx_x  = cfg_proc['idx_x']
        size_x = cfg_proc['size_x']
        size_y = map_cfg_pos['system']['count_tranche']

        cfg_proc['pos_x']  = diagram_border + longbus_x + (idx_x * node_size_x)
        cfg_proc['pos_y']  = diagram_border
        cfg_proc['size_x'] = (   node_margin_x
                               + node_margin_x
                               + (size_x * node_stride_x))
        cfg_proc['size_y'] = (   node_margin_y
                               + node_margin_y
                               + (size_y * node_stride_y))

    # Layout edges.
    #
    for cfg_edge in map_cfg_pos['edge']:

        id_node_src = cfg_edge['id_node_src']
        id_node_dst = cfg_edge['id_node_dst']
        cfg_src     = map_cfg_pos['node'][id_node_src]
        cfg_dst     = map_cfg_pos['node'][id_node_dst]

        cfg_edge['pos_x_start'] = cfg_src['pos_x'] + (cfg_src['size_x'] / 2)
        cfg_edge['pos_y_start'] = cfg_src['pos_y'] + cfg_src['size_y']
        cfg_edge['pos_x_end']   = cfg_dst['pos_x'] + (cfg_dst['size_x'] / 2)
        cfg_edge['pos_y_end']   = cfg_dst['pos_y']

    return map_cfg_pos


# -----------------------------------------------------------------------------
def _render_svg(map_cfg_pos):
    """
    Return a SVG text representation of the specified configuration data.

    """
    rgb = _colorscheme()
    cfg = {
        'node': {
            'rx':                   10,
            'fill':                 rgb.bg_low,
            'fill-opacity':         1.0,
            'stroke':               rgb.edge_mid,
            'stroke-opacity':       1.0,
            'stroke-width':         0.75
        },
        'node_text': {
            'fill':                 rgb.text_mid,
            'dominant-baseline':    'middle',
            'text-anchor':          'middle',
            'font-family':          'Tecnico'
        },
        'proc': {
            'rx':                   0,
            'fill':                 rgb.bg_mid,
            'fill-opacity':         0.5,
            'stroke':               rgb.edge_mid,
            'stroke-opacity':       1.0,
            'stroke-width':         0.75
        },
        'proc_text': {
            'fill':                 rgb.text_mid,
            'dominant-baseline':    'top',
            'text-anchor':          'middle',
            'font-family':          'Tecnico'
        },
        'edge': {
            'stroke':               rgb.edge_mid,
            'stroke-opacity':       1.0,
            'stroke-width':         0.75
        },
    }

    svg  = bowyer.lib.ui.web.markup.svg
    html = bowyer.lib.ui.web.markup.html
    with svg.svg(
           **{'width':  '100%',
              'height': '800'}) as dom_svg:

        with svg.defs():
            html.style('@import url("/tecnicofino.woff2");')

        # Render process swimlanes as a
        # rect with text at the top.
        #
        for (id_proc, cfg_proc) in map_cfg_pos['process'].items():

            svg.rect(
                x           = cfg_proc['pos_x'],
                y           = cfg_proc['pos_y'],
                width       = cfg_proc['size_x'],
                height      = cfg_proc['size_y'],
                **cfg['proc'])
            svg.text(
                id_proc,
                x           = cfg_proc['pos_x'] + (cfg_proc['size_x'] / 2),
                y           = cfg_proc['pos_y'] + 15,
                **cfg['proc_text'])

        # Render nodes as a rect with
        # some text inside.
        #
        for (id_node, cfg_node) in map_cfg_pos['node'].items():

            cfg_node['list_tag'] = ['a', 'b']

            svg.rect(
                x           = cfg_node['pos_x'],
                y           = cfg_node['pos_y'],
                width       = cfg_node['size_x'],
                height      = cfg_node['size_y'],
                **{'class': ' '.join(cfg_node['list_tag'])},
                **cfg['node'])
            svg.text(
                id_node,
                x           = cfg_node['pos_x'] + (cfg_node['size_x'] / 2),
                y           = cfg_node['pos_y'] + (cfg_node['size_y'] / 2),
                **cfg['node_text'])

        # Render edges as a polyline.
        #
        for cfg_edge in map_cfg_pos['edge']:

            str_point_start = '{x},{y}'.format(x = cfg_edge['pos_x_start'],
                                               y = cfg_edge['pos_y_start'])
            str_point_end   = '{x},{y}'.format(x = cfg_edge['pos_x_end'],
                                               y = cfg_edge['pos_y_end'])
            str_points      = '{start} {end}'.format(start = str_point_start,
                                                     end   = str_point_end)
            svg.polyline(
                points = str_points,
                **cfg['edge'])

    # Render the SVG DOM as a single line
    # string that can be sent over SSE.
    #
    str_svg_multiline = dom_svg.render()
    str_svg_oneline   = ''.join(
                (line.strip() for line in str_svg_multiline.splitlines()))
    return str_svg_oneline


# -----------------------------------------------------------------------------
def _rgb_names():
    """
    Return a namedtuple mapping from color name to RGB value.

    """
    grey_light_a = '#FAFAFA'
    grey_light_b = '#F6F6F6'
    grey_light_c = '#F0F0F0'

    grey_mid_a   = '#909090'
    grey_mid_b   = '#606060'
    grey_mid_c   = '#303030'

    grey_dark_a  = '#303030'
    grey_dark_b  = '#202020'
    grey_dark_c  = '#101010'

    orange       = '#FC9403'
    blue         = '#0884A6'
    purple       = '#3A0FBA'

    map_rgb = locals()
    RGB     = collections.namedtuple('RGB', map_rgb)
    return RGB(**map_rgb)


# -----------------------------------------------------------------------------
def _colorscheme():
    """
    Return a palette of colours with functional names.

    """
    rgb      = _rgb_names()
    bg_hi    = rgb.grey_light_a
    bg_mid   = rgb.grey_light_b
    bg_low   = rgb.grey_light_c

    edge_low = rgb.grey_mid_a
    edge_mid = rgb.grey_mid_b
    edge_hi  = rgb.grey_mid_c

    text_low = rgb.grey_mid_a
    text_mid = rgb.grey_mid_b
    text_hi  = rgb.grey_mid_c

    accent_a = rgb.orange
    accent_b = rgb.blue
    accent_c = rgb.purple

    map_rgb = locals()
    del map_rgb['rgb']
    RGB = collections.namedtuple('RGB', map_rgb)
    return RGB(**map_rgb)
