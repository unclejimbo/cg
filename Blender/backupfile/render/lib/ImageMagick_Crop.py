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

magick.Run(	"cropFolder", 
			"C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\face\\crop", 
			"1500x1500+0+0"
			)