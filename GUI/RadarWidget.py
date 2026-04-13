from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
import math
import time

class RadarWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding
        )

        self.theta = 0
        self.r = 0
        self.punkte = []

    def sizeHint(self):
        return QtCore.QSize(200, 200)

    def paintEvent(self, event):

        painter = QtGui.QPainter(self)
        painter.setClipRect(event.rect())

        #Background
        rect = QtCore.QRect(0, 0,
                            painter.device().width(),
                            painter.device().height()
                            )
        brush = QtGui.QBrush(Qt.black)
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, 10, 10)

    #Arcs
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

        #lines
        for winkel in range(0, 181, 30):
            x_end = cx + max_r * math.cos(math.radians(winkel))
            y_end = cy - max_r * math.sin(math.radians(winkel))
            painter.drawLine(cx, cy, int(x_end), int(y_end))

        #text
        font = QtGui.QFont("Arial", 15)
        painter.setFont(font)
        for winkel in range(0, 181, 30):
            text_r = max_r + 15
            text_x = cx + text_r * math.cos(math.radians(winkel))
            text_y = cy - text_r * math.sin(math.radians(winkel))
            painter.drawText(int(text_x) - 10, int(text_y) + 5 , f"{str(winkel)}°")


        #Dots for life data


        pen = QtGui.QPen()
        pen.setColor(QtGui.QColor("red"))
        pen.setWidth(4)
        painter.setPen(pen)
        for t, theta, r in self.punkte:
            punkt_r = (r/400 * max_r)
            px = cx + punkt_r * math.cos(theta)
            py = cy - punkt_r * math.sin(theta)
            painter.drawPoint(int(px), int(py))


        #green Line
        sx = cx + max_r * math.cos(self.theta)
        sy = cy - max_r * math.sin(self.theta)
        pen.setColor(QtGui.QColor("#7ec850"))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawLine(cx, cy, int(sx), int(sy))

        #red line
        object_r = (self.r/400 * max_r)
        ox = cx + object_r * math.cos(self.theta)
        oy = cy - object_r * math.sin(self.theta)
        pen.setColor(QtGui.QColor("red"))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawLine(cx, cy, int(ox), int(oy))





        painter.end()

    def updateData(self, theta, r):
        self.theta = theta
        self.r = r
        self.update()
        self.punkte.append((time.time(), theta, self.r))

        self.punkte = [(t,th,r) for t, th, r in self.punkte
                       if time.time() - t <5.0]
