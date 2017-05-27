from PyQt5 import QtCore
from PyQt5.QtCore import QPoint, QRect, QPointF
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QGraphicsView, QGraphicsRectItem, QGraphicsItem


class DraggableRect(QGraphicsRectItem):
    def __init__(self, parent=None):
        super(QGraphicsRectItem, self).__init__(parent)
        self.setFlag(QGraphicsItem.ItemIsMovable)

    def mousePressEvent(self, event):
        hitRect = self.getHitRect()
        if not hitRect.contains(QPointF(event.pos())):
            event.ignore()
        else:
            super(DraggableRect, self).mousePressEvent(event)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        super(DraggableRect, self).paint(painter, QStyleOptionGraphicsItem, widget)
        hitRect = self.getHitRect()
        painter.fillRect(hitRect, QBrush(QColor(255, 0, 0)))

    def getHitRect(self):
        hitRect = self.boundingRect()
        hitRect.setWidth(40)
        hitRect.setHeight(40)
        return hitRect
