import numpy as np
import math
from camera import Camera


class RayMarcher(object):

    def __init__(self,
                 resolution,
                 camera_pos=[.0, .0, .0],
                 camera_rot=[.0, .0, .0],
                 scene=""):

        self.resolution = np.array(resolution).astype(float)
        self.camera = Camera(
            self.resolution,
            position=camera_pos,
            rotation=camera_rot)

        # ToDo do the scene thingies with json
        self.scene = scene

    def march(self, coords, verbose=False):

        # convert coords to numpy float
        coords = np.array(coords).astype(float)

        if coords[0] >= self.resolution[0] or coords[1] >= self.resolution[1]:
            return .0

        # Hyper Params
        # ToDo get hyper params externely
        MAX_DISTANCE = 1000.0
        MARCH_STEPS = 48
        PLANK = .005

        ray_origin = self.camera.pos
        ray_direction = self.camera.calc_ray_dir(coords)

        march_distance = .0
        epoch = 0

        while True:
            # Get Distance with lambda presset or a custom function
            current_rad = self.testing_dist(ray_origin)
            march_distance += current_rad

            if MAX_DISTANCE < march_distance or MARCH_STEPS < epoch:
                break

            if current_rad < PLANK:
                return 1.

            ray_origin = ray_origin + current_rad * ray_direction
            epoch += 1

        if verbose:
            print("{0} steps marched".format(epoch))
            print("marched {0} units".format(march_distance))

        return .0

    # ToDo make an utility class
    @staticmethod
    def gauss_len(vec):
        return math.sqrt(sum([x * x for x in vec]))

    # ToDo make lambdas pressets for distance funcs in a separate file
    def testing_dist(self, anchor):
        return RayMarcher.gauss_len(anchor) - .6


if __name__ == "__main__":
    # testing rig
    rm = RayMarcher([9, 9], camera_pos=[.0, -1., .0])
    print(rm.march(np.array([3, 3])))
