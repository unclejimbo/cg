import os
import json
import bpy


if __name__ == "__main__":
    parent_obj = bpy.data.objects["Parent Object"]
    path = os.getcwd()
    path = os.path.dirname(path)
    path = os.path.dirname(path)

    transform_path = path + "/Scene/transform.json"

    if not os.path.exists(transform_path):
        os.system(r"touch {}".format(transform_path))
    print(transform_path)

    transform_dict = {}
    transform_dict['Location'] = (parent_obj.location[0], parent_obj.location[1], parent_obj.location[2])
    transform_dict['Rotation'] = (parent_obj.rotation_euler.x, parent_obj.rotation_euler.y, parent_obj.rotation_euler.z)
    transform_dict['Scale'] = (parent_obj.scale[0], parent_obj.scale[1], parent_obj.scale[2])

    with open(transform_path, 'w') as dump_f:
        json.dump(transform_dict, dump_f)