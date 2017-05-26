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
        self.pressPos = QPoint(0, 0)

    def mousePressEvent(self, event):
        super(RubberBandGraphicsView, self).mousePressEvent(event)
        self.pressPos = event.pos()

    def mouseReleaseEvent(self, event):
        rect = self.rubberBandRect()
#        QGraphicsView.mouseReleaseEvent(self, event)
        super(RubberBandGraphicsView, self).mouseReleaseEvent(event)
        if not rect.isNull():
            rect = self.normalizeRect(rect, self.pressPos, event.pos())
            self.rubberBandSelected.emit(rect)

        if event.button() == QtCore.Qt.RightButton:
            self.clicked.emit(event.pos())

    def normalizeRect(self, rect, pos1, pos2):
        diff = rect.width() - rect.height()
        if diff < 0: # 幅を広げる
            diff = abs(diff)
            if pos1.x() > pos2.x(): # 始点が右
                rect.setX(rect.x() - diff)
            else:
                rect.setWidth(rect.width() + diff)
        else: # 高さを広げる
            if pos1.y() > pos2.y(): # 始点が上
                rect.setY(rect.y() - diff)
            else:
                rect.setHeight(rect.height() + diff)
        return rect

