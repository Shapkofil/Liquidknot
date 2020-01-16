import cv2
import numpy as np
import openGL.render


raw_read = openGL.render((1920, 1080))
refine = np.asarray(raw_read[:, :, :3] * 255, dtype=np.uint8)
cv2.imwrite("test_render.png", refine)
