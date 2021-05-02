import sys
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QWidget, QDesktopWidget
from PyQt5.QtWidgets import (QApplication, QPushButton, QLabel)

from PyQt5 import QtGui, QtCore, Qt
from PyQt5.Qt import *
from PyQt5.QtCore import QRect, Qt, QTimer

from PyQt5.QtGui import QPixmap

#Other Win
sys.path.insert(1,'Process-Algorithms/First-Come-First-Serve')
import FCFS
sys.path.insert(1,'Process-Algorithms/Shortest-Remaining-Time-First')
import SRTF
sys.path.insert(1,'Process-Algorithms/Round-Robin')
import RR
sys.path.insert(1,'Process-Algorithms/Non-Preemtive-Priority')
import NPP
sys.path.insert(1,'Process-Algorithms/Preemtive-Priority')
import PP
sys.path.insert(1,'Process-Algorithms/Shortest-Job-First')
import SJF

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
        FCFSButton.setGeometry(QRect(180+50,250, 270, 100))
        #FCFSButton.setStyleSheet("QWidget {background-color: Blue}")
        FCFSButton.setFont(QtGui.QFont('Times New Roman',14))
        FCFSButton.clicked.connect(self.clickedFCFS)

        SRTFButton = QPushButton('Shortest Remaining Time First', self)
        SRTFButton.setGeometry(QRect(180+50,250 + 100+ 25, 270, 100))
        SRTFButton.setFont(QtGui.QFont('Times New Roman',12))
        SRTFButton.clicked.connect(self.clickedSRTF)

        RRButton = QPushButton('Round Robin', self)
        RRButton.setGeometry(QRect(180+50,250 + 100+ 25 + 125, 270, 100))
        RRButton.setFont(QtGui.QFont('Times New Roman',14))
        RRButton.clicked.connect(self.clickedRR)

        NPPButton = QPushButton('None Pre-emptive Priority', self)
        NPPButton.setGeometry(QRect(180+500,250, 270, 100))
        NPPButton.setFont(QtGui.QFont('Times New Roman',14))
        NPPButton.clicked.connect(self.clickedNPP)

        PPButton = QPushButton('Pre-emptive Priority', self)
        PPButton.setGeometry(QRect(180+500,250 + 125, 270, 100))
        PPButton.setFont(QtGui.QFont('Times New Roman',14))
        PPButton.clicked.connect(self.clickedPP)

        SJFButton = QPushButton('Shortest Job First', self)
        SJFButton.setGeometry(QRect(180+500,250 + 100+ 25 + 125, 270, 100))
        SJFButton.setFont(QtGui.QFont('Times New Roman',14))
        SJFButton.clicked.connect(self.clickedSJF)

    def clickedFCFS(self):
        self._FCFSWin = FCFS.FCFSWin()
        self._FCFSWin.show()
        self.hide()

    def clickedSRTF(self):
        self._SRTFWin = SRTF.SRTFWin()
        self._SRTFWin.show()
        self.hide()

    def clickedRR(self):
        self._RR_Win = RR.RR_Win()
        self._RR_Win.show()
        self.hide()

    def clickedNPP(self):
        self._NPPWin = NPP.NPPWin()
        self._NPPWin.show()
        self.hide()

    def clickedPP(self):
        self._PPWin = PP.PPWin()
        self._PPWin.show()
        self.hide()

    def clickedSJF(self):
        self._SJFWin = SJF.SJFWin()
        self._SJFWin.show()
        self.hide()
        
stylesheet = """
    processSchedWin {
        background-image: url(Icons/processes.jpg);
        background-repeat: no-repeat;
        background-position: center;
    }
"""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet)
    ex = processSchedWin()
    sys.exit(app.exec_())