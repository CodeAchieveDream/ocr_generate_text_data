#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import os
import random
from CV_Lib.ocr_data.char_dict.alphabet import alphabet


class Word(object):
    def __init__(self):
        similar_path = 'text_file/font_similar.txt'
        self.similar_lsit = ""
        # self.similar_lsit = self.get_similar(similar_path)

        similar_fanti_path = 'text_file/fanti_similar.txt'
        self.similar_fanti_list = ""
        # self.similar_fanti_list = self.get_txt_list(similar_fanti_path)

        nation_path = 'text_file/nation.txt'
        self.nation_list = ""
        # self.nation_list = self.get_txt_list(nation_path)

        police_path = 'text_file/police_station.txt'
        self.police_station_list = ""
        # self.police_station_list = self.get_txt_list(police_path)

        police_path = 'text_file/police_address.txt'
        self.police_address_list = ""
        # self.police_address_list = self.get_txt_list(police_path)

        books_path = 'text_file/book.txt'
        self.books_list = ""
        self.books_list = self.get_txt_list(books_path)

        # company_path = 'text_file/company_info.txt'
        # self.company_list = ""
        # self.company_list = self.get_txt_list(company_path)

        self.alphabet_set = set(alphabet)

        self.add_fanti = '撣經號團麗貿雲城精寫宪鎮飛區禮真傳蘇灣標學華魇從務龍曉動' \
                         '綠郵劉機統霈錢觀鴻東禪陳密壹風編靌書國鑫綱車錦廠長園暨械' \
                         '際協如電產廣話灏熾鷹會時總薹業碟興銹樓議棟漢麥腦實輪鉿淼'

    def get_txt_list(self, path):
        txt = open(path, 'r').read()
        txt_list = txt.strip('\n').split('\n')
        return txt_list

    def get_similar(self, path):
        similar = open(path, 'r').read()
        similar = similar.replace('\t', '').strip('\n')
        similar_list = similar.split()
        return similar_list

    def random_alphabet(self, font_set):
        while True:
            seq = ""
            try:
                for i in range(10):
                    idx = random.randint(0, len(alphabet) - 1)
                    seq += alphabet[idx]
            except:
                print(" error ")
                continue
            seq_set = set(seq)
            if len(seq_set - font_set) == 0:
                break
        return seq

    def random_date(self):
        year = str(random.randint(0, 9999)).zfill(4)
        month = str(random.randint(0, 99)).zfill(2)
        day = str(random.randint(0, 99)).zfill(2)
        seq = year + '.' + month + '.' + day
        return seq

    def random_police(self, font_set):
        seq = ""
        while True:
            seq = random.choice(self.police_station_list)
            try:
                if len(seq) > 10:
                    start = random.randint(0, len(seq) - 10)
                    seq = seq[start:start + 10]
                elif len(seq) < 7:
                    continue
            except:
                break
            seq_set = set(seq)
            if len(seq_set - set(alphabet)) == 0 and len(seq_set - font_set) == 0:
                break
        return seq

    def random_book(self, font_set):
        while True:
            seq = random.choice(self.books_list)
            try:
                if len(seq) >= 10:
                    start = random.randint(0, len(seq) - 10)
                    seq = seq[start:start + 10]
                else:
                    continue
            except:
                break
            seq_set = set(seq)
            if len(seq_set - set(alphabet)) == 0 and len(seq_set - font_set) == 0:
                break
        return seq

    def random_similar(self, font_set):
        while True:
            seq = ''
            txt_list = random.choices(self.similar_lsit, k=5)
            for txt in txt_list:
                seq += txt
            if len(seq) > 10:
                start = random.randint(0, len(seq) - 10)
                seq = seq[start:start + 10]
            else:
                continue
            seq_set = set(seq)
            if len(seq_set - set(alphabet)) == 0 and len(seq_set - font_set) == 0:
                break
        return seq

    def random_data(self, font_set):
        pass
        # s = ''
        # if random.randint(1, 2) == 1:
        #     s = random.choice(('邮箱:', 'Email:', 'email:', 'E-mail:', 'e-mail:'))
        #     # if random.uniform(0, 1) < 0.5:
        #     #     s += ':'
        #     for k_num in range(random.randint(7, 10)):
        #         s += random.choice(list_alpha)[0]
        #     s += '@'
        #     for k_num in range(random.randint(2, 4)):
        #         s += random.choice(list_alpha)[0]
        #     word = s + '.' + random.choice(('com', 'cn'))
        # else:
        #     s = random.choice(('邮箱', 'Email', 'email', 'E-mail', 'e-mail'))
        #     if random.random() > 0:
        #         s += ':'
        #     s += str(random.randint(100000, 999999999))
        #     word = s + random.choice(('@foxmail.', '@qq.', '@163.', '@126.', '@sina.', '@gmail.')) + random.choice(('net', 'com', 'cn'))

        # flag = random.randint(1, 4)
        # if flag == 1:
        #     for k_num in range(random.randint(10, 16)):
        #         s += str(random.randint(0, 9))
        #     word = s
        #     if random.random() < 0.2:
        #         x = random.randint(4, len(word) - int(len(word) / 2))
        #         word = word.replace(word[x], '(', 1).replace(word[x + int(len(word) / 2) - 1], ')', 1)
        #     elif random.random() > 0.5 and random.random() < 0.7:
        #         x = random.randint(0, len(word) - int(len(word) / 2))
        #         word = word.replace(word[x], ':', 1)
        #     else:
        #         x = random.randint(0, len(word) - int(len(word) / 2))
        #         word = word.replace(word[x], '-', 1)
        #     word = random.choice(["电话:", "传真：", "Tel:", "TEL", "FAX", "Fax:", "fax"]) + word
        # elif flag == 2:
        #     s = str(random.randint(0, 9)) + str(random.randint(100, 999)) + '-' + str(random.randint(1000000, 99999999))
        #     word = s
        #     word = random.choice(["电话:", "传真：", "Tel:", "TEL", "FAX", "Fax:", "fax"]) + word
        # else:
        #     s = random.choice(('http://', 'HTTP://', 'Http://', '网址http:', '网址:Http://', '网站:http://', '网站'))
        #     for k_num in range(random.randint(3, 4)):
        #         s += random.choice(list_alpha)[0]
        #     s += '.'
        #     for k_num in range(random.randint(3, 4)):
        #         s += random.choice(list_alpha)[0]
        #     s += '.'
        #     for k_num in range(random.randint(3, 4)):
        #         s += random.choice(list_alpha)[0]
        #     word = s


if __name__ == '__main__':
    word = Word()
    font = os.listdir('font_file/font_in_all/')
    for i in range(10):
        # print(word.random_seq(random.choice(font)))
        # print(word.random_date())
        # print(word.random_police(random.choice(font)))
        print(word.random_similar(random.choice(font)))



