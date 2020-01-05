import openmesh as om
import os

file_list = os.listdir("./")
print(file_list)

for filename in file_list:
    if ".off" in filename:
        mesh = om.read_trimesh(filename)
        x = []
        y = []
        z = []
        for point in mesh.points():
            x.append(point[0])
            y.append(point[1])
            z.append(point[2])
        print("maxx:", max(x), "minx:", min(x))
        print("maxy:", max(y), "miny:", min(y))
        print("maxz:", max(z), "minz:", min(z))
        for point in mesh.points():
            point[0] = (((point[0] - min(x)) / (max(x) - min(x))) - 0.5) * 2
            point[1] = (((point[1] - min(y)) / (max(y) - min(y))) - 0.5) * 2
            point[2] = (((point[2] - min(z)) / (max(z) - min(z))) - 0.5) * 2
        om.write_mesh("./meshes2/"+filename.split(".")[0]+".obj",mesh)


