#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import cv2
import os
from PIL import ImageFont
import random


class LocalFont(object):
    def __init__(self):
        self.path = 'font_file/font_all/'
        self.all_font = self.get_all_font(self.path)
        self.fanti_font = self.get_all_font(self.path, True)

    def get_all_font(self, font_path, is_fanti=False):
        font_list = []
        fanti_font = ['华文宋体.ttf', '华文中宋.ttf', 'simhei.ttf', 'simsun.ttf', '微软雅黑粗体.ttf']
        for font in os.listdir(font_path):
            if is_fanti:
                if font in fanti_font:
                    path = 'font_file/font_in_all/'
                    font_txt = open(os.path.join(path, font), 'r').read()
                    font_set = set(font_txt)
                    font_list.append([os.path.join(font_path, font), font_set])
            else:
                path = 'font_file/font_in_all/'
                font_txt = open(os.path.join(path, font), 'r').read()
                font_set = set(font_txt)
                font_list.append([os.path.join(font_path, font), font_set])
        return font_list

    def get_random_font(self):
        return random.choice(self.all_font)

    def get_random_fanti_font(self):
        return random.choice(self.fanti_font)


if __name__ == "__main__":
    Font = Font()
    for i in Font.fanti_font:
        print(i)


