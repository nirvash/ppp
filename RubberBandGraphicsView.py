#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from PyQt5.QtCore import QPoint, QRect
from PyQt5.QtWidgets import QGraphicsView


class RubberBandGraphicsView(QGraphicsView):

    # 範囲選択完了時に投げるシグナル
    rubberBandSelected = QtCore.pyqtSignal(QRect)

    clicked = QtCore.pyqtSignal(QPoint)

    def __init__(self, parent = None):
        super(QGraphicsView, self).__init__(parent)

    def mouseReleaseEvent(self, event):
        rect = self.rubberBandRect()
#        QGraphicsView.mouseReleaseEvent(self, event)
        super(RubberBandGraphicsView, self).mouseReleaseEvent(event)
        if not rect.isNull():
            self.rubberBandSelected.emit(rect)

        if event.button() == QtCore.Qt.RightButton:
            self.clicked.emit(event.pos())

