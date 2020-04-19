#! /usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import os
import re
import random


def show(image):
    image = cv2.imread(image)
    cv2.imshow('img', image)
    cv2.moveWindow('img', 300, 10)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    path = '/media/hzl/file/Data-Set/mingpian/image/char.txt'
    txt_list = open(path, 'r').read().split('\n')
    for txt in txt_list:
        img_path, label = txt.split('\t')
        img = os.path.split(img_path)[-1]
        print(img)
        print(label)
        show(os.path.join('/media/hzl/file/Data-Set/mingpian/image/char/', img))














