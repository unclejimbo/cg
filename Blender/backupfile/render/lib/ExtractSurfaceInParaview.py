import os
#### import the simple module from the paraview
from paraview.simple import *

def ReadFileNames(rootDir):
	completeFileName = []
	fileName = []
	list_dirs = os.walk(rootDir) 
	for root, dirs, files in list_dirs:       
		for f in files: 
			completeFileName.append(os.path.join(root, f))
			fileName.append(f.split(".")[0])

	return [completeFileName,fileName]

filepath = "C:\liyue\PolyCube data"
[completeFileName,fileName] = ReadFileNames(filepath)

count = 0
for vtkFileName in completeFileName:
	# create a new 'Legacy VTK Reader'
	vtkModel = LegacyVTKReader(FileNames=[vtkFileName])
	# create a new 'Extract Surface'
	surfaceModel = ExtractSurface(Input=vtkModel)
	# ----------------------------------------------------------------
	# finally, restore active source
	SetActiveSource(surfaceModel)
	# ----------------------------------------------------------------

	writer= CreateWriter(filepath+"/"+fileName[count]+".ply", surfaceModel)
	writer.UpdatePipeline()
	count+=1