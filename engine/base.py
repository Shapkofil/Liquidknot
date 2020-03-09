import bpy

from .. import liquidknot, serialization as srl, PATHS


class LiquidknotRenderEngine(bpy.types.RenderEngine):
    # These three members are used by blender to set up the
    # RenderEngine; define its internal name, visible name and capabilities.
    bl_idname = "LIQUIDKNOT"
    bl_label = "Liquidknot"
    bl_use_preview = False

    bl_use_shading_nodes_custom = False

    # Init is called whenever a new render engine instance is created.
    # Multiple instances may exist at the same time,
    # for example for a viewport and final render.
    def __init__(self):
        self.scene_data = None
        self.draw_data = None

    # When the render engine instance is destroy, this is called. Clean up any
    # render engine data here, for example stopping running render threads.
    def __del__(self):
        pass

    # This is the method called by Blender for both final renders (F12) and
    # small preview for materials, world and lights.
    def render(self, depsgraph):

        scene = depsgraph.scene
        scale = scene.render.resolution_percentage / 100.0
        self.size_x = int(scene.render.resolution_x * scale)
        self.size_y = int(scene.render.resolution_y * scale)

        # Fill the render result with a flat color. The framebuffer is
        # defined as a list of pixels, each pixel itself being a list of
        # R,G,B,A values.

        # Sets the scene to the correct frame
        scene.frame_set(scene.frame_current)

        # Serialize the scene
        srl.scene_to_json(scene, path_to_json=PATHS['SCENE'])
        result = self.begin_result(0, 0, self.size_x, self.size_y)

        layer = result.layers[0]
        liquidknot.brender((self.size_x, self.size_y), filepath=PATHS['EXR'])

        # pixels = liquidknot.brender((self.size_x, self.size_y))
        layer.load_from_file(PATHS['EXR'])
        self.end_result(result)
