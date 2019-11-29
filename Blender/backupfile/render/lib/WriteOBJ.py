def WriteOBJ(filename, vertrices, vts, vns, facesV, facesVt, facesVn):
    f=file(filename,"w+")

    for vertex in vertrices:
        f.write("v ")
        for i in range(len(vertex)):
            f.write(str(vertex[i]))
            f.write(" ")
        f.write("\n")

    if len(vts) != 0:
        for vt in vts:
            f.write("vt ")
            for i in range(len(vt)):
                f.write(str(vt[i]))
                f.write(" ")
            f.write("\n")

    if len(vns) != 0:
        for vn in vns:
            f.write("vn ")
            for i in range(len(vn)):
                f.write(str(vn[i]))
                f.write(" ")
            f.write("\n")

    if len(vts) != 0 and len(vns) != 0:
        for (faceV, faceVt, faceVn) in zip(facesV, facesVt, facesVn):
            f.write("f ")
            for i in range(len(faceV)):
                f.write(str(faceV[i]))
                f.write("/")
                f.write(str(faceVt[i]))
                f.write("/")
                f.write(str(faceVn[i]))
                f.write(" ")
            f.write("\n")
    
    if len(vts) != 0 and len(vns) == 0:
        for (faceV, faceVt) in zip(facesV, facesVt):
            f.write("f ")
            for i in range(len(faceV)):
                f.write(str(faceV[i]))
                f.write("/")
                f.write(str(faceVt[i]))
                f.write(" ")
            f.write("\n")

    if len(vts) == 0 and len(vns) == 0:
        for faceV in facesV:
            f.write("f ")
            for i in range(len(faceV)):
                f.write(str(faceV[i]))
                f.write(" ")
            f.write("\n")
        
    f.close