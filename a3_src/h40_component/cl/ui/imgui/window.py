# -*- coding: utf-8 -*-
"""
Dynamic IMGUI UI window component.

"""


import collections
import os
import re

import sdl2
import dill

import xact.lib.ui.imgui.util
import xact.signal
import xact.util


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Event-loop coroutine to render a dynamic IMGUI UI window.

    """

    signal  = None
    id_node = runtime['id']['id_node']

    _set_all_configured_environment_variables(cfg)
    _initialize_output_data_structures(outputs)

    with xact.lib.ui.imgui.util.ui_context(
                                width  = cfg['width'],
                                height = cfg['height'],
                                name   = cfg['name']) as ctx_ui:

        _initialize_ui_state_data_structures(ctx_ui)

        while True:

            inputs = yield (outputs, signal)

            map_list_msg_by_type = _filter_and_collate(id_node = id_node,
                                                       inputs  = inputs)

            _update_ui_components(
                    ctx_ui      = ctx_ui,
                    list_msg_ui = map_list_msg_by_type['ui_component'])

            # frame_context includes event handling
            with ctx_ui.frame_context() as ctx_frame:

                _step_top_level_components(ctx_ui    = ctx_ui,
                                           ctx_frame = ctx_frame,
                                           inputs    = inputs,
                                           outputs   = outputs)


# -----------------------------------------------------------------------------
def _set_all_configured_environment_variables(cfg):
    """
    Set all configured environment variables.

    When creating a window on a
    remote display, we may need
    to set the XAUTHORITY and
    DISPLAY environment variables.


    """
    if 'env' not in cfg:
        return

    for (key, value) in cfg['env'].items():
        os.environ[key] = value


# -----------------------------------------------------------------------------
def _initialize_output_data_structures(outputs):
    """
    Initialize output data structures.

    We need to ensure that these are initialized
    before the first yield-point as they will
    likely be used to drive feedback edges in the
    compute graph.

    """
    for (id_output, item_output) in outputs.items():
        item_output['ena']  = False
        item_output['list'] = list()


# -----------------------------------------------------------------------------
def _initialize_ui_state_data_structures(ctx_ui):
    """
    Initialize UI state data structures.

    """

    # Map of (id_input, id_component) -> ui_component).
    #
    ctx_ui.ui_state['map_component'] = dict()

    # Set of top level components as (id_input, id_component) pairs.
    #
    ctx_ui.ui_state['set_top_level']   = set()

    # Set of enabled components as (id_input, id_component) pairs.
    #
    ctx_ui.ui_state['set_enabled']     = set()

    # Set default event handler callbacks
    #
    ctx_ui.event_handlers[sdl2.SDL_QUIT] = _quit


# -----------------------------------------------------------------------------
def _quit(event_data, ui_state):
    """
    Quit callback.

    """
    raise xact.signal.Halt(0)


# -----------------------------------------------------------------------------
def _filter_and_collate(id_node, inputs):
    """
    Return a mapping from a message type to a list of messages of that type.

    Discard messages that are not intended for the
    specified id_node.

    """

    map_list_msg_by_type = collections.defaultdict(list)

    for (id_input, item_input) in inputs.items():
        try:

            if not item_input['ena']:
                continue

            for msg in item_input['list']:

                # Ignore messages not intended for
                # the specified id_node.
                #
                if re.match(msg['dst'][0], id_node) is None:
                    continue

                # Keep a note of the point of
                # origin of the message. We
                # may use this later to route
                # responses.
                #
                msg['id_input'] = id_input

                map_list_msg_by_type[msg['type']].append(msg)

        except KeyError:
            continue
    return map_list_msg_by_type


# -----------------------------------------------------------------------------
def _update_ui_components(ctx_ui, list_msg_ui):
    """
    Update the window's cache of UI components.

    """
    for msg_ui in list_msg_ui:

        # Source-specific UI component configuration.
        #
        cache = ctx_ui.ui_state['map_component']
        path  = msg_ui['dst'][1:]
        if path not in cache:
            cache[path] = dict()

        cache[path]['coro'] = _load_coroutine(msg_ui['coro'])

        if 'event_handlers' in msg_ui:
            cache[path]['event_handlers'] = dict(
                                    _iter_event_handler_items(
                                        cfg_handler = msg_ui['event_handlers']))

        _update_component_set(set_items = ctx_ui.ui_state['set_top_level'],
                              path      = path,
                              is_member = msg_ui['is_top_level'])

        _update_component_set(set_items = ctx_ui.ui_state['set_enabled'],
                              path      = path,
                              is_member = msg_ui['is_enabled'])

# -----------------------------------------------------------------------------
def _iter_input_ui_component(inputs):
    """
    Yield all UI component configuration in inputs.

    """
    for (id_input, item_input) in inputs.items():

        try:

            if not item_input['ena']:
                continue

            for msg in item_input['list']:
                if msg.get('type', None) != 'ui_component':
                    continue

                cfg_ui = msg
                yield (id_input, cfg_ui)

        except KeyError:
            continue


# -----------------------------------------------------------------------------
def _load_coroutine(cfg_coro):
    """
    Attempt to load the frontend coroutine for the current UI component.

    """

    try:
        coro = dill.loads(cfg_coro)()
        try:
            coro.send(None)
        except StopIteration:
            raise xact.signal.Halt(0)
    except KeyError:
        pass

    return coro


# -----------------------------------------------------------------------------
def _iter_event_handler_items(cfg_handler):
    """
    Yield (id_handler, fcn_handler) for all event handlers in cfg_handler.

    """

    try:
        for (id_handler, fcn_handler) in cfg_handler:
            yield (id_handler, dill.loads(fcn_handler))
    except KeyError:
        pass


# -----------------------------------------------------------------------------
def _update_component_set(set_items, path, is_member):
    """
    Add or remove this UI component from the specified set.

    """
    if is_member:
        set_items.add(path)
    else:
        set_items.remove(path)


# -----------------------------------------------------------------------------
def _step_top_level_components(ctx_ui, ctx_frame, inputs, outputs):
    """
    Single step all enabled top level UI components.

    """
    list_request  = list()
    list_response = list()
    list_channel  = outputs.keys()

    available     = frozenset(ctx_ui.ui_state['map_component'].keys())
    top_level     = frozenset(ctx_ui.ui_state['set_top_level'])
    enabled       = frozenset(ctx_ui.ui_state['set_enabled'])
    drawn         = available & top_level & enabled

    # Route inbound responses to the appropriate
    # component.
    #
    for id_channel in list_channel:

        if not inputs[id_channel]['ena']:
            continue

        list_response.extend(inputs[id_channel]['list'])

    map_response = xact.lib.ui.imgui.util.route(iter_msg  = list_response,
                                                iter_keys = drawn)

    # TODO: CHOOSE KEYS


    for path in sorted(drawn):

        coroutine = ctx_ui.ui_state['map_component'][path]['coro']
        context   = (ctx_ui, ctx_frame)

        # TODO: ROUTING
        list_response_coro = list_response

        try:
            list_request_coro = coroutine.send((list_response_coro, context))
        except StopIteration:
            raise xact.signal.Halt(0)
        if list_request_coro:
            list_request.extend(list_request_coro)

    # Route outbound requests to the appropriate
    # output port.
    #
    map_request = xact.lib.ui.imgui.util.route(iter_msg  = list_request,
                                               iter_keys = list_channel)

    for id_channel in list_channel:

        outputs[id_channel]['ena'] = False
        outputs[id_channel]['list'].clear()

        if id_channel not in map_request:
            continue

        outputs[id_channel]['ena'] = True
        outputs[id_channel]['list'].extend(map_request[id_channel])

