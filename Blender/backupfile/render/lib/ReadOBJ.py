import numpy as np
def ReadOBJ(filename):
	vertrices = []

	vts = []
	vns = []

	facesV = []
	facesVt = []
	facesVn = []

	# Process the file line by line
	lineInd = -1

	print("Loading OBJ 	")
	for line in open(filename).readlines():
		lineInd += 1
		if line[0] == '#':
			continue

		items = line.strip().split(' ')
		# print(items)
		
		# Process vertex
		if items[0] == 'v':
			vertrices.append([float(s) for s in items[1:]])
		
		elif items[0] == 'vt':
			vts.append([float(s) for s in items[1:]])

		elif items[0] == 'vn':
			vns.append([float(s) for s in items[1:]])

		# Process face indices
		elif items[0] == 'f' :
			face = items[1:]
			facesV.append([int(s.split("/")[0]) for s in face])

			if len(vts) != 0:
				facesVt.append([int(s.split("/")[1]) for s in face])
			if len(vns) != 0:
				facesVn.append([int(s.split("/")[2]) for s in face])

	# Convert to numpy arrays
	vertrices = np.array(vertrices)
	vts = np.array(vts)
	facesV = np.array(facesV)
	facesVt = np.array(facesVt)
	facesVn = np.array(facesVn)

	return [vertrices, vts, vns, facesV, facesVt, facesVn]