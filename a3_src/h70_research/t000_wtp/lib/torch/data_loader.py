# -*- coding: utf-8 -*-
"""
Pytorch data loader component.

"""


import torch.utils.data


# -----------------------------------------------------------------------------
def reset(runtime, cfg, inputs, state, outputs):
    """
    Reset data loader component state.

    """
    pass
    # state['loader'] = torch.utils.data.DataLoader(
    #                         dataset,
    #                         batch_size              = 1,
    #                         shuffle                 = False,
    #                         sampler                 = None,
    #                         batch_sampler           = None,
    #                         num_workers             = 0,
    #                         collate_fn              = None,
    #                         pin_memory              = False,
    #                         drop_last               = False,
    #                         timeout                 = 0,
    #                         worker_init_fn          = None,
    #                         multiprocessing_context = None,
    #                         generator               = None,
    #                         *,
    #                         prefetch_factor         = 2,
    #                         persistent_workers      = False)


# -----------------------------------------------------------------------------
def step(inputs, state, outputs):
    """
    Process the next model.

    """
    outputs.foo['ena']   = False

    print('')
    print(id(outputs['foo']))
    print(id(outputs.foo))

    # outputs.data['ena']   = False

    # outputs['data'] = {'ena': True}

    # outputs['model']['model'] = None

    # if state['update_required']:

    #     model       = state['Network']()
    #     device      = torch.device(
    #                             "cuda" if torch.cuda.is_available() else "cpu")
    #     model_state = torch.load(
    #                         state['filepath_model_state'],
    #                         map_location = device)
    #     state['load'](model, model_state)

    #     outputs['model']['model'] = model
    #     outputs['model']['ena']  = True
    #     state['update_required'] = False