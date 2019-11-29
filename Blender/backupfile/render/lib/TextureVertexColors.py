import TextureBasic
from TextureBasic import *

class TextureVertexColors(TextureBasic):

	def __init__(self):
		super(TextureVertexColors, self).__init__()

	def Setup(self):
		textureProps = Properties('vertexcolors')
		self.texture= self.pmgr.createObject(textureProps)
		self.texture.configure()