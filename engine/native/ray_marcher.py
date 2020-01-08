import numpy as np
import math


class RayMarcher(object):

    def __init__(self,
                 resolution,
                 camera_pos=[.0, .0, .0],
                 camera_rot=np.array([]),
                 scene=""):

        self.resolution = np.array(resolution).astype(float)
        self.camera_pos = np.array(camera_pos).astype(float)
        self.camera_rot = np.array(camera_rot).astype(float)

        # ToDo figure out what scene is going to be
        self.scene = scene

    def set_camera(self, camera_pos, camera_rot=[.0, .0, .0]):
        self.camera_pos = np.array(camera_pos)
        self.camera_rot = np.array(camera_rot)

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

        uv = (2 * coords - self.resolution) / self.resolution

        ray_origin = self.camera_pos
        ray_direction = np.array([uv[0], 1., uv[1]])

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

    @staticmethod
    def gauss_len(vec):
        return math.sqrt(sum([x * x for x in vec]))

    # ToDo make lambdas pressets for distance funcs
    def testing_dist(self, anchor):
        return RayMarcher.gauss_len(anchor) - .5


if __name__ == "__main__":
    rm = RayMarcher([9, 9], camera_pos=[.0, -1., .0])
    print(rm.march(np.array([3, 3])))
