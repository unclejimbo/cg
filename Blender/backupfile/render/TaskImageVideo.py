import sys
sys.path.append('..\\')
sys.path.append('..\\..\\lib')

from DirSetting import *

from Tool.IO import *
from Tool.PrettyColor import *
from Tool.FfmpegWrapper import *
from Tool.ImageMagickWrapper import	*

 

class TaskImageVideo(object):	
	def __init__(self):
		super(TaskImageVideo, self).__init__()
		
		self.PathInput =  '.\\png'
		self.PathOutput=  '.\\jpg'
		self.magickPath=('I:\\togpic\\Mitsuba\\Python\\lib\\ThirdPartyExe\\ImageMagick\\magick.exe')
		self.ffmpegPath=('I:\\togpic\\Mitsuba\\Python\\lib\\ThirdPartyExe\\ffmpeg\\ffmpeg.exe')
					

	def Copy_5(self, inputPath, outputPath):
		### Rename file ###
		# Format 'image_xxx.png'
		ImagePath = ReadFiles(inputPath)
			
		for i in range(len(ImagePath)):
			print(ImagePath[i])

			for j in range(5):
				shutil.copy2(ImagePath[i], outputPath + '\\image' + '_%03i_%03i.png' % (i, j))

	def Rename(self, inputPath, outputPath):
		### Rename file ###
		# Format 'image_xxx.png'
		ImagePath = ReadFiles(inputPath)
		
		for i in range(len(ImagePath)):
			print(ImagePath[i])
			shutil.copy2(ImagePath[i], outputPath + '\\image' + '_%03i.jpg' % (i))


	def ProduceVideo(self, inputPath, outputPath, vidoename):
		### ProduceVideo ###
		video = VideoInfo()

		video.SetInputDir(inputPath)
		video.SetInputFileFormat( "\\" + "image_%03d.jpg")
		video.SetStarFrame("0")
		video.SetOutputDir(outputPath)
		video.SetFps("0.25")
		video.SetVideoName(vidoename)

		ffProcess = Ffmpeg()
		ffProcess.SetFfmpeg(self.ffmpegPath)
		ffProcess.Run('produceVideo', video)


	def Png2Jpg(self, pathInput, PathOutput):

		pngList = ReadFilesDeep(pathInput)
		magick = ImageMagick() 
		magick.magick=self.magickPath
		 

		for png in pngList: 
				magick.Convert2Jpg(png,PathOutput)

	def ImageTrim(self, pathInput):

		pngList = ReadFilesDeep(pathInput)
		magick = ImageMagick() 
		magick.magick=self.magickPath

		for png in pngList: 
				magick.TrimFile(png)



	def ImageCrop(self, pathInput,size):

		pngList = ReadFilesDeep(pathInput)
		magick = ImageMagick() 
		magick.magick=self.magickPath

		for png in pngList: 
				magick.CropFile(png,size)


	def ImageAppend(self, input1, input2, output):		 
		magick = ImageMagick() 
		magick.magick=self.magickPath
		magick.AppendFolder(input1, input2,output,'+append')


	def ImageAppendV2(self, input1, input2, input3,output):		 
		magick = ImageMagick() 
		magick.magick=self.magickPath
		magick.AppendThreeFolder(input1, input2, input3,output,'+append')


	def ImageLabel(self, inputpath, output):

		oneLabel = Label()
		oneLabel.SetBackgroundColor("White")
		oneLabel.SetLabel("Optimized")
		oneLabel.SetFontColor("black")
		 
		magick = ImageMagick() 
		magick.magick=self.magickPath
 		magick.AddLabelFolder(inputpath, output,oneLabel)


 	def CatVideo(self, videoInput, videoOutput):
		#cmd=self.ffmpegPath + " -i "  +videoInput + ' -filter:v "setpts=0.28*PTS"  ' + videoOutput
		cmd=self.ffmpegPath + " -f  concat -i "  + videoInput + ' -c    ' + videoOutput
		print(cmd)
		os.system(cmd)



	def ChangeVideo(self, videoInput, videoOutput):
		#cmd=self.ffmpegPath + " -i "  +videoInput + ' -filter:v "setpts=0.28*PTS"  ' + videoOutput
		cmd=self.ffmpegPath + " -i "  +videoInput + ' -c:v libx264 -crf 36 -b:v 1M    ' + videoOutput
		print(cmd)
		os.system(cmd)
		#os.system(self.ffmpegPath
		#	+ ' -i ' 
		#	+  videoInput 
		#	+ ' -filter:v '+ "setpts=0.5*PTS"
		#	+  videoOutput)

	def TrimVideo(self, videoInput, videoOutput, start, duration):
		#cmd=self.ffmpegPath + " -i "  +videoInput + ' -filter:v "setpts=0.28*PTS"  ' + videoOutput
		cmd=self.ffmpegPath + " -i "  +videoInput + ' -ss '+ start + ' -t '+ duration + '  -async 1  -c copy  ' + videoOutput
		print(cmd)
		os.system(cmd)
		#os.system(self.ffmpegPath
		#	+ ' -i ' 
		#	+  videoInput 
		#	+ ' -filter:v '+ "setpts=0.5*PTS"
		#	+  videoOutput)

if __name__ == '__main__':
	task = TaskImageVideo()
	 
	#task.Png2Jpg('G:\\togpic\\polycubeimage\\png\\quad3', 'G:\\togpic\\polycubeimage\\jpg\\trimNo\\quad3')
	#task.ImageTrim('G:\\togpic\\polycubeimage\\jpg\\trim\\quad3')
	#task.Rename('.\\Data\\png', '.\\Data\\png')
	#task.Rename('G:\\togpic\\polycubeimage\\jpg\\trimNO\\uv2texture', 'G:\\togpic\\polycubeimage\\jpg\\Rename\\uv2texture')
	#task.ProduceVideo('G:\\togpic\\polycubeimage\\jpg\\Rename\\append6', 'G:\\togpic\\polycubeimage\\video', "append6")
	task.ChangeVideo('I:\\video\\hydrographics.avi', 'I:\\video\\hydrographics.mp4')
	#task.TrimVideo('D:\\shilei3.mp4', 'd:\\shilei12.mp4',"00:05:0", "00:10:30")
	#task.ImageCrop('G:\\togpic\\polycubeimage\\jpg\\Rename\\bimba', "100x100+0+0")
	#task.ImageAppend('G:\\togpic\\polycubeimage\\jpg\\Rename\\uv7','G:\\togpic\\polycubeimage\\jpg\\Rename\\uv1','G:\\togpic\\polycubeimage\\jpg\\Rename\\append5')
	#task.ImageAppendV2('G:\\togpic\\polycubeimage\\jpg\\Rename\\label1','G:\\togpic\\polycubeimage\\jpg\\Rename\\label2','G:\\togpic\\polycubeimage\\jpg\\Rename\\label3','G:\\togpic\\polycubeimage\\jpg\\Rename\\append6')
	#task.ImageLabel('G:\\togpic\\polycubeimage\\jpg\\Rename\\uv1', 'G:\\togpic\\polycubeimage\\jpg\\Rename\\label3')
	#task.CatVideo('G:\\paper\\Paper2017\\Deform2017\\video\list.txt', 'G:\\paper\\Paper2017\\Deform2017\\video\\all.mp4')

