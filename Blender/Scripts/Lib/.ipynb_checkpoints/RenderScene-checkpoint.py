import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from ConfigClass import *


class RenderScene:
    # def __init__(self, scene_path=SCENE_PATH, output_path=OUTPUT_PATH, width=WIDTH, height=HEIGHT):
    #     self.scene_path = scene_path
    #     self.output_path = output_path
    #     self.width = width
    #     self.height = height
    def __init__(self):
        self.config = None

    def render(self):
        blenderPath = "D:/tools/blender/blender.exe"
        cmd = blenderPath + " --background --python ../Lib/BlenderBridge.py -- -c "
        cmd = cmd + str(self.config.config_path)
        # cmd = "D:/tools/blender/blender.exe --background --python ../Lib/BlenderBridge.py"
        # cmd = cmd + " -- -s " + self.scene_path
        # cmd = cmd + " -o " + self.output_path
        # cmd = cmd + " --width " + str(self.width)
        # cmd = cmd + " --height " + str(self.height)
        print(cmd)
        os.system(cmd)
