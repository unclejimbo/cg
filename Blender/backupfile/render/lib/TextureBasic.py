from mitsuba.core import *

class TextureBasic(object):

	def __init__(self):
		super(TextureBasic, self).__init__()

		# Mitsuba Plugin Manager
		self.pmgr = PluginManager.getInstance()

	def GetTexture(self):
		return self.texture

