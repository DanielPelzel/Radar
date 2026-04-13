from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt

class RadarWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setsizePolicy(
            QtWidgets.QSizePolicy.minimumExpanding,
            QtWidgets.QSizePolicy.minimumExpanding
        )

        self.theta = 0
        self.r = 0

    def sizeHint(self):
        return QtCore.QSize(200, 200)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        

        painter.end()

    def updateData(self, theta, r):
        self.theta = theta
        self.r = r
        self.update()