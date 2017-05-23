# -*- coding: utf-8 -*-
import os


class Model:
    def __init__(self):
        self.files = []
        self.index = -1
        self.xml = None
        self.outputPathForPositive = './'

    def setCascadePath(self, path):
        self.xml = path

    def getCascadePath(self):
        return self.xml

    def getOutputPathForPositive(self):
        return self.outputPathForPositive

    def setOutputPathForPositive(self, path):
        self.outputPathForPositive = path

    def resetFiles(self):
        self.index = -1
        self.files = []

    def append(self, path):
        self.files.append(path)

    def hasFiles(self):
        return len(self.files) > 0

    def getFile(self, index):
        if len(self.files) > index:
            return self.files[index]
        else:
            return None

    def getCurrentFile(self):
        return self.getFile(self.index)

    def hasNext(self):
        if not self.hasFiles():
            return False
        return self.index + 1 < len(self.files)

    def hasPrev(self):
        if not self.hasFiles():
            return False
        return self.index > 0

    def next(self):
        if self.hasFiles():
            self.index = min( self.index + 1, len(self.files) - 1)

    def prev(self):
        if self.hasFiles():
            self.index = max(0, self.index - 1)

    def setCurrentIndex(self, index):
        self.index = index

    def getBaseFilename(self):
        if not self.hasFiles():
            return ''
        basefilename, ext = os.path.splitext( os.path.basename(self.getCurrentFile()))
        return basefilename


