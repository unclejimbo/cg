from MeshProcess.ReadOBJ import *
from MeshProcess.ReadPLY import *

import numpy as np
import os

def GetRatioTo01(filename):
	if os.path.basename(filename).split(".")[-1] == "obj":
		[vertices, vts, vns, facesV, facesVt, facesVn] = ReadOBJ(filename)
	elif os.path.basename(filename).split(".")[-1] == "ply":
		[vertices, vertexColors, faces] = ReadPLY(filename)

	vxMax = np.max(vertices.T[0])
	vxMin = np.min(vertices.T[0])
	vyMax = np.max(vertices.T[1])
	vyMin = np.min(vertices.T[1])
	vzMax = np.max(vertices.T[2])
	vzMin = np.min(vertices.T[2])

	zoom = max(vxMax-vxMin,max(vyMax-vyMin,vzMax-vzMin))

	return 1.0/zoom

def GetRatioBatch(filenameList):

	vertices = []
	faces = []

	for i in range(len(filenameList)):
		print(filenameList[i])
		[vertices, vts, vns, facesV, facesVt, facesVn] = ReadOBJ(filenameList[i])
		vertices.append(v)

	vertices = np.array(vertices)

	vxMax = np.max(vertices.T[0])
	vxMin = np.min(vertices.T[0])
	vyMax = np.max(vertices.T[1])
	vyMin = np.min(vertices.T[1])
	vzMax = np.max(vertices.T[2])
	vzMin = np.min(vertices.T[2])

	zoom = max(vxMax-vxMin,max(vyMax-vyMin,vzMax-vzMin))

	return 1.0/zoom