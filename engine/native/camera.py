import numpy as np


class Camera(object):

    def __init__(self, resolution, position, rotation, focal_len=1.):
        self.resolution = resolution
        self.pos = np.array(position).astype(float)
        self.rot = np.array(rotation).astype(float)
        self.focal_len = focal_len

    def calc_ray_dir(self, coords, verbose=False):
        uv = (2 * coords - self.resolution + 1) / (self.resolution - 1)

        # Return vectorize the uv and rotate
        return Camera.rotate_vector([uv[0], self.focal_len, uv[1]],
                                    self.rot,
                                    verbose=verbose)

    @staticmethod
    def rotate_vector(vec, rot, numpify=True, verbose=False):
        if numpify:
            vec = np.array(vec).astype(float)
            rot = np.array(rot).astype(float)

        # Rotation matricies for the three world planes
        matrices = [
            np.array([[np.cos(rot[2]), -np.sin(rot[2]), 0],
                      [np.sin(rot[2]), np.cos(rot[2]), 0],
                      [0, 0, 1]]),
            np.array([[np.cos(rot[1]), 0, -np.sin(rot[1])],
                      [0, 1, 0],
                      [np.sin(rot[1]), 0, np.cos(rot[1])]]),
            np.array([[1, 0, 0],
                      [0, np.cos(rot[0]), -np.sin(rot[0])],
                      [0, np.sin(rot[0]), np.cos(rot[0])]])
        ]

        for rot_matrix in matrices:
            vec = np.dot(vec, rot_matrix)

        if verbose:
            print("rotated to {0}".format(vec))

        return vec

    def rotate(self, rot):
        self.rot += rot

    def move(self, amount):
        self.pos += amount


if __name__ == "__main__":
    Camera.rotate_vector([1, 0, 0], [0, 0, np.pi / 6], verbose=True)
