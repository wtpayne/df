# -*- coding: utf-8 -*-
"""
NLP processor component.

"""


import spacy


# -----------------------------------------------------------------------------
def reset(runtime, cfg, inputs, state, outputs):
    """
    Reset the NLP processor component.

    """
    state['nlp'] = spacy.load('en_core_web_sm')
    print('LOADED')
    # state['nlp'] = spacy.load('en_core_web_trf')


# -----------------------------------------------------------------------------
def step(inputs, state, outputs):
    """
    Step the NLP processor component.

    """
    if not inputs['chunk']['ena']:
        return

    print('MSG RX.')

    # for doc in state['nlp'].pipe(
    #                         _iter_text(
    #                                 list_chunk = inputs['chunk']['list'])):

        # print('')
        # print('')
        # print('#' * 160)
        # print('')
        # print('')
        # print([(ent.text, ent.label_) for ent in doc.ents])


# -----------------------------------------------------------------------------
def _iter_text(list_chunk):
    """
    """
    for chunk in list_chunk:
        yield chunk['text']