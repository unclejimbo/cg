import os
import sys
sys.path.append('../..')
from Lib.ConfigClass import Config, singular_colors
import json

scene_path = '/home/wangsd/Workspace/foliation-results/outputs/scenes/paper/homotopy/'
output_path = '/pub/data/wangsd/images/homotopy'
texture_path = '/home/wangsd/Workspace/cg/data/texture/gridlines_critical_20.png'
envmap_path = '/home/wangsd/Workspace/cg/data/envmap/gl-hdr-02.hdr'
material_filename = '36-holographic-effect-transparent.blend'

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
            config.singular_colors = singular_colors
            config.uv_multiply = (1.0, 0.0)
            config.uv_add = (0.0, 0.03)
            config.texture_path = texture_path
            config.show_singularities = True
            config.show_loops = True
            if d[:4] == 'half':
                config.zero_scale = 0.005
                config.pole_scale = 0.005
                config.material = None
                config.material_filename = material_filename
            else:
                config.zero_scale = 0.01
                config.pole_scale = 0.01
                config.material = 'original'
                config.material_filename = None
            config.save_config(os.path.join(root, d, 'config.json'))
