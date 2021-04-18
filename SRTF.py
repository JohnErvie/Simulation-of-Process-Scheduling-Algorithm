import sys 
from PyQt5.QtWidgets import (QMainWindow, QWidget, QDesktopWidget, QApplication, QPushButton, QLabel, QTableWidget)
from PyQt5 import *

from PyQt5 import QtGui, QtCore, Qt
from PyQt5.QtGui import *
from PyQt5.Qt import *
from PyQt5.QtCore import *

import numpy as np

#Other Win
import main

SRTF_values = []

class SRTFWin(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "Shortest Remaining Time First"
        self.width = 1200
        self.height = 950

        self.initWindow()

    def initWindow(self):
        self.resize(self.width, self.height)
        self.setWindowTitle(self.title)

        self.Labels()
        self.Buttons()
        self.center()
        self.Table()
        
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

    def Labels(self):
        titleLabel = QLabel("Shortest Remaining Time First", self)
        titleLabel.setGeometry(QRect(30+150+25,50, 900, 100))
        titleLabel.setStyleSheet("QWidget { color: Black}")
        titleLabel.setFont(QtGui.QFont('Sanserif', 30, QtGui.QFont.Bold))
        
    def Buttons(self):
        backButton = QPushButton('Back', self)
        backButton.setGeometry(QRect(150,850, 150, 50))
        #backButton.setStyleSheet("QWidget {background-color: Blue}")
        backButton.setFont(QtGui.QFont('Times New Roman',14))
        #backButton.clicked.connect(self.clickedBack)

        self.addBtnHeight = 0

        self.addButton = QPushButton('', self)
        self.addButton.setIcon(QtGui.QIcon('Icons/plus.png'))
        self.addButton.setGeometry(QRect(45,220, 37, 37))
        self.addButton.clicked.connect(self.clickedAdd)

        self.deleteBtnHeight = 0

        self.deleteButton = QPushButton('', self)
        self.deleteButton.setIcon(QtGui.QIcon('Icons/remove.png'))
        self.deleteButton.setGeometry(QRect(1080,220, 37, 37))
        self.deleteButton.clicked.connect(self.clickedDelete)
        self.deleteButton.hide()

        calButton = QPushButton('Simulate', self)
        calButton.setGeometry(QRect(1200-150-165,850, 150, 50))
        calButton.setFont(QtGui.QFont('Times New Roman',14))
        calButton.clicked.connect(self._clickedCal)
    
    def Table(self):
        self.row = 1
        self.column = 3
        self.SRTFTable = QTableWidget(self.row,self.column,self)
        self.SRTFTable.setGeometry(QRect(100,50+100, 975, 650))
        
        self.SRTFTable.setHorizontalHeaderLabels(("Process ID", "Arrival Time", "Burst Time"))
        self.SRTFTable.setColumnWidth(0,316)
        self.SRTFTable.setColumnWidth(1,316)
        self.SRTFTable.setColumnWidth(2,316)

        self.updateAddRow()

    #def clickedBack(self):
    #    self._processSchedWin = main.processSchedWin()
    #    self._processSchedWin.show()
    #    self.hide()

    def clickedAdd(self):
        self.addBtnHeight += 37
        self.animAddBtn = QPropertyAnimation(self.addButton, b"geometry")
        self.animAddBtn.setDuration(1)
        self.animAddBtn.start()
        self.animAddBtn.setEndValue(QRect(45,220 + self.addBtnHeight, 37, 37))

        
        self.SRTFTable.insertRow(self.rowCount)

        self.deleteBtnHeight += 37
        self.animdelBtn = QPropertyAnimation(self.deleteButton, b"geometry")
        self.animdelBtn.setDuration(1)
        self.animdelBtn.start()
        self.animdelBtn.setEndValue(QRect(1080,220 - 37 + self.deleteBtnHeight, 37, 37))
        self.deleteButton.show()

        self.updateAddRow()

    def clickedDelete(self):
        if self.SRTFTable.rowCount() > 0:
            self.SRTFTable.removeRow(self.SRTFTable.rowCount()-1)
            
            self.addBtnHeight -= 37
            self.animAddBtn.start()
            self.animAddBtn.setEndValue(QRect(45,220 + self.addBtnHeight, 37, 37))

            self.deleteBtnHeight -= 37
            self.animdelBtn.start()
            self.animdelBtn.setEndValue(QRect(1080,220 - 37 + self.deleteBtnHeight, 37, 37))

            #self.updateTableLineEdit()

        if self.SRTFTable.rowCount() == 1:
            self.deleteButton.hide()

        self.updateDelRow()

    def updateAddRow(self):
        self.rowCount = self.SRTFTable.rowCount()
        self.onlyInt = QIntValidator()
        for i in range(1,3): 
            self.tableLE = QLineEdit()
            self.tableLE.setFont(QtGui.QFont('Times New Roman',14))
            self.tableLE.setValidator(self.onlyInt)
            self.SRTFTable.setCellWidget(self.SRTFTable.rowCount()-1, i, self.tableLE)
        
        if self.SRTFTable.rowCount() > 0:
            for x in range(0,self.SRTFTable.rowCount()):
                self.tableLable = QLineEdit()
                self.tableLable.setFont(QtGui.QFont('Times New Roman',14))
                self.SRTFTable.setCellWidget(self.SRTFTable.rowCount()-1, 0, self.tableLable)

    def updateDelRow(self):
        self.rowCount = self.SRTFTable.rowCount()
        self.onlyInt = QIntValidator()
        for i in range(1,3): 
            self.tableLE = QLineEdit()
            self.tableLE.setFont(QtGui.QFont('Times New Roman',14))
            self.tableLE.setValidator(self.onlyInt)
            self.SRTFTable.setCellWidget(self.SRTFTable.rowCount(), i, self.tableLE)
        
        if self.SRTFTable.rowCount() > 0:
            for x in range(0,self.SRTFTable.rowCount()):
                self.tableLable = QLineEdit()
                self.tableLable.setFont(QtGui.QFont('Times New Roman',14))
                self.SRTFTable.setCellWidget(self.SRTFTable.rowCount(), 0, self.tableLable)

    def _clickedCal(self):
        self.valTables = []
        
        for row in range(0,self.rowCount):
            col_index = 0
            for col in range(0,3):
                item = self.SRTFTable.cellWidget(row, col)
                item_text = item.text()
                if col_index > 0:
                    if item_text == '':
                        self.valTables.append(item_text)
                    else:
                        self.valTables.append(int(item_text))
                else:
                    self.valTables.append(item_text)
                    
                col_index += 1

        self.lengthVal = len(self.valTables)

        #getting all process ID
        processID = []
        i = 0 # PID starts with 0 index
        while i < self.lengthVal:
            processID.append(self.valTables[i])
            i += 3

        emptyCount = 0
        for i in range(self.lengthVal):
            if self.valTables[i] == '':
                emptyCount+=1
        
        if emptyCount > 0:
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Information)
                msg.setText("Error: empty value")
                msg.setInformativeText("There is/are empty value, Please fill it before to proceed.")
                msg.setWindowTitle("Error")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.show()

        # check if there is/are the same process ID
        elif len(processID) != len(set(processID)):
            msgPID = QMessageBox(self)
            msgPID.setIcon(QMessageBox.Information)
            msgPID.setText("Error: Same process ID")
            msgPID.setInformativeText("There is/are the same process ID, Please check it.")
            msgPID.setWindowTitle("Error")
            msgPID.setStandardButtons(QMessageBox.Ok)
            msgPID.show()

        #else:
        #    global SRTF_values
        #    SRTF_values = self.valTables
        #    self._SRTF_ResultWin = SRTF_ResultWin()
        #    self._SRTF_ResultWin.show()
        #    self.hide()

# SRTF Result Window
class SRTF_ResultWin(QMainWindow):
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

        self.variables()
        self.resultLabels()
        self.resultTable()
        self.resultButtons()

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

    def variables(self):
        global SRTF_values
        self.SRTF_valTables = SRTF_values
        lengthSRTF_valTables = len(self.SRTF_valTables)
        '''
        self.PID = []
        self.arrivalTime = []
        self.burstTime = []

        i = 0 # PID starts with 0 index
        while i < lengthSRTF_valTables:
            self.PID.append(self.SRTF_valTables[i])
            i += 3

        i = 1 # PID starts with 1 index
        while i < lengthSRTF_valTables:
            self.arrivalTime.append(self.SRTF_valTables[i])
            i += 3

        i = 2 # PID starts with 2 index
        while i < lengthSRTF_valTables:
            self.burstTime.append(self.SRTF_valTables[i])
            i += 3
        '''
        self.listedVal = []

        self.listedVal = np.array(self.SRTF_valTables).reshape(int(lengthSRTF_valTables/3),3)

        self.allProcess = int(lengthSRTF_valTables/3)

        exe_time = 0
        end_time = 0

        self.waitingTime = []
        waitingTimeIndex = 0

        self.TAT = [] #Turn around Time
        TATIndex = 0

        # finding the lowest arrival time then execute
        loop = True
        i = 0
        while loop != False:
            for count in range(self.allProcess):
                if int(self.listedVal[count][1]) == i:
                    #print("lowest AT row: ", self.listedVal[count][0])
                    if waitingTimeIndex == 0:
                        exe_time = int(self.listedVal[count][1])
                    end_time = exe_time + int(self.listedVal[count][2])
                    self.waitingTime.append([])
                    self.waitingTime[waitingTimeIndex].append(self.listedVal[count][0])
                    self.waitingTime[waitingTimeIndex].append(exe_time - int(self.listedVal[count][1]))
                    #print("Wating Time of ", self.waitingTime[waitingTimeIndex][0], " is ", self.waitingTime[waitingTimeIndex][1])

                    self.TAT.append([])
                    self.TAT[TATIndex].append(self.listedVal[count][0])
                    self.TAT[TATIndex].append(int(self.waitingTime[waitingTimeIndex][1]) + int(self.listedVal[count][2]))
                    #print("Turn Around Time of ", self.TAT[TATIndex][0], " is ", self.TAT[TATIndex][1])

                    #print("execution time: ", exe_time)
                    
                    exe_time = end_time

                    waitingTimeIndex += 1
                    TATIndex += 1
            if waitingTimeIndex == self.allProcess:
                loop = False
            #print(i)
            i += 1

        self.AveWT = 0 # average wating time
        self.AveTT = 0 # Total turn around time

        for i in range(len(self.waitingTime)):
            self.AveWT += int(self.waitingTime[i][1])/3
            self.AveTT += int(self.TAT[i][1])/3

    def resultTable(self):
        self.rowResultTable = self.allProcess
        self.columnResultTable = 5
        self.SRTFResultTable = QTableWidget(self.rowResultTable,self.columnResultTable,self)
        self.SRTFResultTable.setGeometry(QRect(100,50+100, 975, 350))
        self.SRTFResultTable.setFont(QtGui.QFont('Sanserif', 12))

        self.SRTFResultTable.setHorizontalHeaderLabels(("Process ID", "Arrival Time", "Burst Time","Wating Time","Turn Around Time"))
        self.SRTFResultTable.setColumnWidth(0,190)
        self.SRTFResultTable.setColumnWidth(1,190)
        self.SRTFResultTable.setColumnWidth(2,190)
        self.SRTFResultTable.setColumnWidth(3,190)
        self.SRTFResultTable.setColumnWidth(4,190)

        valIndex = 0
        for i in range(self.rowResultTable):
            for j in range(0,3):
                self.SRTFResultTable.setItem(i,j,QTableWidgetItem(str(self.FCFS_valTables[valIndex])))
                valIndex += 1

        for i in range(self.rowResultTable):
            for j in range(self.rowResultTable):
                if str(self.SRTFResultTable.item(i,0).text()) == str(self.waitingTime[j][0]):
                    self.SRTFResultTable.setItem(i,3,QTableWidgetItem(str(self.waitingTime[j][1])))

        for i in range(self.rowResultTable):
            for j in range(self.rowResultTable):
                if str(self.SRTFResultTable.item(i,0).text()) == str(self.TAT[j][0]):
                    self.SRTFResultTable.setItem(i,4,QTableWidgetItem(str(self.TAT[j][1])))
            
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

    def resultButtons(self):
        backButton = QPushButton('Back to SRTF', self)
        backButton.setGeometry(QRect(150,850, 150, 50))
        #backButton.setStyleSheet("QWidget {background-color: Blue}")
        backButton.setFont(QtGui.QFont('Times New Roman',14))
        backButton.clicked.connect(self.clickedBackFCFS)

        calButton = QPushButton('Main Menu', self)
        calButton.setGeometry(QRect(1200-150-165,850, 150, 50))
        calButton.setFont(QtGui.QFont('Times New Roman',14))
        calButton.clicked.connect(self.clickedMainMenu)

    def clickedBackFCFS(self):
        self._FCFSWin = FCFSWin()
        self._FCFSWin.show()
        self.hide()

    def clickedMainMenu(self):
        self._processSchedWin = main.processSchedWin()
        self._processSchedWin.show()
        self.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = SRTFWin()
    sys.exit(app.exec_())