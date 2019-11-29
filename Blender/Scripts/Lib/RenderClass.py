import bpy
import json
import math
import mathutils
import os
from math import radians
import bmesh
from mathutils import Matrix, Euler
import numpy as np
from MaterialFactory import MaterialFactory


class RenderCore:
    def __init__(self, config):
        self.config = config
        self.MaterialFactory = MaterialFactory()
        self.MaterialFactory.texture_path = self.config.texture_path
        self.MaterialFactory.roughness = self.config.roughness
        self.rotation = 0

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

    def choose_material(self):
        material_list = ['original', 'gold', 'glass', 'ceramic', 'roughblue', 'wireframe', 'peeling_paint', 'paint']
        if self.config.material in material_list:
            material_function = {
                'original': self.MaterialFactory.CreateMain(),
                'gold': self.MaterialFactory.CreateGold(),
                'glass': self.MaterialFactory.CreateGlass(),
                'ceramic': self.MaterialFactory.CreateCeramic(),
                'roughblue': self.MaterialFactory.CreateRoughBlue(),
                'wireframe' : self.MaterialFactory.CreateWireframe(),
                'peeling_paint' : self.MaterialFactory.CreatePeelingPaint(),
                'paint' : self.MaterialFactory.CreatePaint()
            }
            mat = material_function[self.config.material]
        else:
            mat = self.MaterialFactory.CreateFromName(self.config.material)
        return mat

    def build_main_mesh(self, path):
        # set material
        mat = self.choose_material()
        if self.config.material == "original":
            img_node = mat.node_tree.nodes['Image Texture']
            texcoord_node = mat.node_tree.nodes.new(type='ShaderNodeTexCoord')
            mutiply_node = mat.node_tree.nodes.new(type='ShaderNodeVectorMath')
            mutiply_node.operation = 'MULTIPLY'
            mutiply_node.inputs[1].default_value[0] = self.config.uv_multiply[0]
            mutiply_node.inputs[1].default_value[1] = self.config.uv_multiply[1]
            add_node = mat.node_tree.nodes.new(type='ShaderNodeVectorMath')
            add_node.operation = 'ADD'
            add_node.inputs[1].default_value[0] = self.config.uv_add[0]
            add_node.inputs[1].default_value[1] = self.config.uv_add[1]
            # link nodes
            mat.node_tree.links.new(texcoord_node.outputs['UV'], mutiply_node.inputs[0])
            mat.node_tree.links.new(mutiply_node.outputs['Vector'], add_node.inputs[0])
            mat.node_tree.links.new(add_node.outputs['Vector'], img_node.inputs['Vector'])

            # # set uv scale
            # scale_node = mat.node_tree.nodes.new(type='ShaderNodeVectorMath')
            # scale_node.operation = 'SCALE'
            # # set uv scale
            # scale_node.inputs['Scale'].default_value = self.config.uv_scale
            # texcoord_node = mat.node_tree.nodes.new(type='ShaderNodeTexCoord')
            # img_node = mat.node_tree.nodes['Image Texture']
            # # link
            # mat.node_tree.links.new(texcoord_node.outputs['UV'], scale_node.inputs['Vector'])
            # mat.node_tree.links.new(scale_node.outputs['Vector'], img_node.inputs['Vector'])

        bpy.ops.import_scene.obj(filepath=path, use_split_objects=False)
        mesh_obj = bpy.data.objects[self.config.object_name.split(".")[0]]
        mesh_obj.name = 'Mesh'
        mesh_obj.active_material = mat
        # rotate
        # mesh_obj.rotation_euler.rotate_axis("Y", self.rotation)
        if self.config.show_singular_face == True:
            # build singular faces
            # set material
            self.MaterialFactory.wireframecolor = (0.026, 0.831, 0.888, 1)
            mat = self.MaterialFactory.CreateColoredWireframe()
            bpy.ops.import_scene.obj(filepath=self.config.scene_path + "singularFaces.obj", use_split_objects=False)
            face_obj = bpy.data.objects["singularFaces"]
            face_obj.name = 'Singular Faces'
            face_obj.active_material = mat
        if self.config.show_loops == True:
            # build loop mesh
            self.MaterialFactory.wireframecolor = (0.888, 0.888, 0, 1)
            mat = self.MaterialFactory.CreateColoredWireframe()
            bpy.ops.import_scene.obj(filepath=self.config.scene_path + "loops.obj", use_split_objects=False)
            loop_obj = bpy.data.objects["loops"]
            loop_obj.name = 'Loops'
            loop_obj.active_material = mat

    def build_singularity_primitives(self):
        scene_collection = bpy.context.scene.collection
        for index, color in self.config.singular_colors.items():
            self.MaterialFactory.color = color
            mat = self.MaterialFactory.CreateColored('Singularity' + index)

            bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=4)
            sphere = bpy.data.objects['Icosphere']
            sphere.name = 'Singularity' + index
            sphere.active_material = mat
            collection = bpy.data.collections.new('Singularity' + index)
            collection.objects.link(sphere)
            scene_collection.objects.unlink(sphere)

    def build_segment_primitives(self):
        scene_collection = bpy.context.scene.collection
        for i, color in enumerate(self.config.segment_colors):

            self.MaterialFactory.color = color
            mat = self.MaterialFactory.CreateColored('Segment' + str(i))

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
            instance = bpy.data.objects.new('Singularity Instance ' + str(i), None)
            instance.location = self.blender_vec(s['position'])
            instance.scale = (self.config.singularity_scale, self.config.singularity_scale, self.config.singularity_scale)
            instance.instance_type = 'COLLECTION'
            instance.instance_collection = bpy.data.collections['Singularity' + str(s['index'])]
            if self.config.show_singularity == True:
                singularities_collection.objects.link(instance)

        cuts_collection = bpy.data.collections.new('Cuts')
        scene_collection.children.link(cuts_collection)
        for i, c in enumerate(scene_json['cuts']):
            seg = c['segment'] % 20
            p0 = mathutils.Vector(self.blender_vec(c['points'][0]))
            p1 = mathutils.Vector(self.blender_vec(c['points'][1]))

            edge_instance = bpy.data.objects.new('Cut Edge Instance ' + str(i), None)
            edge_instance.location = (p0 + p1) / 2
            edge_instance.scale = (self.config.edge_scale, self.config.edge_scale, (p0 - p1).magnitude / 2)
            edge_instance.rotation_mode = 'QUATERNION'
            edge_instance.rotation_quaternion = mathutils.Vector(
                (0, 0, 1)).rotation_difference(p0 - p1)
            # edge_instance.type = 'COLLECTION'
            
            edge_instance.instance_collection = bpy.data.collections['Cut Edge Segment ' + str(seg)]
            if self.config.show_cut == True:
                cuts_collection.objects.link(edge_instance)

            # edge_primitive_name = 'Cut Edge Segment ' + str(c['segment'])
            # bpy.ops.object.collection_instance_add(collection=edge_primitive_name)
            # edge_obj = bpy.data.objects[edge_primitive_name + '.001']
            # edge_obj.name = 'Cut Edge Instance ' + str(i)
            # edge_obj.location = (p0 + p1) / 2
            # # edge_obj.scale = (0.002, 0.002, (p0 - p1).magnitude / 2)
            # edge_obj.scale = (self.config.edge_scale, self.config.edge_scale, (p0 - p1).magnitude / 2)
            # edge_obj.rotation_mode = 'QUATERNION'
            # edge_obj.rotation_quaternion = mathutils.Vector(
            #     (0, 0, 1)).rotation_difference(p0 - p1)
            # scene_collection.objects.unlink(edge_obj)
            # if self.config.show_cut == True:
            #     cuts_collection.objects.link(edge_obj)

            vertex_instance = bpy.data.objects.new('Cut Vertex Instance ' + str(i * 2), None)
            vertex_instance.location = p0
            vertex_instance.scale = (0.002, 0.002, 0.002)
            # vertex_instance.instance_type = 'COLLECTION'
            vertex_instance.instance_collection = bpy.data.collections['Cut Vertex Segment ' + str(seg)]
            if self.config.show_cut == True:
                cuts_collection.objects.link(vertex_instance)
            vertex_instance = bpy.data.objects.new('Cut Vertex Instance ' + str(i * 2 + 1), None)
            vertex_instance.location = p1
            vertex_instance.scale = (0.002, 0.002, 0.002)
            # vertex_instance.instance_type = 'COLLECTION'
            vertex_instance.instance_collection = bpy.data.collections['Cut Vertex Segment ' + str(seg)]
            if self.config.show_cut == True:
                cuts_collection.objects.link(vertex_instance)

            # vertex_primitive_name = 'Cut Vertex Segment ' + str(c['segment'])
            # bpy.ops.object.collection_instance_add(
            #     collection=vertex_primitive_name)
            # vertex_obj = bpy.data.objects[vertex_primitive_name + '.001']
            # vertex_obj.name = 'Cut Vertex Instance ' + str(i * 2)
            # vertex_obj.location = p0
            # vertex_obj.scale = (0.002, 0.002, 0.002)
            # scene_collection.objects.unlink(vertex_obj)
            # cuts_collection.objects.link(vertex_obj)
            # bpy.ops.object.collection_instance_add(
            #     collection=vertex_primitive_name)
            # vertex_obj = bpy.data.objects[vertex_primitive_name + '.001']
            # vertex_obj.name = 'Cut Vertex Instance ' + str(i * 2 + 1)
            # vertex_obj.location = p1
            # vertex_obj.scale = (0.002, 0.002, 0.002)
            # scene_collection.objects.unlink(vertex_obj)
            # if self.config.show_cut == True:
            #     cuts_collection.objects.link(vertex_obj)

    def build_ground(self):
        if self.config.plane == "original":
            bpy.ops.mesh.primitive_plane_add(size=50)
            zmin = bpy.data.objects['Mesh'].bound_box[0][1]
            plane_obj = bpy.data.objects['Plane']
            plane_obj.location = (0, 0, zmin)
            plane_obj.cycles.is_shadow_catcher = True
        elif self.config.plane == "checkerboard":
            bpy.ops.mesh.primitive_plane_add(size=50)
            zmin = bpy.data.objects['Mesh'].bound_box[0][1]
            plane_obj = bpy.data.objects['Plane']
            plane_obj.location = (0, 0, zmin)
            # plane_obj.cycles.is_shadow_catcher = True
            floor_mat = bpy.data.materials.new("Material_Plane")
            floor_mat.use_nodes = True
            # clean nodes
            for node in floor_mat.node_tree.nodes:
                floor_mat.node_tree.nodes.remove(node)
            # build checkerboard nodes
            node_tree = floor_mat.node_tree
            output_node = node_tree.nodes.new(type='ShaderNodeOutputMaterial')
            principled_node = node_tree.nodes.new(type='ShaderNodeBsdfPrincipled')
            checker_texture_node = node_tree.nodes.new(type='ShaderNodeTexChecker')
            checker_texture_node.inputs['Scale'].default_value = 50
            # checker_texture_node.inputs['Color1'].default_value = (1, 0, 0, 1)
            # checker_texture_node.inputs['Color2'].default_value = (0, 0, 1, 1)
            node_tree.links.new(checker_texture_node.outputs['Color'], principled_node.inputs['Base Color'])
            node_tree.links.new(principled_node.outputs['BSDF'], output_node.inputs['Surface'])
            plane_obj.active_material = floor_mat

    def build_camera(self, scene_json):
        # cam_json = scene_json['camera']
        cam = bpy.data.cameras['Camera']
        cam.lens_unit = 'FOV'
        cam.lens = 20
        cam_obj = bpy.data.objects.new('Camera', cam)
        # cam_obj.location = self.blender_vec(cam_json['position'])
        cam_obj.location = (1.3158, -0.43314, 0.89092)
        cam_track = cam_obj.constraints.new(type='TRACK_TO')
        cam_track.target = bpy.data.objects['Mesh']
        cam_track.track_axis = 'TRACK_NEGATIVE_Z'
        cam_track.up_axis = 'UP_Y'
        bpy.context.scene.collection.objects.link(bpy.data.objects['Camera'])
        bpy.context.scene.camera = cam_obj

    def build_direct_light(self):
        sun = bpy.data.lights.new("Sun", type='SUN')
        sun.energy = 2.0
        # sun.use_shadow = False
        sun_obj = bpy.data.objects.new('Sun', sun)
        sun_obj.location = (0.5, 0.5, 10.0)
        sun_obj.data.cycles.cast_shadow = False
        bpy.context.scene.collection.objects.link(bpy.data.objects['Sun'])

        # add additional lights
        light1 = bpy.data.lights.new("Sun2", type='SUN')
        light1.energy = 4
        # light1.use_shadow = False
        light_obj_1 = bpy.data.objects.new('Sun2', light1)
        light_obj_1.location = (3.0, 3.5, 1.0)
        # light_obj_1.rotation_euler(-80, 40, -30)
        light_obj_1.rotation_euler = Euler((radians(-80), radians(40), radians(-30)), 'XYZ')
        light_obj_1.data.cycles.cast_shadow = False
        bpy.context.scene.collection.objects.link(bpy.data.objects['Sun2'])

        light2 = bpy.data.lights.new("Sun3", type='SUN')
        light2.energy = 3
        # light2.use_shadow = False
        light_obj_2 = bpy.data.objects.new('Sun3', light2)
        light_obj_2.location = (1.8, -2.1, 1.2)
        # light_obj_2.rotation_euler(65, 40, 30)
        light_obj_2.rotation_euler = Euler((radians(65), radians(40), radians(30)), 'XYZ')
        light_obj_2.data.cycles.cast_shadow = False
        bpy.context.scene.collection.objects.link(bpy.data.objects['Sun3'])

        light3 = bpy.data.lights.new("Sun4", type='SUN')
        light3.energy = 3.5
        # light3.use_shadow = False
        light_obj_3 = bpy.data.objects.new('Sun4', light3)
        light_obj_3.location = (-3.0, 0.0, 0.5)
        # light_obj_3.rotation_euler(90, 0, -90)
        light_obj_3.rotation_euler = Euler((radians(90), radians(0), radians(-90)), 'XYZ')
        light_obj_3.data.cycles.cast_shadow = False
        bpy.context.scene.collection.objects.link(bpy.data.objects['Sun4'])

    def build_indirect_light(self):
        world = bpy.context.scene.world
        world.use_nodes = True
        texcoord_node = world.node_tree.nodes.new(type='ShaderNodeTexCoord')
        envmap_node = world.node_tree.nodes.new(type='ShaderNodeTexEnvironment')
        envmap_node.image = bpy.data.images.load(self.config.envmap_path)
        world.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.2
        world.node_tree.links.new(
            texcoord_node.outputs['Generated'], envmap_node.inputs['Vector'])
        world.node_tree.links.new(
            envmap_node.outputs['Color'], world.node_tree.nodes['Background'].inputs['Color'])

    def build_rotation(self):
        objects = bpy.data.objects
        # rotation_object = bpy.ops.object.empty_add(type='SPHERE')
        rotation_object = bpy.data.objects.new("empty", None)
        bpy.context.scene.collection.objects.link(rotation_object)
        for i in range(0, len(objects)):
            if 'Cut Vertex Instance' in objects[i].name \
                    or 'Cut Edge Instance' in objects[i].name \
                    or 'Singularity Instance' in objects[i].name \
                    or 'Loops' in objects[i].name \
                    or 'Singular Faces' in object[i].name:
                objects[i].parent = rotation_object
        objects['Mesh'].parent = rotation_object
        rotation_object.rotation_mode = 'XYZ'
        # rotation_object.rotation_euler.rotate_axis("Z", radians(self.rotation))
        rotation_object.rotation_euler.rotate_axis(self.config.rotation_axis, radians(self.rotation))

    def do_render(self):
        bpy.ops.render.render(write_still=True)

    def buildOnly(self):
        scene_file = open(self.config.scene_path + self.config.scene_name)
        scene_json = json.load(scene_file)
        self.clean()
        self.setup_renderer(self.config.output_path, self.config.width, self.config.height)
        self.build_main_mesh(self.config.scene_path + self.config.object_name)
        self.build_singularity_primitives()
        self.build_segment_primitives()
        self.build_addons(scene_json)
        self.build_ground()
        self.build_camera(scene_json)
        self.build_direct_light()
        self.build_indirect_light()

    def renderSingle(self):
        scene_file = open(self.config.scene_path + self.config.scene_name)
        scene_json = json.load(scene_file)
        self.clean()
        self.setup_renderer(self.config.output_path, self.config.width, self.config.height)
        self.build_main_mesh(self.config.scene_path + self.config.object_name)
        self.build_singularity_primitives()
        self.build_segment_primitives()
        self.build_addons(scene_json)
        self.build_ground()
        self.build_camera(scene_json)
        self.build_direct_light()
        self.build_indirect_light()
        self.do_render()

    def renderDir(self):
        f_list = os.listdir(self.config.scene_path)
        scene_list = []
        obj_list = []
        for filename in f_list:
            if os.path.splitext(filename)[1] == '.json':
                # scene_file
                scene_list.append(filename)
            if os.path.splitext(filename)[1] == '.obj':
                # object_file
                obj_list.append(filename)
        # render
        # scene_list and obj_list should have the same length
        if len(scene_list) == len(obj_list):
            for i in range(len(scene_list)):
                # render
                # update output filename
                path = os.getcwd()
                path = os.path.dirname(path)
                path = os.path.dirname(path)
                output_path = path + "\Output\\" + scene_list[i].split(".")[0] + ".png"

                self.config.object_name = obj_list[i]
                self.config.scene_name = scene_list[i]
                self.config.output_path = output_path

                scene_file = open(self.config.scene_path + self.config.scene_name)
                scene_json = json.load(scene_file)
                self.clean()
                self.setup_renderer(self.config.output_path, self.config.width, self.config.height)
                self.build_main_mesh(self.config.scene_path + self.config.object_name)
                self.build_singularity_primitives()
                self.build_segment_primitives()
                self.build_addons(scene_json)
                self.build_ground()
                self.build_camera(scene_json)
                self.build_direct_light()
                self.build_indirect_light()
                self.do_render()

    def renderModelDir(self):
        f_list = os.listdir(self.config.scene_path)
        obj_list = []
        for filename in f_list:
            if os.path.splitext(filename)[1] == '.obj':
                # object_file
                obj_list.append(filename)
        for i in range(len(obj_list)):
            path = os.getcwd()
            path = os.path.dirname(path)
            path = os.path.dirname(path)
            output_path = path + "\Output\\" + obj_list[i].split(".")[0] + ".png"
            self.config.output_path = output_path
            self.config.object_name = obj_list[i]
            self.renderSingle()

    def renderModelMaterial(self):
        material_list = ['original', 'gold', 'glass', 'ceramic', 'roughblue', 'wireframe',
                         'peeling_paint', 'paint', 'Metal01', 'Metal07', 'Metal08',
                         'Metal26','WoodFloor01', 'Marble01', 'Leather05', 'Fabric02',
                         'Fabric03', 'Concrete07', 'Chainmail02'
                         ]
        for material in material_list:
            self.config.material = material
            path = os.getcwd()
            path = os.path.dirname(path)
            path = os.path.dirname(path)
            output_path = path + "\Output\\" + self.config.object_name.split(".")[0] + "_" + material + ".png"
            self.config.output_path = output_path
            self.renderSingle()

    def renderRotation(self):
    # remaining complete
        for rotation in np.arange(self.config.rotation_start, self.config.rotation_end, self.config.rotation_step):
            self.rotation = radians(rotation)
            self.rotation = rotation
            path = os.getcwd()
            path = os.path.dirname(path)
            path = os.path.dirname(path)
            output_path = path + "\Output\\" + self.config.object_name.split(".")[0] + ("_rotation_%03d.png" % (rotation))
            self.config.output_path = output_path
            # self.renderSingle()
            scene_file = open(self.config.scene_path + self.config.scene_name)
            scene_json = json.load(scene_file)
            self.clean()
            self.setup_renderer(self.config.output_path, self.config.width, self.config.height)
            self.build_main_mesh(self.config.scene_path + self.config.object_name)
            self.build_singularity_primitives()
            self.build_segment_primitives()
            self.build_addons(scene_json)
            self.build_ground()
            self.build_camera(scene_json)
            self.build_direct_light()
            self.build_indirect_light()
            self.build_rotation()
            self.do_render()

    def renderRotationAnimation(self):
        path = os.getcwd()
        path = os.path.dirname(path)
        path = os.path.dirname(path)
        output_path = path + "\Output\\" + self.config.object_name.split(".")[0] + "_rotation.avi"
        self.config.output_path = output_path

        scene_file = open(self.config.scene_path + self.config.scene_name)
        scene_json = json.load(scene_file)
        self.clean()
        self.setup_renderer(self.config.output_path, self.config.width, self.config.height)
        self.build_main_mesh(self.config.scene_path + self.config.object_name)
        self.build_singularity_primitives()
        self.build_segment_primitives()
        self.build_addons(scene_json)
        self.build_ground()
        self.build_camera(scene_json)
        self.build_direct_light()
        self.build_indirect_light()

        objects = bpy.data.objects
        rotation_object = bpy.data.objects.new("empty", None)
        bpy.context.scene.collection.objects.link(rotation_object)
        for i in range(0, len(objects)):
            if 'Cut Vertex Instance' in objects[i].name \
                    or 'Cut Edge Instance' in objects[i].name \
                    or 'Singularity Instance' in objects[i].name \
                    or 'Loops' in objects[i].name \
                    or 'Singular Faces' in object[i].name:
                objects[i].parent = rotation_object
        objects['Mesh'].parent = rotation_object
        rotation_object.rotation_mode = 'XYZ'
        rotation_object.rotation_euler.rotate_axis("Z", radians(0))
        rotation_object.keyframe_insert(data_path='rotation_euler', frame=2)
        rotation_object.rotation_euler.rotate_axis("Z", radians(100))
        rotation_object.keyframe_insert(data_path='rotation_euler', frame=12)
        scene = bpy.data.scenes["Scene"]
        scene.render.fps = 12
        scene.frame_start = 1
        scene.frame_end = 12
        scene.frame_current = 1
        bpy.ops.render.render(animation=True)

    def render(self):
        if self.config.mode == 'build_only':
            self.buildOnly()
        elif self.config.mode == "single":
            self.renderSingle()
        elif self.config.mode == "dir":
            self.renderDir()
        elif self.config.mode == "modeldir":
            self.renderModelDir()
        elif self.config.mode == "modelmaterial":
            self.renderModelMaterial()
        elif self.config.mode == "rotation":
            self.renderRotation()
        elif self.config.mode == 'rotation_animation':
            self.renderRotationAnimation()





