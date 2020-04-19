#! /usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import os
import random
import numpy as np
from PIL import ImageFont, Image, ImageDraw
import font, background, text


class Generate(object):
    def __init__(self, background, font, text):
        self.Background = background
        self.Font = font
        self.Text = text

    def random_image(self):
        image = self.Background.get_random_image()
        draw_table = ImageDraw.Draw(im=image)
        return draw_table, image.size, image

    def make_image(self):
        draw, draw_shape, image = self.random_image()
        font_set, font = self.Font.get_random_font()
        text = self.Text.get_random_text(font_set)
        txt_w, txt_h = font.getsize(text)
        offset_x, offset_y = font.getoffset(text)
        draw_w, draw_h = draw_shape[:2]
        draw_h = draw_h // 2
        draw_w = draw_w // 2
        print(draw_h, draw_w)
        start_x = draw_w + random.randint(4, 8)
        start_y = draw_h + random.randint(1, 3)
        draw.text(xy=(start_x, start_y), text=text, fill='#000000', font=font)
        # self.show(image)
        image = np.array(image)
        origin_point = self.get_origin_point(txt_w, txt_h, offset_x, offset_y, start_x, start_y)
        image, rotation_point = self.rotation(image, txt_w, txt_h, offset_x, offset_y, start_x, start_y)
        # self.draw_four_vectors(image, origin_point)
        pts1 = np.float32(rotation_point)
        pts2 = np.float32([[0, 0], [280, 0], [280, 32], [0, 32]])
        M = cv2.getPerspectiveTransform(pts1, pts2)
        image = cv2.warpPerspective(image, M, (280, 32))
        self.show(image)

    def get_origin_point(self, txt_w, txt_h, offset_x, offset_y, start_x, start_y):
        size_w = txt_w + offset_x + random.randint(10, 20)
        size_h = txt_h + offset_y * 2
        point = np.zeros((4, 2))
        point[0][0] = start_x
        point[0][1] = start_y

        point[1][0] = start_x + size_w
        point[1][1] = start_y

        point[2][0] = start_x + size_w
        point[2][1] = start_y + size_h

        point[3][0] = start_x
        point[3][1] = start_y + size_h
        return point

    def rotation(self, img, txt_w, txt_h, offset_x, offset_y, start_x, start_y):
        rotation = random.randint(-2, 2)
        rows, cols = img.shape[:2]
        M = cv2.getRotationMatrix2D(((cols - 1) / 2.0, (rows - 1) / 2.0), rotation, 1)
        img = cv2.warpAffine(img, M, (cols, rows))
        self.show(img)

        size_w = txt_w + offset_x + random.randint(10, 20)
        size_h = txt_h + offset_y * 2

        rotation_point = np.zeros((4, 2), dtype=int)
        if rotation > 0:
            offset = -rotation * 5
            rotation_point[0][0] = start_x
            rotation_point[0][1] = start_y + offset

            rotation_point[1][0] = start_x + size_w
            rotation_point[1][1] = start_y + offset

            rotation_point[2][0] = start_x + size_w
            rotation_point[2][1] = start_y + size_h

            rotation_point[3][0] = start_x
            rotation_point[3][1] = start_y + size_h
        elif rotation < 0:
            offset = -rotation * 5
            rotation_point[0][0] = start_x
            rotation_point[0][1] = start_y

            rotation_point[1][0] = start_x + size_w
            rotation_point[1][1] = start_y

            rotation_point[2][0] = start_x + size_w
            rotation_point[2][1] = start_y + size_h + offset

            rotation_point[3][0] = start_x
            rotation_point[3][1] = start_y + size_h + offset
        else:
            rotation_point[0][0] = start_x
            rotation_point[0][1] = start_y - 2

            rotation_point[1][0] = start_x + size_w
            rotation_point[1][1] = start_y - 2

            rotation_point[2][0] = start_x + size_w
            rotation_point[2][1] = start_y + size_h + 2

            rotation_point[3][0] = start_x
            rotation_point[3][1] = start_y + size_h + 2
        return img, rotation_point

    def draw_four_vectors(self, img, line, color=(0, 255, 0)):
        """
        :param line: [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]
            矩形四点坐标的顺序： left-top, right-top, right-bottom, left-bottom
        """
        img = cv2.line(img, (line[0][0], line[0][1]), (line[1][0], line[1][1]), color)
        img = cv2.line(img, (line[1][0], line[1][1]), (line[2][0], line[2][1]), color)
        img = cv2.line(img, (line[2][0], line[2][1]), (line[3][0], line[3][1]), color)
        img = cv2.line(img, (line[3][0], line[3][1]), (line[0][0], line[0][1]), color)
        self.show(img)
        return img

    def show(self, image):
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        cv2.imshow('image', image)
        cv2.moveWindow('image', 300, 10)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    font = font.Font('font_file/font_in_char', 'font_file/font_tty', 26, 28)
    backimg = background.BackGround('./idcard/')
    Txt = text.Text('text_file/text_file.book_file')
    gen_img = Generate(backimg, font, Txt)
    for i in range(100):
        gen_img.make_image()
































