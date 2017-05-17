#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import pdb
import traceback
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from mainwindow_ui import Ui_MainWindow

from opencv_test import opencv_test

class MainWidget(QMainWindow):
    def __init__(self, parent = None):
        super(MainWidget, self).__init__(parent)
        self.setAcceptDrops(True)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.exec_canny)

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
                self.open_file(path)
                break

        else:
            event.ignore()

    def closeEvent(self, event):
        self.cleanup()
        event.accept()
        super(MainWidget, self).closeEvent(event)

    def cleanup(self):
        self.ui.graphicsView.setScene(None) # これやらないと終了時に異常終了する

    def open_file(self, path):
        if path:
            self.path = path
            self.ui.lineEdit.setText(path)
            pixmap = QPixmap(path)
            self.item = QGraphicsPixmapItem(pixmap)
            self.scene = QGraphicsScene()
            self.scene.setSceneRect(0, 0, pixmap.width(), pixmap.height())
            self.scene.addItem(self.item)
            self.ui.graphicsView.setScene(self.scene)
            self.ui.graphicsView.fitInView(self.item)

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
