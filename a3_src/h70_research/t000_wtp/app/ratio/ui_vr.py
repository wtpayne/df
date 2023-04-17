# -*- coding: utf-8 -*-
"""
Bowyer component to generate a VR UI web page.

"""


import collections
import copy
import json
import textwrap

import bowyer.lib.ui.web.markup.aframe
import bowyer.lib.ui.web.markup.html
import bowyer.lib.ui.web.util
import bowyer.lib.web.util


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Generate diagram VR UI component coroutine.

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

        # Generate HTML and other
        # web resources as required.
        #
        map_ts  = dict()
        map_res = dict()
        for id_in in inputs.keys():
            if inputs[id_in]['ena']:
                map_ts = inputs[id_in]['ts']  # Get a ts for this sim step.
                for (id_path, map_cfg_layout) in inputs[id_in]['map'].items():
                    map_res.update(_generate_web_resources(map_cfg_layout))

        # Fill outputs with generated
        # web resources.
        #
        if map_res:
            for id_out in outputs.keys():
                outputs[id_out]['ena'] = True
                outputs[id_out]['ts'].update(map_ts)
                outputs[id_out]['list'].append(map_res)


# -----------------------------------------------------------------------------
def _generate_web_resources(map_cfg_layout):
    """
    Return the web resources needed to display the specified diagram.

    """
    map_cfg_pos = _calculate_position(map_cfg_layout)
    id_system   = map_cfg_pos['system']['id_system']
    id_res_htm  = '{id_system}.vr.htm'.format(  id_system = id_system )
    id_res_json = '{id_system}.vr.json'.format( id_system = id_system )
    id_res_sse  = '{id_system}.vr.sse'.format(  id_system = id_system )
    rgb         = _colorscheme()
    pos_z       = -1.5
    html        = bowyer.lib.ui.web.markup.html
    aframe      = bowyer.lib.ui.web.markup.aframe
    str_title   = 'System: {id_system}'.format(id_system = id_system)
    page        = html.document(title = str_title)

    with page.head:

        html.meta(charset = 'utf-8')

        html.meta(name    = 'viewport',
                  content = 'width=device-width, initial-scale=1.0')

        html.link(rel     = 'stylesheet',
                  href    = 'tailwind.css')

        html.script(type  = 'text/javascript',
                    src   = 'aframe.js')

        html.script(type  = 'text/javascript',
                    src   = 'aframe_extras.js')

        # html.script(type  = 'text/javascript',
        #             src   = 'aframe_animation_component.js')

        html.script(type  = 'text/javascript',
                    src   = 'super_hands.js')

        html.script(type  = 'text/javascript',
                    src   = 'ratio.js')

    with page:
        with aframe.a_scene(
                        background = 'color: ' + rgb.bg_hi,
                        cursor     = 'rayOrigin: mouse') as scene:

            aframe.a_entity(
                **{'super-hands':     '',
                   'sphere-collider': 'objects: .node',
                   'hand-controls':   'hand: left; handModelStyle: lowPoly; color: #fc9403'})
            aframe.a_entity(
                **{'super-hands':     '',
                   'sphere-collider': 'objects: .node',
                   'hand-controls':   'hand: right; handModelStyle: lowPoly; color: #fc9403'})

            # An entity to manage the other entities.
            #
            list_resource = ','.join((id_res_json,))
            aframe.a_entity(
                visible = False,
                sse     = ('topic: {id_res_sse}; '
                           'resource: {list_resource};').format(
                                            id_res_sse    = id_res_sse,
                                            list_resource = list_resource))

            # Render nodes as a rect with
            # some text inside.
            #
            cfg_runtime_id = map_cfg_pos['runtime']['id']
            for (id_node, cfg_node) in map_cfg_pos['node'].items():
                _add_entity(rgb, pos_z, id_node, cfg_node, cfg_runtime_id)

            # Render edges as a polyline.
            #
            for cfg_edge in map_cfg_pos['edge']:

                str_start = 'start: {x} {y} {z}'.format(
                                                x = cfg_edge['pos_x_start'],
                                                y = cfg_edge['pos_y_start'],
                                                z = cfg_edge['pos_z_start'])
                str_end   = 'end: {x} {y} {z}'.format(
                                                x = cfg_edge['pos_x_end'],
                                                y = cfg_edge['pos_y_end'],
                                                z = cfg_edge['pos_z_end'])
                str_color = 'color: black'
                aframe.a_entity(
                    _class = 'edge',
                    line   = '{start};{end};{color}'.format(
                                                start = str_start,
                                                end   = str_end,
                                                color = str_color))

    # Create a reduced config set for the UI.
    #
    map_cfg_ui = dict()
    for key in ('system', 'host', 'process', 'node', 'edge', 'last_edit'):
        map_cfg_ui[key] = map_cfg_pos[key]

    # Create and return web resources.
    #
    map_res = bowyer.lib.web.util.ResMap()
    map_res.htm(  **{ id_res_htm:  page.render()          })
    map_res.json( **{ id_res_json: json.dumps(map_cfg_ui) })
    map_res.sse(  **{ id_res_sse:  [id_res_json]          })

    return dict(map_res)


# -----------------------------------------------------------------------------
def _add_entity(rgb, pos_z, id_node, cfg_node, cfg_runtime_id):
    """
    Add an entity to the scene.

    """
    id_path    = cfg_runtime_id['id_path']
    id_system  = cfg_runtime_id['id_system']

    list_class_tag = cfg_node['class']
    list_class_tag.append('node')

    if 'selected' in list_class_tag:
        rgb_node = '#FF0000'
    else:
        rgb_node = rgb.node_mid

    bowyer.lib.ui.web.markup.aframe.a_entity(
        id         = id_node,
        _class     = ' '.join(list_class_tag),
        hoverable  = '',
        clickable  = '',
        grabbable  = '',
        node       = ('id_path:   {id_path};'
                      'id_system: {id_system};'
                      'id_node:   {id_node};').format(
                                                id_path   = id_path,
                                                id_system = id_system,
                                                id_node   = id_node),
        geometry   = ('primitive: box; '
                      'width:  {size_w};'
                      'height: {size_h};'
                      'depth:  {size_d};').format(
                                                size_w = cfg_node['size_x'],
                                                size_h = cfg_node['size_y'],
                                                size_d = cfg_node['size_z']),
        material   = ('color: {rgb_color};').format(
                                                rgb_color = rgb_node),
        rotation   = '0.0 0.0 0.0',
        position   = '{pos_x} {pos_y} {pos_z}'.format(
                                                pos_x = cfg_node['pos_x'],
                                                pos_y = cfg_node['pos_y'],
                                                pos_z = cfg_node['pos_z']))


# -----------------------------------------------------------------------------
def _rgb_names():
    """
    Return a namedtuple mapping from color name to RGB value.

    """
    white_light_a = '#FAFAFA'
    white_light_b = '#F0F0F0'
    white_light_c = '#E6E6E6'

    grey_light_a  = '#CACACA'
    grey_light_b  = '#C6C6C6'
    grey_light_c  = '#C0C0C0'

    grey_mid_a    = '#909090'
    grey_mid_b    = '#606060'
    grey_mid_c    = '#303030'

    grey_dark_a   = '#303030'
    grey_dark_b   = '#202020'
    grey_dark_c   = '#101010'

    orange        = '#FC9403'
    blue          = '#0884A6'
    purple        = '#3A0FBA'

    map_rgb = locals()
    RGB     = collections.namedtuple('RGB', map_rgb)
    return RGB(**map_rgb)


# -----------------------------------------------------------------------------
def _colorscheme():
    """
    Return a palette of colours with functional names.

    """
    rgb      = _rgb_names()
    bg_hi    = rgb.white_light_a
    bg_mid   = rgb.white_light_b
    bg_low   = rgb.white_light_c

    node_low = rgb.grey_light_a
    node_mid = rgb.grey_light_b
    node_hi  = rgb.grey_light_c

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


# -------------------------------------------------------------------------
def _calculate_position(map_cfg_layout):
    """
    Convert abstract layout in map_cfg_layout to concrete scene positions.

    The A-Frame coordinate system is as follows:

      - +Y is directed vertically upwards.
      - +X is directed to the right.
      - +Z is directed inwards towards the camera.

    These directions are expressed relative to the
    default camera position (i.e. our orientation
    when we first enter the scene).

    We size system dataflow graph nodes so that
    they are about the same size as a library
    index card:- 15 centimeters by 10 centimeters,
    and about half a centimeter thick.

    The "cards" are placed on a flat horizontal
    plane, as if laying on an invisible table
    in front of the observer. This is done so
    that the observer can reach all parts of
    even a large system by walking around it.

    The data flows through the system from left
    to right across the scene in front of the
    observer. This matches 2D modeling
    conventions.

    The "cards" are oriented so that the shorter
    edge runs in the direction of data flow. This
    is done assuming that system models will
    tend to be much deeper than they are wide,
    as long narrow pipelines are quite prevalent.

    """
    map_cfg_pos        = copy.deepcopy(map_cfg_layout)
    x_cm_size_node     = 10.0  # Short edge - Left to right across the scene.
    y_cm_size_node     =  0.5  # Vertical thickness of "card"
    z_cm_size_node     = 15.0  # Long edge - Depthwise into the scene.
    x_cm_spacing       =  5.0
    y_cm_spacing       = 20.0  # Vertical separation between different layers.
    z_cm_spacing       =  5.0
    x_cm_size_crossbus =  0.0  # Space for crossways buses.
    z_cm_size_longbus  =  0.0
    y_cm_dist_floor    = 76.0  # Height between floor and bottom of diagram.
    z_cm_dist_camera   = 50.0  # Depth between camera and near edge of diagram.
    cm_per_m           = 100
    x_m_size_node      = x_cm_size_node     / cm_per_m
    y_m_size_node      = y_cm_size_node     / cm_per_m
    z_m_size_node      = z_cm_size_node     / cm_per_m
    x_m_spacing        = x_cm_spacing       / cm_per_m
    y_m_spacing        = y_cm_spacing       / cm_per_m
    z_m_spacing        = z_cm_spacing       / cm_per_m
    x_m_size_crossbus  = x_cm_size_crossbus / cm_per_m
    z_m_size_longbus   = z_cm_size_longbus  / cm_per_m
    y_m_dist_floor     = y_cm_dist_floor    / cm_per_m
    z_m_dist_camera    = z_cm_dist_camera   / cm_per_m
    x_m_stride         = (x_m_size_node + x_m_spacing + x_m_size_crossbus)
    y_m_stride         = (y_m_size_node + y_m_spacing)
    z_m_stride         = (z_m_size_node + z_m_spacing + z_m_size_longbus)

    # Get the "length" and "width" of the diagram
    # where "length" is measured in the direction
    # of the dataflow (y in 2D, x in 3D), and
    # "width" is measured across the direction of
    # the dataflow (x in 2D, z in 3D).
    #
    depth_diagram  = 1  # Number of layers
    length_diagram = map_cfg_pos['system']['count_tranche']
    width_diagram  = 0
    for cfg_proc in map_cfg_pos['process'].values():
        width_process  = cfg_proc['size_x']
        width_diagram += width_process

    # Convert them into 3D measurements (in m).
    #
    x_m_size_diagram = length_diagram * x_m_stride
    y_m_size_diagram = depth_diagram  * z_m_stride
    z_m_size_diagram = width_diagram  * z_m_stride

    # We will start with the camera positioned
    # in the middle of the diagram, with the
    # most upstream data source to our left (-x)
    # and the most downstream data sink to our
    # right (+x).
    #
    # The diagram will be flat, at about the same
    # height as a standard office desk. Maybe
    # ever so slightly higher. (y_m_dist_floor)
    #
    #
    #
    x_m_min = -(x_m_size_diagram / 2)
    y_m_min = y_m_dist_floor
    z_m_max = -z_m_dist_camera

    # Layout nodes in the grid.
    #
    for (id_node, cfg_node) in map_cfg_pos['node'].items():
        x_m_offset         = x_m_stride *  cfg_node['idx_y'] # "Down" diagram is L->R
        y_m_offset         = 0                               #
        z_m_offset         = y_m_stride * -cfg_node['idx_x'] # "Across" is into depth.
        cfg_node['pos_x']  = x_m_min + x_m_offset
        cfg_node['pos_y']  = y_m_min + y_m_offset
        cfg_node['pos_z']  = z_m_max + z_m_offset #
        cfg_node['size_x'] = x_m_size_node
        cfg_node['size_y'] = y_m_size_node
        cfg_node['size_z'] = z_m_size_node

    # Layout edges.
    #
    for cfg_edge in map_cfg_pos['edge']:

        id_node_src = cfg_edge['id_node_src']
        id_node_dst = cfg_edge['id_node_dst']
        cfg_src     = map_cfg_pos['node'][id_node_src]
        cfg_dst     = map_cfg_pos['node'][id_node_dst]

        cfg_edge['pos_x_start'] = cfg_src['pos_x'] + (cfg_src['size_x']/2)
        cfg_edge['pos_y_start'] = cfg_src['pos_y']
        cfg_edge['pos_z_start'] = cfg_src['pos_z']
        cfg_edge['pos_x_end']   = cfg_dst['pos_x'] - (cfg_src['size_x']/2)
        cfg_edge['pos_y_end']   = cfg_dst['pos_y']
        cfg_edge['pos_z_end']   = cfg_dst['pos_z']

    return map_cfg_pos
