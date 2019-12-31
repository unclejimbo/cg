import os
import sys
sys.path.append('../..')
from Lib.ConfigClass import Config, singular_colors
import json

scene_path = '/home/wangsd/Workspace/foliation-results/outputs/scenes/paper/palmer_foliation/'
output_path = '/pub/data/wangsd/images/palmer_foliation'
texture_path = '/home/wangsd/Workspace/cg/data/texture/checkerboard.png'
envmap_path = '/home/wangsd/Workspace/cg/data/envmap/gl-hdr-02.hdr'
material_filename = '99-porcelain-texture.blend'

for root, dirs, _ in os.walk(scene_path):
    for d in dirs:
        if os.path.exists(os.path.join(root, d, 'mesh.obj')):
            print('Processing', os.path.join(root, d))
            config = Config()
            config_file = os.path.join(root, d, 'config.json')
            if os.path.exists(config_file):
                with open(os.path.join(root, d, 'config.json')) as jf:
                    config.__dict__ = json.load(jf)
            
            config.scene_path = os.path.join(root, d + '/')
            config.output_path = os.path.join(output_path, d + '.png')
            config.envmap_path = envmap_path
            config.transform_json_name = 'transform.json'
            config.mode = 'single'
            config.use_envmap = True
            config.width = 2000
            config.height = 2000
            config.plane = None
            config.cut_mode = 'Plain'
            config.material = None
            config.material_filename = material_filename
            config.texture_path = texture_path
            config.uv_multiply = (2.0, 0.0)
            config.uv_add = (0.05, 0.05)
            config.show_loops = False
            config.show_singularities = True
            config.zero_scale = 0.01
            config.pole_scale = 0.02

            config.save_config(os.path.join(root, d, 'config.json'))
