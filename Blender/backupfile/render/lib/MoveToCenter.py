from MeshProcess.ReadOBJ import *
from MeshProcess.ReadPLY import *
from MeshProcess.WriteOBJ import *
from MeshProcess.WriteOBJ_WithVT import *
from MeshProcess.WritePLY import *

import numpy as np

def MoveToCenterOBJ(filename):
	[vertrices, faces, vt] = ReadOBJ(filename)

	vxMax = np.max(vertrices.T[0])
	vxMin = np.min(vertrices.T[0])
	vyMax = np.max(vertrices.T[1])
	vyMin = np.min(vertrices.T[1])
	vzMax = np.max(vertrices.T[2])
	vzMin = np.min(vertrices.T[2])

	zoom = max(vxMax-vxMin,max(vyMax-vyMin,vzMax-vzMin))


	for i in range(len(vertrices)):
	    vertrices[i][0] = (vertrices[i][0]-vxMin)/zoom - ((vxMax-vxMin)/(zoom*2.0))
	    vertrices[i][1] = (vertrices[i][1]-vyMin)/zoom - ((vyMax-vyMin)/(zoom*2.0))
	    vertrices[i][2] = (vertrices[i][2]-vzMin)/zoom - ((vzMax-vzMin)/(zoom*2.0))

	WriteOBJ(filename, vertrices, faces)

def MoveToCenterOBJ_WithVT(filename):
	[vertrices, faces, vt] = ReadOBJ(filename)

	vxMax = np.max(vertrices.T[0])
	vxMin = np.min(vertrices.T[0])
	vyMax = np.max(vertrices.T[1])
	vyMin = np.min(vertrices.T[1])
	vzMax = np.max(vertrices.T[2])
	vzMin = np.min(vertrices.T[2])

	zoom = max(vxMax-vxMin,max(vyMax-vyMin,vzMax-vzMin))


	for i in range(len(vertrices)):
	    vertrices[i][0] = (vertrices[i][0]-vxMin)/zoom - ((vxMax-vxMin)/(zoom*2.0))
	    vertrices[i][1] = (vertrices[i][1]-vyMin)/zoom - ((vyMax-vyMin)/(zoom*2.0))
	    vertrices[i][2] = (vertrices[i][2]-vzMin)/zoom - ((vzMax-vzMin)/(zoom*2.0))

	WriteOBJ_WithVT(filename, vertrices, faces, vt)

def MoveToCenterPLY(filename):
	[vertrices, faces] = ReadPLY(filename)

	vertrices = np.array(vertrices)
	faces = np.array(faces)

	vxMax = np.max(vertrices.T[0])
	vxMin = np.min(vertrices.T[0])
	vyMax = np.max(vertrices.T[1])
	vyMin = np.min(vertrices.T[1])
	vzMax = np.max(vertrices.T[2])
	vzMin = np.min(vertrices.T[2])

	zoom = max(vxMax-vxMin,max(vyMax-vyMin,vzMax-vzMin))


	for i in range(len(vertrices)):
	    vertrices[i][0] = (vertrices[i][0]-vxMin)/zoom - ((vxMax-vxMin)/(zoom*2.0))
	    vertrices[i][1] = (vertrices[i][1]-vyMin)/zoom - ((vyMax-vyMin)/(zoom*2.0))
	    vertrices[i][2] = (vertrices[i][2]-vzMin)/zoom - ((vzMax-vzMin)/(zoom*2.0))

	WritePLY(filename, vertrices, faces)
