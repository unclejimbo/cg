import sys
sys.path.append('..\\SceneTask')
sys.path.append('..\\lib')

from DirSetting import *

from Tool.IO import *
from Tool.PrettyColor import *
from Tool.FfmpegWrapper import *
from Tool.ImageMagickWrapper import	*

magick = ImageMagick()
magick.SetMagick("..\\lib\\ThirdPartyExe\\magick.exe")

# ### Six PIC in one PIC ###
# CreatePath("C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\JPG\\append_temp_up")
# CreatePath("C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\JPG\\append_temp_down")
# CreatePath("C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\JPG\\append\\red")

# magick.Run(	"+appendThreeFolder", 
# 			"C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\JPG\\RenderResult_Label\\plane392arapspoke", 
# 			"C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\JPG\\RenderResult_Label\\plane392arapspokerim",
# 			"C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\JPG\\RenderResult_Label\\plane392hybrid",
# 			"C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\JPG\\append_temp_up"
# 			)

# magick.Run(	"+appendThreeFolder", 
# 			"C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\JPG\\RenderResult_Label\\plane1682arapspoke", 
# 			"C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\JPG\\RenderResult_Label\\plane1682arapspokerim",
# 			"C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\JPG\\RenderResult_Label\\plane1682hybrid",
# 			"C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\JPG\\append_temp_down"
# 			)

# magick.Run(	"-appendFolder", 
# 			"C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\JPG\\append_temp_up", 
# 			"C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\JPG\\append_temp_down",
# 			"C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\JPG\\append\\red"
# 			)


# CreatePath("C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\PNG\\append_temp_up")
# CreatePath("C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\PNG\\append_temp_down")
# CreatePath("C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\PNG\\append\\red")

# magick.Run(	"+appendThreeFolder", 
# 			"C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\PNG\\RenderResult_Label\\plane392arapspoke", 
# 			"C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\PNG\\RenderResult_Label\\plane392arapspokerim",
# 			"C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\PNG\\RenderResult_Label\\plane392hybrid",
# 			"C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\PNG\\append_temp_up"
# 			)

# magick.Run(	"+appendThreeFolder", 
# 			"C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\PNG\\RenderResult_Label\\plane1682arapspoke", 
# 			"C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\PNG\\RenderResult_Label\\plane1682arapspokerim",
# 			"C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\PNG\\RenderResult_Label\\plane1682hybrid",
# 			"C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\PNG\\append_temp_down"
# 			)

# magick.Run(	"-appendFolder", 
# 			"C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\PNG\\append_temp_up", 
# 			"C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\PNG\\append_temp_down",
# 			"C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\PNG\\append\\red"
# 			)

### Three PIC in one PIC ###
CreatePath("C:\\Users\\soapk\\Desktop\\NoTrimVersion\\Checkboard\\JPG\\Euclidean\\Torus\\3Duv\\append\\red")
magick.Run(	"+appendThreeFolder", 
			"C:\\Users\\soapk\\Desktop\\NoTrimVersion\\Checkboard\\JPG\\Euclidean\\Torus\\3Duv\\RenderResult_Label\\calabi", 
			"C:\\Users\\soapk\\Desktop\\NoTrimVersion\\Checkboard\\JPG\\Euclidean\\Torus\\3Duv\\RenderResult_Label\\cetm",
			"C:\\Users\\soapk\\Desktop\\NoTrimVersion\\Checkboard\\JPG\\Euclidean\\Torus\\3Duv\\RenderResult_Label\\ricci",
			"C:\\Users\\soapk\\Desktop\\NoTrimVersion\\Checkboard\\JPG\\Euclidean\\Torus\\3Duv\\append\\red"
			)

# CreatePath("C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\PNG\\append\\red")
# magick.Run(	"+appendThreeFolder", 
# 			"C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\PNG\\RenderResult_Label\\bumplane0", 
# 			"C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\PNG\\RenderResult_Label\\bumplane1",
# 			"C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\PNG\\RenderResult_Label\\bumplane2",
# 			"C:\\Users\\soapk\\OneDrive\\xuke\\Mitsuba\\Output\\Deform\\wrinklePlane\\PNG\\append\\red"
# 			)