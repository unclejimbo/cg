import os
# Configure the OBJ files with adding 'usemtl bsdf'
def ConfigOBJ_usemtl(modelPath):
	if os.path.basename(modelPath).split(".")[-1] == "obj":
		# add bsdf in Obj files
		with open(modelPath) as f:
			lines = f.readlines()
			if lines[0:0] != "usemtl bsdf\n":
				lines[0:0] = ['usemtl bsdf\n']
		open(modelPath, 'w').writelines(lines)

		# Print
		print("Add 'usemtl bsdf' " + modelPath)
	else:
		pass