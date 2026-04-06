import time

import PyQt5
import numpy as np
from PyQt5.QtCore import Qt, QObject, QRunnable, pyqtSignal, pyqtSlot, QThreadPool
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QLabel, QApplication, QPushButton, QWidget, QStyleFactory
import serial


class Worker(QRunnable):
    def __init__(self):
        super().__init__()
        self.signals = WorkerSignals()
        self.running = True

    @pyqtSlot()
    def run(self):
        ser = serial.Serial("/dev/cu.usbmodem14201", 9600, timeout=0.1)
        time.sleep(2)
        print(ser.readline())

        ser.reset_input_buffer()


        while self.running:
            line = ser.readline().decode("utf-8", errors = "ignore").strip()

            if line and "," in line:
                parts = line.split(",")

                if len(parts) == 2:
                    theta = np.deg2rad(float(parts[0]))
                    r = float(parts[1])

                    self.signals.data.emit(theta, r)


class WorkerSignals(QObject):
    data = pyqtSignal(float, float)

class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.threadPool = QThreadPool()

        #Daten empfangen
        self.distanzlabel = self.makeLabel("Distanz: -- ")
        self.winkellabel = self.makeLabel("Winkel: -- ")



        #Layout erstellen
        layout = QHBoxLayout()
        layoutRight = QVBoxLayout()

        #Linkes Platzhalter Widget
        layout.addWidget(self.makeLabel("Platzhalter Radar"))

        #Button erstellen
        startButton = QPushButton("Start")
        stopButton = QPushButton("Stop")

        startButton.clicked.connect(self.start)
        stopButton.clicked.connect(self.stop)

        #Rechtes Platzhalter Widget
        layoutRight.addWidget(self.distanzlabel)
        layoutRight.addWidget(self.winkellabel)
        layoutRight.addWidget(startButton)
        layoutRight.addWidget(stopButton)

        #Rechtes Layout anhägen
        layout.addLayout(layoutRight)

        #Center Widget für Fenster
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


        self.setStyleSheet("""
                                   QMainWindow {
                                   background-color: black;
                                   }

                                   QWidget{
                                   background-color: black;
                                   color: lime;
                                   }
                                   
                                   QLabel {
                                   border: 1px solid lime; 
                                   border-radius: 5px;
                                   padding: 5px;
                                   background-color: #1a1a1a;
                                   color: lime;
                                   }

                                   QPushButton {
                                    background-color: #1a1a1a;
                                    border: 1px solid lime; 
                                    padding: 5px;
                                    color: lime;
                                    border-radius: 5px;
                                   }

                                   QPushButton:pressed {
                                   background-color: #2a2a2a;
                                   }

                """)

    def start(self):
        self.worker = Worker()
        self.worker.signals.data.connect(self.updateData)
        self.threadPool.start(self.worker)

    def stop(self):
        if hasattr(self, "worker"):
            self.worker.running = False

    def makeLabel(self, text):
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        return label

    def updateData(self, theta, r):
        self.distanzlabel.setText("Distanz: " + str(r))
        self.winkellabel.setText(f"Winkel: {np.rad2deg(theta):.1f}°")

app = QApplication([])
app.setStyle(QStyleFactory.create('Fusion'))
window = mainWindow()
window.show()
app.exec_()


