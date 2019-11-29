from MeshProcess.ReadOBJ import *
from MeshProcess.WriteOBJ import *
import numpy
def GenerateSphere(sphereOBJ,targetFolderPath,verticesPositionFile):
	sphereOBJ = sphereOBJ
	numbers = []
	for line in open(verticesPositionFile).readlines():
		items = line.strip().split(' ')
		numbers.append([float(s) for s in items[:]])
	numbers = numpy.array(numbers)
	[originSphereVtx, originSphereVts, originSphereVns, originSphereFacesV, originSphereFacesVt, originSphereFacesVn] = ReadOBJ(sphereOBJ)
	for j in range(len(numbers)):
		[tempOBJVtx, tempOBJVts, tempOBJVns, tempOBJFacesV, tempOBJFacesVt, tempOBJFacesVn] = ReadOBJ(sphereOBJ)
		# Move sphere objects
		for i in range(len(originSphereVtx)):
			tempOBJVtx[i][0] = (originSphereVtx[i][0] + float(numbers[j][0]))
			tempOBJVtx[i][1] = (originSphereVtx[i][1] + float(numbers[j][1]))
			tempOBJVtx[i][2] = (originSphereVtx[i][2] + float(numbers[j][2]))
			
		print(targetFolderPath + "\\" + "sphere" + str(j)+".obj")
		WriteOBJ(targetFolderPath + "\\" + "sphere" + str(j)+".obj",tempOBJVtx, tempOBJVts, tempOBJVns, tempOBJFacesV, tempOBJFacesVt, tempOBJFacesVn)