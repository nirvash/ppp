import numpy as np
import cv2

class opencv_test:
    def __init__(self, parent = None):
        self.file = file

    def open_pic(self, file):
        img = cv2.imread(file)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return img

    def canny(self, img):
        edges = cv2.Canny(img, 100, 200)
        edges = cv2.bitwise_not(edges)
        #edges2 = np.zeros_like(img)
        #for i in (0, 1, 2):
        #    edges2[:,:,i] = edges
        #add = cv2.addWeighted(pic, 1, edges2, 0.4, 0)
        #return add
        return edges
