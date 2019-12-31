import os
from Tool.IO import *

class VideoInfo(object):
	

	"""docstring for VideoInfor"""
	fps = '20'                             #used as -r
	outputFormat = '.mp4'				   
	pixelFormat = 'yuv420p'                #used as -pix_fmt
	resolution = '4000x2000'			   #used as -s
	startFrame = '1'                       #used as -start_number
	endFrame = '10000'         			   #used as -vframes
	quality = '15'						   #used as -crf
	encoder = 'libx264'					   #used as -vcodec
	forcedFormat = 'image2'				   #used as -f
	outputDir = '.\\'                      
	inputDir = '.\\'                       #used as -i
	inputFileFormat = '%04d.jpg'
	videoName = 'result'

	def __init__(self):
		pass
	def SetFps(self, fps):
		self.fps = fps
	def SetOutputFormat(self, outputFormat):
		self.outputFormat = outputFormat
	def SetPixelFormat(self, pixelFormat):
		self.pixelFormat = pixelFormat
	def SetResolution(self, resolution):
		self.resolution = resolution
	def SetStarFrame(self, startFrame):
		self.startFrame = startFrame
	def SetEndFrame(self, endFrame):
		self.endFrame = endFrame
	def SetQuality(self, quality):
		self.quality = quality
	def SetEncoder(self, encoder):
		self.encoder =encoder
	def SetForcedFormat(self, forcedFormat):
		self.forcedFormat = forcedFormat
	def SetOutputDir(self, outputDir):
		self.outputDir = outputDir
	def SetInputDir(self, inputDir):
		self.inputDir = inputDir
	def SetInputFileFormat(self, inputFileFormat):
		self.inputFileFormat = inputFileFormat
	def SetVideoName(self, videoName):
		self.videoName = videoName
	def SetAddition(self, add):
		self.add = add


class Ffmpeg(object):

	ffmpeg = '..\\..\\lib\\ThirdPartyExe\\ffmpeg.exe'
	videoInfo = VideoInfo()

	def __init__(self):
		pass

	def SetFfmpeg(self, ffmpeg):
		self.ffmpeg = ffmpeg

	def ProduceVideo(self, videoInfo):
		self.videoInfo = videoInfo
		print(self.ffmpeg)
		os.system(self.ffmpeg 
			+ ' -r ' 
			+ self.videoInfo.fps 
			#+ ' -f ' + self.videoInfo.forcedFormat 
			+ ' -s ' + self.videoInfo.resolution
			+ ' -start_number ' + self.videoInfo.startFrame
			+ ' -i ' + self.videoInfo.inputDir
			+ self.videoInfo.inputFileFormat
			+ ' -vframes ' + self.videoInfo.endFrame
			# + self.videoInfo.add
			+ ' -codec ' + self.videoInfo.encoder
			# + ' -crf ' + self.videoInfo.quality
			+ ' -pix_fmt ' + self.videoInfo.pixelFormat
			+ ' ' + self.videoInfo.outputDir + '\\'
			+ self.videoInfo.videoName
			+ self.videoInfo.outputFormat)

	def Run(self, cmd, videoInfo = ''):
		if(cmd == 'produceVideo'):
			self.ProduceVideo(videoInfo)