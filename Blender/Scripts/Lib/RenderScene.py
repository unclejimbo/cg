import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from ConfigClass import *


class RenderScene:
    def __init__(self):
        # self.config = None
        self.blender_path = "D:/tools/blender_2.81/blender.exe"
        self.background_render = True
        self.config_path = "./config.json"

    def render(self):
        cmd = self.blender_path + " --python ../../Lib/BlenderBridge.py"
        cmd += " -noaudio"
        if self.background_render:
            cmd += " --background"
        cmd += " -- -c " + str(self.config_path)
        print("start rendering...")
        os.system(cmd)
        print("done!")
