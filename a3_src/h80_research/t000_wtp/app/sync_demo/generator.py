# -*- coding: utf-8 -*-
"""
Generate random key-value test data

"""


import random


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Generate key-value data

    """
    signal = None

    rng = random.Random()
    rng.seed(42)

    list_str_random = _list_str_random()
    rng.shuffle(list_str_random)

    # State.
    #
    map_kv_store = dict()

    # Initialize outputs.
    #
    for id_out in outputs.keys():
        outputs[id_out]['ena'] = False
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

        if not inputs['control']['ena']:
            continue

        map_ts     = inputs['control']['ts']
        str_random = list_str_random[map_ts['idx'] % len(list_str_random)]
        map_kv_store[str_random] = rng.randint(0, 100)

        # Fill outputs.
        #
        for id_out in outputs.keys():
            outputs[id_out]['ena'] = True
            outputs[id_out]['ts'].update(map_ts)
            outputs[id_out]['map'].update(map_kv_store)



# -----------------------------------------------------------------------------
def _list_str_random():
    """
    Return a list of test strings.

    """
    return ['actor',
            'fiction',
            'smoke',
            'cotton',
            'east',
            'leonid',
            'lorenzo',
            'declare',
            'david',
            'deal',
            'adrian',
            'proxy',
            'olympic',
            'house',
            'tennis',
            'correct',
            'optimal',
            'animal',
            'verona',
            'forget',
            'diploma',
            'trade',
            'lesson',
            'tribal',
            'reward',
            'cockpit',
            'prelude',
            'guru',
            'lucas',
            'join',
            'vision',
            'contact',
            'little',
            'pirate']