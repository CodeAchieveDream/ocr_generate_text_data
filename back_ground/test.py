#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import numpy as np
import cv2
from imgaug import augmenters as iaa

path = 'idcard/'

sqe_list = [
    iaa.ChangeColorspace(from_colorspace="RGB", to_colorspace="HSV"),
    iaa.WithChannels(0, iaa.Add((-50, 50))),
    iaa.WithChannels(1, iaa.Add((-50, 50))),
    iaa.WithChannels(2, iaa.Add((-50, 50))),
    iaa.ChangeColorspace(from_colorspace="HSV", to_colorspace="RGB"),

    iaa.Add((-80, 80), per_channel=0.5),
    iaa.Multiply((0.5, 1.5), per_channel=0.5),

    iaa.AverageBlur(k=((5), (1, 3))),
    iaa.AveragePooling(2),
    iaa.AddElementwise((-20, -5)),
    iaa.AdditiveGaussianNoise(scale=(0, 0.05*255)),
    iaa.JpegCompression(compression=(50, 99)),
    iaa.MultiplyHueAndSaturation(mul_hue=(0.5, 1.5)),
    iaa.WithBrightnessChannels(iaa.Add((-50, 50))),
    iaa.WithBrightnessChannels(iaa.Add((-50, 50)), to_colorspace=[iaa.CSPACE_Lab, iaa.CSPACE_HSV]),

    iaa.MaxPooling(2),
    iaa.MinPooling((1, 2)),
    # iaa.Superpixels(p_replace=(0.1, 0.2), n_segments=(16, 128)),
    iaa.Clouds(),
    iaa.Fog(),

    iaa.AdditiveGaussianNoise(scale=0.1*255, per_channel=True),
    iaa.Dropout(p=(0, 0.2)),

    # iaa.WithChannels(0, iaa.Affine(rotate=(0, 0))),
    iaa.ChannelShuffle(0.35),

    iaa.WithColorspace(to_colorspace="HSV", from_colorspace="RGB", children=iaa.WithChannels(
        0, iaa.Add((0, 50)))),
    #
    iaa.WithHueAndSaturation([
        iaa.WithChannels(0, iaa.Add((-30, 10))),
        iaa.WithChannels(1, [
            iaa.Multiply((0.5, 1.5)),
            iaa.LinearContrast((0.75, 1.25))])]),
    #
    # # iaa.Canny()
    # iaa.FastSnowyLandscape(
    #     lightness_threshold=140,
    #     lightness_multiplier=2.5
    # )
]


def show(image):
    image = cv2.resize(image, (0, 0), fx=3, fy=3)
    cv2.imshow("image", image)
    cv2.moveWindow("image", 300, 0)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def back_image_filter(image):
    image = cv2.medianBlur(image, 7)
    image = cv2.medianBlur(image, 7)
    image = cv2.blur(image, (7, 7))
    image = cv2.GaussianBlur(image, (5, 5), sigmaX=5)
    return image


def generate(img):
    seq = iaa.SomeOf((1, 2), sqe_list)
    # seq = iaa.OneOf(sqe_list)
    image_aug = seq.augment_image(img)
    return image_aug


def main():
    img_list = os.listdir(path)
    for k, i in enumerate(img_list):
        img = cv2.imread(os.path.join(path, i))
        # img = cv2.resize(img, (1120, 128))
        img = cv2.resize(img, (0, 0), fx=2, fy=2)
        # img = back_image_filter(img)
        # img = generate(img)
        # show(img)
        cv2.imwrite(os.path.join(path, i), img)
    # os.rename(os.path.join(path, i), os.path.join(path, 'img_'+str(k)+'.png'))


if __name__ == '__main__':
    main()
