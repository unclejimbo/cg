import sys
sys.path.append('..\\lib')
sys.path.append('..\\SceneTask')

from DirSetting import *

from Tool.IO import *
from Tool.FfmpegWrapper import *

def ProduceVideo_PNG(inputPath, outputPath):
	### ProduceVideo ###
	video = VideoInfo()

	video.SetInputDir(inputPath)
	video.SetInputFileFormat( "\\" + "huizhao_%03d.png")
	video.SetStarFrame("0")
	video.SetOutputDir(outputPath)
	video.SetFps("30")
	video.SetQuality("35")
	video.SetVideoName("huizhao" + "_PNG_fps30")

	ffProcess = Ffmpeg()
	ffProcess.SetFfmpeg("..\\lib\\ThirdPartyExe\\ffmpeg.exe")
	ffProcess.Run('produceVideo', video)

def ProduceVideo_JPG(inputPath, outputPath):
	### ProduceVideo ###
	video = VideoInfo()

	video.SetInputDir(inputPath)
	video.SetInputFileFormat( "\\" + "image_%03d.jpg")
	video.SetStarFrame("0")
	video.SetOutputDir(outputPath)
	video.SetFps("1")
	video.SetQuality("35")
	video.SetVideoName("Torus_3Duv" + "_JPG")

	ffProcess = Ffmpeg()
	ffProcess.SetFfmpeg("..\\lib\\ThirdPartyExe\\ffmpeg.exe")
	ffProcess.Run('produceVideo', video)

ProduceVideo_PNG(	'C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\face\\crop',
					'C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\face\\crop'
			)

# ProduceVideo_JPG(	'C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\face\\PLY_VertexColors',
# 					'C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\face\\PLY_VertexColors'
# 			)