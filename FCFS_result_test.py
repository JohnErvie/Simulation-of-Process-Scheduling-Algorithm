import sys 
from PyQt5.QtWidgets import (QMainWindow, QWidget, QDesktopWidget, QApplication, QPushButton, QLabel, QTableWidget)
from PyQt5 import *

from PyQt5 import QtGui, QtCore, Qt
from PyQt5.QtGui import *
from PyQt5.Qt import *
from PyQt5.QtCore import *

import numpy as np

class FCFS_ResultWin(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "First Come First Serve Result"
        self.width = 1200
        self.height = 950

        self.initWindow()

    def initWindow(self):
        self.resize(self.width, self.height)
        self.setWindowTitle(self.title)
        self.center()

        self.resultLabels()
        self.resultTable()

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

        #print(self.FCFS_valTables)

    def resultLabels(self):
        titleResultLabel = QLabel("Result", self)
        titleResultLabel.setGeometry(QRect(30+125+350,50, 900, 100))
        titleResultLabel.setStyleSheet("QWidget { color: Black}")
        titleResultLabel.setFont(QtGui.QFont('Sanserif', 30, QtGui.QFont.Bold))

    def resultTable(self):
        self.values = ['p1', 1, 24, 'p2', 22, 3, 'p3', 25, 3]
        self.waitingTime = [['p1', 0], ['p2', 3], ['p3', 3]]
        self.TAT = [['p1', 24], ['p2', 6], ['p3', 6]]
        self.lenVal = int(len(self.values))

        self.rowResultTable = int(self.lenVal/3)
        self.columnResultTable = 5
        self.FCFSResultTable = QTableWidget(self.rowResultTable,self.columnResultTable,self)
        self.FCFSResultTable.setGeometry(QRect(100,50+100, 975, 350))
        self.FCFSResultTable.setFont(QtGui.QFont('Sanserif', 12))

        self.FCFSResultTable.setHorizontalHeaderLabels(("Process ID", "Arrival Time", "Burst Time","Wating Time","Turn Around Time"))
        self.FCFSResultTable.setColumnWidth(0,190)
        self.FCFSResultTable.setColumnWidth(1,190)
        self.FCFSResultTable.setColumnWidth(2,190)
        self.FCFSResultTable.setColumnWidth(3,190)
        self.FCFSResultTable.setColumnWidth(4,190)

        valIndex = 0
        for i in range(self.rowResultTable):
            for j in range(0,3):
                self.FCFSResultTable.setItem(i,j,QTableWidgetItem(str(self.values[valIndex])))
                valIndex += 1

        for i in range(self.rowResultTable):
            for j in range(self.rowResultTable):
                if str(self.FCFSResultTable.item(i,0).text()) == str(self.waitingTime[j][0]):
                    self.FCFSResultTable.setItem(i,3,QTableWidgetItem(str(self.waitingTime[j][1])))

        for i in range(self.rowResultTable):
            for j in range(self.rowResultTable):
                if str(self.FCFSResultTable.item(i,0).text()) == str(self.TAT[j][0]):
                    self.FCFSResultTable.setItem(i,4,QTableWidgetItem(str(self.TAT[j][1])))

        self.AveWT = 0 # average wating time
        self.AveTT = 0 # Total turn around time

        for i in range(len(self.waitingTime)):
            self.AveWT += int(self.waitingTime[i][1])/3
            self.AveTT += int(self.TAT[i][1])/3

        self.aveWTLabel = QLabel(self)
        self.aveWTLabel.setGeometry(QRect(100,500, 900, 50))
        self.aveWTLabel.setStyleSheet("QWidget { color: Black}")
        self.aveWTLabel.setFont(QtGui.QFont('Sanserif', 13, QtGui.QFont.Bold))
        self.aveWTLabel.setText("Average Waiting Time: " + str(self.AveWT))

        self.aveTTLabel = QLabel(self)
        self.aveTTLabel.setGeometry(QRect(100,500 + 25, 900, 50))
        self.aveTTLabel.setStyleSheet("QWidget { color: Black}")
        self.aveTTLabel.setFont(QtGui.QFont('Sanserif', 13, QtGui.QFont.Bold))
        self.aveTTLabel.setText("Average Turn Around Time: " + str(self.AveTT))



        print("Average Wating Time: ", self.AveWT)
        print("Average Turn Around Time: ", self.AveTT)
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = FCFS_ResultWin()
    sys.exit(app.exec_())