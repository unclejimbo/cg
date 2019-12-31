from MeshProcess.ReadOBJ import *
from MeshProcess.WriteOBJ import *

from MeshProcess.ReadPLY import *
from MeshProcess.WritePLY import *

import numpy as np
import os
def Scale(filename, ratio):
	if os.path.basename(filename).split(".")[-1] == "obj":
		# Read OBJ
		[vertices, vts, vns, facesV, facesVt, facesVn] = ReadOBJ(filename)
		# Scale all points
		vertices = ScaleAllPoint(vertices, ratio)
		# Write new OBJ
		WriteOBJ(filename, vertices, vts, vns, facesV, facesVt, facesVn)

	elif os.path.basename(filename).split(".")[-1] == "ply":
		# Read PLY
		[vertices, vertexColors, faces] = ReadPLY(filename)
		# Scale all points
		vertices = ScaleAllPoint(vertices, ratio)
		# Write new PLY
		WritePLY(filename, vertices, vertexColors, faces)

def ScaleAllPoint(vertices, ratio):
	for i in range(len(vertices)):
		vertices[i][0] = vertices[i][0]*ratio
		vertices[i][1] = vertices[i][1]*ratio
		vertices[i][2] = vertices[i][2]*ratio
	return vertices