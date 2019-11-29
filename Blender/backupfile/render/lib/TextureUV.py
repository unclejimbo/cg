import TextureBasic
from TextureBasic import *

class TextureUV(TextureBasic):

	def __init__(self):
		super(TextureUV, self).__init__()

		self.dirBitmap = None
		self.uoffset = 0.0
		self.voffset = 0.0
		self.uscale = 1.0
		self.vscale = 1.0
		self.wrapMode = 'repeat'
		self.cache = False
		self.channel = None

	def SetDirBitmap(self, dirBitmap):
		self.dirBitmap = dirBitmap

	def SetUoffset(self, uoffset):
		self.uoffset = uoffset

	def SetVoffset(self, voffset):
		self.voffset = voffset

	def SetUscale(self, uscale):
		self.uscale = uscale

	def SetVscale(self, vscale):
		self.vscale = vscale

	def SetWrapMode(self, wrapMode):
		self.wrapMode = wrapMode
	
	def SetChannel(self, channel):
		self.channel = channel

	def Setup(self):
		textureProps = Properties('bitmap')
		textureProps['filename'] = self.dirBitmap
		textureProps['uoffset'] = self.uoffset
		textureProps['voffset'] = self.voffset
		textureProps['uscale'] = self.uscale
		textureProps['vscale'] = self.vscale
		textureProps['wrapMode'] = self.wrapMode
		textureProps['cache'] = self.cache

		if self.channel != None:
			textureProps['channel'] = self.channel

		print(textureProps)

		self.texture = self.pmgr.createObject(textureProps)
		self.texture.configure()