import shutil
import os
import sys
sys.path.append('..\\')
sys.path.append('..\\..\\lib')
 

from Tool.IO import *
from DirSetting import *

from MeshProcess.GenerateSphere import *
from MeshProcess.GenerateCylinder import *
from MeshProcess.MoveToCenterXYZ import *
from MeshProcess.GetRatioTo01 import *
from MeshProcess.Scale import *
from MeshProcess.ConfigOBJ_usemtl import *

class MeshFactory(object):

	def __init__(self):
		super(MeshFactory, self).__init__()

		self.InputPath=None 
 		 
		self.OutputPathVertex=None
		self.OutputPathEdge=None

	def Generate(self):
		# Generate sphere & cylinder #
		txtPathList = ReadFilesDeep(self.InputPath)
		for item in txtPathList:
			#print(item.split('\\')[-1])
			if(item.split('\\')[-1] == 'vtx.txt'):
				# pass
				 
				if os.path.isdir(self.OutputPathVertex):
					shutil.rmtree(self.OutputPathVertex)

				CreatePath(self.OutputPathVertex)
				GenerateSphere(dirSphereOBJ_3, self.OutputPathVertex, item)
			
			elif(item.split('\\')[-1] == 'edge.txt'):
				
				# pass

				if os.path.isdir(self.OutputPathEdge):
					shutil.rmtree(self.OutputPathEdge)

				CreatePath(self.OutputPathEdge)
				GenerateCylinder(dirCylinderOBJ_face212, self.OutputPathEdge, item)


if __name__ == '__main__':
	# RenderVertexEdge_original()
	factory= MeshFactory()
	factory.InputPath ='.\\Data\\Txt' 
	factory.OutputPathVertex='.\\Data\\Model\Vertex'
	factory.OutputPathEdge='.\\Data\\Model\Edge'
	factory.Generate()
	# RenderVertexEdge_CoatingHK_polycube()
	# RenderVertexEdge_ThinDielectric

	 