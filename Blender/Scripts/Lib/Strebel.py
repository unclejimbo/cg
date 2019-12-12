from matplotlib import cm
from PIL import Image, ImageDraw
import numpy as np
import math
from PIL import ImagePath, ImageFont
import os
import sys
import shutil


class Strebel:
    def __init__(self):
        self.size = 1000
        self.colormap_name = "jet"
        self.number = 10
        self.line_width = 2
        self.line_color_x = ["#FF4081"]
        self.line_color_y = ["#FF4081"]
        self.image_color = "white"
        self.critical_line_color_x = "red"
        self.critical_line_color_y = "black"
        self.critical_color_x = "red"
        self.critical_color_y = "black"
        self.checkerboard_colors = ["white", "black"]
        self.checkerboard_linecolors = ["red", "red", "green", "green"]
        self.checkerboard_linewidth = 10
        self.circle_color = "black"
        self.line_number = 6
        self.circle_line_width = 5

        path = os.getcwd()
        path = os.path.dirname(path)
        path = os.path.dirname(path)
        dir = path + "/Output/Strebel/"
        self.output_path = dir
        if not os.path.exists(dir):
            os.makedirs(dir)


    def Colormap(self):
        size = self.size
        image = Image.new("RGB", (size, size))
        draw = ImageDraw.Draw(image)
        rg = range(size)
        cmap = cm.get_cmap(self.colormap_name)
        mapper = cm.ScalarMappable(cmap=cmap)
        colors = mapper.to_rgba(rg, bytes=True)
        for x, c in zip(rg, colors):
            draw.line([x, 0, x, size - 1], fill=tuple(c[0:3]))
        image.save(self.output_path + "Colormap_" + self.colormap_name + '.png')
        return image

    def ColormapQuantized(self):
        image = Image.new("RGB", (self.size, self.size))
        draw = ImageDraw.Draw(image)
        rg = range(self.number)
        cmap = cm.get_cmap(self.colormap_name)
        mapper = cm.ScalarMappable(cmap=cmap)
        colors = mapper.to_rgba(rg, bytes=True)
        width = self.size / self.number
        for x, c in zip(rg, colors):
            draw.rectangle([x * width, 0, (x + 1) * width, self.size-1], fill=tuple(c[0:3]))
        image.save(self.output_path + "ColormapQuantized_" + self.colormap_name + '.png')
        return image

    def ColormapSym(self):
        image = Image.new("RGB", (self.size, self.size))
        draw = ImageDraw.Draw(image)
        half = int(self.size / 2)
        rg = range(half)
        cmap = cm.get_cmap(self.colormap_name)
        mapper = cm.ScalarMappable(cmap=cmap)
        colors = mapper.to_rgba(rg, bytes=True)
        for x, c in zip(rg, colors):
            draw.line([x, 0, x, self.size - 1], fill=tuple(c[0:3]))
        colors = colors[::-1]
        for x, c in zip(rg, colors):
            draw.line([x + half, 0, x + half, self.size - 1], fill=tuple(c[0:3]))
        draw.line([(half, 0), (half, self.size - 1)], fill="black", width=2)
        image.save(self.output_path + "ColormapSym_" + self.colormap_name + '.png')
        return image

    def ColormapQuantizedSym(self):
        image = Image.new("RGB", (self.size, self.size))
        draw = ImageDraw.Draw(image)
        rg = range(self.number)
        cmap = cm.get_cmap(self.colormap_name)
        mapper = cm.ScalarMappable(cmap=cmap)
        colors = mapper.to_rgba(rg, bytes=True)
        width = self.size / (2 * self.number)
        for x, c in zip(rg, colors):
            draw.rectangle([x * width, 0, (x + 1) * width, self.size - 1], fill=tuple(c[0:3]))
        half = int(self.size / 2)
        colors = colors[::-1]
        for x, c in zip(rg, colors):
            draw.rectangle([x * width + half, 0, (x + 1) * width + half, self.size - 1], fill=tuple(c[0:3]))
        draw.line([(half, 0), (half, self.size - 1)], fill="black", width=2)
        image.save(self.output_path + "ColormapQuantizedSym_" + self.colormap_name + '.png')
        return image

    def CriticalLine(self):
        image = Image.new("RGB", (self.size, self.size), color = self.image_color)
        draw = ImageDraw.Draw(image)

        self.DrawCriticalLineX(draw)
        self.DrawCriticalLineY(draw)
        return image

    def CriticalLineV2(self):
        image = Image.new("RGB", (self.size, self.size), color = self.image_color)
        draw = ImageDraw.Draw(image)

        self.DrawCriticalLineXV2(draw)
        self.DrawCriticalLineYV2(draw)
        return image

    def CriticalLineX(self):
        image = Image.new("RGB", (self.size, self.size), color = self.image_color)
        draw = ImageDraw.Draw(image)

        self.DrawCriticalLineXV2(draw)
        return image

    def CriticalLineY(self):
        image = Image.new("RGB", (self.size, self.size), color = self.image_color)
        draw = ImageDraw.Draw(image)

        self.DrawCriticalLineYV2(draw)
        return image

    def LineAngle(self):
        image = Image.new("RGB", (self.size, self.size), color = self.image_color)
        draw = ImageDraw.Draw(image)

        draw.line([(0, 0), (self.size - 200, self.size - 1)], fill="red", width=self.line_width)

        self.DrawCriticalLineXV2(draw)
        self.DrawCriticalLineYV2(draw)
        return image

    def CheckerboardV1(self):
        colors = self.checkerboard_colors

        image = Image.new("RGB", (self.size, self.size))
        draw = ImageDraw.Draw(image)

        width = self.size / self.number

        for i in range(self.number):
            for j in range(self.number):
                color = colors[(i + j) % 2]
                corners = [width * i, width * j, width * (i + 1), width * (j + 1)]
                draw.rectangle(corners, fill=color)
        path = self.output_path + "checkerboard_v1"
        if not os.path.exists(path):
            os.makedirs(path)
        image.save(self.output_path + "checkerboard_v1/checkerboard_v1_" + self.checkerboard_colors[0] +
                   "_" + self.checkerboard_colors[1] + "_" + str(self.number) + '.png')
        return image

    def CheckerboardV1_white(self):
        colors = self.checkerboard_colors
        colors[1] = "#ffffff"

        image = Image.new("RGB", (self.size, self.size))
        draw = ImageDraw.Draw(image)

        width = self.size / self.number

        for i in range(self.number):
            for j in range(self.number):
                color = colors[(i + j) % 2]
                corners = [width * i, width * j, width * (i + 1), width * (j + 1)]
                draw.rectangle(corners, fill=color)
        path = self.output_path + "checkerboard_v1_white"
        if not os.path.exists(path):
            os.makedirs(path)
        image.save(self.output_path + "checkerboard_v1_white/checkerboard_v1_" + self.checkerboard_colors[0] +
                   "_" + self.checkerboard_colors[1] + "_" + str(self.number) + '.png')
        return image

    def CheckerboardV2(self):
        size = self.size
        colorsLine = self.checkerboard_linecolors
        widthline = self.checkerboard_linewidth

        colors = self.checkerboard_colors

        image = Image.new("RGB", (self.size, self.size))
        draw = ImageDraw.Draw(image)

        width = self.size / self.number

        for i in range(self.number):
            for j in range(self.number):
                color = colors[(i + j) % 2]
                corners = [width * i, width * j, width * (i + 1), width * (j + 1)]
                draw.rectangle(corners, fill=color)

        draw = ImageDraw.Draw(image)
        draw.line([(0, 0), (0, size - 1)], fill=colorsLine[0], width=widthline)
        draw.line([(size - 1, 0), (size - 1, size - 1)], fill=colorsLine[1], width=widthline)
        draw.line([(0, 0), (size - 1, 0)], fill=colorsLine[2], width=widthline)
        draw.line([(0, size - 1), (size - 1, size - 1)], fill=colorsLine[3], width=widthline)

        path = self.output_path + "checkerboard_v2"
        if not os.path.exists(path):
            os.makedirs(path)

        image.save(self.output_path + "checkerboard_v2/checkerboard_v2_" + self.checkerboard_colors[0] +
                   "_" + self.checkerboard_colors[1] + "_" + str(self.number) + '.png')
        return image

    def CheckerboardV2_white(self):
        size = self.size
        colorsLine = self.checkerboard_linecolors
        widthline = self.checkerboard_linewidth

        colors = self.checkerboard_colors
        colors[1] = "#ffffff"

        image = Image.new("RGB", (self.size, self.size))
        draw = ImageDraw.Draw(image)

        width = self.size / self.number

        for i in range(self.number):
            for j in range(self.number):
                color = colors[(i + j) % 2]
                corners = [width * i, width * j, width * (i + 1), width * (j + 1)]
                draw.rectangle(corners, fill=color)

        draw = ImageDraw.Draw(image)
        draw.line([(0, 0), (0, size - 1)], fill=colorsLine[0], width=widthline)
        draw.line([(size - 1, 0), (size - 1, size - 1)], fill=colorsLine[1], width=widthline)
        draw.line([(0, 0), (size - 1, 0)], fill=colorsLine[2], width=widthline)
        draw.line([(0, size - 1), (size - 1, size - 1)], fill=colorsLine[3], width=widthline)

        path = self.output_path + "checkerboard_v2_white"
        if not os.path.exists(path):
            os.makedirs(path)

        image.save(self.output_path + "checkerboard_v2_white/checkerboard_v2_" + self.checkerboard_colors[0] +
                   "_" + self.checkerboard_colors[1] + "_" + str(self.number) + '.png')
        return image


    def DrawCriticalLineXV2(self, draw):
        draw.line([(0, 0), (0, self.size - 1)], fill=self.critical_line_color_x, width=self.line_width)
        draw.line([(self.size - 1, 0), (self.size - 1, self.size - 1)], fill="cyan", width=self.line_width)

    def DrawCriticalLineYV2(self, draw):
        draw.line([(0, 0), (self.size - 1, 0)], fill=self.critical_line_color_y, width=self.line_width)
        draw.line([(0, self.size - 1), (self.size - 1, self.size - 1)], fill="magenta", width=self.line_width)

    def DrawCriticalLineX(self, draw):
        draw.line([(0, 0), (0, self.size - 1)], fill=self.critical_line_color_x, width=self.line_width)
        draw.line([(self.size - 1, 0), (self.size - 1, self.size - 1)], fill=self.critical_line_color_x, width=self.line_width)

    def DrawCriticalLineY(self, draw):
        draw.line([(0, 0), (self.size - 1, 0)], fill=self.critical_line_color_y, width=self.line_width)
        draw.line([(0, self.size - 1), (self.size - 1, self.size - 1)], fill=self.critical_line_color_y, width=self.line_width)

    def CircleV1(self):
        n = self.number
        size = self.size * 2
        color = self.circle_color
        bgColor = self.image_color
        image = Image.new("RGB", (size, size), bgColor)
        draw = ImageDraw.Draw(image)
        width = (size / n)
        for i in range(n):
            for j in range(n):
                corners = [width * i, width * j, width * (i + 1), width * (j + 1)]
                draw.arc(corners, 0, 360, fill=color, width = self.circle_line_width)

        draw.line([(0, 0), (0, size - 1)], fill="red", width=1)
        draw.line([(size - 1, 0), (size - 1, size - 1)], fill="red", width=1)

        path = self.output_path + "circle_v1"
        if not os.path.exists(path):
            os.makedirs(path)
        image.save(self.output_path + "circle_v1/circle_v1_" + self.circle_color + "_" + self.image_color + '.png')
        return image

    def CircleV2(self):
        n = self.number
        size = self.size * 2
        color = self.circle_color
        bgColor = self.image_color
        outline = "orange"
        image = Image.new("RGB", (size, size), bgColor)
        draw = ImageDraw.Draw(image)
        width = size / n
        for i in range(n):
            for j in range(n):
                corners = [width * i, width * j, width * (i + 1), width * (j + 1)]
                draw.ellipse(corners, fill=color, outline=outline)

        draw.line([(0, 0), (0, size - 1)], fill="red", width=1)
        draw.line([(size - 1, 0), (size - 1, size - 1)], fill="red", width=1)

        path = self.output_path + "circle_v2"
        if not os.path.exists(path):
            os.makedirs(path)
        image.save(self.output_path + "circle_v2/circle_v2_" + self.circle_color + "_" + self.image_color + '.png')
        return image

    def LinesBasicX(self, draw):
        n = self.line_number
        size = self.size
        widthline = self.line_width * 3
        colorCritical = self.critical_color_x
        lineColors = self.line_color_x

        interval = size / n
        start = 1
        end = n
        xs = np.linspace(start, end, n - 1, False)
        for x, c in zip(xs, lineColors):
            draw.line([(x * interval - 1, 0), (x * interval - 1, size - 1)], fill=c, width=widthline)

        draw.line([(0, 0), (0, size - 1)], fill=colorCritical, width=widthline)
        draw.line([(size - 1, 0), (size - 1, size - 1)], fill=colorCritical, width=widthline)

    def LinesX(self):
        image = Image.new("RGB", (self.size, self.size), self.image_color)
        draw = ImageDraw.Draw(image)
        self.LinesBasicX(draw)
        image.save(self.output_path + "linesx_" + self.critical_color_x + '.png')
        return image

    def LinesBasicY(self, draw):
        n = self.line_number
        size = self.size
        widthline = self.line_width * 3
        colorCritical = self.critical_color_y
        lineColors = self.line_color_y

        interval = size / n
        start = 1
        end = n
        xs = np.linspace(start, end, n - 1, False)
        for x, c in zip(xs, lineColors):
            draw.line([(0, x * interval - 1), (size - 1, x * interval - 1)], fill=c, width=widthline)

        draw.line([(0, 0), (size - 1, 0)], fill=colorCritical, width=widthline)
        draw.line([(0, size - 1), (size - 1, size - 1)], fill=colorCritical, width=widthline)

    def LinesY(self):
        image = Image.new("RGB", (self.size, self.size), self.image_color)
        draw = ImageDraw.Draw(image)
        self.LinesBasicY(draw)
        image.save(self.output_path + "linesy_" + self.critical_color_y + '.png')
        return image

    def LinesXY(self, file_number):
        image = Image.new("RGB", (self.size, self.size), self.image_color)
        draw = ImageDraw.Draw(image)
        self.LinesBasicX(draw)
        self.LinesBasicY(draw)

        path = self.output_path + "lines_xy"
        if not os.path.exists(path):
            os.makedirs(path)
        image.save(self.output_path + "lines_xy/linesxy_" + str(file_number) + ".png")
        return image

    def rgba2hex(self, color):
        color_hex = '#%02x%02x%02x' % (int(color[0]*255),int(color[1]*255),int(color[2]*255))
        return color_hex

    def GridLetter(self):
        number = self.number
        image = Image.new("RGB", (self.size, self.size), self.image_color)
        draw = ImageDraw.Draw(image)
        width = self.size / number
        cmap = cm.get_cmap("tab20")
        for i in range(number):
            for j in range(number):
                corners = [(j) * width, (i) * width, (j+1) * width, (i+1) * width]
                color = self.rgba2hex(cmap(0.05+i*0.05 + j * 0.05))
                print(color)
                draw.rectangle(corners, fill=color)
                font = ImageFont.truetype("arial.ttf", 50)
                msg = chr(65+i)+str(j)
                w, h = font.getsize(msg)
                print("w",w,"h",h)
                draw.text(((j) * width+h/2, (i) * width+w/2), msg, font=font,align='center')
            # for j in range(number):
        image.save("test.png")
        img_2 = image.transpose(Image.FLIP_LEFT_RIGHT)
        img_2.save("test2.png")


# if __name__ == '__main__':
#     strebel = Strebel()
#     strebel.GridLetter()













