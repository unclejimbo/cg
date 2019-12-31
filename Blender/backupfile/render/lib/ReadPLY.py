from plyfile import PlyData, PlyElement, make2d
import numpy as np
def ReadPLY(filename):
    plydata = PlyData.read(filename)

    nVerts = plydata['vertex'].count
    verts = np.zeros((nVerts,3))
    verts[:,0] = np.array(plydata['vertex'].data['x'])
    verts[:,1] = np.array(plydata['vertex'].data['y'])
    verts[:,2] = np.array(plydata['vertex'].data['z'])

    vertexColors = []
    if "red" in str(plydata['vertex']):
        vertexColors = np.zeros((nVerts,3))
        vertexColors[:,0] = np.array(plydata['vertex'].data['red'])
        vertexColors[:,1] = np.array(plydata['vertex'].data['green'])
        vertexColors[:,2] = np.array(plydata['vertex'].data['blue'])

    faces = make2d(plydata['face'].data['vertex_indices'])

    return [verts, vertexColors, faces]