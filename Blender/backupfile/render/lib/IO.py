import os
import shutil

def ReadFilesOBJ(rootDir):
	filePath = []
	fileName = []
	list_dirs = os.listdir(rootDir) 
	for f in list_dirs:
		if '.obj' in f:
			filePath.append(os.path.join(rootDir, f))
			fileName.append(f.split(".")[0])

	return filePath

# Read files from the path
def ReadFiles(rootDir):
	filePath = []
	fileName = []
	list_dirs = os.listdir(rootDir) 
	for f in list_dirs:
		if not 'Thumbs' or not '.db' in f:
			filePath.append(os.path.join(rootDir, f))
			fileName.append(f.split(".")[0])

	return filePath

# Read all files from the root path
def ReadFilesDeep(rootDir):
	filePath = []
	fileName = []
	list_dirs = os.walk(rootDir) 
	for root, dirs, files in list_dirs:       
		for f in files:
			if not 'Thumbs' or not '.db' in f:
				filePath.append(os.path.join(root, f))
				fileName.append(f.split(".")[0])
				# fileName.append(f)

	return filePath

def ReadFilesDeep_PNG(rootDir):
	filePath = []
	fileName = []
	list_dirs = os.walk(rootDir) 
	for root, dirs, files in list_dirs:       
		for f in files:
			if '.png' in f:
				filePath.append(os.path.join(root, f))
				fileName.append(f.split(".")[0])

	return filePath 

def ReadFilesDeep_JPG(rootDir):
	filePath = []
	fileName = []
	list_dirs = os.walk(rootDir) 
	for root, dirs, files in list_dirs:       
		for f in files:
			if '.jpg' in f:
				filePath.append(os.path.join(root, f))
				fileName.append(f.split(".")[0])

	return filePath

def DeleteFile(fileDir):
	print("Delete: " + fileDir)
	os.remove(fileDir)

def DeleteFilesDeep_PNG(rootDir):
	imagePathList = ReadFilesDeep_PNG(rootDir)

	for i in range(len(imagePathList)):
		DeleteFile(imagePathList[i])

def DeleteFilesDeep_JPG(rootDir):
	imagePathList = ReadFilesDeep_JPG(rootDir)

	for i in range(len(imagePathList)):
		DeleteFile(imagePathList[i])

# Create new folder
def SetFolder(folderName, rootPath):
	# Set folder path
	folderPath = os.path.join(rootPath, folderName)

	# Create new folder
	if not os.path.isdir(folderPath):
		os.makedirs(folderPath)

	return folderPath

def CreatePath(path):
	# Create Path
	if not os.path.isdir(path):
		os.makedirs(path)
		
	return path