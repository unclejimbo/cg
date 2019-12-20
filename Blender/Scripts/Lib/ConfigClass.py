import os
import json

singular_colors = {
    '-1': 0x00DCFF, '-2': 0x0080FF, '-3': 0x8000FF, '1': 0xFF0000, '2': 0xFFFF00
}

segment_colors = [0x800000, 0xD2691E, 0x808000, 0x008080, 0x000080,
                  0xFF0000, 0xFFA500, 0xFFFF00, 0x00FF00, 0x008000,
                  0x00FFFF, 0x0000FF, 0x800080, 0xFF00FF, 0x808080,
                  0xFFC0CB, 0xFFDA89, 0xF5F5DC, 0xF5FFFA, 0xE6E6FA]

# paths
scene_path = './'
data_path = os.path.dirname(os.path.abspath(__file__)) + '/../../Data/'
texture_path = data_path + 'Texture/linesxy_145.png'
envmap_path = data_path + 'HDR/gl-hdr-02.hdr'
output_path = 'image.png'
cut_json_name = "cuts.json"
singularity_json_name = "singularities.json"
transform_json_name = "transform.json"
object_name = "mesh.obj"

# renderer
width = 2000
height = 1500
mode = "single"
plane = "predefined"
use_envmap = False

# main mesh
material = "original"
material_filename = None
model_color = (1.0, 1.0, 1.0, 1.0)
roughness = 0.0
specular = 0.0
sheen = 0.0
clearcoat = 0.0

# singularities
pole_scale = 0.005
zero_scale = 0.005
singularity_material = None
edge_scale = 0.002
edge_material = None
singular_face_material = None
show_singularities = True
show_singularity_color = False

# loops
loop_material = None
show_loops = False

# cuts
cut_mode = 'Segment'

# texcoords
uv_multiply = (1.5, 1.5)
uv_add = (0.05, 0.05)

# wireframe size is relative to original size
wireframe_size = 0.2
wireframe_color = (0, 0, 0, 1.0)

# animation
rotation_start = 0
rotation_end = 360
rotation_step = 1
rotation_axis = "Z"


class Config:
    def __init__(self, singular_colors=singular_colors, segment_colors=segment_colors,
                 texture_path=texture_path, envmap_path=envmap_path, scene_path=scene_path, output_path=output_path,
                 width=width, height=height, mode=mode, sheen=sheen,
                 object_name=object_name, material=material, plane=plane, rotation_start=rotation_start,
                 rotation_end=rotation_end, rotation_step=rotation_step, edge_scale=edge_scale,
                 pole_scale=pole_scale, zero_scale=zero_scale, roughness=roughness, rotation_axis=rotation_axis,
                 cut_mode=cut_mode, show_singularities=show_singularities,
                 show_loops=show_loops, uv_multiply=uv_multiply, uv_add=uv_add, clearcoat=clearcoat,
                 use_envmap=use_envmap, wireframe_size=wireframe_size,
                 material_filename=material_filename, wireframe_color=wireframe_color,
                 singularity_material=singularity_material, edge_material=edge_material, model_color=model_color,
                 loop_material=loop_material, singular_face_material=singular_face_material,
                 cut_json_name=cut_json_name, singularity_json_name=singularity_json_name,
                 transform_json_name=transform_json_name, specular=specular, show_singularity_color=show_singularity_color):
        self.singular_colors = singular_colors
        self.segment_colors = segment_colors
        self.texture_path = texture_path
        self.envmap_path = envmap_path
        self.scene_path = scene_path
        self.output_path = output_path
        self.width = width
        self.height = height
        self.object_name = object_name
        self.mode = mode
        self.sheen = sheen
        self.material = material
        self.plane = plane
        self.rotation_start = rotation_start
        self.rotation_end = rotation_end
        self.rotation_step = rotation_step
        self.edge_scale = edge_scale
        self.zero_scale = zero_scale
        self.pole_scale = pole_scale
        self.roughness = roughness
        self.rotation_axis = rotation_axis
        self.cut_mode = cut_mode
        self.show_singularities = show_singularities
        self.show_loops = show_loops
        self.uv_multiply = uv_multiply
        self.uv_add = uv_add
        self.clearcoat = clearcoat
        self.use_envmap = use_envmap
        self.wireframe_size = wireframe_size
        self.material_filename = material_filename
        self.wireframe_color = wireframe_color
        self.singularity_material = singularity_material
        self.edge_material = edge_material
        self.model_color = model_color
        self.loop_material = loop_material
        self.singular_face_material = singular_face_material
        self.cut_json_name = cut_json_name
        self.singularity_json_name = singularity_json_name
        self.transform_json_name = transform_json_name
        self.specular = specular
        self.show_singularity_color = show_singularity_color

    def save_config(self, file_path):
        config_dict = {}
        config_dict['singular_colors'] = self.singular_colors
        config_dict['segment_colors'] = self.segment_colors
        config_dict['texture_path'] = self.texture_path
        config_dict['envmap_path'] = self.envmap_path
        config_dict['scene_path'] = self.scene_path
        config_dict['output_path'] = self.output_path
        config_dict['width'] = self.width
        config_dict['height'] = self.height
        config_dict['object_name'] = self.object_name
        config_dict['mode'] = self.mode
        config_dict['sheen'] = self.sheen
        config_dict['material'] = self.material
        config_dict['plane'] = self.plane
        config_dict['rotation_start'] = self.rotation_start
        config_dict['rotation_end'] = self.rotation_end
        config_dict['rotation_step'] = self.rotation_step
        config_dict['edge_scale'] = self.edge_scale
        config_dict['pole_scale'] = self.pole_scale
        config_dict['zero_scale'] = self.zero_scale
        config_dict['roughness'] = self.roughness
        config_dict['rotation_axis'] = self.rotation_axis
        config_dict['cut_mode'] = self.cut_mode
        config_dict['show_singularities'] = self.show_singularities
        config_dict['show_loops'] = self.show_loops
        config_dict['uv_multiply'] = self.uv_multiply
        config_dict['uv_add'] = self.uv_add
        config_dict['clearcoat'] = self.clearcoat
        config_dict['use_envmap'] = self.use_envmap
        config_dict['wireframe_size'] = self.wireframe_size
        config_dict['material_filename'] = self.material_filename
        config_dict['wireframe_color'] = self.wireframe_color
        config_dict['singularity_material'] = self.singularity_material
        config_dict['edge_material'] = self.edge_material
        config_dict['model_color'] = self.model_color
        config_dict['loop_material'] = self.loop_material
        config_dict['singular_face_material'] = self.singular_face_material
        config_dict['cut_json_name'] = self.cut_json_name
        config_dict['singularity_json_name'] = self.singularity_json_name
        config_dict['transform_json_name'] = self.transform_json_name
        config_dict['specular'] = self.specular
        config_dict['show_singularity_color'] = self.show_singularity_color

        with open(file_path, 'w') as dump_f:
            json.dump(config_dict, dump_f)
