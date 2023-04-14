# -*- coding: utf-8 -*-
"""
Pytorch inference node.

"""


import os
import sys

import numpy
import PIL
import torch
import torch.nn.functional
import torchvision.transforms


# =============================================================================
class ToTargetTensor(object):
    """
    """

    # -------------------------------------------------------------------------
    def __call__(self, target):
        """
        """
        return torch.as_tensor(numpy.array(target), dtype=torch.int64).unsqueeze(0)


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Model inference coroutine.

    """
    signal = None

    state['device'] = None
    state['model']  = None

    resolution = 448
    normalize  = torchvision.transforms.Normalize([0.485, 0.456, 0.406],
                                                  [0.229, 0.224, 0.225])
    cropper    = torchvision.transforms.CenterCrop(resolution)
    transform  = torchvision.transforms.Compose([
                    torchvision.transforms.Resize(resolution,
                                                  PIL.Image.NEAREST),
                    cropper,
                    torchvision.transforms.ToTensor(),
                    normalize])

    os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'
    sys.path.append('/media/wtp/Data/dev/STEGO/src/')
    import crf

    while True:

        inputs = yield (outputs, signal)

        for id_out in outputs.keys():
            outputs[id_out]['ena']       = False

        dnn_interval = 300; # About every ten seconds.
        is_dnn_step  = inputs['control']['idx'] % dnn_interval == 0

        if not is_dnn_step:
            continue

        print('STEP DNN (STEGO)')

        # Update model state.
        if inputs['model']['ena']:
            state['device'] = torch.device(
                                "cuda" if torch.cuda.is_available() else "cpu")
            state['model'] = inputs['model']['model']
            state['model'].to(state['device'])
            state['model'].eval()


        if state['model'] and inputs['sample']['ena']:
            img = PIL.Image.fromarray(inputs['sample']['buff'])
            img = transform(img).unsqueeze(0).cuda()

            with torch.no_grad():

                code1 = state['model'](img)
                code2 = state['model'](img.flip(dims=[3]))
                code  = (code1 + code2.flip(dims=[3])) / 2
                code  = torch.nn.functional.interpolate(
                                            code,
                                            img.shape[-2:],
                                            mode          = 'bilinear',
                                            align_corners = False)

                linear_probs  = torch.log_softmax(
                                            state['model'].linear_probe(code),
                                            dim = 1).cpu()

                cluster_probs = state['model'].cluster_probe(
                                            code,
                                            2,
                                            log_probs = True).cpu()

                single_img    = img[0].cpu()

                linear_pred   = crf.dense_crf(
                                        single_img,
                                        linear_probs[0]).argmax(0)

                cluster_pred  = crf.dense_crf(
                                        single_img,
                                        cluster_probs[0]).argmax(0)

            cluster_data = state['model'].label_cmap[cluster_pred]
            cluster_buff = cluster_data.astype(numpy.uint8)
            cluster_img  = PIL.Image.fromarray(cluster_buff)
            resized_img  = cluster_img.resize((160, 120), resample = 0)
            resized_buff = numpy.array(resized_img)

            for id_out in outputs.keys():
                outputs[id_out]['ena']       = True
                outputs[id_out]['ts_rel_us'] = inputs['sample']['ts_rel_us']
                outputs[id_out]['buff']      = resized_buff