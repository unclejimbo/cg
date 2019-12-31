import os

from MeshProcess.ReadOBJ import *
from MeshProcess.WriteOBJ import *

from MeshProcess.ReadPLY import *
from MeshProcess.WritePLY import *

import numpy as np

def MoveToCenterXYZ(filename, x, y, z):
	if os.path.basename(filename).split(".")[-1] == "obj":
		# Read OBJ
		[vertices, vts, vns, facesV, facesVt, facesVn] = ReadOBJ(filename)
		# Move all point to center
		vertices = MoveAllPointToXYZ(vertices, x, y, z)
		# Write new OBJ
		WriteOBJ(filename, vertices, vts, vns, facesV, facesVt, facesVn)
		# WriteOBJ(filename+'_center('+ str(x) +','+ str(y) + ',' + str(z) + ').obj',vertices,faces)

	elif os.path.basename(filename).split(".")[-1] == "ply":
		# Read PLY
		[vertices, vertexColors, faces] = ReadPLY(filename)
		# Move all point to center
		vertices = MoveAllPointToXYZ(vertices, x, y, z)
		# Write new PLY
		WritePLY(filename, vertices, vertexColors, faces)

def MoveAllPointToXYZ(vertices, x, y, z):
	vxMax = np.max(vertices.T[0])
	vxMin = np.min(vertices.T[0])
	vyMax = np.max(vertices.T[1])
	vyMin = np.min(vertices.T[1])
	vzMax = np.max(vertices.T[2])
	vzMin = np.min(vertices.T[2])

	# Center point values
	xCenter = ( (vxMax-vxMin)/2.0 ) + vxMin
	yCenter = ( (vyMax-vyMin)/2.0 ) + vyMin
	zCenter = ( (vzMax-vzMin)/2.0 ) + vzMin

	# Center point values
	# xCenter = ( (vxMax+vxMin)/2.0 )
	# yCenter = ( (vyMax+vyMin)/2.0 )
	# zCenter = ( (vzMax+vzMin)/2.0 )

	xDistance = xCenter - x
	yDistance = yCenter - y
	zDistance = zCenter - z

	for i in range(len(vertices)):
		vertices[i][0] = (vertices[i][0] - xDistance)
		vertices[i][1] = (vertices[i][1] - yDistance)
		vertices[i][2] = (vertices[i][2] - zDistance)

	return vertices