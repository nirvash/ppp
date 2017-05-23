#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import pdb
import traceback

from PyQt5.QtCore import QRectF
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, Qt

from FaceDetector import FaceDetector
from mainwindow_ui import Ui_MainWindow

from opencv_test import opencv_test


class MainWidget(QMainWindow):
    def __init__(self, parent = None):
        super(MainWidget, self).__init__(parent)
        self.setAcceptDrops(True)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButtonAction.clicked.connect(self.exec_canny)
        self.ui.pushButtonLeft.clicked.connect(self.move_prev)
        self.ui.pushButtonRight.clicked.connect(self.move_next)
        self.ui.graphicsView.rubberBandSelected.connect(self.rubberBandSelected)
        self.ui.graphicsView.clicked.connect(self.viewClicked)
        self.ui.lineEdit_scale.setText("1.1")
        self.ui.lineEdit_neighbor.setText("2")
        self.files = []
        self.index = -1
        self.scene = None
        self.xml = None

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
                    self.ui.cascadeFilepath.setText(path)
                    self.xml = path
                    return

            self.index = -1
            self.files = []
            for url in mimedata.urls():
                path = url.toLocalFile()
                print path
                if os.path.isdir(path):
                    self.append_files(path)
                else:
                    self.files.append(path)

            if len(self.files) > 0:
                self.index = 0
                self.open_file(self.files[0])
        else:
            event.ignore()


    def append_files(self, path):
        if not path.endswith("/"):
            path += "/"
        files = os.listdir(path)
        for file in files:
            if file.endswith(".png") or file.endswith(".jpg"):
                self.files.append(path + file)


    def closeEvent(self, event):
        self.cleanup()
        event.accept()
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
        self.scene.addRect(QRectF(rect), pen)

    def viewClicked(self, pos):
        print "clicked: {0}".format(pos)
        if not hasattr(self, 'pixmap'):
            return

        for item in self.scene.items():
            if not isinstance(item, QGraphicsPixmapItem):
                self.scene.removeItem(item)

    def open_file(self, path):
        if path:
            self.path = path
            self.ui.imageFilepath.setText(path)
            self.load_image()
            self.update_image()

    def load_image(self):
        if hasattr(self, 'path'):
            scale = float(self.ui.lineEdit_scale.text())
            neighbor = int(self.ui.lineEdit_neighbor.text())
            detector = FaceDetector()
            img = detector.open(self.path)
            img = detector.detect(img, self.xml, scale, neighbor)
            height, width, dim = img.shape
            bytesPerLine = dim * width
            image = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)
            self.pixmap = QPixmap.fromImage(image)

    def update_image(self):
        self.item = QGraphicsPixmapItem(self.pixmap)
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, self.pixmap.width(), self.pixmap.height())
        self.scene.addItem(self.item)
        self.ui.graphicsView.setScene(self.scene)
        self.ui.graphicsView.fitInView(self.item, QtCore.Qt.KeepAspectRatio)

    def exec_canny(self):
        if hasattr(self, 'path'):
            cv_test = opencv_test()
            pic, pic2 = cv_test.open_pic(self.path)
            cv_img = cv_test.canny(pic2)
            height, width, dim = cv_img.shape
            bytesPerLine = dim * width
            image = QImage(cv_img.data, width, height, bytesPerLine, QImage.Format_RGB888)
            pic_item = QGraphicsPixmapItem(QPixmap.fromImage(image))
            self.scene.addItem(pic_item)

    def move_next(self):
        if self.index == -1:
            return

        if self.index < len(self.files) - 1:
            self.index += 1
            self.open_file(self.files[self.index])

    def move_prev(self):
        if self.index > 0:
            self.index -= 1
            self.open_file(self.files[self.index])


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
