import sys
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QWidget, QDesktopWidget
from PyQt5.QtWidgets import (QApplication, QPushButton, QLabel)

from PyQt5 import QtGui, QtCore, Qt
from PyQt5.Qt import *
from PyQt5.QtCore import QRect, Qt, QTimer

from PyQt5.QtGui import QPixmap

#Other Win
import FCFS
import SRTF

class processSchedWin(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "Simulation of Process Scheduling Algorithm"
        self.width = 1200
        self.height = 950

        self.initWindow()

    def initWindow(self):
        self.resize(self.width, self.height)
        self.setWindowTitle(self.title)

        self.Buttons()
        self.center()
        
        self.show()

    #move window to center
    def center(self):
        # geometry of the main window
        qr = self.frameGeometry()

        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()

        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)

        # top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft())

    def Buttons(self):
        titleLabel = QLabel("Simulation of Process Scheduling", self)
        titleLabel.setGeometry(QRect(30+150,50, 900, 100))
        titleLabel.setStyleSheet("QWidget { color: Black}")
        titleLabel.setFont(QtGui.QFont('Sanserif', 30, QtGui.QFont.Bold))

        titleLabel = QLabel("Algorithm", self)
        titleLabel.setGeometry(QRect(30+150+290,50+50, 900, 100))
        titleLabel.setStyleSheet("QWidget { color: Black}")
        titleLabel.setFont(QtGui.QFont('Sanserif', 30, QtGui.QFont.Bold))

        FCFSButton = QPushButton('First Come First Serve', self)
        FCFSButton.setGeometry(QRect(180,250, 270, 100))
        #FCFSButton.setStyleSheet("QWidget {background-color: Blue}")
        FCFSButton.setFont(QtGui.QFont('Times New Roman',14))
        FCFSButton.clicked.connect(self.clickedFCFS)

        SRTFButton = QPushButton('Shortest Remaining Time First', self)
        SRTFButton.setGeometry(QRect(180,250 + 100+ 25, 270, 100))
        SRTFButton.setFont(QtGui.QFont('Times New Roman',12))
        SRTFButton.clicked.connect(self.clickedSRTF)

    def clickedFCFS(self):
        self._FCFSWin = FCFS.FCFSWin()
        self._FCFSWin.show()
        self.hide()

    def clickedSRTF(self):
        self._SRTFWin = SRTF.SRTFWin()
        self._SRTFWin.show()
        self.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = processSchedWin()
    sys.exit(app.exec_())