import numpy as np
import cv2


class FaceDetector:
    def __init__(self):
        self.file = None

    def open(self, file):
        img = cv2.imread(file)
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return rgb

    def detect(self, img, xml, scale, neighbor):
        if not xml:
            return img

        try:
            cascade = cv2.CascadeClassifier(xml)
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            gray = cv2.equalizeHist(gray)
            facerect = cascade.detectMultiScale(gray, scaleFactor=scale, minNeighbors=neighbor, minSize=(24, 24))
            color = (255, 0, 0) #RGB

            if len(facerect) > 500:
                print "too many face detected {0}".format(len(facerect))
            else:
                for rect in facerect:
                    cv2.rectangle(img, tuple(rect[0:2]),tuple(rect[0:2]+rect[2:4]), color, thickness=4)
        except:
            pass

        return img
