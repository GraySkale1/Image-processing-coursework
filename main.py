import BuiltWindows as bw
import IProcess as IP
from PIL import Image

WIDTH, HEIGHT = 1920, 1080

load = bw.FormPage(100, 100, "Generic")
load.run()

im = IP.ImManipulate(load.path)

