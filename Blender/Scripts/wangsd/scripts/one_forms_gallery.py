import os
import sys
sys.path.append('../..')
from Lib.ConfigClass import Config, singular_colors
import json

scene_path = '/home/wangsd/Workspace/foliation-results/outputs/scenes/paper/one_forms_gallery/'
output_path = '/pub/data/wangsd/images/one_forms_gallery'
gridlines1 = '/home/wangsd/Workspace/cg/data/texture/gridlines_10_color1.png'
gridlines2 = '/home/wangsd/Workspace/cg/data/texture/gridlines_10_color2.png'
checkerboard1 = '/home/wangsd/Workspace/cg/data/texture/checkerboard_10_color1.png'
checkerboard2 = '/home/wangsd/Workspace/cg/data/texture/checkerboard_10_color2.png'
envmap_path = '/home/wangsd/Workspace/cg/data/envmap/gl-hdr-02.hdr'
material_filename = '99-porcelain-texture.blend'

for root, dirs, _ in os.walk(scene_path):
    for d in dirs:
        if os.path.exists(os.path.join(root, d, 'mesh.obj')):
            config_dir = os.path.join(root, d, 'configs')
            if not os.path.exists(config_dir):
                os.mkdir(config_dir)

            config = Config()
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
            config.material = 'original'
            config.material_filename = None
            config.uv_multiply = (1.0, 1.0)
            config.show_singularities = True
            config.zero_scale = 0.02
            config.pole_scale = 0.05
            config.show_loops = False

            if d[-8:] == 'oneforms':
                config.uv_add = (0.05, 0.05)
                config.texture_path = checkerboard2
                config.output_path = os.path.join(output_path, d + '_checker.png')
                config.save_config(os.path.join(root, d, 'configs', 'config.1.json'))

                config.uv_add = (0.0, 0.0)
                config.texture_path = gridlines2
                config.output_path = os.path.join(output_path, d + '_lines.png')
                config.save_config(os.path.join(root, d, 'configs', 'config.2.json'))
            else:
                config.uv_add = (0.05, 0.05)
                config.texture_path = checkerboard1
                config.output_path = os.path.join(output_path, d + '_checker.png')
                config.save_config(os.path.join(root, d, 'configs', 'config.1.json'))

                config.uv_add = (0.0, 0.0)
                config.texture_path = gridlines1
                config.output_path = os.path.join(output_path, d + '_lines.png')
                config.save_config(os.path.join(root, d, 'configs', 'config.2.json'))

