import os
import sys
sys.path.append("..")
from PIL import Image, ImageDraw, ImageFont
import cv2
import imageio

class TaskImageVideo():
    def __init__(self):
        path = os.getcwd()
        path = os.path.dirname(path)
        path = os.path.dirname(path)
        path = os.path.dirname(path)
        self.ImageInput = path + "/Output/"
        self.PngPath = self.ImageInput + "Png/"
        self.JpgPath = self.ImageInput + "Jpg/"
        self.CropPath = self.ImageInput + "Crop/"
        self.VideoOutput = self.ImageInput + "video/"
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

                draw = ImageDraw.Draw(img)
                width, height = img.size
                font = ImageFont.truetype("arial.ttf", 50)
                draw.text((100, height-100), os.path.splitext(filename)[0], font=font, fill="#ff0000")
                img.save(output_name)

                # save another Jpg file
                jpg_path = self.ImageInput + "Jpg2/"
                if not os.path.exists(jpg_path):
                    os.makedirs(jpg_path)
                output_name_2 = jpg_path + os.path.splitext(filename)[0] + '.jpg'
                img_rgb = Image.new("RGB", img.size, (255, 255, 255))
                img_rgb.paste(img, mask=img.split()[3])
                img_rgb.save(output_name_2)
                # os.remove(self.ImageInput + filename)
                idx += 1

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
        jpg_path = self.ImageInput + "Jpg2/"
        self.CropPath = self.ImageInput + "Crop/"
        if not os.path.exists(jpg_path):
            os.makedirs(jpg_path)
        if not os.path.exists(self.CropPath):
            os.makedirs(self.CropPath)
        # crop image/remove white background
        # read from jpg file
        f_list = os.listdir(jpg_path)
        for filename in f_list:
            # read image
            img = cv2.imread(jpg_path + filename)
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

    def ProduceCompositeVideo(self, path1, path2, output_path):
        f_list1 = os.listdir(path1)
        f_list1.sort(key=lambda a: os.stat(path1 + "/" + a).st_ctime)
        f_list2 = os.listdir(path2)
        count = 0
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        for filename in f_list1:
            if filename in f_list2:
                # image compose
                img1 = Image.open(path1+filename)
                img2 = Image.open(path2+filename)
                size1 = img1.size
                size2 = img2.size
                joint = Image.new('RGB', (size1[0] + size2[0], size1[1]))
                loc1, loc2 = (0, 0), (size1[0], 0)
                joint.paste(img1, loc1)
                joint.paste(img2, loc2)
                output = output_path + "image_%03d"%(count) + ".jpg"
                joint.save(output)
                count += 1
        # generate video
        cmd = self.ffmpegPath + " -y -r " + str(self.framerate) + " -i " + \
              output_path + "image_%03d.jpg" + " -c:v libx264" + \
              " -pix_fmt " + self.pixel_format + " " + output_path + self.VideoName + ".mp4"
        os.system(cmd)
        print("write done")

