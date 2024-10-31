import numpy as np
from PIL import Image

class ImManipulate():
    def __init__(path):
        image = Image.open(path)
        self.ImageRaw = np.asarray(image)