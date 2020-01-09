import numpy as np
from ray_marcher import RayMarcher


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

    def render(self):
        result = np.zeros(self.resolution, dtype=float)

        # initializing ray_marcher
        rm = RayMarcher(self.resolution,
                        camera_pos=self.camera_pos,
                        camera_rot=self.camera_rot)

        for x in range(self.resolution[0]):
            for y in range(self.resolution[1]):
                result[x, y] = rm.march([x, y])

        return result


if __name__ == "__main__":
    rayman = RayManager([24, 24],
                        camera_pos=[.0, -2., .0],
                        camera_rot=[np.pi / 6, .0, 0.])
    print(rayman.render())
