import os
import sys
sys.path.append("..")
from Lib.RenderScene import RenderScene
from Lib.ConfigClass import Config


config = Config()
config.width = 400
config.height = 300

config.mode = "rotation"


config.save_config()

RenderScene = RenderScene()
RenderScene.config = config

RenderScene.render()