import sys
sys.path.append('..\\..\\lib')

from MeshProcess.ReadOBJ import *
from MeshProcess.WriteOBJ import *

from MeshProcess.MoveToCenterXYZ import *
from MeshProcess.GetRatioTo01 import *
from MeshProcess.Scale import *

MoveToCenterXYZ('.\\bunny_remeshed_quad.obj', 0, 0, 0)
Scale('.\\bunny_remeshed_quad.obj', GetRatioTo01('.\\bunny_remeshed_quad.obj'))

[vertrices, vts, vns, facesV, facesVt, facesVn] = ReadOBJ('.\\bunny_remeshed_quad.obj')

f = file('.\\bunny_remeshed_quad.txt', "w+")

for i in range(len(facesV)):
	for j in range(len(facesV[i])):

		for k in range(len(vertrices[facesV[i][j] - 1])):
			f.write(str(vertrices[facesV[i][j] - 1][k]))
			f.write(" ")

		for k in range(len(vertrices[facesV[i][(j + 1) % len(facesV[i])] - 1])):
			f.write(str(vertrices[facesV[i][(j + 1) % len(facesV[i])] - 1][k]))
			f.write(" ")

		f.write("\n")

f.close


