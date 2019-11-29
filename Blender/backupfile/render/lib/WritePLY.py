from plyfile import PlyData, PlyElement, make2d
import numpy as np
def WritePLY(filename, vertices, vertexColors, faces):
    f = file(filename,"w+")

    # write ply header
    f.write("ply")
    f.write("\n")
    f.write("format ascii 1.0")
    f.write("\n")
    f.write("element vertex " + str(len(vertices)))
    f.write("\n")
    f.write("property float x")
    f.write("\n")
    f.write("property float y")
    f.write("\n")
    f.write("property float z")
    f.write("\n")

    ### PLY with vertex color ###
    if len(vertexColors) != 0:
        f.write("property uchar red")
        f.write("\n")
        f.write("property uchar green")
        f.write("\n")
        f.write("property uchar blue")
        f.write("\n")

    f.write("element face " + str(len(faces)))
    f.write("\n")
    f.write("property list uchar int vertex_indices")
    f.write("\n")
    f.write("end_header")
    f.write("\n")

    ### PLY without vertex color
    if len(vertexColors) == 0:
        for vertex in vertices:
            for i in range(len(vertex)):
                f.write(str(vertex[i]))
                f.write(" ")
            f.write("\n")
    ### PLY with vertex color ###
    else:
        for vertex, vertexColor in zip(vertices, vertexColors):
            for i in range(len(vertex)):
                f.write(str(vertex[i]))
                f.write(" ")

            for i in range(len(vertexColor)):
                f.write(str(int(vertexColor[i])))
                f.write(" ")

            f.write("\n")

    for face in faces:
        f.write("3 ")
        for i in range(len(face)):
            f.write(str(face[i]))
            f.write(" ")
        f.write("\n")

    f.close