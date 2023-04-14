# -*- coding: utf-8 -*-
"""
Bowyer component for printing data to a stream.

"""


import os.path
import pprint
import sys


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Debug print coroutine.

    """
    signal = None

    # Read config.
    #
    spec_ostream   = cfg.get('output',   'stdout')
    list_delimpath = cfg.get('path',     list())
    do_prettyprint = cfg.get('pretty',   True)
    do_enabledonly = cfg.get('only_ena', True)

    # Select the output stream.
    #
    ostream = None
    if spec_ostream == 'stdout':
        ostream = sys.stdout
    elif spec_ostream == 'stderr':
        ostream = sys.stderr
    else:
        os.makedirs(os.path.dirname(spec_ostream), exist_ok = True)
        ostream = open(spec_ostream, 'wt')

    # Define which inputs
    # we are going to read.
    #
    list_tup_path = list(list())
    if not list_delimpath:
        for key in inputs.keys():
            list_tup_path.append(tuple(key,))
    else:
        for path in list_delimpath:
            list_tup_path.append(tuple(path.split('.')))


    while True:

        inputs = yield (outputs, signal)

        for tup_path in list_tup_path:

            # Check enable flag on selected input.
            #
            id_input = tup_path[0]
            selected = inputs[id_input]
            if do_enabledonly and 'ena' in selected and not selected['ena']:
                continue

            # Drill down to selected data item.
            #
            cursor = inputs
            for name in tup_path:
                cursor = cursor[name]

            # Print it.
            #
            if do_prettyprint:
                pprint.pprint(cursor, stream = ostream)
            else:
                print(cursor, file = ostream)
