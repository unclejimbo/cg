import os
import sys
sys.path.append('../..')
from Lib.RenderScene import RenderScene
import json

scene_path = '/home/wangsd/Workspace/foliation-results/outputs/scenes/paper/teaser/'

renderer = RenderScene()
renderer.blender_path = '/home/wangsd/Devtools/blender-2.81-linux-glibc217-x86_64/blender'
renderer.background_render = True

for root, dirs, _ in os.walk(scene_path):
    for d in dirs:
        if os.path.exists(os.path.join(root, d, 'mesh.obj')):
            # a single config
            config_file = os.path.join(root, d, 'config.json')
            if os.path.exists(config_file):
                renderer.config_path = config_file
                renderer.render()

            # multiple configs
            config_dir = os.path.join(root, d, 'configs')
            if os.path.exists(config_dir):
                config_files = os.listdir(config_dir)
                for config_file in config_files:
                    if config_file[:6] == 'config':
                        renderer.config_path = os.path.join(config_dir, config_file)
                        renderer.render()
