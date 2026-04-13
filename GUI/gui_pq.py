import time

import PyQt5
import numpy as np
from PyQt5.QtCore import Qt, QObject, QRunnable, pyqtSignal, pyqtSlot, QThreadPool
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QLabel, QApplication, QPushButton, QWidget, QStyleFactory
import serial
from RadarWidget import RadarWidget


class Worker(QRunnable):
    """
    reads data from the serial port and sends it to the GUI
    """

    def __init__(self):
        super().__init__()
        self.signals = WorkerSignals()
        self.running = True

    @pyqtSlot()
    def run(self):
        """
        main function of the worker thread
        reads data from the serial port and sends it to the GUI
        Format of the data: theta, r (deg, cm)
        :return:
        """


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
    """
    Defines the signals available from a running worker thread.
    """

    data = pyqtSignal(float, float)

class mainWindow(QMainWindow):
    """
    main Window of the GUI
    """

    def __init__(self):
        super().__init__()

        self.resize(800, 400)
        self.setMinimumSize(500, 220)
        self.setWindowTitle("Radar")

        self.threadPool = QThreadPool()

        #Daten empfangen
        self.distanzlabel = self.makeLabel("Distanz: -- ")
        self.winkellabel = self.makeLabel("Winkel: -- ")



        #Layout erstellen
        layout = QHBoxLayout()
        layoutRight = QVBoxLayout()

        #Linkes  Widget
        self.radar = RadarWidget()
        layout.addWidget(self.radar)

        #Button erstellen
        startButton = QPushButton("Start")
        stopButton = QPushButton("Stop")

        startButton.clicked.connect(self.start)
        stopButton.clicked.connect(self.stop)

        #Rechtes Platzhalter Widget
        rightPlaceholder = QWidget()
        rightPlaceholder.setLayout(layoutRight)
        rightPlaceholder.setFixedWidth(200)
        layout.addWidget(rightPlaceholder)

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
                background-color: #2d4a2d;
            }

            QWidget {
                background-color: #2d4a2d;
                color: #c8e6c8;
            }

            QLabel {
                border: 1px solid #7ec850;
                border-radius: 5px;
                padding: 5px;
                background-color: #3a5e3a;
                color: #c8e6c8;
            }

            QPushButton {
                background-color: #3a5e3a;
                border: 1px solid #7ec850;
                padding: 5px;
                color: #c8e6c8;
                border-radius: 5px;
            }

            QPushButton:pressed {
                background-color: #4a7a4a;
            }
        """)



    def start(self):
        """create a new worker thread and start it"""

        self.worker = Worker()
        self.worker.signals.data.connect(self.updateData)
        self.worker.signals.data.connect(self.radar.updateData)
        self.threadPool.start(self.worker)

    def stop(self):
        """stop the worker thread"""

        if hasattr(self, "worker"):
            self.worker.running = False

    def makeLabel(self, text):
        """create a QLabel with the given text and center it"""

        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        return label

    def updateData(self, theta, r):
        """update the GUI with the new data"""
        print(f"theta_deg: {np.rad2deg(theta):.1f}, r: {r}")
        self.distanzlabel.setText("Distanz: " + str(r))
        self.winkellabel.setText(f"Winkel: {np.rad2deg(theta):.1f}°")


app = QApplication([])
app.setStyle(QStyleFactory.create('Fusion'))
window = mainWindow()
window.show()
app.exec_()


