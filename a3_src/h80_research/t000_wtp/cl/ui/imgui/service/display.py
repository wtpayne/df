# -*- coding: utf-8 -*-
"""
Xact immediate mode graphical user interface display component.

"""


import collections
import os

import sdl2
import dill

import stableflow.lib.service.util
import stableflow.lib.ui.imgui.util
import stableflow.signal


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Xact immediate mode graphical user interface display component coroutine.

    Manages a single graphical user
    interface window as well as all
    of the components that are sent
    to be displayed on it.

    """

    # Configure and open a graphical
    # user interface window so that we
    # can render components once we have
    # recieved them.
    #
    _set_all_configured_environment_variables(cfg)
    with stableflow.lib.ui.imgui.util.ui_context(
                                   id_node      = runtime['id']['id_node'],
                                   id_screen    = cfg['id_screen'],
                                   name         = cfg['name'],
                                   width        = cfg['width'],
                                   height       = cfg['height'],
                                   filepath_ttf = cfg['filepath_ttf'],
                                   font_size    = cfg['font_size']) as ctx_ui:

        _initialize_ui_state_data_structures(ctx_ui)

        # Send out a request to the service
        # broker to see if there are any top
        # level user interface components
        # for us to display.
        #
        set_id_port = stableflow.lib.service.util.get_inout_ids(inputs, outputs)
        _set_output_request(set_id_port = set_id_port,
                            id_com      = 'toplevel',
                            spec        = ('imgui', 'toplevel', '*'),
                            ctx_ui      = ctx_ui,
                            outputs     = outputs)
        signal = None

        while True:

            inputs = yield (outputs, signal)

            # Collate input messages
            # into a map from id_com
            # to list-of-message. Also
            # keep a list of references
            # to any new UI components
            # that are seen.
            #
            (map_msg_in, list_msg_ui) = _collate_input_messages(
                                                    ctx_ui      = ctx_ui,
                                                    set_id_port = set_id_port,
                                                    inputs      = inputs)

            # Register any new UI
            # components before the
            # frame context is opened
            # so that we can update
            # our event handlers prior
            # to the new components
            # being rendered.
            #
            _register_new_ui_components(list_msg_ui = list_msg_ui,
                                        ctx_ui      = ctx_ui)

            # Render components and
            # single-step each
            # component coroutine.
            #
            with ctx_ui.frame_context() as ctx_frame:
                (signal, list_msg_out) = _step_ui(ctx_ui      = ctx_ui,
                                                  ctx_frame   = ctx_frame,
                                                  map_msg_in  = map_msg_in)

            # Update the output buffer
            # with messages for the
            # service broker(s)
            #
            _set_output_messages(set_id_port  = set_id_port,
                                 list_msg_out = list_msg_out,
                                 outputs      = outputs)


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
def _initialize_ui_state_data_structures(ctx_ui):
    """
    Initialize UI state data structures.

    """
    ctx_ui.ui_state['map_spec']      = dict() # spec -> set(id_com).
    ctx_ui.ui_state['map_coro']      = dict() # id_com -> coro
    ctx_ui.ui_state['set_top_level'] = set()  # {id_com}
    ctx_ui.ui_state['set_enabled']   = set()  # {id_com}

    ctx_ui.event_handlers[sdl2.SDL_QUIT] = _quit


# -----------------------------------------------------------------------------
def _quit(event_data, ui_state):
    """
    Quit callback.

    """
    raise stableflow.signal.Halt(0)


# -----------------------------------------------------------------------------
def _set_output_request(set_id_port, id_com, spec, ctx_ui, outputs):
    """
    Add a request message to the node outputs and update ctx_ui map_spec.

    """
    for id_port in set_id_port:
        outputs[id_port]['ena']  = False
        outputs[id_port]['list'] = list()

    for id_port in set_id_port:
        outputs[id_port]['ena']  = True
        outputs[id_port]['list'].append({'_node': ctx_ui.id_node,
                                         '_type': 'request',
                                         '_spec': spec})

    if spec not in ctx_ui.ui_state['map_spec']:
        ctx_ui.ui_state['map_spec'][spec] = set()
    ctx_ui.ui_state['map_spec'][spec].add(id_com)


# -----------------------------------------------------------------------------
def _collate_input_messages(set_id_port, inputs, ctx_ui):
    """
    Return a map of input messages indexed by destination coroutine id.

    """
    map_msg_in  = collections.defaultdict(list)
    list_msg_ui = list()

    for(_, msg) in stableflow.lib.service.util.iter_msg(set_id_port = set_id_port,
                                                  inputs      = inputs):
        is_match = False
        for (spec_coro, set_id_com) in ctx_ui.ui_state['map_spec'].items():
            if stableflow.lib.service.util.is_match(spec_coro, msg['_spec']):
                is_match = True
                for id_com in set_id_com:
                    map_msg_in[id_com].append(msg)

        if not is_match:
            continue

        if ('type' in msg) and (msg['type'] == 'ui_component'):
            list_msg_ui.append(msg)

    return (map_msg_in, list_msg_ui)


# -----------------------------------------------------------------------------
def _set_output_messages(set_id_port, list_msg_out, outputs):
    """
    Write messages from list_msg_out to the specified outputs.

    """

    for id_port in set_id_port:
        outputs[id_port]['ena'] = False
        outputs[id_port]['list'].clear()

    for msg_out in list_msg_out:
        for id_port in set_id_port:
            outputs[id_port]['ena'] = True
            outputs[id_port]['list'].append(msg_out)


# -----------------------------------------------------------------------------
def _register_new_ui_components(list_msg_ui, ctx_ui):
    """
    Register new UI components.

    """
    for msg in list_msg_ui:

        try:

            id_com = msg['_spec']
            ctx_ui.ui_state['map_coro'][id_com] = _load_coroutine(
                                                    id_node  = ctx_ui.id_node,
                                                    cfg_coro = msg['coro'])

            _update_component_set(
                            set_items = ctx_ui.ui_state['set_top_level'],
                            id_com    = id_com,
                            is_member = msg['is_top_level'])

            _update_component_set(
                            set_items = ctx_ui.ui_state['set_enabled'],
                            id_com    = id_com,
                            is_member = msg['is_enabled'])

            for (id_event, dill_callback) in msg['event_handlers']:
                fcn_callback = dill.loads(dill_callback)
                ctx_ui.event_handlers[id_event] = fcn_callback

        except KeyError:
            continue


# -----------------------------------------------------------------------------
def _load_coroutine(id_node, cfg_coro):
    """
    Attempt to load the frontend coroutine for the current UI component.

    """

    try:
        coro = dill.loads(cfg_coro)(id_node)
        try:
            coro.send(None)
        except StopIteration:
            raise stableflow.signal.Halt(0)
    except KeyError:
        pass

    return coro


# -----------------------------------------------------------------------------
def _update_component_set(set_items, id_com, is_member):
    """
    Add or remove this UI component from the specified set.

    """
    if is_member:
        set_items.add(id_com)
    else:
        set_items.remove(id_com)


# -----------------------------------------------------------------------------
def _step_ui(ctx_ui, ctx_frame, map_msg_in):
    """
    Single step all top level UI components.

    """
    available    = frozenset(ctx_ui.ui_state['map_coro'].keys())
    top_level    = frozenset(ctx_ui.ui_state['set_top_level'])
    enabled      = frozenset(ctx_ui.ui_state['set_enabled'])
    drawn        = available & top_level & enabled
    list_msg_out = list()

    for id_com in sorted(drawn):

        list_msg_out_part = []
        try:

            list_msg_out_part = ctx_ui.ui_state['map_coro'][id_com].send(
                                    (ctx_ui, ctx_frame, map_msg_in[id_com]))

            # Update our routing map.
            #
            for msg_out in list_msg_out_part:
                is_request = (     ('_type' in msg_out)
                               and (msg_out['_type'] == 'request'))
                if is_request:
                    spec = msg_out['_spec']
                    if spec not in ctx_ui.ui_state['map_spec']:
                        ctx_ui.ui_state['map_spec'][spec] = set()
                    if id_com not in ctx_ui.ui_state['map_spec'][spec]:
                        ctx_ui.ui_state['map_spec'][spec].add(id_com)

        except StopIteration:
            raise stableflow.signal.Halt(0)

        if list_msg_out_part:
            list_msg_out.extend(list_msg_out_part)

    signal = None
    return (signal, list_msg_out)


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

