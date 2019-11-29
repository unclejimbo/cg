import argparse
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from RenderUtils import *


def render(scene_path, output_path, width, height):
    scene_file = open(scene_path + 'scene.json')
    scene_json = json.load(scene_file)
    clean()
    setup_renderer(output_path, width, height)
    build_main_mesh(scene_path + 'mesh.obj')
    build_singularity_primitives()
    build_segment_primitives()
    build_addons(scene_json)
    build_ground()
    build_camera(scene_json)
    build_direct_light()
    build_indirect_light()
    do_render()


if __name__ == '__main__':
    argv = sys.argv
    argv = argv[argv.index('--') + 1:]

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--scene_path', required=True)
    parser.add_argument('-o', '--output_path', default='/tmp/image.png')
    parser.add_argument('--width', type=int, default=2000)
    parser.add_argument('--height', type=int, default=1500)
    args = parser.parse_args(argv)

    render(args.scene_path, args.output_path, args.width, args.height)
