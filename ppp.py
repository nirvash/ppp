#!/usr/bin/python
# -*- coding: utf-8 -*-
import ConfigParser
import os
import sys
import pdb
import traceback

from PyQt5.QtCore import QRectF, QRect
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, Qt

from DraggableRect import DraggableRect
from Effector import Effector
from FaceDetector import FaceDetector
from Model import Model
from mainwindow_ui import Ui_MainWindow

from opencv_test import opencv_test




class MainWidget(QMainWindow):
    def __init__(self, parent = None):
        super(MainWidget, self).__init__(parent)
        self.setAcceptDrops(True)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButtonCropP.clicked.connect(self.crop_as_positive)
        self.ui.pushButtonCropPM.clicked.connect(self.crop_as_positive_mirror)
        self.ui.pushButtonCropN.clicked.connect(self.crop_as_negative)
        self.ui.pushButtonClear.clicked.connect(self.clearAllSelection)
        self.ui.pushButtonFaceDetect.clicked.connect(self.face_detect)
        self.ui.pushButtonShowOriginal.clicked.connect(self.load_image)
        self.ui.pushButtonLeft.clicked.connect(self.move_prev)
        self.ui.pushButtonRight.clicked.connect(self.move_next)
        self.ui.graphicsView.rubberBandSelected.connect(self.rubberBandSelected)
        self.ui.graphicsView.clicked.connect(self.viewClicked)
        self.ui.pushButtonTest.clicked.connect(self.effect_test)
        self.ui.lineEdit_scale.setText("1.1")
        self.ui.lineEdit_neighbor.setText("2")
        self.model = Model()
        self.scene = None
        self.loadConfig()
        self.updatePrevNextButton()

    def loadConfig(self):
        config = ConfigParser.SafeConfigParser()
        config.read('./config.ini')
        section = 'settings'
        if config.has_section(section):
            if config.has_option(section, 'cascade_xml'):
                self.setCascadeXml(config.get(section, 'cascade_xml'))

            if config.has_option(section, "outputPathForPositive"):
                path = config.get(section, 'outputPathForPositive')
                self.model.setOutputPathForPositive(path)

            if config.has_option(section, "outputPathForNegative"):
                path = config.get(section, 'outputPathForNegative')
                self.model.setOutputPathForNegative(path)


    def saveConfig(self):
        config = ConfigParser.SafeConfigParser()
        config.read('./config.ini')
        section = 'settings'
        if not config.has_section(section):
            config.add_section(section)
        path = self.model.getCascadePath()
        config.set(section, 'cascade_xml', path)
        with open('./config.ini', 'w') as file:
            config.write(file)

    def setCascadeXml(self, path):
        self.model.setCascadePath(path)
        self.ui.cascadeFilepath.setText(path)

    def resizeEvent(self, event):
        super(MainWidget, self).resizeEvent(event)
        if self.scene:
            self.ui.graphicsView.fitInView(self.item,  QtCore.Qt.KeepAspectRatio)

    def dragEnterEvent(self, event):
        mimedata = event.mimeData()
        if mimedata.hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        mimedata = event.mimeData()
        if mimedata.hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        mimedata = event.mimeData()
        if mimedata.hasUrls():
            event.accept()
            for url in mimedata.urls():
                path = url.toLocalFile()
                print path
                if path.endswith(".xml"):
                    self.setCascadeXml(path)
                    return

            self.model.resetFiles()
            for url in mimedata.urls():
                path = url.toLocalFile()
                print path
                if os.path.isdir(path):
                    self.append_files(path)
                else:
                    self.model.append(path)

            if self.model.hasFiles():
                self.model.setCurrentIndex(0)
                self.showCurrentFile()
        else:
            event.ignore()

    def append_files(self, path):
        if not path.endswith("/"):
            path += "/"
        files = os.listdir(path)
        for file in files:
            if file.endswith(".png") or file.endswith(".jpg"):
                self.model.append(path + file)

    def closeEvent(self, event):
        self.cleanup()
        event.accept()
        self.saveConfig()
        super(MainWidget, self).closeEvent(event)

    def cleanup(self):
        self.ui.graphicsView.setScene(None) # これやらないと終了時に異常終了する

    def rubberBandSelected(self, rect):
        print "rubber: {0}".format(rect)
        if not hasattr(self, 'pixmap'):
            return

        pen = QPen()
        pen.setColor(QColor(255, 0, 0))
        pen.setWidth(4)

        # View座標系からScene(= pixmap)の座標系に変換
        p1 = self.ui.graphicsView.mapToScene(rect.topLeft())
        p2 = self.ui.graphicsView.mapToScene(rect.bottomRight())
        rect.setTopLeft(p1.toPoint())
        rect.setBottomRight(p2.toPoint())

        rectItem = DraggableRect(QRectF(rect))
        rectItem.setPen(pen)
        self.scene.addItem(rectItem)
        # self.scene.addRect(QRectF(rect), pen)

    def viewClicked(self, pos):
        print "clicked: {0}".format(pos)
        if not hasattr(self, 'pixmap'):
            return
        pos = self.ui.graphicsView.mapToScene(pos)
        self.clearSelection(pos)

    def clearSelection(self, pos):
        for item in self.scene.items():
            if not isinstance(item, QGraphicsPixmapItem):
                if item.isUnderMouse():
                    self.scene.removeItem(item)
                    break

    def clearAllSelection(self):
        for item in self.scene.items():
            if not isinstance(item, QGraphicsPixmapItem):
                self.scene.removeItem(item)

    def crop_as_positive(self):
        self.crop_(self.model.getOutputPathForPositive())

    def crop_as_positive_mirror(self):
        self.crop_(self.model.getOutputPathForPositive(), True)

    def crop_as_negative(self):
        self.crop_(self.model.getOutputPathForNegative())

    def crop_(self, path, mirror = False):
        rects = []
        for item in self.scene.items():
            if not isinstance(item, QGraphicsPixmapItem):
                rect = item.sceneBoundingRect()
                rects.append(rect.toRect())

        rects = sorted(rects, key=lambda rect:(rect.x() + rect.y(), rect.x()))
        self.crop(rects, path, mirror)

    def crop(self, rects, path, mirror):
        if len(rects) == 0:
            return

        detector = FaceDetector()
        img = detector.open(self.model.getCurrentFile())
        basefilename = self.model.getBaseFilename()
        img = detector.crop(img, rects, basefilename, path, mirror)

    def showCurrentFile(self):
        path = self.model.getCurrentFile()
        if path:
            self.ui.imageFilepath.setText(path)
            if self.ui.checkBoxFaceDetect.isChecked():
                self.face_detect()
            else:
                self.load_image()
        self.updatePrevNextButton()

    def load_image(self):
        if self.model.hasFiles():
            scale = float(self.ui.lineEdit_scale.text())
            neighbor = int(self.ui.lineEdit_neighbor.text())
            detector = FaceDetector()
            img = detector.open(self.model.getCurrentFile())
            height, width, dim = img.shape
            bytesPerLine = dim * width
            image = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)
            self.pixmap = QPixmap.fromImage(image)
            self.update_image()

    def face_detect(self):
        if self.model.hasFiles():
            scale = float(self.ui.lineEdit_scale.text())
            neighbor = int(self.ui.lineEdit_neighbor.text())
            detector = FaceDetector()
            img = detector.open(self.model.getCurrentFile())
            img = detector.detect(img, self.model.getCascadePath(), scale, neighbor)
            height, width, dim = img.shape
            bytesPerLine = dim * width
            image = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)
            self.pixmap = QPixmap.fromImage(image)
            self.update_image()

    def update_image(self):
        self.item = QGraphicsPixmapItem(self.pixmap)
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, self.pixmap.width(), self.pixmap.height())
        self.scene.addItem(self.item)
        self.ui.graphicsView.setScene(self.scene)
        self.ui.graphicsView.fitInView(self.item, QtCore.Qt.KeepAspectRatio)

    def effect_test(self):
        return self.exec_canny()
        effector = Effector()
        img = effector.process(self.model.getCurrentFile())
        height, width = img.shape
        bytesPerLine = 1 * width
        image = QImage(img.data, width, height, bytesPerLine, QImage.Format_Grayscale8)
        self.pixmap = QPixmap.fromImage(image)
        self.update_image()

    def exec_canny(self):
        cv_test = opencv_test()
        pic = cv_test.open_pic(self.model.getCurrentFile())
        cv_img = cv_test.canny(pic)
        height, width = cv_img.shape
        bytesPerLine = 1 * width
        image = QImage(cv_img.data, width, height, bytesPerLine, QImage.Format_Grayscale8)
        self.pixmap = QPixmap.fromImage(image)
        self.update_image()

    def move_next(self):
        if not self.model.hasNext():
            return
        self.model.next()
        self.showCurrentFile()

    def move_prev(self):
        if not self.model.hasPrev():
            return
        self.model.prev()
        self.showCurrentFile()

    def updatePrevNextButton(self):
        self.ui.pushButtonRight.setEnabled(self.model.hasNext())
        self.ui.pushButtonLeft.setEnabled(self.model.hasPrev())


def exception_handler(t, value, tb):
    traceback.print_exception(t, value, tb)
    pdb.pm()


def main():
    sys.excepthook = exception_handler
    app = QApplication(sys.argv)
    window = MainWidget()
    app.setActiveWindow(window)
    window.resize(800, 600)
    window.show()
    #window.raise_()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
