import sys
sys.path.append('..\\')
sys.path.append('..\\..\\lib')

from DirSetting import *

from Tool.IO import *
from Tool.PrettyColor import *
from SceneBasic.SuperScene import *
from MeshProcess.MoveToCenterXYZ import *
from MeshProcess.GetRatioTo01 import *
from MeshProcess.Scale import *
from MeshProcess.ConfigOBJ_usemtl import *

class RenderChernPerfect(SuperScene):
	def __init__(self):
		super(RenderChernPerfect, self).__init__()
		
		self.dirBitmap='..\\..\\..\\canvas\\circle20.png'
		PathOutput=None
		Path1=None
		Path2=None
		Path3=None
		Path4=None
		Path5=None
		Path6=None
		Path7=None
		Path8=None

		Path9=None
		Path10=None
		Path11=None

		Path12=None

		self.curdir=None

		self.ImageName="HuiZhao"

		#self.shapeRotateX =-60
		#self.shapeRotateY =0
		self.shapeRotateX = -60
		self.shapeRotateY = -40
		self.shapeRotateZ = 0
		self.rotationStepSize = 26
		self.colorList=["hotpink","magenta","lightSteelBlue","yellow","peachPuff", "firebrick3", "chocolate", "lawnGreen"]
		self.uScale=1.0
		self.vScale=1.0

	def ProcessModels(model):
	
		MoveToCenterXYZ(model, 0, 0, 0)		
		ScaleRatioTo01 = GetRatioTo01(model)
		Scale(model, ScaleRatioTo01)	
		ConfigOBJ_usemtl(model)



	def RenderListPath1(self, modelFile):
		 
		# Wireframe
		self.CreateMaterail3()


	 
		if os.path.basename(modelFile).split(".")[1] == "obj":
				shape = ModelOBJ()
		elif os.path.basename(modelFile).split(".")[1] == "ply":
				shape = ModelPLY()
		shape.SetToWorldRotate(self.shapeRotateX,self.shapeRotateY, self.shapeRotateZ)
		shape.SetFaceNormals(True)	
		shape.SetFileName(modelFile)
		shape.SetMaterial(self.M1)
		self.ImageName = "".join(os.path.basename(modelFile).split(".")[:-1])
		shape.Setup(self.scene)
		self.shape=shape



	def RenderPath1(self):
		
		#self.List1 = ReadFilesDeep(self.Path1)
		self.List1 = ReadFilesOBJ(self.Path1)

		# Process Model #
		for i in range(len(self.List1)):
			ConfigOBJ_usemtl(self.List1[i])


		self.CreateMaterail3()


		for i in range(len(self.List1)):
			if os.path.basename(self.List1[i]).split(".")[1] == "obj":
				shape = ModelOBJ()
			elif os.path.basename(self.List1[i]).split(".")[1] == "ply":
				shape = ModelPLY()
			shape.SetToWorldRotate(self.shapeRotateX,self.shapeRotateY, self.shapeRotateZ)
			shape.SetFaceNormals(True)	
			shape.SetFileName(self.List1[i])
			shape.SetMaterial(self.M1)
			self.ImageName = "".join(os.path.basename(self.List1[i]).split(".")[:-1])
			shape.Setup(self.scene)
			#print("fff")
			#self.shape=shape



	def RenderPath1V2(self):
		
		self.List1 = ReadFilesDeep(self.Path1)
		# Process Model #
		for i in range(len(self.List1)):
			ConfigOBJ_usemtl(self.List1[i])
 


		for i in range(len(self.List1)):
			if os.path.basename(self.List1[i]).split(".")[1] == "obj":
				shape = ModelOBJ()
			elif os.path.basename(self.List1[i]).split(".")[1] == "ply":
				shape = ModelPLY()
			shape.SetToWorldRotate(self.shapeRotateX,self.shapeRotateY, self.shapeRotateZ)
			shape.SetFaceNormals(True)	
			shape.SetFileName(self.List1[i])
			self.ImageName = "".join(os.path.basename(self.List1[i]).split(".")[:-1])


					# Wireframe
			wireframe = TextureWireframe()
			wireframe.SetLineWidth(0.00025)
			wireframe.Setup()

			# # Roughplastic
			M1 = MaterialRoughPlastic()
			M1.SetDistribution('ggx')
			#self.M1.SetDiffuseReflectance(Spectrum(0.70))
			colorname=self.colorList[i%len(self.colorList)]
			print(colorname)
			M1.SetColorName(self.colorDitc[colorname])
			M1.SetTexture(wireframe)
			M1.Setup()
			shape.SetMaterial(M1)			
			shape.Setup(self.scene)
			 

	def CreateMaterail1(self):


		wireframe = TextureWireframe()
		wireframe.SetLineWidth(0.0004)
		#wireframe.SetEdgeColorRGB(255,0,0)
		#wireframe.SetInteriorColorRGB(0,0,0)
		wireframe.Setup()

 
		frontMaterial = MaterialRoughPlastic()
		#frontMaterial.SetColorName(self.colorDitc["lightOrange"])
		# Sku blue
		#frontMaterial.SetTexture(wireframe)
		# Setup
		frontMaterial.Setup()


		wireframe = TextureWireframe()
		wireframe.SetLineWidth(0.0009)
		wireframe.SetEdgeColorRGB(255,99,71)
		#wireframe.SetInteriorColorRGB(0,0,0)
		wireframe.Setup()
		# Back Material
		backMaterial = MaterialRoughPlastic()
		backMaterial.SetColorName(self.colorDitc["lightOrange"])
		# Dark orange
		#backMaterial.SetColorRGB(255, 51, 34)
		#backMaterial.SetColorName(self.colorDitc["yellow"])
		#backMaterial.SetTexture(wireframe)
		# Setup
		backMaterial.Setup()

		# Twosided Material
		self.M1 = MaterialTwosided()
		self.M1.SetFrontMaterial(frontMaterial)
		self.M1.SetBackMaterial(backMaterial)
		self.M1.Setup()

	def CreateMaterail2(self):


		texture = TextureUV()
		texture.SetDirBitmap(self.dirBitmap)
		texture.SetUscale(self.uScale)
		texture.SetVscale(self.vScale)
		texture.Setup()

		frontMaterial = MaterialRoughPlastic()
		# Sku blue
		frontMaterial.SetTexture(texture)
		# Setup
		frontMaterial.Setup()

		# Back Material
		backMaterial = MaterialRoughPlastic()
		# Dark orange
		backMaterial.SetColorRGB(255, 51, 34)
		# Setup
		backMaterial.Setup()

		# Twosided Material
		self.M1 = MaterialTwosided()
		self.M1.SetFrontMaterial(frontMaterial)
		self.M1.SetBackMaterial(backMaterial)
		self.M1.Setup()


	def CreateMaterail4(self):


		wireframe = TextureWireframe()
		wireframe.SetLineWidth(0.001)
		wireframe.SetEdgeColorRGB(0,0,0)
		wireframe.SetInteriorColorRGB(135,206,250)
		wireframe.Setup()

 
		frontMaterial = MaterialRoughPlastic()
		frontMaterial.SetColorName(self.colorDitc["blue"])
		# Sku blue
		#frontMaterial.SetTexture(wireframe)
		# Setup
		frontMaterial.Setup()


		wireframe = TextureWireframe()
		wireframe.SetLineWidth(0.001)
		wireframe.SetEdgeColorRGB(255,0,0)
		wireframe.SetInteriorColorRGB(135,206,250)
		wireframe.Setup()
		# Back Material
		backMaterial = MaterialRoughPlastic()
		# Dark orange
		#backMaterial.SetColorRGB(255, 51, 34)
		#backMaterial.SetColorName(self.colorDitc["skyBlue"])
		#backMaterial.SetTexture(wireframe)
		# Setup
		backMaterial.Setup()

		# Twosided Material
		self.M1 = MaterialTwosided()
		self.M1.SetFrontMaterial(frontMaterial)
		self.M1.SetBackMaterial(backMaterial)
		self.M1.Setup()



	def CreateMaterail3(self):
		# Wireframe
		wireframe = TextureWireframe()
		wireframe.SetLineWidth(0.0009)
		#wireframe.SetEdgeColorRGB(255,0,0)
		#wireframe.SetInteriorColorRGB(0,0,0)
		wireframe.Setup()

		# # Roughplastic
		self.M1 = MaterialRoughPlastic()
		self.M1.SetDistribution('ggx')
		self.M1.SetDiffuseReflectance(Spectrum(0.60))
		#self.M1.SetColorName(self.colorDitc["skyBlue"])
		self.M1.SetTexture(wireframe)
		self.M1.Setup()

	def CreateMaterail5(self):
		 

		# # Roughplastic
		self.M1 = MaterialRoughPlastic()
		self.M1.SetDistribution('ggx')
		self.M1.SetDiffuseReflectance(Spectrum(0.60))
		#self.M1.SetColorName(self.colorDitc["skyBlue"])		 
		self.M1.Setup()


	def RenderPath1V3(self):
		
		self.List1 = ReadFilesDeep(self.Path1)
		# Process Model #
		for i in range(len(self.List1)):
			MoveToCenterXYZ(self.List1[i], 0, 0, 0)		
			ScaleRatioTo01 = GetRatioTo01(self.List1[i])
			Scale(self.List1[i], ScaleRatioTo01)	
			ConfigOBJ_usemtl(self.List1[i])
			 
			#ConfigOBJ_usemtl(self.List1[i])


		self.CreateMaterail1()


		for i in range(len(self.List1)):
			if os.path.basename(self.List1[i]).split(".")[1] == "obj":
				shape = ModelOBJ()
			elif os.path.basename(self.List1[i]).split(".")[1] == "ply":
				shape = ModelPLY()
			shape.SetToWorldRotate(self.shapeRotateX,self.shapeRotateY, self.shapeRotateZ)
			shape.SetFaceNormals(True)	
			shape.SetFileName(self.List1[i])
			shape.SetMaterial(self.M1)
			self.ImageName = "".join(os.path.basename(self.List1[i]).split(".")[:-1])
			shape.Setup(self.scene)
			#print("fff")




	def RenderPath2(self):



		self.List2 = ReadFilesDeep(self.Path2)
		# Process Model #
		for i in range(len(self.List2)):
			ConfigOBJ_usemtl(self.List2[i])


		self.M2 = MaterialPlastic()
		self.M2.SetColorName(self.colorDitc["red"])
		self.M2.Setup()


		for i in range(len(self.List2)):
			if os.path.basename(self.List2[i]).split(".")[1] == "obj":
				shape = ModelOBJ()
			elif os.path.basename(self.List2[i]).split(".")[1] == "ply":
				shape = ModelPLY()	
			shape.SetToWorldRotate(self.shapeRotateX,self.shapeRotateY, self.shapeRotateZ)	
			shape.SetFileName(self.List2[i])
			shape.SetFaceNormals(True)
			shape.SetMaterial(self.M2)
			shape.Setup(self.scene)


	def RenderPath3(self):



		self.List3= ReadFilesDeep(self.Path3)
		# Process Model #
		for i in range(len(self.List3)):
			ConfigOBJ_usemtl(self.List3[i])


		self.M3 = MaterialPlastic()
		self.M3.SetColorName(self.colorDitc["green"])
		self.M3.Setup()


		for i in range(len(self.List3)):
			if os.path.basename(self.List3[i]).split(".")[1] == "obj":
				shape = ModelOBJ()
			elif os.path.basename(self.List3[i]).split(".")[1] == "ply":
				shape = ModelPLY()		
			shape.SetToWorldRotate(self.shapeRotateX,self.shapeRotateY, self.shapeRotateZ)
			shape.SetFileName(self.List3[i])
			shape.SetFaceNormals(True)
			shape.SetMaterial(self.M3)
			shape.Setup(self.scene)


	def RenderPath4(self):

		self.List4 = ReadFilesDeep(self.Path4)
		# Process Model #
		for i in range(len(self.List4)):
			ConfigOBJ_usemtl(self.List4[i])


		self.M4 = MaterialPlastic()
		self.M4.SetColorName(self.colorDitc["blue"])
		self.M4.Setup()


		for i in range(len(self.List4)):
			if os.path.basename(self.List4[i]).split(".")[1] == "obj":
				shape = ModelOBJ()
			elif os.path.basename(self.List4[i]).split(".")[1] == "ply":
				shape = ModelPLY()		
			shape.SetToWorldRotate(self.shapeRotateX,self.shapeRotateY, self.shapeRotateZ)
			shape.SetFileName(self.List4[i])
			shape.SetFaceNormals(True)
			shape.SetMaterial(self.M4)
			shape.Setup(self.scene)



 	def RenderPath5(self):

		self.List5 = ReadFilesDeep(self.Path5)
		# Process Model #
		for i in range(len(self.List5)):
			ConfigOBJ_usemtl(self.List5[i])


		self.M5 = MaterialPlastic()
		self.M5.SetColorName(self.colorDitc["black"])
		self.M5.Setup()


		for i in range(len(self.List5)):
			if os.path.basename(self.List5[i]).split(".")[1] == "obj":
				shape = ModelOBJ()
			elif os.path.basename(self.List5[i]).split(".")[1] == "ply":
				shape = ModelPLY()		
			shape.SetToWorldRotate(self.shapeRotateX,self.shapeRotateY, self.shapeRotateZ)
			shape.SetFileName(self.List5[i])
			shape.SetMaterial(self.M5)
			shape.Setup(self.scene)




	def RenderPath6(self):

		self.List6 = ReadFilesDeep(self.Path6)
		# Process Model #
		for i in range(len(self.List6)):
			ConfigOBJ_usemtl(self.List6[i])


		self.M6 = MaterialPlastic()
		self.M6.SetColorName(self.colorDitc["black"])
		self.M6.Setup()


		for i in range(len(self.List6)):
			if os.path.basename(self.List6[i]).split(".")[1] == "obj":
				shape = ModelOBJ()
			elif os.path.basename(self.List6[i]).split(".")[1] == "ply":
				shape = ModelPLY()		
			shape.SetToWorldRotate(self.shapeRotateX,self.shapeRotateY, self.shapeRotateZ)
			shape.SetFileName(self.List6[i])
			shape.SetFaceNormals(False)
			shape.SetMaterial(self.M6)
			shape.Setup(self.scene)



	def RenderPath7(self):

		self.List7 = ReadFilesDeep(self.Path7)
		# Process Model #
		for i in range(len(self.List7)):
			ConfigOBJ_usemtl(self.List7[i])


		self.M7 = MaterialPlastic()
		self.M7.SetColorName(self.colorDitc["saddleBrown"])
		self.M7.Setup()


		for i in range(len(self.List7)):
			if os.path.basename(self.List7[i]).split(".")[1] == "obj":
				shape = ModelOBJ()
			elif os.path.basename(self.List7[i]).split(".")[1] == "ply":
				shape = ModelPLY()		
			shape.SetToWorldRotate(self.shapeRotateX,self.shapeRotateY, self.shapeRotateZ)
			shape.SetFileName(self.List7[i])
			shape.SetFaceNormals(False)
			shape.SetMaterial(self.M7)
			shape.Setup(self.scene)

	def RenderPath8(self):

		self.List8 = ReadFilesDeep(self.Path8)
		# Process Model #
		for i in range(len(self.List8)):
			ConfigOBJ_usemtl(self.List8[i])


		self.M8 = MaterialRoughPlastic()
		self.M8.SetDistribution('ggx')
		self.M8.SetDiffuseReflectance(Spectrum(0.70))
		self.M8.SetColorName(self.colorDitc["black"])
		self.M8.Setup()


		for i in range(len(self.List8)):
			if os.path.basename(self.List8[i]).split(".")[1] == "obj":
				shape = ModelOBJ()
			elif os.path.basename(self.List8[i]).split(".")[1] == "ply":
				shape = ModelPLY()		
			shape.SetToWorldRotate(self.shapeRotateX,self.shapeRotateY, self.shapeRotateZ)
			shape.SetFileName(self.List8[i])
			shape.SetFaceNormals(True)
			shape.SetMaterial(self.M8)
			shape.Setup(self.scene)


	def RenderPath9(self):

		self.List9 = ReadFilesDeep(self.Path9)
		# Process Model #
		for i in range(len(self.List9)):
			ConfigOBJ_usemtl(self.List9[i])


		self.M9 = MaterialPlastic()
		self.M9.SetColorName(self.colorDitc["red"])
		self.M9.Setup()


		for i in range(len(self.List9)):
			if os.path.basename(self.List9[i]).split(".")[1] == "obj":
				shape = ModelOBJ()
			elif os.path.basename(self.List9[i]).split(".")[1] == "ply":
				shape = ModelPLY()		
			shape.SetToWorldRotate(self.shapeRotateX,self.shapeRotateY, self.shapeRotateZ)
			shape.SetFileName(self.List9[i])
			shape.SetFaceNormals(False)
			shape.SetMaterial(self.M9)
			shape.Setup(self.scene)

	def RenderPath10(self):

		self.List10 = ReadFilesDeep(self.Path10)
		# Process Model #
		for i in range(len(self.List10)):
			ConfigOBJ_usemtl(self.List10[i])


		self.M10 = MaterialPlastic()
		self.M10.SetColorName(self.colorDitc["green"])
		self.M10.Setup()


		for i in range(len(self.List10)):
			if os.path.basename(self.List10[i]).split(".")[1] == "obj":
				shape = ModelOBJ()
			elif os.path.basename(self.List10[i]).split(".")[1] == "ply":
				shape = ModelPLY()		
			shape.SetToWorldRotate(self.shapeRotateX,self.shapeRotateY, self.shapeRotateZ)
			shape.SetFileName(self.List10[i])
			shape.SetFaceNormals(False)
			shape.SetMaterial(self.M10)
			shape.Setup(self.scene)

	def RenderPath11(self):

		self.List11 = ReadFilesDeep(self.Path11)
		# Process Model #
		for i in range(len(self.List11)):
			ConfigOBJ_usemtl(self.List11[i])


		self.M11 = MaterialPlastic()
		self.M11.SetColorName(self.colorDitc["blue"])
		self.M11.Setup()


		for i in range(len(self.List11)):
			if os.path.basename(self.List11[i]).split(".")[1] == "obj":
				shape = ModelOBJ()
			elif os.path.basename(self.List11[i]).split(".")[1] == "ply":
				shape = ModelPLY()		
			shape.SetToWorldRotate(self.shapeRotateX,self.shapeRotateY, self.shapeRotateZ)
			shape.SetFileName(self.List11[i])
			shape.SetFaceNormals(False)
			shape.SetMaterial(self.M11)
			shape.Setup(self.scene)



	def RenderPath12(self):
		self.CreateMaterail4()
		self.RenderPathCore(self.Path12,self.M1)


	def RenderPathCore(self, pathIndex, mIndex):

		self.curList = ReadFilesDeep(pathIndex)
		# Process Model #
		for i in range(len(self.curList)):
			ConfigOBJ_usemtl(self.curList[i])

 

		for i in range(len(self.curList)):
			if os.path.basename(self.curList[i]).split(".")[1] == "obj":
				shape = ModelOBJ()
			elif os.path.basename(self.curList[i]).split(".")[1] == "ply":
				shape = ModelPLY()		
			shape.SetToWorldRotate(self.shapeRotateX,self.shapeRotateY, self.shapeRotateZ)
			shape.SetFileName(self.curList[i])
			shape.SetFaceNormals(True)
			shape.SetMaterial(mIndex)
			shape.Setup(self.scene)





	def RenderRotateX(self):
		self.shapeRotateX = 0
		self.shapeRotateY = 0
		self.shapeRotateZ = 0
		self.RenderScene()
		for r in range( (360 / self.rotationStepSize) ):
			self.shapeRotateX = self.shapeRotateX + self.rotationStepSize
			self.RenderScene()
		
	def RenderRotateY(self):
		
		self.shapeRotateX = 0
		self.shapeRotateY = 0
		self.shapeRotateZ = 0
		self.RenderScene()
		for r in range( (360 / self.rotationStepSize) ):
			self.shapeRotateY= self.shapeRotateY+ self.rotationStepSize
			self.RenderScene()
		

	def RenderRotateZ(self):		
		
		self.shapeRotateX = 0
		self.shapeRotateY = 0
		self.shapeRotateZ = 0
 		self.RenderScene()
		for r in range( (360 / self.rotationStepSize) ):
			self.shapeRotateZ = self.shapeRotateZ + self.rotationStepSize
			self.RenderScene()
		


	def RenderRotate(self):
		#self.RenderRotateX()
		self.RenderRotateY()
		#self.RenderRotateZ()


	def RenderFolder(self):
		modelList = ReadFilesDeep(self.Path1)

		for i in range(len(modelList)):
			ConfigOBJ_usemtl(modelList[i])
			self.RenderSceneBatch(modelList[i])





	def RenderSceneBatch(self, modelFile): 
		 	#self.modelPath = "Test."
			self.dirOutput = self.PathOutput
			 
 			self.BuildDefaultElementMulti()

			# For testing
			self.film.SetHeight(200)
			self.film.SetWidth(200)
			
  

			self.RenderListPath1(modelFile)
			 

			 
			# shape rotate angle
	 		#self.sensor.SetToWorldLookAt(Point(1.5, 0.5, 2.2), Point(0, 0, 0), Vector(0., 1, 0))
	 		 
			#self.emitter.SetToWorldRotate(-30, 0, 0)
			#self.emitter.SetScale(1.5)
			# Hookup scene
			self.HookUpSceneMulti()

			# Setup image name
		 
			# Setup output file
			 
			self.SetOutputFile(self.ImageName)

			# Start rendering
			self.Render()

	

	

	def RenderScene(self):

 
		 	#self.modelPath = "Test."
			self.dirOutput = self.PathOutput
			 
 			self.BuildDefaultElementMulti()

			# For testing
			self.film.SetHeight(100)
			self.film.SetWidth(100)
			
  
			self.RenderPath1V3()
			#self.RenderPath1()
			
			#self.RenderPath2()
			#self.RenderPath3()
			#self.RenderPath4()

			#self.RenderPath5()
			#self.RenderPath6()


			#self.RenderPath7()
			#self.RenderPath8()


			#self.RenderPath9()
			#self.RenderPath10()
			#self.RenderPath11()

			#self.RenderPath12()

			# shape rotate angle
	 		self.sensor.SetToWorldLookAt(Point(0, 0, 3.5), Point(0, 0, 0), Vector(0., 1, 0))
	 		 
			#self.emitter.SetToWorldRotate(0, 0, 0)
			self.emitter.SetScale(1.6)
			# Hookup scene
			self.HookUpSceneMulti()

			# Setup image name
		 
			# Setup output file
			#self.ImageName = self.ImageName  + '_'+ str(self.uScale) + '_' + str(self.vScale) 
			#self.ImageName=  self.curdir
			#self.ImageName = self.ImageName
			self.SetOutputFile(self.ImageName)

			# Start rendering
			self.Render()

	def ConfigInOut(self, curPath):
		 	self.RootCur=curPath
			self.PathOutput="D:\\demo"
			self.Path1= self.RootCur+"\\Model"
		
			self.Path2=self.RootCur+"\\SolutionArrow\\InitialDirection\\RedEdges"
			self.Path3=self.RootCur+"\\SolutionArrow\\InitialDirection\\GreenEdges"
			self.Path4=self.RootCur+"\\SolutionArrow\\InitialDirection\\BlueEdges"
		
			self.Path5=self.RootCur+"\\cylinder"
			self.Path6=self.RootCur+"\\InnerCylinder"

			self.Path7=self.RootCur+"\\OriginalModel\\OriginalEdges\\AllEdges"
			self.Path8=self.RootCur+"\\tet\\Original\\ZDir\\slice4\\InnerCylinder"

			self.Path9=self.RootCur+"\\ImprovedMapResult\\OriginalFaces\\XPatches"
			self.Path10=self.RootCur+"\\ImprovedMapResult\\OriginalFaces\\YPatches"
			self.Path11=self.RootCur+"\\ImprovedMapResult\\OriginalFaces\\ZPatches"

			self.Path12=self.RootCur+"\\cylinder"
			#self.imageName="Test"
			#print(self.Path1)
			#print(self.Path7)	



	def RenderSceneBatchV2(self):
		dirs=ReadFiles("D:\\render\\polycube\\quad\\PolycubeSpace") 
		print(self.curdir)
		for i in range(len(dirs)):
			#print(dirs[i])
			self.ConfigInOut(dirs[i])
			self.curdir="".join(os.path.basename(dirs[i]).split(".")[:1])
			self.RenderScene()
			

  
	def RenderBatchUV(self):
		 
		for i in range(60):						
			self.RenderScene()
			self.uScale=self.uScale+0.025
			self.vScale=self.vScale+0.025





if __name__ == '__main__':
 
	poly=RenderChernPerfect()

	poly.ConfigInOut("D:\\demo")
	poly.RenderScene()
	#poly.RenderBatchUV()
	#poly.RenderSceneBatchV2()
	 