import os
import json


class Config:
    def __init__(self):
        # paths
        self.scene_path = './'
        self.data_path = os.path.dirname(
            os.path.abspath(__file__)) + '/../../Data/'
        self.envmap_path = self.data_path + 'HDR/gl-hdr-02.hdr'
        self.output_path = 'image.png'
        self.cut_json_name = "cuts.json"
        self.singularity_json_name = "singularities.json"
        self.transform_json_name = "transform.json"
        self.trace_json_name = "traceLines.json"
        self.object_name = "mesh.obj"

        # renderer
        self.width = 2000
        self.height = 1500
        self.mode = "single"
        self.plane = "predefined"
        self.use_envmap = False

        # general material
        self.material = 'original'
        self.material_filename = None
        self.color_mode = 'base'
        self.render_style = 'plain'
        self.base_color = 0x9FC0E1
        self.roughness = 0.0
        self.specular = 0.0
        self.sheen = 0.0
        self.clearcoat = 0.0
        self.alpha = 0.4

        # texture
        self.texture_path = self.data_path + 'Texture/checkerboard_10_color1.png'
        self.uv_multiply = (1.0, 1.0)
        self.uv_add = (0.0, 0.0)

        # wireframe size is relative to original size
        self.wireframe_size = 0.2
        self.wireframe_color = 0x000000

        # main mesh
        self.show_main = True

        # singularities
        self.show_singularities = True
        self.pole_scale = 0.005
        self.zero_scale = 0.005
        self.singular_colors = {
            # '-1': 0x00DCFF, '-2': 0x00DCFF, '-3': 0x80DCFF, '1': 0xFFFF00, '2': 0xFFFF00
            '-1': 0x00FF00, '-2': 0x800080, '-3': 0xFFFFFF, '1': 0xFFA500, '2': 0xFF0000
        }

        # loops
        self.show_loops = False
        self.loop_color = 0xFFFF8032

        # cuts
        self.show_cut = True
        self.cut_mode = 'plain'
        self.edge_scale = 0.002
        self.cut_color = 0x808080
        self.segment_colors = [0x800000, 0xD2691E, 0x808000, 0x008080, 0x000080,
                               0xFF0000, 0xFFA500, 0xFFFF00, 0x00FF00, 0x008000,
                               0x00FFFF, 0x0000FF, 0x800080, 0xFF00FF, 0x808080,
                               0xFFC0CB, 0xFFDA89, 0xF5F5DC, 0xF5FFFA, 0xE6E6FA,
                               0x000000, 0xA9A9A9, 0x900C3F, 0x7D5A5A, 0xABC2EB]

        # trace lines
        self.show_trace_lines = True
        self.trace_scale = 0.001
        self.primal_trace_color = 0xFF0000
        self.conjugate_trace_color = 0x00FF00

        # foliation graph
        self.show_foliation_graph = False
        self.foliation_graph_color = 0x00FFFF

        # cylinder
        self.show_cylinders = False
        self.cylinder_mode = 'plain'

        # animation
        self.rotation_start = 0
        self.rotation_end = 360
        self.rotation_step = 1
        self.rotation_axis = "Z"

    def save_config(self, file_path):
        with open(file_path, 'w') as dump_f:
            json.dump(self.__dict__, dump_f)
