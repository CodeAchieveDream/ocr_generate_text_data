#! /usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw, ImageFont
import random
import numpy as np
import cv2
import os
from imgaug_image import generate
from word import Word
from localfont import LocalFont
import traceback
import matplotlib.pyplot as plt


def random_image():
    bg_image = 'back_ground/idcard/'
    bg_list = os.listdir(bg_image)
    random.shuffle(bg_list)
    bg = random.choice(bg_list)
    image = Image.open(os.path.join(bg_image, bg))
    return image


def draw_four_vectors(img, line, color=(0, 255, 0)):
    img = cv2.line(img, (line[0][0], line[0][1]), (line[1][0], line[1][1]), color)
    img = cv2.line(img, (line[1][0], line[1][1]), (line[2][0], line[2][1]), color)
    img = cv2.line(img, (line[2][0], line[2][1]), (line[3][0], line[3][1]), color)
    img = cv2.line(img, (line[3][0], line[3][1]), (line[0][0], line[0][1]), color)
    return img


def get_rectangle_box(point):
    min_x = min(point[0][0], point[3][0]) - 1
    max_x = max(point[1][0], point[2][0]) + 1
    min_y = min(point[0][1], point[1][1]) - 1
    max_y = max(point[2][1], point[3][1]) + 1
    point[0][0], point[0][1] = min_x, min_y
    point[1][0], point[1][1] = max_x, min_y
    point[2][0], point[2][1] = max_x, max_y
    point[3][0], point[3][1] = min_x, max_y
    return point


def rotation(image, point):
    rotation = random.uniform(-3, 3)
    h, w = image.shape[:2]
    center_w = (w - 1) / 2.0
    center_h = (h - 1) / 2.0
    M = cv2.getRotationMatrix2D((center_w, center_h), rotation, 1)
    point = np.array(point)
    for i, index in enumerate(point):
        index = np.append(index, 1)
        a = np.mat(index).T
        rota_mat = np.mat(M)
        new_index = np.array(rota_mat * a).ravel()
        point[i, :] = new_index
    # print("new point :", point)
    point = get_rectangle_box(point)
    image = cv2.warpAffine(image, M, (w, h))
    # show(image)
    if image[point[0][1]: point[3][1], point[0][0]: point[1][0]].shape[0] == 0:
        image = draw_four_vectors(image, point)
        plot(image)
    return image, point


def get_gray_hex():
    gray = random.randint(18, 100)
    gray = hex(gray)
    gray = '#' + gray[2:] + gray[2:] + gray[2:]
    return gray


def get_color_hex():
    font_color_list = ['#9660F5', '#37DCEB', '#E3EB37', '#F4C46C', '#6CF4BA',
                       '#F1532F', '#3D48C7', '#D431CA', '#D4316B', '#E1F46C']
    return random.choice(font_color_list)


def show(image):
    cv2.imshow('image', image)
    cv2.moveWindow('image', 300, 10)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def plot(image):
    plt.imshow(image)
    plt.show()


def extendEdge(point, padL, padR, padU, padD):
    point[0][0] = point[0][0] - padL
    point[0][1] = point[0][1] - padU

    point[1][0] = point[1][0] + padR
    point[1][1] = point[1][1] - padU

    point[2][0] = point[2][0] + padR
    point[2][1] = point[2][1] + padD

    point[3][0] = point[3][0] - padL
    point[3][1] = point[3][1] + padD
    return point


def pad_image(point, img_h, img_w):
    pad_w = 280 - img_w
    pad_h = 32 - img_h
    pad_h_U, pad_h_D = pad_h // 2, pad_h - pad_h // 2
    if 10 <= pad_w:
        pad_w_L = random.randint(3, 10)
        pad_w_R = pad_w - pad_w_L
    else:
        pad_w_L = pad_w // 2
        pad_w_R = pad_w - pad_w_L
    point = extendEdge(point, pad_w_L, pad_w_R, pad_h_U, pad_h_D)
    return point


def updata_point_by_img(new_h, new_w, point):
    point[0][0] = point[0][0] + 360
    new_point = [[point[0][0], point[0][1]],
                 [point[0][0] + new_w, point[0][1]],
                 [point[0][0] + new_w, point[0][1] + new_h],
                 [point[0][0], point[0][1] + new_h]]
    return new_point


def resize_280x32(image, point):
    txt_img = image[point[0][1]: point[3][1], point[0][0]: point[1][0]+1]
    txt_h, txt_w = np.shape(txt_img)[:2]
    if txt_h <= 32 and txt_w <= 280:
        point = pad_image(point, txt_h, txt_w)
        point[1][0] += 1
        point[2][0] += 1
        # img = image[point[0][1]: point[3][1], point[0][0]: point[1][0]]
        return image, point
    else:
        scale_w = 280 / txt_w
        scale_h = 32 / txt_h
        scale = min(scale_w, scale_h)
        new_img = cv2.resize(txt_img, (0, 0), fx=scale, fy=scale)
        new_h, new_w = np.shape(new_img)[:2]
        point_up = updata_point_by_img(new_h, new_w, point)
        image[point_up[0][1]: point_up[3][1], point_up[0][0]: point_up[1][0], :] = new_img
        point_pad = pad_image(point_up, new_h, new_w)
        # img = image[point_pad[0][1]: point_pad[3][1], point_pad[0][0]: point_pad[1][0]]
        return image, point_pad


def get_transform_image(image, point):
    flag = random.choice([1, 2, 3, 4])
    if flag == 1:
        point[0][0] -= random.randint(0, 5)
        point[0][1] -= random.randint(0, 5)
    if flag == 2:
        point[1][0] += random.randint(0, 5)
        point[1][1] -= random.randint(0, 5)
    if flag == 3:
        point[2][0] += random.randint(0, 5)
        point[2][1] += random.randint(0, 5)
    if flag == 4:
        point[3][0] -= random.randint(0, 5)
        point[3][1] += random.randint(0, 5)
    pts1 = np.float32(point)
    pts2 = np.float32([[0, 0], [280, 0], [280, 32], [0, 32]])
    M = cv2.getPerspectiveTransform(pts1, pts2)
    img = cv2.warpPerspective(image, M, (280, 32))
    return img


if __name__ == '__main__':
    n = 3000000
    label_path = '/media/hzl/file/Data-Set/mingpian/image/char.txt'
    save_path = '/media/hzl/file/Data-Set/mingpian/image/char/'
    label_image_path = '/ssd1/data/'
    label = open(label_path, 'w')
    rotation_prob = 0.5
    transform_prob = 0.5
    generate_prob = 0

    local_font = LocalFont()
    random_word = Word()

    for i in range(n):
        # if i > 100:
        #     break
        if i % 10000 == 0:
            print(i)
        font = local_font.get_random_font()
        font_path, font_set = font[0], font[1]

        # txt = random_word.random_alphabet(font_set)
        txt = random_word.random_book(font_set).replace(' ', '')

        back_ground = random_image()
        image = np.array(back_ground)
        draw_table = ImageDraw.Draw(im=back_ground)
        bg_y, bg_x = np.shape(image)[:2]

        w_x = random.randint(bg_x//2 - 1000, bg_x//2 + 1000)
        w_y = random.randint(bg_y//2 - 180, bg_y//2 + 180)

        font_size = random.randint(26, 32)
        try:
            txt_w, txt_h = ImageFont.truetype(font_path, font_size).getsize(txt)
            start_x, start_y = ImageFont.truetype(font_path, font_size).getoffset(txt)
        except:
            print(txt)
            traceback.print_exc()
            continue

        font_color = get_gray_hex()

        draw_table.text(xy=(w_x, w_y), text=txt, fill=font_color, font=ImageFont.truetype(font_path, font_size))
        image = np.array(back_ground)
        point = [[w_x, w_y+start_y-1],
                [w_x+(txt_w-start_x), w_y+start_y-1],
                [w_x+(txt_w-start_x), w_y+(txt_h)],
                [w_x, w_y+(txt_h)]]

        try:
            if random.uniform(0, 1) <= rotation_prob:
                image, point = rotation(image, point)

            image, point = resize_280x32(image, point)
            img = image[point[0][1]: point[3][1], point[0][0]: point[1][0]]
            if np.shape(img) != (32, 280, 3):
                print("error1", np.shape(img))

            if random.uniform(0, 1) <= transform_prob:
                img = get_transform_image(image, point)
                if np.shape(img) != (32, 280, 3):
                    print("error2", np.shape(img))
            else:
                img = image[point[0][1]: point[3][1], point[0][0]: point[1][0]]
                if np.shape(img) != (32, 280, 3):
                    print("error3", np.shape(img))

            if random.uniform(0, 1) <= generate_prob:
                img = generate(img)
        except:
            print(i, txt)
            traceback.print_exc()
            continue
        if np.shape(img) != (32, 280, 3):
            print("error4", np.shape(img))
        # plot(img)
        # show(img)
        save_img = Image.fromarray(img)
        img_path = os.path.join(save_path, str(i) + '.jpg')
        label_img_path = os.path.join(label_image_path, str(i) + '.jpg')
        save_img.save(img_path, 'JPEG')  # 保存在当前路径下，格式为PNG
        label.write(label_img_path + '\t' + txt + '\n')
    label.close()

