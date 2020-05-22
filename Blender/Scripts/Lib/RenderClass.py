import bpy
import json
import math
import mathutils
import os
from math import radians
import bmesh
from mathutils import Matrix, Euler, Vector
import numpy as np
from MaterialFactory import MaterialFactory


class RenderCore:
    def __init__(self, config):
        self.config = config
        self.MaterialFactory = MaterialFactory()
        self.MaterialFactory.texture_path = self.config.texture_path
        self.MaterialFactory.roughness = self.config.roughness
        self.MaterialFactory.specular = self.config.specular
        self.MaterialFactory.sheen = self.config.sheen
        self.MaterialFactory.clearcoat = self.config.clearcoat
        self.MaterialFactory.wireframe_size = self.config.wireframe_size
        self.MaterialFactory.material_filename = self.config.material_filename
        self.MaterialFactory.wireframe_color = self.config.wireframe_color
        self.MaterialFactory.model_color = self.config.model_color
        self.rotation = 0
        self.singularity_json = None
        self.cut_json = None
        self.trace_json = None

    def blender_vec(self, vec):
        # return (vec[0], -vec[2], vec[1])
        return (vec[0], vec[1], vec[2])

    def gammaCorrect(self, srgb):
        if srgb < 0:
            return 0
        elif srgb < 0.04045:
            return srgb / 12.92
        else:
            return ((srgb + 0.055) / 1.055) ** 2.4

    def hex2rgba(self, h):
        b = (h & 0xFF) / 255.0
        g = ((h >> 8) & 0xFF) / 255.0
        r = ((h >> 16) & 0xFF) / 255.0
        linearR = self.gammaCorrect(r)
        linearG = self.gammaCorrect(g)
        linearB = self.gammaCorrect(b)
        return linearR, linearG, linearB, 1.0

    def load_json(self):
        cut_json_path = self.config.scene_path + self.config.cut_json_name
        singularity_json_path = self.config.scene_path + self.config.singularity_json_name
        trace_json_path = self.config.scene_path + self.config.trace_json_name
        if os.path.exists(cut_json_path):
            cut_file = open(cut_json_path)
            cut_json = json.load(cut_file)
            self.cut_json = cut_json['cuts']
        if os.path.exists(singularity_json_path):
            singularity_file = open(singularity_json_path)
            singularity_json = json.load(singularity_file)
            self.singularity_json = singularity_json['singularities']
        if os.path.exists(trace_json_path):
            trace_file = open(trace_json_path)
            trace_json = json.load(trace_file)
            self.trace_json = trace_json

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
        prefs = bpy.context.preferences
        cprefs = prefs.addons['cycles'].preferences
        for compute_device_type in ('CUDA', 'OPENCL', 'NONE'):
            try:
                cprefs.compute_device_type = compute_device_type
                break
            except TypeError:
                pass

        cprefs.get_devices()
        print('Num devices:', len(cprefs.devices))
        for device in cprefs.devices:
            print('Use device', device.name)
            device.use = True

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
        tree.links.new(
            render_node.outputs['Image'], originoutput_node.inputs[0])

    def choose_material(self):
        material_list = ['model_only', 'color_only', 'original', 'gold', 'glass', 'ceramic', 'roughblue', 'wireframe',
                         'peeling_paint', 'paint', 'vertex_color', 'wireframe_only']
        if self.config.material in material_list and self.config.material_filename is None:
            material_function = {
                'model_only': self.MaterialFactory.CreateModelOnly(),
                'color_only': self.MaterialFactory.CreateColorOnly(),
                'original': self.MaterialFactory.CreateMain(),
                'gold': self.MaterialFactory.CreateGold(),
                'glass': self.MaterialFactory.CreateGlass(),
                'ceramic': self.MaterialFactory.CreateCeramic(),
                'roughblue': self.MaterialFactory.CreateRoughBlue(),
                'wireframe': self.MaterialFactory.CreateWireframe(),
                'peeling_paint': self.MaterialFactory.CreatePeelingPaint(),
                'paint': self.MaterialFactory.CreatePaint(),
                'vertex_color': self.MaterialFactory.CreateVertexColor(),
                'wireframe_only': self.MaterialFactory.CreateWireframeOnly()
                # 'vertex_color_cmap' : self.MaterialFactory.CreateVertexColorCmap()
            }
            mat = material_function[self.config.material]
        elif self.config.material_filename is None:
            mat = self.MaterialFactory.CreateFromName(self.config.material)
        else:
            mat = self.MaterialFactory.CreateFromFile()

        if self.config.material == "original" or self.config.material == 'wireframe':
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
            mat.node_tree.links.new(
                texcoord_node.outputs['UV'], mutiply_node.inputs[0])
            mat.node_tree.links.new(
                mutiply_node.outputs['Vector'], add_node.inputs[0])
            mat.node_tree.links.new(
                add_node.outputs['Vector'], img_node.inputs['Vector'])
        if self.config.material_filename == "99-porcelain-texture.blend" or self.config.material_filename == 'Knittr.blend':
            # set texture
            mat.node_tree.nodes['Image Texture'].image = bpy.data.images.load(
                filepath=self.config.texture_path)
            # Add
            mat.node_tree.nodes['Vector Math'].inputs[1].default_value[0] = self.config.uv_add[0]
            mat.node_tree.nodes['Vector Math'].inputs[1].default_value[1] = self.config.uv_add[1]
            # Multiply
            mat.node_tree.nodes['Vector Math.001'].inputs[1].default_value[0] = self.config.uv_multiply[0]
            mat.node_tree.nodes['Vector Math.001'].inputs[1].default_value[1] = self.config.uv_multiply[1]

        return mat

    def build_main_mesh(self, path):
        if self.config.show_cylinders:
            return

        if self.config.object_name.split('.')[-1] == 'ply':
            bpy.ops.import_mesh.ply(filepath=path)
        else:
            bpy.ops.import_scene.obj(
                filepath=path, use_split_objects=False, axis_forward='Y', axis_up='Z')

        mesh_obj = bpy.data.objects[self.config.object_name.split(".")[0]]
        mesh_obj.parent = self.parent_object
        mesh_obj.name = 'Mesh'
        # set material
        mat = self.choose_material()
        mesh_obj.active_material = mat

    def build_singular_faces(self):
        # rotate
        if self.config.show_singularities:
            # build singular faces
            # set material
            if self.config.singular_face_material is None:
                self.MaterialFactory.wireframecolor = (0.026, 0.831, 0.888, 1)
                mat = self.MaterialFactory.CreateColoredWireframe()
            else:
                tmp = self.config.material_filename
                self.MaterialFactory.material_filename = self.config.singular_face_material
                mat = self.MaterialFactory.CreateFromFile()
                self.MaterialFactory.material_filename = tmp

            if self.config.object_name[-3:] == 'obj':
                bpy.ops.import_scene.obj(
                    filepath=self.config.scene_path + "singularFaces.obj", use_split_objects=False)
            else:
                bpy.ops.import_mesh.ply(
                    filepath=self.config.scene_path + 'singularFaces.ply')
            face_obj = bpy.data.objects["singularFaces"]
            face_obj.name = 'Singular Faces'
            face_obj.active_material = mat

    def build_loops(self):
        if self.config.show_loops:
            # build loop mesh
            if self.config.loop_material is None:
                self.MaterialFactory.wireframecolor = (1.0, 0.5, 0.2, 1)
                mat = self.MaterialFactory.CreateColoredWireframe()
            else:
                tmp = self.config.material_filename
                self.MaterialFactory.material_filename = self.config.loop_material
                mat = self.MaterialFactory.CreateFromFile()
                self.MaterialFactory.material_filename = tmp

            if self.config.object_name[-3:] == 'obj':
                bpy.ops.import_scene.obj(
                    filepath=self.config.scene_path + "loops.obj", use_split_objects=False)
            else:
                bpy.ops.import_mesh.ply(
                    filepath=self.config.scene_path + 'loops.ply')
            loop_obj = bpy.data.objects["loops"]
            loop_obj.parent = self.parent_object
            loop_obj.name = 'Loops'
            loop_obj.active_material = mat

    def build_foliation_graph(self):
        if self.config.show_foliation_graph:
            if self.config.object_name[-3:] == 'obj':
                path = os.path.join(self.config.scene_path,
                                    'foliationGraph.obj')
                if not os.path.exists(path):
                    return
                bpy.ops.import_scene.obj(
                    filepath=path, use_split_objects=False)
            else:
                path = os.path.join(self.config.scene_path,
                                    'foliationGraph.ply')
                if not os.path.exists(path):
                    return
                bpy.ops.import_mesh.ply(filepath=path)

            self.MaterialFactory.wireframecolor = (0.2, 0.8, 0.2, 1.0)
            mat = self.MaterialFactory.CreateColoredWireframe()
            obj = bpy.data.objects['foliationGraph']
            obj.parent = self.parent_object
            obj.name = 'Foliation Graph'
            obj.active_material = mat

    def build_cylinders(self):
        if self.config.show_cylinders:
            for _, _, files in os.walk(self.config.scene_path):
                for i, f in enumerate(files):
                    if f[:8] == 'cylinder':
                        fpath = os.path.join(self.config.scene_path, f)
                        if self.config.object_name[-3:] == 'obj':
                            bpy.ops.import_scene.obj(
                                filepath=fpath, use_split_objects=False)
                        else:
                            bpy.ops.import_mesh.ply(filepath=fpath)
                        obj = bpy.data.objects[f[:-4]]
                        obj.parent = self.parent_object
                        if self.config.cylinder_mode == 'plain':
                            obj.active_material = self.choose_material()
                        elif self.config.cylinder_mode == 'colors':
                            color = self.config.segment_colors[i % len(
                                self.config.segment_colors)]
                            self.MaterialFactory.color = color
                            obj.active_material = self.MaterialFactory.CreateColored(
                                f[:-4])

    def build_singularity_primitives(self):
        scene_collection = bpy.context.scene.collection
        for index, color in self.config.singular_colors.items():
            if self.config.singularity_material is None:
                self.MaterialFactory.color = color
                mat = self.MaterialFactory.CreateColored('Singularity' + index)
            else:
                tmp = self.config.material_filename
                self.MaterialFactory.material_filename = self.config.singularity_material
                mat = self.MaterialFactory.CreateFromFile()
                self.MaterialFactory.material_filename = tmp
                if self.config.show_singularity_color == True and\
                        self.config.singularity_material == "75-phone-screen.blend":
                    glossy_bsdf_node = mat.node_tree.nodes['Glossy BSDF']
                    # hex to rgba
                    glossy_bsdf_node.inputs[0].default_value = self.hex2rgba(
                        color)

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
            if self.config.cut_mode == "Plain":
                color = 0x808080

            if self.config.edge_material is None:
                self.MaterialFactory.color = color
                mat = self.MaterialFactory.CreateColored('Segment' + str(i))
            else:
                tmp = self.config.material_filename
                self.MaterialFactory.material_filename = self.config.edge_material
                mat = self.MaterialFactory.CreateFromFile()
                self.MaterialFactory.material_filename = tmp

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

    def build_trace_lines(self, lines, name, color):
        self.MaterialFactory.color = color
        mat = self.MaterialFactory.CreateColored(name)

        curves = bpy.data.curves.new(name, 'CURVE')
        curves.dimensions = '3D'
        curves.bevel_depth = self.config.trace_scale
        for line in lines:
            polyline = curves.splines.new('POLY')
            polyline.points.add(len(line) - 1)
            for i, p in enumerate(line):
                polyline.points[i].co = (p[0], p[1], p[2], 1)

        tracelines = bpy.data.objects.new(name, curves)
        tracelines.parent = self.parent_object
        tracelines.active_material = mat
        bpy.data.collections['Trace Lines'].objects.link(tracelines)

    def build_addons(self):
        scene_collection = bpy.context.scene.collection

        # singularities
        singularities_collection = bpy.data.collections.new('Singularities')
        scene_collection.children.link(singularities_collection)
        for i, s in enumerate(self.singularity_json):
            if s['type'] == 'vertex':
                instance = bpy.data.objects.new(
                    'Singularity Instance ' + str(i), None)
                instance.parent = self.parent_object
                instance.location = self.blender_vec(s['position'])
                scale = 0
                if s['index'] > 0:
                    scale = self.config.pole_scale
                else:
                    scale = self.config.zero_scale
                instance.scale = (scale, scale, scale)
                instance.instance_type = 'COLLECTION'
                instance.instance_collection = bpy.data.collections['Singularity' + str(
                    s['index'])]
                if self.config.show_singularities == True:
                    singularities_collection.objects.link(instance)

        # cuts
        cuts_collection = bpy.data.collections.new('Cuts')
        scene_collection.children.link(cuts_collection)
        for i, c in enumerate(self.cut_json):
            seg = c['segment'] % 20
            p0 = mathutils.Vector(self.blender_vec(c['points'][0]))
            p1 = mathutils.Vector(self.blender_vec(c['points'][1]))

            edge_instance = bpy.data.objects.new(
                'Cut Edge Instance ' + str(i), None)
            edge_instance.parent = self.parent_object
            edge_instance.location = (p0 + p1) / 2
            edge_instance.scale = (
                self.config.edge_scale, self.config.edge_scale, (p0 - p1).magnitude / 2)
            edge_instance.rotation_mode = 'QUATERNION'
            edge_instance.rotation_quaternion = mathutils.Vector(
                (0, 0, 1)).rotation_difference(p0 - p1)
            edge_instance.instance_type = 'COLLECTION'

            if self.config.cut_mode == "Segment" or self.config.cut_mode == "Plain":
                edge_instance.instance_collection = bpy.data.collections['Cut Edge Segment ' + str(
                    seg)]
            elif self.config.cut_mode == "zero_mode":
                if c['zeroConnected'] == False:
                    edge_instance.instance_collection = bpy.data.collections['Cut Edge Segment 14']
                elif c['zeroConnected'] == True:
                    edge_instance.instance_collection = bpy.data.collections['Cut Edge Segment 5']
            elif self.config.cut_mode == 'incoherent':
                if c['incoherent'] == False:
                    edge_instance.instance_collection = bpy.data.collections['Cut Edge Segment 14']
                elif c['incoherent'] == True:
                    edge_instance.instance_collection = bpy.data.collections['Cut Edge Segment 11']

            if self.config.cut_mode != "None":
                cuts_collection.objects.link(edge_instance)

            vertex_instance = bpy.data.objects.new(
                'Cut Vertex Instance ' + str(i * 2), None)
            vertex_instance.parent = self.parent_object
            vertex_instance.location = p0
            vertex_instance.scale = (
                self.config.edge_scale, self.config.edge_scale, self.config.edge_scale)
            vertex_instance.instance_type = 'COLLECTION'
            # vertex_instance.instance_collection = bpy.data.collections['Cut Vertex Segment ' + str(seg)]
            if self.config.cut_mode == "Segment" or self.config.cut_mode == "Plain":
                vertex_instance.instance_collection = bpy.data.collections['Cut Vertex Segment ' + str(
                    seg)]
            elif self.config.cut_mode == "zero_mode":
                if c['zeroConnected'] == False:
                    vertex_instance.instance_collection = bpy.data.collections[
                        'Cut Vertex Segment 14']
                elif c['zeroConnected'] == True:
                    vertex_instance.instance_collection = bpy.data.collections['Cut Vertex Segment 5']
            elif self.config.cut_mode == 'incoherent':
                if c['incoherent'] == False:
                    vertex_instance.instance_collection = bpy.data.collections[
                        'Cut Vertex Segment 14']
                elif c['incoherent'] == True:
                    vertex_instance.instance_collection = bpy.data.collections[
                        'Cut Vertex Segment 11']

            if self.config.cut_mode != "None":
                cuts_collection.objects.link(vertex_instance)
            vertex_instance = bpy.data.objects.new(
                'Cut Vertex Instance ' + str(i * 2 + 1), None)
            vertex_instance.parent = self.parent_object
            vertex_instance.location = p1
            vertex_instance.scale = (
                self.config.edge_scale, self.config.edge_scale, self.config.edge_scale)
            vertex_instance.instance_type = 'COLLECTION'
            # vertex_instance.instance_collection = bpy.data.collections['Cut Vertex Segment ' + str(seg)]
            if self.config.cut_mode == "Segment" or self.config.cut_mode == "Plain":
                vertex_instance.instance_collection = bpy.data.collections['Cut Vertex Segment ' + str(
                    seg)]
            elif self.config.cut_mode == "zero_mode":
                if c['zeroConnected'] == False:
                    vertex_instance.instance_collection = bpy.data.collections[
                        'Cut Vertex Segment 14']
                elif c['zeroConnected'] == True:
                    vertex_instance.instance_collection = bpy.data.collections['Cut Vertex Segment 5']
            elif self.config.cut_mode == 'incoherent':
                if c['incoherent'] == False:
                    vertex_instance.instance_collection = bpy.data.collections[
                        'Cut Vertex Segment 14']
                elif c['incoherent'] == True:
                    vertex_instance.instance_collection = bpy.data.collections[
                        'Cut Vertex Segment 11']

            if self.config.cut_mode != "None":
                cuts_collection.objects.link(vertex_instance)

        # trace lines
        trace_collection = bpy.data.collections.new('Trace Lines')
        scene_collection.children.link(trace_collection)
        self.build_trace_lines(
            self.trace_json['primalTraceLines'], 'Primal trace', self.config.primal_trace_color)
        self.build_trace_lines(
            self.trace_json['primalCriticalTraceLines'], 'Primal critical trace', self.config.primal_trace_color)
        self.build_trace_lines(
            self.trace_json['conjugateTraceLines'], 'Conjugate trace', self.config.conjugate_trace_color)
        self.build_trace_lines(
            self.trace_json['conjugateCriticalTraceLines'], 'Conjugate critical trace', self.config.conjugate_trace_color)

    def build_parent_object(self):
        self.parent_object = bpy.data.objects.new("Parent Object", None)
        self.parent_object.rotation_mode = 'XYZ'
        bpy.context.scene.collection.objects.link(self.parent_object)

        transform_json = os.path.join(
            self.config.scene_path, self.config.transform_json_name)
        if os.path.exists(transform_json):
            # read json
            with open(transform_json, 'r') as load_f:
                transform = json.load(load_f)
            # set transform
            for i in range(3):
                self.parent_object.location[i] = transform['Location'][i]
                self.parent_object.rotation_euler[i] = transform['Rotation'][i]
                self.parent_object.scale[i] = transform['Scale'][i]

    def build_ground(self):
        objects = bpy.data.objects
        parent_object = objects["Parent Object"]
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
            principled_node = node_tree.nodes.new(
                type='ShaderNodeBsdfPrincipled')
            checker_texture_node = node_tree.nodes.new(
                type='ShaderNodeTexChecker')
            checker_texture_node.inputs['Scale'].default_value = 50
            # checker_texture_node.inputs['Color1'].default_value = (1, 0, 0, 1)
            # checker_texture_node.inputs['Color2'].default_value = (0, 0, 1, 1)
            node_tree.links.new(
                checker_texture_node.outputs['Color'], principled_node.inputs['Base Color'])
            node_tree.links.new(
                principled_node.outputs['BSDF'], output_node.inputs['Surface'])
            plane_obj.active_material = floor_mat
        elif self.config.plane == "predefined":
            path = os.getcwd()
            path = os.path.dirname(path)
            path = os.path.dirname(path)
            path = os.path.dirname(path)
            filename = path + "/Data/Materials/predefined/predefined.blend"
            with bpy.data.libraries.load(filename) as (src, dst):
                dst.objects = src.objects
            grid = dst.objects[20]
            number = dst.objects[10]
            plane = dst.objects[9]
            # zmin = bpy.data.objects['Mesh'].bound_box[0][1]

            z_offset = -1.0
            # parent_object.location[2] -= objects['Mesh'].bound_box[0][1]
            # parent_object.location[2] += z_offset

            grid.location[2] = z_offset
            number.location[2] = z_offset
            plane.location[2] = z_offset

            plane.scale[0] = 10
            plane.scale[1] = 10

            bpy.context.scene.collection.objects.link(grid)
            bpy.context.scene.collection.objects.link(number)
            bpy.context.scene.collection.objects.link(plane)

    def build_camera(self):
        path = os.getcwd()
        path = os.path.dirname(path)
        path = os.path.dirname(path)
        path = os.path.dirname(path)
        filename = path + "/Data/Materials/predefined/predefined.blend"
        with bpy.data.libraries.load(filename) as (src, dst):
            dst.objects = src.objects

        cam = dst.objects[23]
        cam.location *= 0.8

        # center = Vector(self.blender_vec(cam_json['center']))
        center = Vector((0, 0, 0))
        direction = center - cam.location
        rot_quat = direction.to_track_quat('-Z', 'Y')
        cam.rotation_euler = rot_quat.to_euler()

        bpy.context.scene.collection.objects.link(cam)
        bpy.context.scene.camera = cam

    def build_direct_light(self):
        path = os.getcwd()
        path = os.path.dirname(path)
        path = os.path.dirname(path)
        path = os.path.dirname(path)
        filename = path + "/Data/Materials/predefined/predefined.blend"
        with bpy.data.libraries.load(filename) as (src, dst):
            dst.objects = src.objects
            dst.materials = src.materials

        light_1 = dst.objects[17]
        light_2 = dst.objects[18]
        light_3 = dst.objects[19]

        light_1.active_material.node_tree.nodes["Emission"].inputs[1].default_value = 17
        light_2.active_material.node_tree.nodes["Emission"].inputs[1].default_value = 14
        light_3.active_material.node_tree.nodes["Emission"].inputs[1].default_value = 23.4

        bpy.context.scene.collection.objects.link(light_1)
        bpy.context.scene.collection.objects.link(light_2)
        bpy.context.scene.collection.objects.link(light_3)

    def build_indirect_light(self):
        world = bpy.context.scene.world
        world.use_nodes = True
        if self.config.use_envmap == True:
            texcoord_node = world.node_tree.nodes.new(
                type='ShaderNodeTexCoord')
            envmap_node = world.node_tree.nodes.new(
                type='ShaderNodeTexEnvironment')
            envmap_node.image = bpy.data.images.load(self.config.envmap_path)
            world.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.2
            world.node_tree.links.new(
                texcoord_node.outputs['Generated'], envmap_node.inputs['Vector'])
            world.node_tree.links.new(
                envmap_node.outputs['Color'], world.node_tree.nodes['Background'].inputs['Color'])

    def build_rotation(self):
        objects = bpy.data.objects
        parent_object = objects["Parent Object"]
        parent_object.rotation_mode = 'XYZ'
        parent_object.rotation_euler.rotate_axis(
            self.config.rotation_axis, radians(self.rotation))

    def do_render(self):
        bpy.ops.render.render(write_still=True)

    def buildOnly(self):
        self.load_json()
        self.clean()
        self.setup_renderer(self.config.output_path,
                            self.config.width, self.config.height)
        self.build_parent_object()
        self.build_main_mesh(self.config.scene_path + self.config.object_name)
        self.build_singular_faces()
        self.build_loops()
        self.build_foliation_graph()
        self.build_cylinders()
        self.build_singularity_primitives()
        self.build_segment_primitives()
        self.build_addons()
        self.build_ground()
        self.build_camera()
        self.build_direct_light()
        self.build_indirect_light()

    def renderSingle(self):
        self.buildOnly()
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
                path = os.path.dirname(path)
                output_path = path + "/Output/" + \
                    scene_list[i].split(".")[0] + ".png"

                self.config.object_name = obj_list[i]
                self.config.scene_name = scene_list[i]
                self.config.output_path = output_path
                self.renderSingle()

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
            path = os.path.dirname(path)
            output_path = path + "/Output/" + \
                obj_list[i].split(".")[0] + ".png"
            self.config.output_path = output_path
            self.config.object_name = obj_list[i]
            self.renderSingle()

    def renderModelMaterial(self):
        material_list = ['original', 'gold', 'glass', 'ceramic', 'roughblue', 'wireframe',
                         'peeling_paint', 'paint', 'Metal01',
                         'Metal07', 'Metal08', 'Metal26', 'WoodFloor01', 'Marble01', 'Leather05',
                         'Fabric02', 'Fabric03', 'Concrete07', 'Chainmail02', 'vertex_color'
                         ]
        for material in material_list:
            self.config.material = material
            path = os.getcwd()
            path = os.path.dirname(path)
            path = os.path.dirname(path)
            path = os.path.dirname(path)
            output_path = path + "/Output/" + \
                self.config.object_name.split(".")[0] + "_" + material + ".png"
            self.config.output_path = output_path
            self.renderSingle()

    def renderRotation(self):
        prefix = self.config.output_path.split(".png")[0]
        for rotation in np.arange(self.config.rotation_start, self.config.rotation_end, self.config.rotation_step):
            self.rotation = rotation
            self.config.output_path = prefix + "_rotation_%03d" % (rotation)
            self.buildOnly()
            self.build_rotation()
            self.do_render()

    def renderRotationAnimation(self):
        path = os.getcwd()
        path = os.path.dirname(path)
        path = os.path.dirname(path)
        path = os.path.dirname(path)
        output_path = path + "/Output/" + \
            self.config.object_name.split(".")[0] + "_rotation.avi"
        self.config.output_path = output_path

        self.buildOnly()
        objects = bpy.data.objects
        rotation_object = bpy.data.objects.new("empty", None)
        bpy.context.scene.collection.objects.link(rotation_object)
        for i in range(0, len(objects)):
            if 'Cut Vertex Instance' in objects[i].name \
                    or 'Cut Edge Instance' in objects[i].name \
                    or 'Singularity Instance' in objects[i].name \
                    or 'Loops' in objects[i].name \
                    or 'Singular Faces' in object[i].name \
                    or 'Trace Vertex Instance' in objects[i].name \
                    or 'Trace Edge Instance' in objects[i].name:
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
