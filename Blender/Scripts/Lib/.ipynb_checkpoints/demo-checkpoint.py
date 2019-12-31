import argparse
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from render_class import *



singular_colors = {
    '-1': 0xFF0000,
    '-2': 0xFF4500,
    '-3': 0x8B0000,
    '1': 0x9932CC
}

segment_colors = [0x800000, 0xD2691E, 0x808000, 0x008080, 0x000080,
                  0xFF0000, 0xFFA500, 0xFFFF00, 0x00FF00, 0x008000,
                  0x00FFFF, 0x0000FF, 0x800080, 0xFF00FF, 0x808080,
                  0xFFC0CB, 0xFFDA89, 0xF5F5DC, 0xF5FFFA, 0xE6E6FA]

data_path = os.path.dirname(os.path.abspath(__file__)) + '/../../data/'
texture_path = data_path + 'texture/checkerboard.png'
# envmap_path = data_path + 'envmap/gl-hdr-02.hdr'
envmap_path = data_path + 'HDR/gl-hdr-02.hdr'

render_class = render_class(singular_colors, segment_colors, data_path, texture_path, envmap_path)


scene_path = "../../Scene/eight/"
path = os.getcwd()
path = os.path.dirname(path)
path = os.path.dirname(path)
output_path = path + "\Output\image.png"

width = 2000
height = 1500

render_class.render(scene_path, output_path, width, height)
