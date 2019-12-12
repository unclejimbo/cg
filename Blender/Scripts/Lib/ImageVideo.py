import os
import sys
sys.path.append("..")
from PIL import Image
import cv2
import imageio

class TaskImageVideo():
    def __init__(self):
        path = os.getcwd()
        path = os.path.dirname(path)
        path = os.path.dirname(path)
        self.ImageInput = path + "/Output/"
        self.PngPath = self.ImageInput + "Png/"
        self.JpgPath = self.ImageInput + "Jpg/"
        self.CropPath = self.ImageInput + "Crop/"
        self.VideoOutput = self.ImageInput + "video/"
        # self.PngPath = path + "\Output\\Png\\"
        # self.JpgPath = path + "\Output\\Jpg\\"
        # self.CropPath = path + "\Output\\Crop\\"
        # self.VideoOutput = path + "\Output\\video\\"

        self.VideoName = 'result'
        self.ffmpegPath = 'D://FFmpeg/ffmpeg/bin/ffmpeg.exe'
        self.framerate = 2
        self.pixel_format = "yuv420p"
        self.input_format = "image_%03d.jpg"

    def Rename(self):
        self.PngPath = self.ImageInput + "Png/"
        if not os.path.exists(self.PngPath):
            os.makedirs(self.PngPath)

        # rename
        f_list = os.listdir(self.ImageInput)
        idx = 0
        for index, filename in enumerate(f_list):
            if os.path.splitext(filename)[1] == '.png':
                img = Image.open(self.ImageInput + filename)
                output_name = self.PngPath + "image_%03d" % (idx) + ".png"
                img.save(output_name)
                # os.remove(self.ImageInput + filename)
                idx += 1

    #                 os.rename(self.ImageInput+filename, output_name)

    def PreProcessing(self):
        self.JpgPath = self.ImageInput + "Jpg/"
        self.CropPath = self.ImageInput + "Crop/"
        if not os.path.exists(self.JpgPath):
            os.makedirs(self.JpgPath)
        if not os.path.exists(self.CropPath):
            os.makedirs(self.CropPath)

        # rename and conver to jpg
        f_list = os.listdir(self.PngPath)
        for filename in f_list:
            if os.path.splitext(filename)[1] == '.png':
                # read image
                img = Image.open(self.PngPath + filename)
                # rename
                output_name = self.JpgPath + os.path.splitext(filename)[0] + '.jpg'
                # conver to jpg
                img_rgb = Image.new("RGB", img.size, (255, 255, 255))
                img_rgb.paste(img, mask=img.split()[3])
                img_rgb.save(output_name)
                # img_rgb = img.convert('RGB')
                # img_rgb.save(output_name)

    def CropImage(self):
        self.JpgPath = self.ImageInput + "Jpg/"
        self.CropPath = self.ImageInput + "Crop/"
        if not os.path.exists(self.JpgPath):
            os.makedirs(self.JpgPath)
        if not os.path.exists(self.CropPath):
            os.makedirs(self.CropPath)
        # crop image/remove white background
        # read from jpg file
        f_list = os.listdir(self.JpgPath)
        for filename in f_list:
            # read image
            img = cv2.imread(self.JpgPath + filename)
            # convert to gray, and threshold
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            th, threshed = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
            # Morph-op to remove noise
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
            morphed = cv2.morphologyEx(threshed, cv2.MORPH_CLOSE, kernel)
            # find th max-area contour
            cnts = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
            cnt = sorted(cnts, key=cv2.contourArea)[-1]
            # crop and save it
            x, y, w, h = cv2.boundingRect(cnt)
            dst = img[y:y + h, x:x + w]
            cv2.imwrite(self.CropPath + filename, dst)

    def ProduceVideo(self):
        self.VideoOutput = self.ImageInput + "video/"
        if not os.path.exists(self.VideoOutput):
            os.makedirs(self.VideoOutput)

        ### ProduceVideo ###
        cmd = self.ffmpegPath + " -y -r " + str(self.framerate) + " -i " + \
              self.JpgPath + self.input_format + " -c:v libx264" + \
              " -pix_fmt " + self.pixel_format + " " + self.VideoOutput + self.VideoName + ".mp4"

        # cmd = self.ffmpegPath + " -y -r " + str(self.framerate) + " -i " + \
        #       self.JpgPath + self.input_format + \
        #       " -pix_fmt " + self.pixel_format + " " + self.VideoOutput + self.VideoName + ".mp4"
        os.system(cmd)
        print("write done")

    def ProduceVideo_2(self):
        self.VideoOutput = self.ImageInput + "video/"
        if not os.path.exists(self.VideoOutput):
            os.makedirs(self.VideoOutput)
        video_path = self.VideoOutput + self.VideoName + ".mp4"
        writer = imageio.get_writer(video_path, mode="I", fps=self.framerate)
        f_list = os.listdir(self.JpgPath)
        for i in range(len(f_list)):
            filename = self.JpgPath + "/" + self.input_format%(i)
            writer.append_data(imageio.imread(filename))
        writer.close()
        print("write done")

