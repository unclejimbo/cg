import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from ConfigClass import *


class RenderScene:
    def __init__(self):
        self.config = None

    def render(self):
        cmd = self.config.blender_path + " --python ../Lib/BlenderBridge.py"
        cmd += " -noaudio"
        if self.config.background_render:
            cmd += " --background"
        cmd += " -- -c " + str(self.config.config_path)
        print("start rendering...")
        os.system(cmd)
        print("done!")
