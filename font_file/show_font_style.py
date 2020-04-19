#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import os
import cv2
import random
from PIL import ImageFont, ImageDraw, Image


def show_word(image):
    cv2.imshow('test', image)
    cv2.moveWindow('test', 300, 10)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def get_bg_image():
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    image = Image.new('RGBA', (1500, 300), color=color)
    return image

def main():
    font_path = './font_all/'
    font_list = os.listdir(font_path)
    alphabet_font = ['FZWBJW.TTF', '华文中宋.ttf', '微软雅黑粗体.ttf', '方正中等线简体.TTF', '方正准圆简体.TTF',
                     '方正大黑简体.ttf', '方正姚体简体.TTF', 'fdbsjw.ttf', ]
    fanti_font = ['华文宋体.ttf', '华文中宋.ttf', 'simhei.ttf', 'simsun.ttf', '微软雅黑粗体.ttf']
    for i, font in enumerate(font_list):
        print("current font_file: ", font)
        # image = get_bg_image()
        image = Image.new('RGBA', (1500, 300), color=(212, 212, 212))

        # txt = "ABCDEFGHIJKLMNOPQRSTUVWXYZ\n" \
        #       "abcdefghijklmnopqrstuvwxyz\n" \
        #       "123456789\n"
        txt = '叶文洁走到悬崖边，她曾在这里亲手结束了两个军人的生命。她并没有像其他同行的人那样眺望云\n' \
              '海，而是把目光集中到一个方向，在那一片云层下面，有一个叫齐家屯的小村庄…叶文洁的心脏艰\n' \
              '难地跳动着，像一根即将断裂的琴弦，黑雾开始在她的眼前出现，她用尽生命的最后能量坚持着，在一切\n' \
              '都没入永恒的黑暗之前，她想再看—次红岸基地的日落。在西方的天际，正在云海中下沉的夕阳仿佛被融\n' \
              '化了，太阳的血在云海和天空中弥散开来，映现出一大片壮丽的血红。这是人们的落日……”叶文洁轻轻地说。'
        # txt = '撣經號團麗貿雲城精寫宪鎮\n' \
        #       '飛區禮真傳蘇灣標學華魇從\n' \
        #       '務龍曉動綠郵劉機統霈錢觀\n' \
        #       '鴻東禪陳密壹風編靌書國鑫\n' \
        #       '綱車錦廠長園暨械際協如電\n' \
        #       '產廣話灏熾鷹會時總薹業碟\n' \
        #       '興銹樓議棟漢麥腦實輪鉿淼'
        draw = ImageDraw.Draw(im=image)
        font = ImageFont.truetype(os.path.join(font_path, font), size=30)
        draw.text((50, 50), text=txt, font=font, fill=(50, 50, 50))
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        show_word(image)


if __name__ == "__main__":
    main()








