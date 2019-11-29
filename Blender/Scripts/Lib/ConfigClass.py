import os
import json


singular_colors = {
    '-1':0xFF0000,'-2':0xFF4500,'-3':0x8B0000,'1':0x9932CC, '2':0xFFA500
}

segment_colors = [0x800000, 0xD2691E, 0x808000, 0x008080, 0x000080,
                  0xFF0000, 0xFFA500, 0xFFFF00, 0x00FF00, 0x008000,
                  0x00FFFF, 0x0000FF, 0x800080, 0xFF00FF, 0x808080,
                  0xFFC0CB, 0xFFDA89, 0xF5F5DC, 0xF5FFFA, 0xE6E6FA]


data_path = os.path.dirname(os.path.abspath(__file__)) + '/../../Data/'
texture_path = data_path + 'Texture/checkerboard.png'
envmap_path = data_path + 'HDR/gl-hdr-02.hdr'

# envmap_path = data_path + 'HDR/green_point_park_2k.hdr'

blender_path =  "D:/tools/blender_2.81/blender.exe"
SCENE_PATH = "../../Scene/eight/"
scene_name = "scene.json"
object_name = "mesh.obj"

plane = "original"
rotation_start = 0
rotation_end = 360
rotation_step = 1
rotation_axis = "Z"

path = os.getcwd()
path = os.path.dirname(path)
path = os.path.dirname(path)
# OUTPUT_PATH = path + "\Output\\" +  scene_name.split(".")[0]+ ".png"
OUTPUT_PATH = path + "\Output\\" +  object_name.split(".")[0]+ ".png"

WIDTH = 2000
HEIGHT = 1500

CONFIG_PATH = "./config.json"

mode = "single"

material = "original"

edge_scale = 0.002
singularity_scale = 0.010
roughness = 0.0

show_cut = True
show_singularity = True
show_singular_face = False
show_loops = False

uv_multiply = (3.0, 3.0)
uv_add = (0.05, 0.05)


class Config:
    def __init__(self, singular_colors=singular_colors, segment_colors = segment_colors, data_path = data_path,
        texture_path = texture_path, envmap_path = envmap_path, scene_path = SCENE_PATH, output_path = OUTPUT_PATH,
                 width = WIDTH, height = HEIGHT, config_path = CONFIG_PATH, scene_name = scene_name, mode = mode,
                 object_name = object_name, material = material, plane = plane, rotation_start = rotation_start,
                 rotation_end = rotation_end, rotation_step = rotation_step, edge_scale = edge_scale,
                 singularity_scale = singularity_scale, roughness = roughness, rotation_axis = rotation_axis,
                 show_cut = show_cut, show_singularity = show_singularity, show_singular_face = show_singular_face,
                 show_loops = show_loops, blender_path = blender_path, uv_multiply = uv_multiply, uv_add = uv_add):
        self.singular_colors = singular_colors
        self.segment_colors = segment_colors
        self.data_path = data_path
        self.texture_path = texture_path
        self.envmap_path = envmap_path
        self.scene_path = scene_path
        self.output_path = output_path
        self.width = width
        self.height = height
        self.config_path = config_path
        self.scene_name = scene_name
        self.object_name = object_name
        self.mode = mode
        self.material = material
        self.plane = plane
        self.rotation_start = rotation_start
        self.rotation_end = rotation_end
        self.rotation_step = rotation_step
        self.edge_scale = edge_scale
        self.singularity_scale = singularity_scale
        self.roughness = roughness
        self.rotation_axis = rotation_axis
        self.show_cut = show_cut
        self.show_singularity = show_singularity
        self.show_singular_face = show_singular_face
        self.show_loops = show_loops
        self.blender_path = blender_path
        self.uv_multiply = uv_multiply
        self.uv_add = uv_add

    def save_config(self):
        config_dict = {}
        config_dict['singular_colors'] = self.singular_colors
        config_dict['segment_colors'] = self.segment_colors
        config_dict['data_path'] = self.data_path
        config_dict['texture_path'] = self.texture_path
        config_dict['envmap_path'] = self.envmap_path
        config_dict['scene_path'] = self.scene_path
        config_dict['output_path'] = self.output_path
        config_dict['width'] = self.width
        config_dict['height'] = self.height
        config_dict['config_path'] = self.config_path
        config_dict['scene_name'] = self.scene_name
        config_dict['object_name'] = self.object_name
        config_dict['mode'] = self.mode
        config_dict['material'] = self.material
        config_dict['plane'] = self.plane
        config_dict['rotation_start'] = self.rotation_start
        config_dict['rotation_end'] = self.rotation_end
        config_dict['rotation_step'] = self.rotation_step
        config_dict['edge_scale'] = self.edge_scale
        config_dict['singularity_scale'] = self.singularity_scale
        config_dict['roughness'] = self.roughness
        config_dict['rotation_axis'] = self.rotation_axis
        config_dict['show_cut'] = self.show_cut
        config_dict['show_singularity'] = self.show_singularity
        config_dict['show_singular_face'] = self.show_singular_face
        config_dict['show_loops'] = self.show_loops
        config_dict['blender_path'] = self.blender_path
        config_dict['uv_multiply'] = self.uv_multiply
        config_dict['uv_add'] = self.uv_add

        with open(self.config_path,'w') as dump_f:
            json.dump(config_dict, dump_f)
