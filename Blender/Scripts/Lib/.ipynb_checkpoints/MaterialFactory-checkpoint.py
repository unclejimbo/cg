import bpy
import json
import math
import mathutils
import os


class MaterialFactory:
    def hex2rgba(self, h):
        b = (h & 0xFF) / 255.0
        g = ((h >> 8) & 0xFF) / 255.0
        r = ((h >> 16) & 0xFF) / 255.0
        return r, g, b, 1.0

    def CreateMainMaterial(self, texture_path, roughness=0.0, specular=0.0):
        mat = bpy.data.materials.new('Main')
        mat.use_nodes = True
        img_node = mat.node_tree.nodes.new(type='ShaderNodeTexImage')
        img_node.image = bpy.data.images.load(filepath=texture_path)
        bsdf_node = mat.node_tree.nodes['Principled BSDF']
        bsdf_node.inputs['Roughness'].default_value = roughness
        bsdf_node.inputs['Specular'].default_value = specular
        mat.node_tree.links.new(
            img_node.outputs['Color'], bsdf_node.inputs['Base Color'])
        return mat

    def CreateColoredMaterial(self, name, color):
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
        bsdf_node = mat.node_tree.nodes['Principled BSDF']
        mat.node_tree.nodes.remove(bsdf_node)
        color_node = mat.node_tree.nodes.new(type='ShaderNodeRGB')
        color_node.outputs[0].default_value = self.hex2rgba(color)
        output_node = mat.node_tree.nodes['Material Output']
        mat.node_tree.links.new(
            color_node.outputs['Color'], output_node.inputs['Surface'])
        return mat


