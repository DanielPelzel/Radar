from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
import math

class RadarWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding
        )

        self.theta = 0
        self.r = 0


    def sizeHint(self):
        return QtCore.QSize(200, 200)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setClipRect(event.rect())

        rect = QtCore.QRect(0, 0,
                            painter.device().width(),
                            painter.device().height()
                            )
        brush = QtGui.QBrush(Qt.black)
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, 10, 10)


        pen = QtGui.QPen()
        pen.setColor(QtGui.QColor("#7ec850"))
        pen.setWidth(1)
        painter.setPen(pen)

        width = painter.device().width()
        height = painter.device().height()

        cx = width // 2
        cy = height -1

        max_r = min(width // 2 , height)-20

        for i in range(1,5):
            r = max_r // 4 * i
            painter.drawArc(cx-r, cy-r, 2*r, 2*r, 0*16, 180*16)

        pen.setWidth(1)
        painter.setPen(pen)

        for winkel in range(0, 360, 30):
            x_end = cx + max_r * math.cos(math.radians(winkel))
            y_end = cy + max_r * math.sin(math.radians(winkel))
            painter.drawLine(cx, cy, int(x_end), int(y_end))

        painter.end()

    def updateData(self, theta, r):
        self.theta = theta
        self.r = r
        self.update()
