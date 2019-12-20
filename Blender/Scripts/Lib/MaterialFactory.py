import bpy
import json
import math
import mathutils
import os
import sys
import cc0assetsloader as loader
# import matplotlib.pyplot as plt


class MaterialFactory:
    def __init__(self):
        self.roughness = 0.0
        self.specular = 0.0
        self.sheen = None
        self.clearcoat = None
        self.texture_path = None
        self.color = None
        self.wireframecolor = (0.026, 0.831, 0.888, 1)
        self.wireframe_size = None
        self.material_filename = None
        self.material_name = None
        self.wireframe_color = (0, 0, 0, 1.0)
        self.model_color = None

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

    def CreateMain(self):
        mat = bpy.data.materials.new('Main')
        mat.use_nodes = True
        img_node = mat.node_tree.nodes.new(type='ShaderNodeTexImage')
        img_node.image = bpy.data.images.load(filepath=self.texture_path)
        # rgb_node = mat.node_tree.nodes.new(type='ShaderNodeRGB')
        # rgb_node.outputs['Color'].default_value = (0.8, 0.8, 0.8, 1.0)
        bsdf_node = mat.node_tree.nodes['Principled BSDF']
        bsdf_node.inputs['Roughness'].default_value = self.roughness
        bsdf_node.inputs['Specular'].default_value = self.specular
        bsdf_node.inputs['Sheen'].default_value = self.sheen
        bsdf_node.inputs['Clearcoat'].default_value = self.clearcoat
        mat.node_tree.links.new(
            img_node.outputs['Color'], bsdf_node.inputs['Base Color'])
        return mat

    def CreateColorOnly(self):
        mat = bpy.data.materials.new('Main')
        mat.use_nodes = True
        rgb_node = mat.node_tree.nodes.new(type='ShaderNodeRGB')
        # rgb_node.outputs['Color'].default_value = (0.8, 0.8, 0.8, 1.0)
        rgb_node.outputs['Color'].default_value = self.model_color
        bsdf_node = mat.node_tree.nodes['Principled BSDF']
        bsdf_node.inputs['Roughness'].default_value = self.roughness
        bsdf_node.inputs['Specular'].default_value = self.specular
        mat.node_tree.links.new(
            rgb_node.outputs['Color'], bsdf_node.inputs['Base Color'])
        return mat

    def CreateModelOnly(self):
        path = os.getcwd()
        path = os.path.dirname(path)
        path = os.path.dirname(path)
        path = os.path.dirname(path)
        filename = path + "/Data/Materials/" + "55-tomato-material-modified.blend"
        with bpy.data.libraries.load(filename, link=False) as (src, dst):
            dst.materials = src.materials
        return dst.materials[0]

    def CreateVertexColor(self):
        mat = bpy.data.materials.new('Material Vertex Color')
        mat.use_nodes = True
        bsdf_node = mat.node_tree.nodes['Principled BSDF']
        vertex_color_node = mat.node_tree.nodes.new(type='ShaderNodeVertexColor')
        vertex_color_node.layer_name = 'Col'
        mat.node_tree.links.new(vertex_color_node.outputs['Color'], bsdf_node.inputs['Base Color'])
        return mat

    # def CreateVertexColorCmap(self):
    #     mat = bpy.data.materials.new('Material Vertex Color Cmap')
    #     mat.use_nodes = True
    #     bsdf_node = mat.node_tree.nodes['Principled BSDF']
    #     vertex_color_node = mat.node_tree.nodes.new(type='ShaderNodeVertexColor')
    #     mesh = bpy.data.objects['Mesh'].data
    #     mesh.vertex_colors.new(name = 'Col')
    #     vertices = mesh.vertices
    #     max = -100
    #     for i in range(len(vertices)):
    #         print(vertices[i].to_tuple())
    #         if vertices[i][0] > max:
    #             max = vertices[i][0]
    #     for index, vertex_color in enumerate(mesh.vertex_colors['Col'].data):
    #         # vertex_color.color = plt.cm.hot(index/len(mesh.vertex_colors['Col'].data))
    #         vertex_color.color = plt.cm.hot(vertices[index][0]/max)
    #     vertex_color_node.layer_name = 'Col'
    #     mat.node_tree.links.new(vertex_color_node.outputs['Color'], bsdf_node.inputs['Base Color'])
    #     return mat

    def CreateColored(self, name):
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
        bsdf_node = mat.node_tree.nodes['Principled BSDF']
        bsdf_node.inputs['Base Color'].default_value = self.hex2rgba(self.color)
        bsdf_node.inputs['Roughness'].default_value = 0.0
        bsdf_node.inputs['Specular'].default_value = 1.0
        #output_node = mat.node_tree.nodes['Material Output']
        #mat.node_tree.links.new(
        #    color_node.outputs['Color'], output_node.inputs['Surface'])
        return mat


    def CreateColoredWireframe(self):
        mat = bpy.data.materials.new('Material Colored Wireframe')
        mat.use_nodes = True
        bsdf_node = mat.node_tree.nodes['Principled BSDF']
        bsdf_node.inputs['Roughness'].default_value = self.roughness
        bsdf_node.inputs['Specular'].default_value = self.specular
        # bsdf_node.inputs['Base Color'].default_value = (0.026, 0.831, 0.888, 1)
        bsdf_node.inputs['Base Color'].default_value = self.wireframecolor
        mix_node = mat.node_tree.nodes.new(type='ShaderNodeMixShader')
        wire_node = mat.node_tree.nodes.new(type='ShaderNodeWireframe')
        wire_mat_node = mat.node_tree.nodes.new(type='ShaderNodeBsdfDiffuse')
        rgb_node = mat.node_tree.nodes.new(type='ShaderNodeRGB')
        # color
        rgb_node.outputs['Color'].default_value = self.wireframe_color
        output_node = mat.node_tree.nodes['Material Output']
        # set size
        size = wire_node.inputs['Size'].default_value
        # wire_node.inputs['Size'].default_value = size / 5
        wire_node.inputs['Size'].default_value = size * self.wireframe_size
        mat.node_tree.links.new(bsdf_node.outputs['BSDF'], mix_node.inputs[1])
        mat.node_tree.links.new(rgb_node.outputs['Color'], wire_mat_node.inputs['Color'])
        mat.node_tree.links.new(wire_mat_node.outputs['BSDF'], mix_node.inputs[2])
        mat.node_tree.links.new(wire_node.outputs['Fac'], mix_node.inputs['Fac'])
        mat.node_tree.links.new(mix_node.outputs['Shader'], output_node.inputs['Surface'])
        return mat


    def CreateWireframe(self):
        mat = bpy.data.materials.new('Material Wireframe')
        mat.use_nodes = True
        bsdf_node = mat.node_tree.nodes['Principled BSDF']
        bsdf_node.inputs['Roughness'].default_value = self.roughness
        bsdf_node.inputs['Specular'].default_value = self.specular
        img_node = mat.node_tree.nodes.new(type='ShaderNodeTexImage')
        img_node.image = bpy.data.images.load(filepath=self.texture_path)
        mix_node = mat.node_tree.nodes.new(type='ShaderNodeMixShader')
        wire_node = mat.node_tree.nodes.new(type='ShaderNodeWireframe')
        wire_mat_node = mat.node_tree.nodes.new(type='ShaderNodeBsdfDiffuse')
        rgb_node = mat.node_tree.nodes.new(type='ShaderNodeRGB')
        # rgb_node.outputs['Color'].default_value = (0.1, 0.1, 0.1, 1.0)
        # color
        # rgb_node.outputs['Color'].default_value = (0.1, 0.1, 0.1, 1.0)
        rgb_node.outputs['Color'].default_value = self.wireframe_color
        # rgb_node.outputs['Color'].default_value = (0, 1, 0, 1.0)
        output_node = mat.node_tree.nodes['Material Output']
        # set size
        size = wire_node.inputs['Size'].default_value
        # wire_node.inputs['Size'].default_value = size / 5
        wire_node.inputs['Size'].default_value = size * self.wireframe_size
        mat.node_tree.links.new(img_node.outputs['Color'], bsdf_node.inputs['Base Color'])
        mat.node_tree.links.new(bsdf_node.outputs['BSDF'], mix_node.inputs[1])
        mat.node_tree.links.new(rgb_node.outputs['Color'], wire_mat_node.inputs['Color'])
        mat.node_tree.links.new(wire_mat_node.outputs['BSDF'], mix_node.inputs[2])
        mat.node_tree.links.new(wire_node.outputs['Fac'], mix_node.inputs['Fac'])
        mat.node_tree.links.new(mix_node.outputs['Shader'], output_node.inputs['Surface'])
        return mat

    def CreateWireframeOnly(self):
        mat = bpy.data.materials.new('Material Wireframe')
        mat.use_nodes = True
        bsdf_node = mat.node_tree.nodes['Principled BSDF']
        bsdf_node.inputs['Roughness'].default_value = self.roughness
        bsdf_node.inputs['Specular'].default_value = self.specular

        mix_node = mat.node_tree.nodes.new(type='ShaderNodeMixShader')
        wire_node = mat.node_tree.nodes.new(type='ShaderNodeWireframe')
        wire_mat_node = mat.node_tree.nodes.new(type='ShaderNodeBsdfDiffuse')
        rgb_node = mat.node_tree.nodes.new(type='ShaderNodeRGB')
        # rgb_node.outputs['Color'].default_value = (0.1, 0.1, 0.1, 1.0)
        # color
        # rgb_node.outputs['Color'].default_value = (0.1, 0.1, 0.1, 1.0)
        rgb_node.outputs['Color'].default_value = self.wireframe_color
        # rgb_node.outputs['Color'].default_value = (0, 1, 0, 1.0)
        output_node = mat.node_tree.nodes['Material Output']
        # set size
        size = wire_node.inputs['Size'].default_value
        # wire_node.inputs['Size'].default_value = size / 5
        wire_node.inputs['Size'].default_value = size * self.wireframe_size
        bsdf_node.inputs['Base Color'].default_value = self.model_color
        mat.node_tree.links.new(bsdf_node.outputs['BSDF'], mix_node.inputs[1])
        mat.node_tree.links.new(rgb_node.outputs['Color'], wire_mat_node.inputs['Color'])
        mat.node_tree.links.new(wire_mat_node.outputs['BSDF'], mix_node.inputs[2])
        mat.node_tree.links.new(wire_node.outputs['Fac'], mix_node.inputs['Fac'])
        mat.node_tree.links.new(mix_node.outputs['Shader'], output_node.inputs['Surface'])
        return mat

    def create_peeling_paint_metal_node_group(self, node_tree):
        peeling_paint_metal_node_group = self.add_peeling_paint_metal_node_group()
        node = node_tree.nodes.new(type='ShaderNodeGroup')
        node.name = "Peeling Paint Metal"
        node.node_tree = peeling_paint_metal_node_group
        return node

    def add_parametric_color_ramp(self):
        group = bpy.data.node_groups.new(type="ShaderNodeTree", name="Parametric Color Ramp")
        # Input
        input_node = group.nodes.new(type="NodeGroupInput")
        group.inputs.new("NodeSocketFloatFactor", "Fac")
        group.inputs.new("NodeSocketColor", "Color1")
        group.inputs.new("NodeSocketColor", "Color2")
        group.inputs.new("NodeSocketFloatFactor", "Pos1")
        group.inputs.new("NodeSocketFloatFactor", "Pos2")
        self.set_socket_value_range(group.inputs["Fac"], default_value=0.5)
        self.set_socket_value_range(group.inputs["Pos1"], default_value=0.0)
        self.set_socket_value_range(group.inputs["Pos2"], default_value=1.0)
        # Math
        denominator_subtract_node = group.nodes.new(type="ShaderNodeMath")
        denominator_subtract_node.operation = "SUBTRACT"
        denominator_subtract_node.use_clamp = True
        numerator_subtract_node = group.nodes.new(type="ShaderNodeMath")
        numerator_subtract_node.operation = "SUBTRACT"
        numerator_subtract_node.use_clamp = True
        divide_node = group.nodes.new(type="ShaderNodeMath")
        divide_node.operation = "DIVIDE"
        divide_node.use_clamp = True
        group.links.new(input_node.outputs["Pos2"], denominator_subtract_node.inputs[0])
        group.links.new(input_node.outputs["Fac"], denominator_subtract_node.inputs[1])
        group.links.new(input_node.outputs["Pos2"], numerator_subtract_node.inputs[0])
        group.links.new(input_node.outputs["Pos1"], numerator_subtract_node.inputs[1])
        group.links.new(denominator_subtract_node.outputs["Value"], divide_node.inputs[0])
        group.links.new(numerator_subtract_node.outputs["Value"], divide_node.inputs[1])
        # Mixing
        mix_node = group.nodes.new(type="ShaderNodeMixRGB")
        group.links.new(divide_node.outputs["Value"], mix_node.inputs["Fac"])
        group.links.new(input_node.outputs["Color2"], mix_node.inputs[1])
        group.links.new(input_node.outputs["Color1"], mix_node.inputs[2])
        # Output
        output_node = group.nodes.new(type="NodeGroupOutput")
        group.outputs.new("NodeSocketColor", "Color")
        group.links.new(mix_node.outputs["Color"], output_node.inputs["Color"])
        # Return
        return group

    def create_parametric_color_ramp_node(self, node_tree):
        color_ramp_node_group = self.add_parametric_color_ramp()
        node = node_tree.nodes.new(type='ShaderNodeGroup')
        node.name = "Parametric Color Ramp"
        node.node_tree = color_ramp_node_group
        return node

    def set_socket_value_range(self, socket, default_value=0.0,
                               min_value=0.0, max_value=1.0):
        socket.default_value = default_value
        socket.min_value = min_value
        socket.max_value = max_value

    def add_tri_parametric_color_ramp(self):
        group = bpy.data.node_groups.new(type="ShaderNodeTree", name="Tri Parametric Color Ramp")
        # Input
        input_node = group.nodes.new(type="NodeGroupInput")
        group.inputs.new("NodeSocketFloatFactor", "Fac")
        group.inputs.new("NodeSocketColor", "Color1")
        group.inputs.new("NodeSocketColor", "Color2")
        group.inputs.new("NodeSocketColor", "Color3")
        group.inputs.new("NodeSocketFloatFactor", "Pos1")
        group.inputs.new("NodeSocketFloatFactor", "Pos2")
        group.inputs.new("NodeSocketFloatFactor", "Pos3")
        self.set_socket_value_range(group.inputs["Fac"], default_value=0.5)
        self.set_socket_value_range(group.inputs["Pos1"], default_value=0.25)
        self.set_socket_value_range(group.inputs["Pos2"], default_value=0.50)
        self.set_socket_value_range(group.inputs["Pos3"], default_value=0.75)
        # Nested color ramp
        nested_color_ramp_node = self.create_parametric_color_ramp_node(group)
        group.links.new(input_node.outputs["Color1"], nested_color_ramp_node.inputs["Color1"])
        group.links.new(input_node.outputs["Color2"], nested_color_ramp_node.inputs["Color2"])
        group.links.new(input_node.outputs["Pos1"], nested_color_ramp_node.inputs["Pos1"])
        group.links.new(input_node.outputs["Pos2"], nested_color_ramp_node.inputs["Pos2"])
        group.links.new(input_node.outputs["Fac"], nested_color_ramp_node.inputs["Fac"])
        # Math
        denominator_subtract_node = group.nodes.new(type="ShaderNodeMath")
        denominator_subtract_node.operation = "SUBTRACT"
        denominator_subtract_node.use_clamp = True
        numerator_subtract_node = group.nodes.new(type="ShaderNodeMath")
        numerator_subtract_node.operation = "SUBTRACT"
        numerator_subtract_node.use_clamp = True
        divide_node = group.nodes.new(type="ShaderNodeMath")
        divide_node.operation = "DIVIDE"
        divide_node.use_clamp = True
        group.links.new(input_node.outputs["Pos3"], denominator_subtract_node.inputs[0])
        group.links.new(input_node.outputs["Fac"], denominator_subtract_node.inputs[1])
        group.links.new(input_node.outputs["Pos3"], numerator_subtract_node.inputs[0])
        group.links.new(input_node.outputs["Pos2"], numerator_subtract_node.inputs[1])
        group.links.new(denominator_subtract_node.outputs["Value"], divide_node.inputs[0])
        group.links.new(numerator_subtract_node.outputs["Value"], divide_node.inputs[1])
        # Mixing
        mix_node = group.nodes.new(type="ShaderNodeMixRGB")
        group.links.new(divide_node.outputs["Value"], mix_node.inputs["Fac"])
        group.links.new(input_node.outputs["Color3"], mix_node.inputs[1])
        group.links.new(nested_color_ramp_node.outputs["Color"], mix_node.inputs[2])
        # Output
        output_node = group.nodes.new(type="NodeGroupOutput")
        group.outputs.new("NodeSocketColor", "Color")
        group.links.new(mix_node.outputs["Color"], output_node.inputs["Color"])
        # Return
        return group

    def create_tri_parametric_color_ramp_node(self, node_tree):
        tri_color_ramp_node_group = self.add_tri_parametric_color_ramp()
        node = node_tree.nodes.new(type='ShaderNodeGroup')
        node.name = "Tri Parametric Color Ramp"
        node.node_tree = tri_color_ramp_node_group
        return node

    def add_peeling_paint_metal_node_group(self):
        group = bpy.data.node_groups.new(type="ShaderNodeTree", name="Peeling Paint Metal")
        input_node = group.nodes.new(type="NodeGroupInput")
        group.inputs.new("NodeSocketColor", "Paint Color")
        group.inputs.new("NodeSocketColor", "Metal Color")
        group.inputs.new("NodeSocketFloat", "Scale")
        group.inputs.new("NodeSocketFloat", "Detail")
        group.inputs.new("NodeSocketFloat", "Distortion")
        group.inputs.new("NodeSocketFloatFactor", "Threshold")
        self.set_socket_value_range(group.inputs["Scale"], default_value=4.5, min_value=0.0, max_value=1000.0)
        self.set_socket_value_range(group.inputs["Detail"], default_value=8.0, min_value=0.0, max_value=16.0)
        self.set_socket_value_range(group.inputs["Distortion"], default_value=0.5, min_value=0.0, max_value=1000.0)
        self.set_socket_value_range(group.inputs["Threshold"], default_value=0.42)
        group.inputs["Paint Color"].default_value = (0.152, 0.524, 0.067, 1.000)
        group.inputs["Metal Color"].default_value = (0.062, 0.015, 0.011, 1.000)
        tex_coord_node = group.nodes.new(type="ShaderNodeTexCoord")
        mapping_node = group.nodes.new(type="ShaderNodeMapping")
        group.links.new(tex_coord_node.outputs["Object"], mapping_node.inputs["Vector"])
        # Peeling region segmentation
        peeling_noise_node = group.nodes.new(type="ShaderNodeTexNoise")
        group.links.new(mapping_node.outputs["Vector"], peeling_noise_node.inputs["Vector"])
        group.links.new(input_node.outputs["Scale"], peeling_noise_node.inputs["Scale"])
        group.links.new(input_node.outputs["Detail"], peeling_noise_node.inputs["Detail"])
        group.links.new(input_node.outputs["Distortion"], peeling_noise_node.inputs["Distortion"])
        peeling_threshold_node = self.create_parametric_color_ramp_node(group)
        peeling_threshold_node.inputs["Color1"].default_value = (0.0, 0.0, 0.0, 1.0)
        peeling_threshold_node.inputs["Color2"].default_value = (1.0, 1.0, 1.0, 1.0)
        # Base color
        epsilon_subtract_node = group.nodes.new(type="ShaderNodeMath")
        epsilon_subtract_node.operation = "SUBTRACT"
        epsilon_subtract_node.inputs[1].default_value = 0.001
        group.links.new(input_node.outputs["Threshold"], epsilon_subtract_node.inputs[0])
        group.links.new(peeling_noise_node.outputs["Fac"], peeling_threshold_node.inputs["Fac"])
        group.links.new(epsilon_subtract_node.outputs["Value"], peeling_threshold_node.inputs["Pos1"])
        group.links.new(input_node.outputs["Threshold"], peeling_threshold_node.inputs["Pos2"])
        color_mix_node = group.nodes.new(type="ShaderNodeMixRGB")
        group.links.new(peeling_threshold_node.outputs["Color"], color_mix_node.inputs["Fac"])
        group.links.new(input_node.outputs["Metal Color"], color_mix_node.inputs[1])
        group.links.new(input_node.outputs["Paint Color"], color_mix_node.inputs[2])
        # Ambient occulusion
        epsilon_add_node = group.nodes.new(type="ShaderNodeMath")
        epsilon_add_node.operation = "ADD"
        epsilon_add_node.inputs[1].default_value = 0.010
        group.links.new(input_node.outputs["Threshold"], epsilon_add_node.inputs[0])
        fallout_subtract_node = group.nodes.new(type="ShaderNodeMath")
        fallout_subtract_node.operation = "SUBTRACT"
        fallout_subtract_node.inputs[1].default_value = 0.060
        group.links.new(input_node.outputs["Threshold"], fallout_subtract_node.inputs[0])
        ao_node = self.create_tri_parametric_color_ramp_node(group)
        ao_node.inputs["Color1"].default_value = (1.0, 1.0, 1.0, 1.0)
        ao_node.inputs["Color2"].default_value = (0.0, 0.0, 0.0, 1.0)
        ao_node.inputs["Color3"].default_value = (1.0, 1.0, 1.0, 1.0)
        group.links.new(peeling_noise_node.outputs["Fac"], ao_node.inputs["Fac"])
        group.links.new(fallout_subtract_node.outputs["Value"], ao_node.inputs["Pos1"])
        group.links.new(input_node.outputs["Threshold"], ao_node.inputs["Pos2"])
        group.links.new(epsilon_add_node.outputs["Value"], ao_node.inputs["Pos3"])
        ao_mix_node = group.nodes.new(type="ShaderNodeMixRGB")
        ao_mix_node.blend_type = "MULTIPLY"
        ao_mix_node.inputs["Fac"].default_value = 1.0
        group.links.new(color_mix_node.outputs["Color"], ao_mix_node.inputs[1])
        group.links.new(ao_node.outputs["Color"], ao_mix_node.inputs[2])
        # Metallic
        metallic_node = group.nodes.new(type="ShaderNodeMixRGB")
        metallic_node.inputs["Color1"].default_value = (1.0, 1.0, 1.0, 1.0)
        metallic_node.inputs["Color2"].default_value = (0.0, 0.0, 0.0, 1.0)
        group.links.new(peeling_threshold_node.outputs["Color"], metallic_node.inputs["Fac"])
        # Roughness
        roughness_node = group.nodes.new(type="ShaderNodeMixRGB")
        roughness_node.inputs["Color1"].default_value = (0.50, 0.50, 0.50, 1.0)
        roughness_node.inputs["Color2"].default_value = (0.05, 0.05, 0.05, 1.0)
        group.links.new(peeling_threshold_node.outputs["Color"], roughness_node.inputs["Fac"])
        # Bump
        height_node = self.create_tri_parametric_color_ramp_node(group)
        height_node.inputs["Color1"].default_value = (0.0, 0.0, 0.0, 1.0)
        height_node.inputs["Color2"].default_value = (1.0, 1.0, 1.0, 1.0)
        height_node.inputs["Color3"].default_value = (0.5, 0.5, 0.5, 1.0)
        height_peak_add_node = group.nodes.new(type="ShaderNodeMath")
        height_peak_add_node.operation = "ADD"
        height_peak_add_node.inputs[1].default_value = 0.005
        height_tail_add_node = group.nodes.new(type="ShaderNodeMath")
        height_tail_add_node.operation = "ADD"
        height_tail_add_node.inputs[1].default_value = 0.025
        group.links.new(input_node.outputs["Threshold"], height_peak_add_node.inputs[0])
        group.links.new(input_node.outputs["Threshold"], height_tail_add_node.inputs[0])
        group.links.new(peeling_noise_node.outputs["Fac"], height_node.inputs["Fac"])
        group.links.new(input_node.outputs["Threshold"], height_node.inputs["Pos1"])
        group.links.new(height_peak_add_node.outputs["Value"], height_node.inputs["Pos2"])
        group.links.new(height_tail_add_node.outputs["Value"], height_node.inputs["Pos3"])
        bump_node = group.nodes.new(type="ShaderNodeBump")
        group.links.new(height_node.outputs["Color"], bump_node.inputs["Height"])
        # Output
        output_node = group.nodes.new("NodeGroupOutput")
        group.outputs.new("NodeSocketColor", "Color")
        group.outputs.new("NodeSocketColor", "Metallic")
        group.outputs.new("NodeSocketColor", "Roughness")
        group.outputs.new("NodeSocketVectorDirection", "Bump")
        group.links.new(ao_mix_node.outputs["Color"], output_node.inputs["Color"])
        group.links.new(metallic_node.outputs["Color"], output_node.inputs["Metallic"])
        group.links.new(roughness_node.outputs["Color"], output_node.inputs["Roughness"])
        group.links.new(bump_node.outputs["Normal"], output_node.inputs["Bump"])
        return group

    def CreatePeelingPaint(self):
        mat = bpy.data.materials.new('Material Peeling Paint')
        mat.use_nodes = True
        # clean nodes
        for node in mat.node_tree.nodes:
            mat.node_tree.nodes.remove(node)
        # build nodes
        node_tree = mat.node_tree
        output_node = node_tree.nodes.new(type='ShaderNodeOutputMaterial')
        principled_node = node_tree.nodes.new(type='ShaderNodeBsdfPrincipled')
        peeling_paint_metal_node = self.create_peeling_paint_metal_node_group(node_tree)

        node_tree.links.new(peeling_paint_metal_node.outputs['Color'], principled_node.inputs['Base Color'])
        node_tree.links.new(peeling_paint_metal_node.outputs['Metallic'], principled_node.inputs['Metallic'])
        node_tree.links.new(peeling_paint_metal_node.outputs['Roughness'], principled_node.inputs['Roughness'])
        node_tree.links.new(peeling_paint_metal_node.outputs['Bump'], principled_node.inputs['Normal'])
        node_tree.links.new(principled_node.outputs['BSDF'], output_node.inputs['Surface'])
        return mat

    def CreatePaint(self):
        mat = bpy.data.materials.new('Material Paint')
        mat.use_nodes = True
        # build nodes
        bsdf_node = mat.node_tree.nodes['Principled BSDF']
        bsdf_node.inputs['Base Color'].default_value = (0.152, 0.524, 0.067, 1.0)
        bsdf_node.inputs['Metallic'].default_value = 0.0
        bsdf_node.inputs['Specular'].default_value = 0.5
        bsdf_node.inputs['Roughness'].default_value = 0.05
        return mat

    def CreateGold(self):
        mat = bpy.data.materials.new('Mateiral Gold')
        mat.use_nodes = True
        bsdf_node = mat.node_tree.nodes['Principled BSDF']
        bsdf_node.inputs['Base Color'].default_value = (1.00, 0.71, 0.22, 1.0)
        bsdf_node.inputs['Metallic'].default_value = 1.0
        bsdf_node.inputs['Specular'].default_value = 0.5
        bsdf_node.inputs['Roughness'].default_value = 0.1
        return mat

    def CreateGlass(self):
        mat = bpy.data.materials.new('Mateiral Glass')
        mat.use_nodes = True
        principled_node = mat.node_tree.nodes['Principled BSDF']
        principled_node.inputs['Base Color'].default_value = (0.95, 0.95, 0.95, 1.0)
        principled_node.inputs['Metallic'].default_value = 0.0
        principled_node.inputs['Specular'].default_value = 0.5
        principled_node.inputs['Roughness'].default_value = 0.0
        principled_node.inputs['Clearcoat'].default_value = 0.5
        principled_node.inputs['Clearcoat Roughness'].default_value = 0.030
        principled_node.inputs['IOR'].default_value = 1.45
        principled_node.inputs['Transmission'].default_value = 0.98
        return mat

    def CreateCeramic(self):
        mat = bpy.data.materials.new('Mateiral Glass')
        mat.use_nodes = True
        principled_node = mat.node_tree.nodes['Principled BSDF']
        principled_node.inputs['Base Color'].default_value = (0.8, 0.8, 0.8, 1.0)
        principled_node.inputs['Subsurface'].default_value = 0.1
        principled_node.inputs['Subsurface Color'].default_value = (0.9, 0.9, 0.9, 1.0)
        principled_node.inputs['Subsurface Radius'].default_value = (1.0, 1.0, 1.0)
        principled_node.inputs['Metallic'].default_value = 0.2
        principled_node.inputs['Specular'].default_value = 0.5
        principled_node.inputs['Roughness'].default_value = 0.0
        return mat

    def CreateRoughBlue(self):
        mat = bpy.data.materials.new('Mateiral Glass')
        mat.use_nodes = True
        principled_node = mat.node_tree.nodes['Principled BSDF']
        principled_node.inputs['Base Color'].default_value = (0.1, 0.2, 0.6, 1.0)
        principled_node.inputs['Metallic'].default_value = 0.5
        principled_node.inputs['Specular'].default_value = 0.5
        principled_node.inputs['Roughness'].default_value = 0.9
        return mat

    def CreateFromName(self, name):
        self.material_name = name
        loader.build_pbr_textured_nodes_from_name(self.material_name)
        mat = bpy.data.materials[self.material_name]
        return mat

    def CreateFromFile(self):
        path = os.getcwd()
        path = os.path.dirname(path)
        path = os.path.dirname(path)
        path = os.path.dirname(path)
        filename = path + "/Data/Materials/" + self.material_filename
        with bpy.data.libraries.load(filename, link=False) as (src, dst):
            dst.materials = src.materials
        return dst.materials[0]


