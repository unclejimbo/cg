import argparse
import os
import sys
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from RenderClass import *
from ConfigClass import *


if __name__ == '__main__':
    argv = sys.argv
    argv = argv[argv.index('--') + 1:]

    parser = argparse.ArgumentParser(description='Render')
    # parser.add_argument('-s', '--scene_path', required=True)
    # parser.add_argument('-o', '--output_path', required=True)
    # parser.add_argument('--width', type=int, required=True)
    # parser.add_argument('--height', type=int, required=True)
    parser.add_argument('-c', '--config_path', required=True )
    args = parser.parse_args(argv)

    with open(args.config_path,'r') as load_f:
        load_dict = json.load(load_f)

    # RenderClass = RenderCore(args.singular_colors, args.segment_colors, args.data_path, args.texture_path, args.envmap_path)
    # RenderClass.render(args.scene_path, args.output_path, args.width, args.height)
    RenderClass = RenderCore(load_dict['singular_colors'], load_dict['segment_colors'],
                             load_dict['data_path'], load_dict['texture_path'], load_dict['envmap_path'])
    RenderClass.render(load_dict['scene_path'], load_dict['output_path'],
                       load_dict['width'], load_dict['height'])

