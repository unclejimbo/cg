import os
from Tool.IO import *

class Annotation(object):
	
	def __init__(self):
		self.backgroundColor = 'None'
		self.fontColor = 'white'
		self.gravity = 'center'
		self.size = '450x100'
		self.annotation = 'Annotation'
		self.geometry = '+0+100'

	def SetBackgroundColor(self, backgroundColor):
		self.backgroundColor = backgroundColor
	def SetFontColor(self, fontColor):
		self.fontColor = fontColor
	def SetGravity(self, gravity):
		self.gravity = gravity
	def SetSize(self, size):
		self.size = size
	def SetGeometry(self, geometry):
		self.geometry = geometry
	def SetAnnotation(self, annotation):
		self.annotation = annotation

class Label(object):
	def __init__(self):
		self.backgroundColor = 'None'
		self.fontColor = 'Red'
		self.font = 'Arial'
		self.pointsize = '74'
		self.gravity = 'Center'
		self.label = 'Label'

	def SetBackgroundColor(self, backgroundColor):
		self.backgroundColor = backgroundColor
	def SetFontColor(self, fontColor):
		self.fontColor = fontColor
	def SetFront(self, font):
		self.font = font
	def SetPointSize(self, pointsize):
		self.pointsize = pointsize	
	def SetGravity(self, gravity):
		self.gravity = gravity
	def SetLabel(self, label):
		self.label = label

class ImageMagick(object):

	def __init__(self):
		self.magick = '..\\ThirdPartyExe\\ImageMagick\\magick.exe'
		self.annotationInfo = None
		self.labelInfo = None

	def SetMagick(self, magick):
		self.magick = magick

	def TrimFile(self, inputImg):
		print("Trim File: " + inputImg)
		os.system(self.magick + ' ' + inputImg +' -trim ' + inputImg)

	def TrimFolder(self, inputFolder):
		list_dirs = os.walk(inputFolder)
		for root, dirs, files in list_dirs:     
			for f in files: 
				self.TrimFile(os.path.join(root, f))

	def CropFile(self, inputImg, size):
		print("Crop File: " + inputImg + " To " + size)
		os.system(self.magick + ' ' + 'convert' + ' ' + inputImg + ' ' + '-gravity center -crop' + ' ' + size + ' ' + inputImg)

	def CropFolder(self, inputFolder, size):
		list_dirs = os.walk(inputFolder)
		for root, dirs, files in list_dirs:     
			for f in files: 
				self.CropFile(os.path.join(root, f), size)

	def AddAnnotation(self, inputImg, outputImg, annotationInfo):
		self.annotationInfo = annotationInfo
		os.system(	self.magick
					+ ' -background ' + self.annotationInfo.backgroundColor
					+ ' -fill ' + self.annotationInfo.fontColor
					+ ' -gravity '+ self.annotationInfo.gravity
					+ ' -size ' + self.annotationInfo.size
					+ ' caption:"'
					+ self.annotationInfo.annotation
					+ ' " '
					+ inputImg
					+ ' +swap -gravity south'
					+ ' -geometry ' + self.annotationInfo.geometry
					+ ' -composite '
					+ outputImg)
		
	def AddLabel(self, inputImg, outputImg, labelInfo):
		self.labelInfo = labelInfo
		# print(	self.magick
		# 			+ ' '
		# 			+ inputImg
		# 			+ ' -background ' + self.labelInfo.backgroundColor
		# 			+ ' -font ' + self.labelInfo.font
		# 			+ ' -fill ' + self.labelInfo.fontColor
		# 			+ ' -pointsize '+ self.labelInfo.pointsize
		# 			+ ' label:"'
		# 			+ self.labelInfo.label
		# 			+ ' " '
		# 			+ ' -gravity '+ self.labelInfo.gravity
		# 			+ ' -append '
		# 			+ outputImg)
		print("Add Label" + " \"" + labelInfo.label + "\" " + ": " + inputImg)
		os.system(	self.magick
					+ ' '
					+ inputImg
					+ ' -background ' + self.labelInfo.backgroundColor
					+ ' -font ' + self.labelInfo.font
					+ ' -fill ' + self.labelInfo.fontColor
					+ ' -pointsize '+ self.labelInfo.pointsize
					+ ' label:"'
					+ self.labelInfo.label
					+ ' " '
					+ ' -gravity '+ self.labelInfo.gravity
					+ ' -append '
					+ outputImg)


	def AddLabelFolder(self, inputFolder, outputFolder, labelInfo):
		list_dirs = os.walk(inputFolder)
		for root, dirs, files in list_dirs:     
			for f in files:
				self.AddLabel(os.path.join(root, f), outputFolder + '\\' + f, labelInfo)

	def Append(self, inputImg1, inputImg2, outputImg, append):
		print("Append: " + os.path.basename(inputImg1) + " ---- " + os.path.basename(inputImg2) + " To: " + os.path.basename(outputImg))
		os.system(self.magick + ' ' + inputImg1 + ' '+ inputImg2 + ' ' + append + ' ' + outputImg)
	
	def AppendThree(self, inputImg1, inputImg2, inputImg3, outputImg, append):
		print("Append: " + os.path.basename(inputImg1) + " ---- " + os.path.basename(inputImg2) + " ---- " + os.path.basename(inputImg3) +" To: " + os.path.basename(outputImg))
		os.system(self.magick + ' ' + inputImg1 + ' '+ inputImg2 +  ' '+ inputImg3 +' ' + append + ' ' + outputImg)

	def AppendFolder(self, inputFolder1, inputFolder2, outputFolder, append):
		list_dirs1 = os.walk(inputFolder1)
		list_dirs2 = os.walk(inputFolder2)
		filePath1 = []
		filePath2 = []

		for root, dirs, files in list_dirs1:
			for f in files:
				filePath1.append(os.path.join(root, f))

		for root, dirs, files in list_dirs2:
			for f in files:
				filePath2.append(os.path.join(root, f))
		i = 0
		for inputImg1, inputImg2 in zip(filePath1, filePath2):
			i = i + 1
			self.Append(inputImg1, inputImg2, outputFolder + '\\' + 'image_%03i' % (i) + '.' + os.path.basename(inputImg1).split('.')[-1], append)

	def AppendThreeFolder(self, inputFolder1, inputFolder2, inputFolder3, outputFolder, append):
		list_dirs1 = os.walk(inputFolder1)
		list_dirs2 = os.walk(inputFolder2)
		list_dirs3 = os.walk(inputFolder3)
		filePath1 = []
		filePath2 = []
		filePath3 = []

		for root, dirs, files in list_dirs1:
			for f in files:
				filePath1.append(os.path.join(root, f))

		for root, dirs, files in list_dirs2:
			for f in files:
				filePath2.append(os.path.join(root, f))

		for root, dirs, files in list_dirs3:
			for f in files:
				filePath3.append(os.path.join(root, f))

		i = 0
		for inputImg1, inputImg2, inputImg3 in zip(filePath1, filePath2, filePath3):
			i = i + 1
			self.AppendThree(inputImg1, inputImg2, inputImg3, outputFolder + '\\' + 'image_%03i' % (i) + '.' + os.path.basename(inputImg1).split('.')[-1], append)

	def ConvertToJpg(self, inputImg):
		print("Convert To JPG: " + inputImg)
		os.system(self.magick + ' convert' + ' ' + inputImg + ' ' + '-background white -flatten' + ' ' + inputImg.split(".")[0] + ".jpg")

	def Convert2Jpg(self, inputImg, pathJPG):
		jpgFile=pathJPG +'\\' +  "".join(os.path.basename(inputImg).split(".")[:-1]) + ".jpg"
		
		cmd=self.magick + ' convert' + ' ' + inputImg + ' ' + '-background white -flatten' + ' ' + jpgFile
		print(cmd)
		os.system(cmd)


	def Convert16BitTo8Bit(self, inputImg, outputImg):
		os.system(self.magick + ' ' + inputImg + ' -evaluate multiply 16 -depth 8 ' + outputImg)

	def ConverToWhiteBG(self, inputImg, outputImg):
		os.system(self.magick + ' convert' + ' ' + inputImg + ' ' + '-background white -flatten' + ' ' + outputImg)

	def ConverToWhiteBGFolder(self, inputFolder, outputFolder):
		list_dirs = os.walk(inputFolder)
		for root, dirs, files in list_dirs:     
			for f in files:
				self.ConverToWhiteBG(os.path.join(root, f), outputFolder + '\\' + f)

	def Run(self, cmd, img1 = '', img2 = '', img3 = '', img4 = ''):
		if(cmd == 'trimFile'):
			self.TrimFile(img1)
		
		if(cmd == 'trimFolder'):
			self.TrimFolder(img1)

		if(cmd == 'cropFile'):
			self.CropFile(img1, img2)
		
		if(cmd == 'cropFolder'):
			self.CropFolder(img1, img2)

		if(cmd == 'convertToJPG'):
			self.ConvertToJpg(img1)
		
		if(cmd == '16BitTo8Bit'):
			self.Convert16BitTo8Bit(img1, img2)

		if(cmd == 'whiteBackground'):
			self.ConverToWhiteBG(img1, img2)

		if(cmd == 'whiteBackgroundFolder'):
			self.ConverToWhiteBGFolder(img1, img2)

		if(cmd == '+append'):
			self.Append(img1, img2, img3, '+append')
		
		if(cmd == '+appendFolder'):
			self.AppendFolder(img1, img2, img3, '+append')
		
		if(cmd == '+appendThreeFolder'):
			self.AppendThreeFolder(img1, img2, img3, img4, '+append')
		
		if(cmd == '-append'):
			self.Append(img1, img2, img3, '-append')
		
		if(cmd == '-appendFolder'):
			self.AppendFolder(img1, img2, img3, '-append')
		
		if(cmd == 'annotate'):
			self.AddAnnotation(img1, img2, img3)
		
		if(cmd == 'label'):
			self.AddLabel(img1, img2, img3)
		
		if(cmd == 'addLabelFolder'):
			self.AddLabelFolder(img1, img2, img3)
