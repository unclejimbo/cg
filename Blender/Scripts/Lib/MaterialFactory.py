import bpy
import os
import cc0assetsloader as loader


class MaterialFactory:
    def __init__(self, config):
        self.config = config

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

    def create_bsdf(self, color_mode, render_style):
        mat = bpy.data.materials.new('Main')
        mat.use_nodes = True

        bsdf_node = mat.node_tree.nodes['Principled BSDF']
        bsdf_node.inputs['Roughness'].default_value = self.config.roughness
        bsdf_node.inputs['Specular'].default_value = self.config.specular
        bsdf_node.inputs['Sheen'].default_value = self.config.sheen
        bsdf_node.inputs['Clearcoat'].default_value = self.config.clearcoat

        output_node = mat.node_tree.nodes['Material Output']

        if color_mode == 'texture':
            img_node = mat.node_tree.nodes.new(type='ShaderNodeTexImage')
            img_node.image = bpy.data.images.load(
                filepath=self.config.texture_path)
            texcoord_node = mat.node_tree.nodes.new(type='ShaderNodeTexCoord')
            mutiply_node = mat.node_tree.nodes.new(type='ShaderNodeVectorMath')
            mutiply_node.operation = 'MULTIPLY'
            mutiply_node.inputs[1].default_value[0] = self.config.uv_multiply[0]
            mutiply_node.inputs[1].default_value[1] = self.config.uv_multiply[1]
            add_node = mat.node_tree.nodes.new(type='ShaderNodeVectorMath')
            add_node.operation = 'ADD'
            add_node.inputs[1].default_value[0] = self.config.uv_add[0]
            add_node.inputs[1].default_value[1] = self.config.uv_add[1]
            mat.node_tree.links.new(
                texcoord_node.outputs['UV'], mutiply_node.inputs[0])
            mat.node_tree.links.new(
                mutiply_node.outputs['Vector'], add_node.inputs[0])
            mat.node_tree.links.new(
                add_node.outputs['Vector'], img_node.inputs['Vector'])
            mat.node_tree.links.new(
                img_node.outputs['Color'], bsdf_node.inputs['Base Color'])
        elif color_mode == 'vcolor':
            vertex_color_node = mat.node_tree.nodes.new(
                type='ShaderNodeVertexColor')
            vertex_color_node.layer_name = 'Col'
            mat.node_tree.links.new(
                vertex_color_node.outputs['Color'], bsdf_node.inputs['Base Color'])
        else:
            rgb_node = mat.node_tree.nodes.new(type='ShaderNodeRGB')
            rgb_node.outputs['Color'].default_value = self.hex2rgba(
                self.config.base_color)
            mat.node_tree.links.new(
                rgb_node.outputs['Color'], bsdf_node.inputs['Base Color'])

        if render_style == 'wireframe':
            wire_node = mat.node_tree.nodes.new(type='ShaderNodeWireframe')
            size = wire_node.inputs['Size'].default_value
            wire_node.inputs['Size'].default_value = size * \
                self.config.wireframe_size
            wire_mat_node = mat.node_tree.nodes.new(
                type='ShaderNodeBsdfDiffuse')
            wire_color_node = mat.node_tree.nodes.new(type='ShaderNodeRGB')
            wire_color_node.outputs['Color'].default_value = self.hex2rgba(
                self.config.wireframe_color)
            mix_node = mat.node_tree.nodes.new(type='ShaderNodeMixShader')
            mat.node_tree.links.new(
                bsdf_node.outputs['BSDF'], mix_node.inputs[1])
            mat.node_tree.links.new(
                wire_color_node.outputs['Color'], wire_mat_node.inputs['Color'])
            mat.node_tree.links.new(
                wire_mat_node.outputs['BSDF'], mix_node.inputs[2])
            mat.node_tree.links.new(
                wire_node.outputs['Fac'], mix_node.inputs['Fac'])
            mat.node_tree.links.new(
                mix_node.outputs['Shader'], output_node.inputs['Surface'])
        elif render_style == 'transparent':
            trans_node = mat.node_tree.nodes.new(
                type='ShaderNodeBsdfTransparent')
            mix_node = mat.node_tree.nodes.new(type='ShaderNodeMixShader')
            mix_node.inputs['Fac'].default_value = self.config.alpha
            mat.node_tree.links.new(
                bsdf_node.outputs['BSDF'], mix_node.inputs[1])
            mat.node_tree.links.new(
                trans_node.outputs['BSDF'], mix_node.inputs[2])
            mat.node_tree.links.new(
                mix_node.outputs['Shader'], output_node.inputs['Surface'])
            mat.blend_method = 'HASHED'
            mat.shadow_method = 'HASHED'

        return mat

    def create_from_name(self, name):
        loader.build_pbr_textured_nodes_from_name(name)
        mat = bpy.data.materials[name]
        return mat

    def create_from_file(self, name):
        path = os.getcwd()
        path = os.path.dirname(path)
        path = os.path.dirname(path)
        path = os.path.dirname(path)
        filename = path + "/Data/Materials/" + name
        with bpy.data.libraries.load(filename, link=False) as (src, dst):
            dst.materials = src.materials

        if name == '99-porcelain-texture.blend' or name == 'Knittr.blend':
            mat = dst.materials[2]
            mat.node_tree.nodes['Image Texture'].image = bpy.data.images.load(
                filepath=self.config.texture_path)
            mat.node_tree.nodes['Vector Math'].inputs[1].default_value[0] = self.config.uv_add[0]
            mat.node_tree.nodes['Vector Math'].inputs[1].default_value[1] = self.config.uv_add[1]
            mat.node_tree.nodes['Vector Math.001'].inputs[1].default_value[0] = self.config.uv_multiply[0]
            mat.node_tree.nodes['Vector Math.001'].inputs[1].default_value[1] = self.config.uv_multiply[1]
            return mat
        else:
            return dst.materials[0]
