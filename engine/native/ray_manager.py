import numpy as np
from .ray_marcher import RayMarcher


class RayManager:

    def __init__(self,
                 resolution,
                 camera_pos=[.0, .0, .0],
                 camera_rot=[.0, .0, .0],
                 scene=""):
        self.resolution = resolution
        self.camera_pos = camera_pos
        self.camera_rot = camera_rot
        self.scene = scene

    def render(self , verbose = False):
        result = []

        # initializing ray_marcher
        rm = RayMarcher(self.resolution,
                        camera_pos=self.camera_pos,
                        camera_rot=self.camera_rot)

        if verbose: 
            print("starting the ray_shooting")
        for x in range(self.resolution[0]):
            for y in range(self.resolution[1]):
                result.append(rm.march([y ,x],verbose=verbose))

        return result


if __name__ == "__main__":
    rayman = RayManager([24, 24],
                        camera_pos=[.0, -1., .0],
                        camera_rot=[.0, .0, np.pi / 6])
    print(rayman.render())
