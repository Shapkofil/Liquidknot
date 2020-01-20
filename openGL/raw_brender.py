import numpy as np
from core import render
import time


def raw_brender(resolution,
                vertex_code=None,
                fragment_code=None):
    raw_data = render(resolution, vertex_code, fragment_code)
    refine = np.reshape(raw_data, (resolution[0] * resolution[1], 4))
    return refine


# ToDo entry point
if __name__ == "__main__":
    init = time.time()
    print(raw_brender((1980, 1080)))
    print(time.time()-init)
