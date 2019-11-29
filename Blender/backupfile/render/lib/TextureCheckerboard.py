import TextureBasic
from TextureBasic import *

class TextureCheckerboard(TextureBasic):

	def __init__(self):
		super(TextureCheckerboard, self).__init__()

		self.color0 = Spectrum(0.4)
		self.color1 = Spectrum(0.2)

		self.uoffset = 1.0
		self.voffset = 1.0
		self.uscale = 1.0
		self.vscale = 1.0

	def SetColor0(self, color0):
		self.color0 = color0

	def SetColor1(self, color1):
		self.color1 = color1

	def SetUscale(self, uscale):
		self.uscale = uscale

	def SetVscale(self, vscale):
		self.vscale = vscale

	def SetUoffset(self, uoffset):
		self.uoffset = uoffset

	def SetVoffset(self, voffset):
		self.voffset = voffset

	def Setup(self):
		textureProps = Properties('checkerboard')
		textureProps['color0'] = self.color0
		textureProps['color1'] = self.color1
		textureProps['uoffset'] = self.uoffset
		textureProps['voffset'] = self.voffset
		textureProps['uscale'] = self.uscale
		textureProps['vscale'] = self.vscale

		self.texture = self.pmgr.createObject(textureProps)
		
		self.texture.configure()