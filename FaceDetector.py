import traceback

import cv2
import os

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

    def crop(self, img, rects, basefilename, path):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        try:
            baseIndex = 0
            for i, rect in enumerate(rects):
                output = ''
                cropped = img[rect.y():rect.y()+rect.height(), rect.x():rect.x()+rect.width()]
                output = "{0}crop_{1}_{2:0>3d}.jpg".format(path, basefilename, i + baseIndex)
                while os.path.exists(output):
                    baseIndex += 1
                    output = "{0}crop_{1}_{2:0>3d}.jpg".format(path, basefilename, i + baseIndex)

                cv2.imwrite(output, cropped)
                print output
        except:
            traceback.print_exc()
