#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import numpy as np

class Effector(object):
    def __init__(self):
        # 8近傍の定義
        self.kernel25 = np.ones((5, 5), np.uint8)
        self.kernel16 = np.ones((4, 4), np.uint8)
        self.kernel8 = np.ones((3, 3), np.uint8)

    def process(self, file):
        img = cv2.imread(file)
        #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #diff = cv2.morphologyEx(img, cv2.MORPH_CLOSE, self.kernel25, iterations=1)
        #diff = cv2.morphologyEx(diff, cv2.MORPH_OPEN, self.kernel25, iterations=1)
        img_dilate = cv2.dilate(img, self.kernel8, iterations=1)
        img_diff = cv2.absdiff(img, img_dilate)
        img_diff_not = cv2.bitwise_not(img_diff)
        gray = cv2.cvtColor(img_diff_not, cv2.COLOR_RGB2GRAY)
        # gray = cv2.equalizeHist(gray)
        return gray