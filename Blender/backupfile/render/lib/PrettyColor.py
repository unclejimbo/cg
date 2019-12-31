class PrettyColor():

	def __init__(self):
		self.colorDitc = {
		# Pink
		'pink': 			[255, 192, 203],
		'lightpink':		[255, 174, 185],
		'hotpink':			[255, 105, 180],

		# Purple
		'magenta':			[255, 0, 255],
		'darkorchid':		[191, 62, 255],
		'purple':			[128, 0, 128],
		'indigo':			[75, 0, 130],
		'mediumPurple':		[147, 112, 219],

		# Blue
		'blue':				[0, 0, 255],
		'slateblue':		[122, 103, 238],
		'navy':				[0, 0, 128],
		'royalBlue':		[100, 149, 237],
		'lightSteelBlue':	[176, 196, 222],
		'aliceBlue':		[240, 248, 255],
		'skyBlue':			[135, 206, 250],
		'deepSkyBlue':		[0, 191, 255],

		# Green
		'cyan':				[0, 255, 255],
		'turquoise':		[64, 224, 208],
		'mintCream':		[0, 255, 127],
		'green':			[0, 255, 0],
		'darjGreen':		[0, 128, 0],
		'lawnGreen':		[124, 252, 0],
		'olivedrab':		[107, 142, 35],
		
		# Yellow
		'yellow':			[255, 255, 0],
		'darkKhaki':		[189, 183, 107],
		'khaki':			[240, 230, 140],
		'gold':				[255, 215, 0],
		'orange':			[255, 165, 0],
		'lightOrange': 		[230, 150, 60],
		'darkOrange':		[255, 140, 0],

		# Brown
		'peachPuff':		[255, 218, 185],
		'chocolate':		[210, 105, 30],
		'saddleBrown':		[139, 69, 19],
		'tomato':			[255, 99, 71],
		'salmon':			[250, 128, 114],

		# White
		'snow':				[255, 250, 250],
		'black':			[0, 0, 0],
		'white':			[255, 255, 255],

		# Red
		'red':				[255, 0, 0],
		'brown':			[165, 42, 42],
		'darkRed':			[139, 0, 0],
		'firebrick3':		[205, 38, 38]
		}

	def getBestColor(self):
		pass

	def getColorDitc(self):
		return self.colorDitc

# test = PrettyColor()
# print(len(test.colorDitc))