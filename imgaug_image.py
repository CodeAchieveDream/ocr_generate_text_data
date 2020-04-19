#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import numpy as np
import cv2
import random
from imgaug import augmenters as iaa


gen_img = [
    iaa.AverageBlur(k=((5, 11), (1, 3))),
    iaa.AveragePooling(4),
    iaa.MaxPooling(4),
    iaa.MinPooling((1, 2)),
    iaa.Superpixels(p_replace=(0.1, 0.2), n_segments=(16, 128)),
    iaa.Clouds(),
    iaa.Fog(),
    iaa.AddElementwise((-40, -20)),
    iaa.AdditiveGaussianNoise(scale=(0, 0.2*255)),
    iaa.AdditiveGaussianNoise(scale=0.1*255, per_channel=True),
    iaa.Dropout(p=(0, 0.2)),
    iaa.JpegCompression(compression=(50, 99)),
    # iaa.WithChannels(0, iaa.Affine(rotate=(0, 10))),
    iaa.ChannelShuffle(0.35),

    iaa.WithColorspace(to_colorspace="HSV", from_colorspace="RGB", children=iaa.WithChannels(
        0, iaa.Add((0, 50)))),

    iaa.WithBrightnessChannels(iaa.Add((-50, 50))),

    iaa.WithBrightnessChannels(iaa.Add((-50, 50)), to_colorspace=[iaa.CSPACE_Lab, iaa.CSPACE_HSV]),

    iaa.WithHueAndSaturation([
        iaa.WithChannels(0, iaa.Add((-30, 10))),
        iaa.WithChannels(1, [
            iaa.Multiply((0.5, 1.5)),
            iaa.LinearContrast((0.75, 1.25))])]),

    iaa.MultiplyHueAndSaturation(mul_hue=(0.5, 1.5)),

    # iaa.Canny()
    # iaa.FastSnowyLandscape(
    #     lightness_threshold=140,
    #     lightness_multiplier=2.5
    # ),
    iaa.WithChannels(0, iaa.Add((-50, 50))),
    iaa.WithChannels(1, iaa.Add((-50, 50))),
    iaa.WithChannels(2, iaa.Add((-50, 50))),
]


def generate(img):
    seq = iaa.SomeOf((1, 2), gen_img)
    # seq = iaa.OneOf(sqe_list)
    image_aug = seq.augment_image(img)
    return image_aug


if __name__ == "__main__":
    path = "back_ground/idcard/"
    img_list = os.listdir(path)
    for i, name in enumerate(img_list):
        image = cv2.imread(path+name)
        # image = cv2.resize(image, (0, 0), fx=, fy=3)
        img = generate(image)
        # im = np.vstack((cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)))
        im = np.vstack((image, img))
        cv2.imshow('img', im)
        cv2.moveWindow('img', 300, 10)
        cv2.waitKey(0)
        cv2.destroyAllWindows()



