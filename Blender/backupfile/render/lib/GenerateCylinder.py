from ThirdPartyLib.Rotation import unit_vector,vector_norm,rotation_matrix,angle_between_vectors,vector_product
from MeshProcess.WriteOBJ import *
from MeshProcess.ReadOBJ import *
import numpy,math

def GenerateCylinder(cylinderOBJ, targetFolder, targetPositionFile):
	#read vectors from file
	numbers = []
	for line in open(targetPositionFile).readlines():
		items = line.strip().split(' ')
		numbers.append([float(s) for s in items[:]])
	numbers = numpy.array(numbers)

	[originCylinderVtx, originCylinderVts, originCylinderVns, originCylinderFacesV, originCylinderFacesVt, originCylinderFacesVn] = ReadOBJ(cylinderOBJ)
	# Calculate the max and min values at Z direction
	maxZ = np.max(originCylinderVtx.T[2])
	minZ = np.min(originCylinderVtx.T[2])
	
	for j in range(len(numbers)):
		rotX = float(numbers[j][3]) - float(numbers[j][0])
		rotY = float(numbers[j][4]) - float(numbers[j][1])
		rotZ = float(numbers[j][5]) - float(numbers[j][2])
		vectorLength = math.sqrt(rotX*rotX+rotY*rotY+rotZ*rotZ)
		[tempOBJVtx, tempOBJVts, tempOBJVns, tempOBJFacesV, tempOBJFacesVt, tempOBJFacesVn] = ReadOBJ(cylinderOBJ)
		# Scale and rotate cylinder objects
		for i in range(len(originCylinderVtx)):
			angle = angle_between_vectors([0,0,1],[rotX,rotY,rotZ])
			Mr = rotation_matrix(angle,vector_product([0,0,1],[rotX,rotY,rotZ]))
			tempOBJVtx[i][2] = ((tempOBJVtx[i][2]-minZ)*vectorLength)/(maxZ-minZ) + minZ
			tempOBJVtx[i] = numpy.dot(Mr[:3,:3],[tempOBJVtx[i][0],tempOBJVtx[i][1],tempOBJVtx[i][2]])		
		# Move cylinder objects
		for i in range(len(tempOBJVtx)):
			tempOBJVtx[i][0] = round(tempOBJVtx[i][0] + float(numbers[j][0]),6)
			tempOBJVtx[i][1] = round(tempOBJVtx[i][1] + float(numbers[j][1]),6)
			tempOBJVtx[i][2] = round(tempOBJVtx[i][2] + float(numbers[j][2]),6)

		print(targetFolder + "\\" + "cylinder" +str(j)+".obj")	
		WriteOBJ(targetFolder + "\\" + "cylinder" +str(j)+".obj",tempOBJVtx, tempOBJVts, tempOBJVns, tempOBJFacesV, tempOBJFacesVt, tempOBJFacesVn)