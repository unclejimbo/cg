import TextureBasic
from TextureBasic import *

class TextureCurvature(TextureBasic):

	def __init__(self):
		super(TextureCurvature, self).__init__()

		# 'mean' or 'gaussian'
		self.curvature = 'mean'

		# A scale factor to bring curvature value into the displayable range [-1, 1]
		# Everything outside of this range will be clamped
		self.scale = 1.0 

	def SetScale(self, scale):
		self.scale = scale

	def SetCurvature(self, curvature):
		self.curvature = curvature

	def Setup(self):
		textureProps = Properties('curvature')
		textureProps['curvature'] = self.curvature
		textureProps['scale'] = self.scale
		
		self.texture = self.pmgr.createObject(textureProps)

		self.texture.configure()