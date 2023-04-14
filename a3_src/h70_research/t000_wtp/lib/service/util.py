# -*- coding: utf-8 -*-
"""
Message handling utilities module.


"""


import collections


# -----------------------------------------------------------------------------
def iter_elementary_spec(spec_compound):
    """
    Yield each elementary spec in the specified compound spec.

    Yield each elementary data set specification
    that is contained within the specified
    compound data set specification by taking
    a depth-first walk through all the nested
    dictionaries in the compound spec, and
    yielding each elementary spec that is
    visited by the walk.

    """
    stack = collections.deque(sorted(spec_compound.items()));

    while True:

        try:
            (path_parent, value_parent) = stack.pop()
        except IndexError:
            return

        if not isinstance(path_parent, list):
            path_parent = [path_parent]

        if isinstance(value_parent, dict):

            for (key_child, value_child) in sorted(value_parent.items()):

                stack.append((path_parent + [key_child], value_child))

        spec_elementary = value_parent
        yield (tuple(path_parent), spec_elementary)


# -----------------------------------------------------------------------------
def is_match(spec_lhs, spec_rhs):
    """
    Return True iff the LHS specification matches the RHS specification.

    """

    for (element_rhs, element_lhs) in zip(spec_rhs, spec_lhs):

        is_wildcard    = element_rhs == '*' or element_lhs == '*'
        is_equal_value = element_rhs == element_lhs
        is_good_match  = is_wildcard or is_equal_value

        if not is_good_match:
            return False

    return True


# -----------------------------------------------------------------------------
def reset_outputs(set_id_port, outputs):
    """
    Reset all outputs in the specified set.

    """
    for id_port in set_id_port:
        outputs[id_port]['ena'] = False
        if 'list' not in outputs[id_port]:
            outputs[id_port]['list'] = list()
        outputs[id_port]['list'].clear()


# -----------------------------------------------------------------------------
def get_inout_ids(inputs, outputs):
    """
    Return the set of bidirectional input output ids.

    """
    set_id_input  = set(inputs.keys())
    set_id_output = set(outputs.keys())
    set_id_inout  = set_id_input & set_id_output
    return set_id_inout


# -----------------------------------------------------------------------------
def iter_msg(set_id_port, inputs):
    """
    Yield (id_port, message) pairs for each message in the specified inputs.

    """
    for id_port in set_id_port:

        item_input = inputs[id_port]

        try:

            if not item_input['ena']:
                continue

            for msg in item_input['list']:
                yield (id_port, msg)

        except KeyError:
            continue


# -----------------------------------------------------------------------------
def iter_msg_filter(set_id_port, inputs, **kwargs):
    """
    Yield (id_port, message) pairs for each message in the specified inputs.

    Filter by keyword. All keywords must be present in the message and match.

    """
    for (id_port, msg) in iter_msg(set_id_port = set_id_port,
                                   inputs      = inputs):
        try:

            is_match = True
            for key, value in kwargs.items():
                if msg[key] != value:
                    is_match = False

            if is_match:
                yield msg

        except KeyError:
            pass


# -----------------------------------------------------------------------------
def add_message(outputs, message):
    """
    Add a message to all outputs.

    """
    for id_out in outputs.keys():
        outputs[id_out]['ena']  = True
        outputs[id_out]['list'].append(message)


# -----------------------------------------------------------------------------
def offer(spec, id_node, outputs):
    """
    Add an offer to all outputs.

    """
    for id_out in outputs.keys():
        outputs[id_out]['ena']  = True
        outputs[id_out]['list'].append({
            '_node': id_node,
            '_type': 'offer',
            '_spec': spec})


# -----------------------------------------------------------------------------
def request(spec, id_node, outputs):
    """
    Add a request to all outputs.

    """
    for id_out in outputs.keys():
        outputs[id_out]['ena']  = True
        outputs[id_out]['list'].append({
            '_node': id_node,
            '_type': 'request',
            '_spec': spec})
