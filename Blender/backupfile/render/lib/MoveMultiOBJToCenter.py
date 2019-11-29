from MeshProcess.ReadOBJ import *
from MeshProcess.WriteOBJ import *
from MeshProcess.WriteOBJ_WithVT import *

import numpy as np
import os

def MoveMutilOBJToCenter(fileDir):

	absFileName = []
	list_dirs = os.walk(fileDir)
	for root, dirs, files in list_dirs:     
		for f in files:
			absFileName.append(os.path.join(root, f))
	vertrices = []
	faces = []

	for i in range(len(absFileName)):
		[v, f, vt] = ReadOBJ(absFileName[i])
		vertrices.append(v)

	vertrices = np.array(vertrices)

	vxMax = np.max(vertrices.T[0])
	vxMin = np.min(vertrices.T[0])
	vyMax = np.max(vertrices.T[1])
	vyMin = np.min(vertrices.T[1])
	vzMax = np.max(vertrices.T[2])
	vzMin = np.min(vertrices.T[2])

	zoom = max(vxMax-vxMin,max(vyMax-vyMin,vzMax-vzMin))

	for i in range(len(absFileName)):
		[vertex, face, vt] = ReadOBJ(absFileName[i])

		for j in range(len(vertex)):
		    vertex[j][0] = (vertex[j][0]-vxMin)/zoom - ((vxMax-vxMin)/(zoom*2.0))
		    vertex[j][1] = (vertex[j][1]-vyMin)/zoom - ((vyMax-vyMin)/(zoom*2.0))
		    vertex[j][2] = (vertex[j][2]-vzMin)/zoom - ((vzMax-vzMin)/(zoom*2.0))

		WriteOBJ(absFileName[i].split('.')[0]+'_normalized.obj', vertex, face)