import os
import sys
sys.path.append('..')
from Lib.ConfigClass import Config, singular_colors
import json

scene_path = '/home/wangsd/Workspace/foliation-results/outputs/scenes/paper/detail_compare/'
output_path = '/pub/data/wangsd/images/detail_compare'
texture_path = '/home/wangsd/Workspace/cg/data/texture/gridlines_critical_20.png'
envmap_path = '/home/wangsd/Workspace/cg/data/envmap/gl-hdr-02.hdr'

for root, dirs, _ in os.walk(scene_path):
    for d in dirs:
        if os.path.exists(os.path.join(root, d, 'mesh.obj')):
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
            config.cut_mode = 'None'
            config.material = "original"
            config.material_filename = None
            config.texture_path = texture_path
            config.uv_multiply = (1.0, 0.0)
            config.show_loops = True
            
            if d == 'input':
                config.show_singularities = False
                config.uv_add = (0.03, 0.03)
            elif (d == 'unconstrained5') or \
                (d == 'unconstrained6') or \
                (d == 'unconstrained7'):
                config.show_singularities = True
                config.pole_scale = 0.02
                config.zero_scale = 0.01
                config.uv_add = (0.0, 0.03)
            else:
                config.show_singularities = True
                config.pole_scale = 0.005
                config.zero_scale = 0.005
                config.uv_add = (0.0, 0.03)

            config.save_config(os.path.join(root, d, 'config.json'))
