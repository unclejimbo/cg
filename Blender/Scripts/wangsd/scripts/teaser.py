import os
import sys
sys.path.append('../..')
from Lib.ConfigClass import Config, singular_colors
import json

scene_path = '/home/wangsd/Workspace/foliation-results/outputs/scenes/paper/teaser/'
output_path = '/pub/data/wangsd/images/teaser'
envmap_path = '/home/wangsd/Workspace/cg/data/envmap/gl-hdr-02.hdr'
checkerboard1 = '/home/wangsd/Workspace/cg/data/texture/checkerboard_10_color3.png'
checkerboard2 = '/home/wangsd/Workspace/cg/data/texture/checkerboard_10_color4.png'
checkerboard3 = '/home/wangsd/Workspace/cg/data/texture/checkerboard_10_color5.png'
material1 = 'Knittr.blend'

for root, dirs, _ in os.walk(scene_path):
    for d in dirs:
        if os.path.exists(os.path.join(root, d, 'mesh.obj')):
            print('Processing', os.path.join(root, d))
            config_dir = os.path.join(root, d, 'configs')
            if not os.path.exists(config_dir):
                os.mkdir(config_dir)
        
            config = Config()
            config.scene_path = os.path.join(root, d + '/')
            config.envmap_path = envmap_path
            config.transform_json_name = 'transform.json'
            config.mode = 'single'
            config.use_envmap = True
            config.width = 2000
            config.height = 2000
            config.plane = None
            config.material = None
            config.show_loops = False
            config.zero_scale = 0.02
            config.pole_scale = 0.02
            config.show_singularities = True
            config.cut_mode = 'Plain'
            config.uv_add = (0.05, 0.05)
                
            if True:
                config.material_filename = material1
                config.texture_path = checkerboard1

                config.uv_multiply = (2.0, 0.0)
                config.output_path = os.path.join(output_path, d + '.png')
                config.save_config(os.path.join(config_dir, 'config.1.json'))

                config.uv_multiply = (2.0, 2.0)
                config.output_path = os.path.join(output_path, d + '_uv.png')
                config.save_config(os.path.join(config_dir, 'config.2.json'))
