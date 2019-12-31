import TextureBasic
from TextureBasic import *

class TextureWireframe(TextureBasic):

	def __init__(self):
		super(TextureWireframe, self).__init__()

		self.lineWidth = 0.0005
		self.interiorColor = Spectrum(0.95)
		self.edgeColor = Spectrum(0.3)

	def SetLineWidth(self, lineWidth):
		self.lineWidth = lineWidth

	def SetInteriorColorSpectrum(self, spectrum):
		self.interiorColor = spectrum

	def SetInteriorColorName(self, color):
		self.interiorColor = Spectrum([color[0]/255.0, color[1]/255.0, color[2]/255.0])
	
	def SetInteriorColorRGB(self, r, g, b):
		self.interiorColor = Spectrum([r/255.0, g/255.0, b/255.0])

	def SetEdgeColorSpectrum(self, spectrum):
		self.edgeColor = spectrum

	def SetEdgeColorName(self, color):
		self.edgeColor = Spectrum([color[0]/255.0, color[1]/255.0, color[2]/255.0])
	
	def SetEdgeColorRGB(self, r, g, b):
		self.edgeColor = Spectrum([r/255.0, g/255.0, b/255.0])
	
	def Setup(self):
		textureProps = Properties('wireframe')
		textureProps['lineWidth'] = self.lineWidth
		textureProps['interiorColor'] = self.interiorColor
		textureProps['edgeColor'] = self.edgeColor
		self.texture = self.pmgr.createObject(textureProps)
		self.texture.configure()