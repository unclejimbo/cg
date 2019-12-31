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
    parser.add_argument('-c', '--config_path', required=True )
    args = parser.parse_args(argv)

    with open(args.config_path,'r') as load_f:
        load_dict = json.load(load_f)

    config = Config()
    # update
    config.__dict__ = load_dict
    RenderClass = RenderCore(config)
    RenderClass.render()

