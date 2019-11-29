from ReadOBJ import *
from WriteOBJ import *

[vertrices, vts, vns, facesV, facesVt, facesVn] = ReadOBJ('.\\polycube_\#0.obj')

f = file('.\\polycube_edge.txt', "w+")

# print(vertrices)
# print(facesV)
for i in range(len(facesV)):
	for j in range(len(facesV[i])):
		# continue
		# print(facesV[i][j])
		if not j == len(facesV[i]) - 1:

			for k in range(len(vertrices[facesV[i][j] - 1])):
				f.write(str(vertrices[facesV[i][j] - 1][k]))
				f.write(" ")

			for k in range(len(vertrices[facesV[i][j + 1] - 1])):
				f.write(str(vertrices[facesV[i][j + 1] - 1][k]))
				f.write(" ")
			f.write("\n")
			# print(vertrices[facesV[i][j] - 1])
			# print(vertrices[facesV[i][j + 1] - 1])
			# print("####")
		else:
			for k in range(len(vertrices[facesV[i][j] - 1])):
				f.write(str(vertrices[facesV[i][j] - 1][k]))
				f.write(" ")

			for k in range(len(vertrices[facesV[i][0] - 1])):
				f.write(str(vertrices[facesV[i][0] - 1][k]))
				f.write(" ")
			f.write("\n")

			# print(vertrices[facesV[i][j] - 1])
			# print(vertrices[facesV[i][0] - 1])
			# print("####")
		# print(f[i])

f.close


