#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import
from fontTools.ttLib import TTFont
import json
import os
import os.path
from CV_Lib.ocr_data.char_dict.alphabet import alphabet
import random
import traceback


def codeToChar():
    file = open('char_key_value.txt', 'r')
    code = file.read().strip('\n').split('\n')
    char_dict = {}
    for s in code:
        key, value = s.split(' ')
        char_dict[key] = value
    return char_dict


def get_font_char(font_path):
    char_dict = codeToChar()
    font = TTFont(font_path)
    try:
        char_encode_list = font.getGlyphNames()
    except:
        traceback.print_exc()
        return
    s = ""
    for ch in char_encode_list[1:]:
        if 'uni' in ch:
            ch = ch.replace('uni', '\\u')
            try:
                s += ch.encode().decode('unicode_escape')
            except:
                # traceback.print_exc()
                pass
        else:
            if len(ch) == 1:
                s += ch
            else:
                if ch in char_dict.keys():
                    s += char_dict[ch]
    return s


#### 某些字体包含的不全，导致某些汉字无法显示
if __name__ == '__main__':
    font_tty_dir = './font_all/'
    font_inchar_dir = './font_in_all/'
    font_list = os.listdir(font_tty_dir)
    for i, font in enumerate(font_list):
        # if i >= 1:
        #     break
        font_path = os.path.join(font_tty_dir, font)
        chars = get_font_char(font_path)
        char_path = os.path.join(font_inchar_dir, font)
        f = open(char_path, 'w')
        f.write(chars)





