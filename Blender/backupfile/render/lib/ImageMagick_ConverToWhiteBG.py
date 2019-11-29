import sys
sys.path.append('..\\SceneTask')
sys.path.append('..\\lib')

from DirSetting import *

from Tool.IO import *
from Tool.PrettyColor import *
from Tool.FfmpegWrapper import *
from Tool.ImageMagickWrapper import	*

magick = ImageMagick()
magick.SetMagick("..\\lib\\ThirdPartyExe\\magick.exe")

imageFolder = ReadFiles("C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\sphere\\RenderResult\\")
outputFolder = ReadFiles("C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\sphere\\RenderResult_White\\")

for itemI, itemO in zip(imageFolder, outputFolder):
	magick.Run(	"whiteBackgroundFolder",
				itemI,
				itemO
				)