import os
import sys
sys.path.append('..\\SceneTask')
sys.path.append('..\\lib')

from DirSetting import *

from Tool.IO import *
from Tool.PrettyColor import *
from Tool.FfmpegWrapper import *
from Tool.ImageMagickWrapper import	*

fileRootPath = "C:\\Users\\soapk\\Desktop\\PIC"
imagePathList = ReadFilesDeep(fileRootPath)

magick = ImageMagick()
magick.SetMagick("..\\lib\\ThirdPartyExe\\magick.exe")

for item in imagePathList:
	magick.Run("trimFile",
				item
				)