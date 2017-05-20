import numpy as np
import cv2


class FaceDetector:
    def __init__(self):
        self.file = None

    def open(self, file):
        img = cv2.imread(file)
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return rgb

    def detect(self, img, xml):
        if not xml:
            return img

        try:
            cascade = cv2.CascadeClassifier(xml)
            facerect = cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=2, minSize=(24, 24))
            color = (255, 255, 0)

            for rect in facerect:
                cv2.rectangle(img, tuple(rect[0:2]),tuple(rect[0:2]+rect[2:4]), color, thickness=4)
        except:
            pass

        return img
