import bpy
import json
import math
import mathutils
import os

# data_path = os.path.dirname(os.path.abspath(__file__)) + '/../../data/'
# texture_path = data_path + 'texture/checkerboard.png'
# # envmap_path = data_path + 'envmap/gl-hdr-02.hdr'
# envmap_path = data_path + 'HDR/gl-hdr-02.hdr'

# singular_colors = {
#     '-1': 0xFF0000,
#     '-2': 0xFF4500,
#     '-3': 0x8B0000,
#     '1': 0x9932CC
# }
#
# segment_colors = [0x800000, 0xD2691E, 0x808000, 0x008080, 0x000080,
#                   0xFF0000, 0xFFA500, 0xFFFF00, 0x00FF00, 0x008000,
#                   0x00FFFF, 0x0000FF, 0x800080, 0xFF00FF, 0x808080,
#                   0xFFC0CB, 0xFFDA89, 0xF5F5DC, 0xF5FFFA, 0xE6E6FA]


class render_class:
    def __init__(self, singular_colors, segment_colors, data_path, texture_path, envmap_path):
        self.singular_colors = singular_colors
        self.segment_colors = segment_colors
        self.data_path = data_path
        self.texture_path = texture_path
        self.envmap_path = envmap_path

    def blender_vec(self, vec):
        return (vec[0], -vec[2], vec[1])

    def hex2rgba(self, h):
        b = (h & 0xFF) / 255.0
        g = ((h >> 8) & 0xFF) / 255.0
        r = ((h >> 16) & 0xFF) / 255.0
        return r, g, b, 1.0

    def clean(self):
        for item in bpy.data.collections:
            bpy.data.collections.remove(item)
        for item in bpy.data.objects:
            bpy.data.objects.remove(item)
        for item in bpy.data.images:
            bpy.data.images.remove(item)
        for item in bpy.data.meshes:
            bpy.data.meshes.remove(item)
        for item in bpy.data.materials:
            bpy.data.materials.remove(item)
        for item in bpy.data.lights:
            bpy.data.lights.remove(item)

    def setup_renderer(self, output_path, width, height):
        bpy.context.scene.render.engine = 'CYCLES'
        bpy.context.scene.cycles.device = 'GPU'
        bpy.context.scene.render.filepath = output_path
        bpy.context.scene.render.resolution_x = width
        bpy.context.scene.render.resolution_y = height
        bpy.context.scene.render.film_transparent = True
        bpy.context.scene.view_layers[0].cycles.use_denoising = True

        bpy.context.scene.use_nodes = True
        tree = bpy.context.scene.node_tree
        render_node = tree.nodes.new(type='CompositorNodeRLayers')
        alpha_node = tree.nodes.new(type='CompositorNodeAlphaOver')
        vieweroutput_node = tree.nodes.new(type='CompositorNodeViewer')
        originoutput_node = tree.nodes.new(type='CompositorNodeComposite')
        tree.links.new(render_node.outputs['Image'], alpha_node.inputs[2])
        tree.links.new(render_node.outputs['Alpha'], alpha_node.inputs[0])
        tree.links.new(alpha_node.outputs[0], vieweroutput_node.inputs[0])
        tree.links.new(render_node.outputs['Image'], originoutput_node.inputs[0])

    def build_main_mesh(self, path):
        mat = bpy.data.materials.new('Main')
        mat.use_nodes = True
        img_node = mat.node_tree.nodes.new(type='ShaderNodeTexImage')
        img_node.image = bpy.data.images.load(filepath=self.texture_path)
        # bsdf_node = mat.node_tree.nodes['Principled BSDF']
        for node in mat.node_tree.nodes:
            if node.type == 'BSDF_PRINCIPLED':
                bsdf_node = node
        bsdf_node.inputs['Roughness'].default_value = 0.0
        bsdf_node.inputs['Specular'].default_value = 0.0
        mat.node_tree.links.new(
            img_node.outputs['Color'], bsdf_node.inputs['Base Color'])

        bpy.ops.import_scene.obj(filepath=path, use_split_objects=False)
        mesh_obj = bpy.data.objects['mesh']
        mesh_obj.name = 'Mesh'
        mesh_obj.active_material = mat

    def build_singularity_primitives(self):
        scene_collection = bpy.context.scene.collection
        for index, color in self.singular_colors.items():
            mat = bpy.data.materials.new('Singularity' + index)
            mat.use_nodes = True
            # bsdf_node = mat.node_tree.nodes['Principled BSDF']
            for node in mat.node_tree.nodes:
                if node.type == 'BSDF_PRINCIPLED':
                    bsdf_node = node
            mat.node_tree.nodes.remove(bsdf_node)
            color_node = mat.node_tree.nodes.new(type='ShaderNodeRGB')
            color_node.outputs[0].default_value = self.hex2rgba(color)
            # output_node = mat.node_tree.nodes['Material Output']
            for node in mat.node_tree.nodes:
                if node.type == 'OUTPUT_MATERIAL':
                    output_node = node
            mat.node_tree.links.new(
                color_node.outputs['Color'], output_node.inputs['Surface'])

            bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=4)
            sphere = bpy.data.objects['Icosphere']
            sphere.name = 'Singularity' + index
            sphere.active_material = mat
            collection = bpy.data.collections.new('Singularity' + index)
            collection.objects.link(sphere)
            scene_collection.objects.unlink(sphere)

    def build_segment_primitives(self):
        scene_collection = bpy.context.scene.collection
        for i, color in enumerate(self.segment_colors):
            mat = bpy.data.materials.new('Segment' + str(i))
            mat.use_nodes = True
            bsdf_node = mat.node_tree.nodes['Principled BSDF']
            mat.node_tree.nodes.remove(bsdf_node)
            color_node = mat.node_tree.nodes.new(type='ShaderNodeRGB')
            color_node.outputs[0].default_value = self.hex2rgba(color)
            output_node = mat.node_tree.nodes['Material Output']
            mat.node_tree.links.new(
                color_node.outputs['Color'], output_node.inputs['Surface'])

            bpy.ops.mesh.primitive_cylinder_add()
            cylinder = bpy.data.objects['Cylinder']
            cylinder.name = 'Cut Edge Segment ' + str(i)
            cylinder.active_material = mat
            edge_collection = bpy.data.collections.new(
                'Cut Edge Segment ' + str(i))
            edge_collection.objects.link(cylinder)
            scene_collection.objects.unlink(cylinder)

            bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=4)
            sphere = bpy.data.objects['Icosphere']
            sphere.name = 'Cut Vertex Segment ' + str(i)
            sphere.active_material = mat
            vertex_collection = bpy.data.collections.new(
                'Cut Vertex Segment ' + str(i))
            vertex_collection.objects.link(sphere)
            scene_collection.objects.unlink(sphere)

    def build_addons(self, scene_json):
        scene_collection = bpy.context.scene.collection

        singularities_collection = bpy.data.collections.new('Singularities')
        scene_collection.children.link(singularities_collection)
        for i, s in enumerate(scene_json['singularities']):
            primitive_name = 'Singularity' + str(s['index'])
            bpy.ops.object.collection_instance_add(
                collection=primitive_name, location=self.blender_vec(s['position']))
            obj = bpy.data.objects[primitive_name + '.001']
            obj.name = 'Singularity Instance ' + str(i)
            obj.scale = (0.01, 0.01, 0.01)
            scene_collection.objects.unlink(obj)
            singularities_collection.objects.link(obj)

        cuts_collection = bpy.data.collections.new('Cuts')
        scene_collection.children.link(cuts_collection)
        for i, c in enumerate(scene_json['cuts']):
            p0 = mathutils.Vector(self.blender_vec(c['points'][0]))
            p1 = mathutils.Vector(self.blender_vec(c['points'][1]))

            edge_primitive_name = 'Cut Edge Segment ' + str(c['segment'])
            bpy.ops.object.collection_instance_add(collection=edge_primitive_name)
            edge_obj = bpy.data.objects[edge_primitive_name + '.001']
            edge_obj.name = 'Cut Edge Instance ' + str(i)
            edge_obj.location = (p0 + p1) / 2
            edge_obj.scale = (0.002, 0.002, (p0 - p1).magnitude / 2)
            edge_obj.rotation_mode = 'QUATERNION'
            edge_obj.rotation_quaternion = mathutils.Vector(
                (0, 0, 1)).rotation_difference(p0 - p1)
            scene_collection.objects.unlink(edge_obj)
            cuts_collection.objects.link(edge_obj)

            vertex_primitive_name = 'Cut Vertex Segment ' + str(c['segment'])
            bpy.ops.object.collection_instance_add(
                collection=vertex_primitive_name)
            vertex_obj = bpy.data.objects[vertex_primitive_name + '.001']
            vertex_obj.name = 'Cut Vertex Instance ' + str(i * 2)
            vertex_obj.location = p0
            vertex_obj.scale = (0.002, 0.002, 0.002)
            scene_collection.objects.unlink(vertex_obj)
            cuts_collection.objects.link(vertex_obj)
            bpy.ops.object.collection_instance_add(
                collection=vertex_primitive_name)
            vertex_obj = bpy.data.objects[vertex_primitive_name + '.001']
            vertex_obj.name = 'Cut Vertex Instance ' + str(i * 2 + 1)
            vertex_obj.location = p1
            vertex_obj.scale = (0.002, 0.002, 0.002)
            scene_collection.objects.unlink(vertex_obj)
            cuts_collection.objects.link(vertex_obj)

    def build_ground(self):
        bpy.ops.mesh.primitive_plane_add(size=50)
        zmin = bpy.data.objects['Mesh'].bound_box[0][1]
        plane_obj = bpy.data.objects['Plane']
        plane_obj.location = (0, 0, zmin)
        plane_obj.cycles.is_shadow_catcher = True

    def build_camera(self, scene_json):
        cam_json = scene_json['camera']
        cam = bpy.data.cameras['Camera']
        cam.lens_unit = 'FOV'
        cam.lens = 20
        cam_obj = bpy.data.objects.new('Camera', cam)
        cam_obj.location = self.blender_vec(cam_json['position'])
        cam_track = cam_obj.constraints.new(type='TRACK_TO')
        cam_track.target = bpy.data.objects['Mesh']
        cam_track.track_axis = 'TRACK_NEGATIVE_Z'
        cam_track.up_axis = 'UP_Y'
        bpy.context.scene.collection.objects.link(bpy.data.objects['Camera'])
        bpy.context.scene.camera = cam_obj

    def build_direct_light(self):
        sun = bpy.data.lights.new("Sun", type='SUN')
        sun.energy = 2.0
        sun_obj = bpy.data.objects.new('Sun', sun)
        sun_obj.location = (0.5, 0.5, 10.0)
        bpy.context.scene.collection.objects.link(bpy.data.objects['Sun'])

    def build_indirect_light(self):
        world = bpy.context.scene.world
        world.use_nodes = True
        texcoord_node = world.node_tree.nodes.new(type='ShaderNodeTexCoord')
        envmap_node = world.node_tree.nodes.new(type='ShaderNodeTexEnvironment')
        envmap_node.image = bpy.data.images.load(self.envmap_path)
        world.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.2
        world.node_tree.links.new(
            texcoord_node.outputs['Generated'], envmap_node.inputs['Vector'])
        world.node_tree.links.new(
            envmap_node.outputs['Color'], world.node_tree.nodes['Background'].inputs['Color'])

    def do_render(self):
        bpy.ops.render.render(write_still=True)

    def render(self, scene_path, output_path, width, height):
        scene_file = open(scene_path + 'scene.json')
        scene_json = json.load(scene_file)
        self.clean()
        self.setup_renderer(output_path, width, height)
        self.build_main_mesh(scene_path + 'mesh.obj')
        self.build_singularity_primitives()
        self.build_segment_primitives()
        self.build_addons(scene_json)
        self.build_ground()
        self.build_camera(scene_json)
        self.build_direct_light()
        self.build_indirect_light()
        self.do_render()
