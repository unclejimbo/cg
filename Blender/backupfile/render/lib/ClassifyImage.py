import os 
import shutil
import sys
sys.path.append('..\\SceneTask')
sys.path.append('..\\lib')

from Tool.IO import *

def ClassifyImage(filePath):
	imageList = ReadFilesDeep(filePath)

	folderPathCalabi = filePath + "\\RenderResult\\calabi"
	folderPathCetm = filePath + "\\RenderResult\\cetm"
	folderPathRicci = filePath + "\\RenderResult\\ricci"

	CreatePath(folderPathCalabi)
	CreatePath(folderPathCetm)
	CreatePath(folderPathRicci)

	for image in imageList:
		if "calabi" in image:
			shutil.copy2(image, folderPathCalabi)
		if "cetm" in image:
			shutil.copy2(image, folderPathCetm)
		if "ricci" in image:
			shutil.copy2(image, folderPathRicci)

filePath = "C:\\Users\\soapk\\Desktop\\NoTrimVersion\\Checkboard\\JPG\\texture1\\Euclidean\\"
folderList = ReadFiles(filePath)

print(folderList)

for item in folderList:
	for i in range(2):
		if i == 0:
			ClassifyImage(item + "\\3Duv")
		if i == 1:
			ClassifyImage(item + "\\flatuv")
