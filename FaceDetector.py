import traceback

import cv2
import os
import numpy as np

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
            height, width = img.shape[:2]
            #size = (height / 2, width / 2)
            #gray = cv2.resize(img, size)
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            gray = cv2.equalizeHist(gray)
            (faces, neighbors, weights) = cascade.detectMultiScale3(gray, scaleFactor=scale, minNeighbors=neighbor, minSize=(24, 24), outputRejectLevels=True)
            gray = cv2.flip(gray, 1)
            (facesm, neighborsm, weightsm) = cascade.detectMultiScale3(gray, scaleFactor=scale, minNeighbors=neighbor, minSize=(24, 24), outputRejectLevels=True)

            color = (0, 200, 0) #RGB
            colorm = (0, 255, 0)
            # CV_AA = 16

            if len(faces) > 500:
                print "too many face detected {0}".format(len(faces))
            else:
                for i, rect in enumerate(faces):
                    cv2.rectangle(img, tuple(rect[0:2]),tuple(rect[0:2]+rect[2:4]), color, thickness=4)

            if len(facesm) > 500:
                print "too many face detected {0}".format(len(facesm))
            else:
                for i, rectm in enumerate(facesm):
                    rect = np.array(rectm)
                    rect[0] = width - rectm[0] - rectm[2]
                    cv2.rectangle(img, tuple(rect[0:2]),tuple(rect[0:2]+rect[2:4]), colorm, thickness=4)

        except:
            traceback.print_exc()

        return img

    def crop(self, img, rects, basefilename, path, mirror = False):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        try:
            baseIndex = 0
            for i, rect in enumerate(rects):
                if rect.width() < 24 or rect.height() < 24:
                    continue

                self.cropImpl(baseIndex, basefilename, i, img, mirror, path, rect)
        except:
            traceback.print_exc()

    def cropImpl(self, baseIndex, basefilename, i, img, mirror, path, rect):
        output = ''
        cropped = img[rect.y():rect.y() + rect.height(), rect.x():rect.x() + rect.width()]
        if mirror:
            cropped = cv2.flip(cropped, 1)  # 1: Y Axis
        output = "{0}crop_{1}_{2:0>3d}.jpg".format(path, basefilename, i + baseIndex)
        while os.path.exists(output):
            baseIndex += 1
            output = "{0}crop_{1}_{2:0>3d}.jpg".format(path, basefilename, i + baseIndex)
        cv2.imwrite(output, cropped)
        print output
