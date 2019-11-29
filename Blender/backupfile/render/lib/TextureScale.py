import TextureBasic
from TextureBasic import *

class TextureScale(TextureBasic):

	def __init__(self):
		super(TextureScale, self).__init__()

		self.scale = 1.0
		self.scaledTexture = None

	def SetScale(self, scale):
		self.scale = scale

	def SetScaledTexture(self, texture):
		self.scaledTexture = texture.GetTexture()

	def Setup(self):
		textureProps = Properties('scale')
		textureProps['scale'] = self.scale

		self.texture = self.pmgr.createObject(textureProps)

		if self.scaledTexture != None:
			self.texture.addChild('scaledTexture', self.scaledTexture)

		self.texture.configure()