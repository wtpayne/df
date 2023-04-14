# -*- coding: utf-8 -*-
"""
Tetra environment model component.

"""


import math
import time
import os
import queue
import multiprocessing

import cv2
import panda3d.core
# panda3d.core.loadPrcFileData('', 'window-type offscreen')
panda3d.core.loadPrcFileData('', 'audio-library-name null')
# panda3d.core.loadPrcFileData('', 'load-file-type p3assimp')
import direct
import direct.showbase.ShowBase
import direct.task
import numpy.random
import numpy

import xact.util


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Tetra environment model component coroutine.

    """
    signal             = None
    tup_name_output    = ('ais_00', 'camera_00', 'radar_00', 'comms_00')
    tup_field_to_clear = ('list', )
    xact.util.clear_outputs(outputs             = outputs,
                            iter_name_output    = tup_name_output,
                            iter_field_to_clear = tup_field_to_clear)

    sim = Sim(cfg)
    while True:
        inputs = yield (outputs, signal)

        sim.taskMgr.step()
        sim.graphicsEngine.renderFrame()
        img_frame = capture_screenshot(node_camera = sim.camNode)

        outputs['camera_00']['ena'] = True
        outputs['camera_00']['list'].clear()
        outputs['camera_00']['list'].append(img_frame)


# -----------------------------------------------------------------------------
def capture_screenshot(node_camera):
    """
    Capture an image from the specified camera.

    """
    display_region = node_camera.getDisplayRegion(0)
    texture_gpu    = display_region.getScreenshot()
    texture_ram    = texture_gpu.getRamImage()
    texture_view   = memoryview(texture_ram).tolist()

    size_y         = texture_gpu.getYSize()
    size_x         = texture_gpu.getXSize()
    count_channels = 4
    size_img       = (size_y, size_x, count_channels)

    ndarray_img    = numpy.array(texture_view, dtype = numpy.uint8)
    ndarray_img    = ndarray_img.reshape(size_img)
    ndarray_img    = ndarray_img[::-1]
    return ndarray_img




# =============================================================================
class Sim(direct.showbase.ShowBase.ShowBase):
    """
    Environment simulation.

    """

    # -------------------------------------------------------------------------
    def __init__(self, cfg):
        """
        Environment simulation ctor.

       """
        direct.showbase.ShowBase.ShowBase.__init__(self)

        # Load the environment model.
        self.scene = self.loader.loadModel("models/environment")
        # Reparent the model to render.
        self.scene.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)

        mybuffer = base.win.makeTextureBuffer("My Buffer", 512, 512)
        mytexture = mybuffer.getTexture()
        mybuffer.setSort(-100)
        mycamera = base.makeCamera(mybuffer)
        mycamera.reparentTo(self.scene)

        self.buffer = mybuffer

        # load_prc_file_data("", """
        #     textures-power-2 none
        #     gl-coordinate-system default
        #     window-title Panda3D ShaderTerrainMesh Demo
        #     filled-wireframe-apply-shader true
        #     # As an optimization, set this to the maximum number of cameras
        #     # or lights that will be rendering the terrain at any given time.
        #     stm-max-views 8
        #     # Further optimize the performance by reducing this to the max
        #     # number of chunks that will be visible at any given time.
        #     stm-max-chunk-count 2048
        # """)

        # direct.showbase.ShowBase.ShowBase.__init__(self)

        # self.camLens.set_fov(90)
        # self.camLens.set_near_far(0.1, 50000)

        # self.terrain_node = panda3d.core.ShaderTerrainMesh()

        # heightfield = self.loader.loadTexture(cfg['dirpath_res'] + 'ocean_heightfield.png')
        # # heightfield = self.loader.loadTexture('/media/wtp/Data/models/ocean_heightfield.png')
        # heightfield.wrap_u = panda3d.core.SamplerState.WM_clamp
        # heightfield.wrap_v = panda3d.core.SamplerState.WM_clamp
        # self.terrain_node.heightfield = heightfield

        # # Set the target triangle width. For a value of 10.0 for example,
        # # the terrain will attempt to make every triangle 10 pixels wide on screen.
        # self.terrain_node.target_triangle_width = 10.0

        # # Generate the terrain
        # self.terrain_node.generate()

        # # Attach the terrain to the main scene and set its scale. With no scale
        # # set, the terrain ranges from (0, 0, 0) to (1, 1, 1)
        # self.terrain = self.render.attach_new_node(self.terrain_node)
        # self.terrain.set_scale(1024, 1024, 10)
        # self.terrain.set_pos(-512, -512, 0.0)

        # # Set a shader on the terrain. The ShaderTerrainMesh only works with
        # # an applied shader. You can use the shaders used here in your own application
        # terrain_shader = panda3d.core.Shader.load(panda3d.core.Shader.SL_GLSL,
        #                                           cfg['dirpath_res'] + 'xact_lib/src/xact/app/tetra/terrain.vert.glsl',
        #                                           cfg['dirpath_res'] + 'xact_lib/src/xact/app/tetra/terrain.frag.glsl')
        # self.terrain.set_shader(terrain_shader)
        # self.terrain.set_shader_input("camera", self.camera)

        # # Shortcut to view the wireframe mesh
        # self.accept("f3", self.toggleWireframe)

        # grass_tex = self.loader.loadTexture("/media/wtp/Data/models/grass.png")
        # grass_tex.set_minfilter(SamplerState.FT_linear_mipmap_linear)
        # grass_tex.set_anisotropic_degree(16)
        # self.terrain.set_texture(grass_tex)

        # self.boat = self.loader.loadModel(cfg['dirpath_res'] + 'boat.obj')
        # # self.boat = self.loader.loadModel(cfg['dirpath_res'] + '11806_boat_v1_L3.obj')
        # self.boat.reparentTo(self.render)
        # self.boat.setScale(0.1, 0.1, 0.1)
        # self.boat.setPos(0, 0, 4.3)
        # self.taskMgr.add(self.testTask, 'testTask')

    # -------------------------------------------------------------------------
    def testTask(self, task):
        """
        Foo

        """
        angleDegrees    = task.time * 6.0
        angleRadians    = angleDegrees * (math.pi / 180.0)
        sinAngleRadians = math.sin(angleRadians)
        cosAngleRadians = math.cos(angleRadians)

        self.camera.setPos(200 * sinAngleRadians, -200 * cosAngleRadians, 30)
        self.camera.setHpr(angleDegrees, 0, 0)
        return direct.task.Task.cont


