from PyQt5 import QtCore
from PyQt5.QtCore import QPoint, QRect
from PyQt5.QtWidgets import QGraphicsView


class RubberBandGraphicsView(QGraphicsView):

    # 範囲選択完了時に投げるシグナル
    rubberBandSelected = QtCore.pyqtSignal(QRect)

    def __init__(self, parent = None):
        super(QGraphicsView, self).__init__(parent)

    def mouseReleaseEvent(self, event):
        rect = self.rubberBandRect()
        QGraphicsView.mouseReleaseEvent(self, event)
        if not rect.isNull():
            self.rubberBandSelected.emit(rect)
