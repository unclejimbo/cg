import sys
sys.path.append('..\\SceneTask')
sys.path.append('..\\lib')

from DirSetting import *

from Tool.IO import *
from Tool.PrettyColor import *
from Tool.FfmpegWrapper import *
from Tool.ImageMagickWrapper import	*

# For Labeling JPG
magick = ImageMagick()
magick.SetMagick("..\\lib\\ThirdPartyExe\\magick.exe")

# # One
# oneLabel = Label()
# oneLabel.SetBackgroundColor("None")
# oneLabel.SetLabel("Figure 10: Bar Twist and Rotation by the hybrid mode")

# CreatePath("C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\PNG\\RenderResult_Label")
# magick.Run(	"addLabelFolder", 
# 			"C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\PNG\\append\\red", 
# 			"C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\PNG\\RenderResult_Label", 
# 			oneLabel
# 			)

# oneLabel.SetBackgroundColor("White")

# CreatePath("C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\JPG\\RenderResult_Label")
# magick.Run(	"addLabelFolder", 
# 			"C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\JPG\\append\\red", 
# 			"C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\JPG\\RenderResult_Label", 
# 			oneLabel
# 			)

# One
oneLabel = Label()
oneLabel.SetBackgroundColor("None")
oneLabel.SetLabel("Calabi")

# CreatePath("C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\PNG\\RenderResult_Label\\plane392arapspoke")
# magick.Run(	"addLabelFolder", 
# 			"C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\PNG\\RenderResult\\plane392arapspoke", 
# 			"C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\PNG\\RenderResult_Label\\plane392arapspoke", 
# 			oneLabel
# 			)

oneLabel.SetBackgroundColor("White")

CreatePath("C:\\Users\\soapk\\Desktop\\NoTrimVersion\\Checkboard\\JPG\\Euclidean\\Torus\\3Duv\\RenderResult_Label\\calabi")
magick.Run(	"addLabelFolder", 
			"C:\\Users\\soapk\\Desktop\\NoTrimVersion\\Checkboard\\JPG\\Euclidean\\Torus\\3Duv\\RenderResult\\calabi", 
			"C:\\Users\\soapk\\Desktop\\NoTrimVersion\\Checkboard\\JPG\\Euclidean\\Torus\\3Duv\\RenderResult_Label\\calabi", 
			oneLabel
			)

# Two
twoLabel = Label()
twoLabel.SetBackgroundColor("None")
twoLabel.SetLabel("CETM")

# CreatePath("C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\PNG\\RenderResult_Label\\plane392arapspokerim")
# magick.Run(	"addLabelFolder", 
# 			"C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\PNG\\RenderResult\\plane392arapspokerim", 
# 			"C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\PNG\\RenderResult_Label\\plane392arapspokerim", 
# 			twoLabel
# 			)

twoLabel.SetBackgroundColor("White")

CreatePath("C:\\Users\\soapk\\Desktop\\NoTrimVersion\\Checkboard\\JPG\\Euclidean\\Torus\\3Duv\\RenderResult_Label\\cetm")
magick.Run(	"addLabelFolder", 
			"C:\\Users\\soapk\\Desktop\\NoTrimVersion\\Checkboard\\JPG\\Euclidean\\Torus\\3Duv\\RenderResult\\cetm", 
			"C:\\Users\\soapk\\Desktop\\NoTrimVersion\\Checkboard\\JPG\\Euclidean\\Torus\\3Duv\\RenderResult_Label\\cetm", 
			twoLabel
			)

# Three
threeLabel = Label()
threeLabel.SetBackgroundColor("None")
threeLabel.SetLabel("RICCI")

# CreatePath("C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\PNG\\RenderResult_Label\\plane392hybrid")
# magick.Run(	"addLabelFolder", 
# 			"C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\PNG\\RenderResult\\plane392hybrid", 
# 			"C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\PNG\\RenderResult_Label\\plane392hybrid", 
# 			threeLabel
# 			)

threeLabel.SetBackgroundColor("White")

CreatePath("C:\\Users\\soapk\\Desktop\\NoTrimVersion\\Checkboard\\JPG\\Euclidean\\Torus\\3Duv\\RenderResult_Label\\ricci")
magick.Run(	"addLabelFolder", 
			"C:\\Users\\soapk\\Desktop\\NoTrimVersion\\Checkboard\\JPG\\Euclidean\\Torus\\3Duv\\RenderResult\\ricci", 
			"C:\\Users\\soapk\\Desktop\\NoTrimVersion\\Checkboard\\JPG\\Euclidean\\Torus\\3Duv\\RenderResult_Label\\ricci", 
			threeLabel
			)

# # Four
# fourLabel = Label()
# fourLabel.SetBackgroundColor("None")
# fourLabel.SetLabel("(d) ARAP Spoke 1682")

# CreatePath("C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\PNG\\RenderResult_Label\\plane1682arapspoke")
# magick.Run(	"addLabelFolder", 
# 			"C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\PNG\\RenderResult\\plane1682arapspoke", 
# 			"C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\PNG\\RenderResult_Label\\plane1682arapspoke", 
# 			fourLabel
# 			)

# fourLabel.SetBackgroundColor("White")

# CreatePath("C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\JPG\\RenderResult_Label\\plane1682arapspoke")
# magick.Run(	"addLabelFolder", 
# 			"C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\JPG\\RenderResult\\plane1682arapspoke", 
# 			"C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\JPG\\RenderResult_Label\\plane1682arapspoke", 
# 			fourLabel
# 			)

# # Five
# fiveLabel = Label()
# fiveLabel.SetBackgroundColor("None")
# fiveLabel.SetLabel("(e) Spoke-Rim 1682")

# CreatePath("C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\PNG\\RenderResult_Label\\plane1682arapspokerim")
# magick.Run(	"addLabelFolder", 
# 			"C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\PNG\\RenderResult\\plane1682arapspokerim", 
# 			"C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\PNG\\RenderResult_Label\\plane1682arapspokerim", 
# 			fiveLabel
# 			)

# fiveLabel.SetBackgroundColor("White")

# CreatePath("C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\JPG\\RenderResult_Label\\plane1682arapspokerim")
# magick.Run(	"addLabelFolder", 
# 			"C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\JPG\\RenderResult\\plane1682arapspokerim", 
# 			"C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\JPG\\RenderResult_Label\\plane1682arapspokerim", 
# 			fiveLabel
# 			)

# # Six
# sixLabel = Label()
# sixLabel.SetBackgroundColor("None")
# sixLabel.SetLabel("(f) Hybrid 1682")

# CreatePath("C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\PNG\\RenderResult_Label\\plane1682hybrid")
# magick.Run(	"addLabelFolder", 
# 			"C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\PNG\\RenderResult\\plane1682hybrid", 
# 			"C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\PNG\\RenderResult_Label\\plane1682hybrid", 
# 			sixLabel
# 			)

# sixLabel.SetBackgroundColor("White")

# CreatePath("C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\JPG\\RenderResult_Label\\plane1682hybrid")
# magick.Run(	"addLabelFolder", 
# 			"C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\JPG\\RenderResult\\plane1682hybrid", 
# 			"C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\JPG\\RenderResult_Label\\plane1682hybrid", 
# 			sixLabel
# 			)