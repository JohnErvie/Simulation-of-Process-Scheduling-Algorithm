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

        self.setStyleSheet("SRTFWin{background-image: url(Icons/bgimg.jpg);background-repeat: no-repeat;background-position: center;}")

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
        backButton.clicked.connect(self.clickedBack)

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

    def clickedBack(self):
        self._processSchedWin = main.processSchedWin()
        self._processSchedWin.show()
        self.hide()

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

            for i in range(3):
                self.valTables.append(0)

        self.lengthVal = len(self.valTables)

        #getting all process ID
        processID = []
        i = 0 # PID starts with 0 index
        while i < self.lengthVal:
            processID.append(self.valTables[i])
            i += 6

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
            msgPID.setInformativeText("There are the same process ID, Please check it.")
            msgPID.setWindowTitle("Error")
            msgPID.setStandardButtons(QMessageBox.Ok)
            msgPID.show()

        else:
            global SRTF_values
            SRTF_values = self.valTables
            self._SRTF_ResultWin = SRTF_ResultWin()
            self._SRTF_ResultWin.show()
            self.hide()

# SRTF Result Window
class SRTF_ResultWin(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "Short Remaining Time First Result"
        self.width = 1200
        self.height = 950

        global SRTF_values
        self.SRTF_valTables = SRTF_values
        self.lengthSRTF_valTables = len(self.SRTF_valTables)

        self.allProcess = int(self.lengthSRTF_valTables/6)

        self.listedVal = []

        for i in range(self.allProcess): # adding 2d array
            self.listedVal.append([])

        self.indexVal = 0
        for row in range(self.allProcess): # Converting the values to 2d array
            for col in range(6):
                self.listedVal[row].append(self.SRTF_valTables[self.indexVal])
                self.indexVal += 1

        #print(self.listedVal)

        self.timeCount = 0
        self.queue = []
        self.readyQueue = []

        self.processID = []
        i = 0 # PID starts with 0 index
        while i < self.lengthSRTF_valTables:
            self.processID.append(self.SRTF_valTables[i])
            i += 6

        self.totalEndTime = 0
        self.numTerminate = 0

        self.cpuUtil = 0
        self.aveTT = 0
        self.aveWT = 0
        self.currentJob = ""

        # For Gantt Chart
        self.savedTotalUsedTime = 0
        self.ganttChartRow = 0
        self.totalUsedTime = 0

        self.totalBurstTime = 0
        for i in range(self.allProcess): #computing the Cpu Utilization
            self.totalBurstTime += int(self.listedVal[i][2])

        self.totalUsedTime = 0

        self.Donemsg = QMessageBox(self)
        self.Donemsg.setIcon(QMessageBox.Information)
        self.Donemsg.setText("The process are done!")
        #self.Donemsg.setInformativeText("The process are done!")
        self.Donemsg.setWindowTitle("Done")
        self.Donemsg.setStandardButtons(QMessageBox.Ok)

        self.initWindow()

    def initWindow(self):
        self.resize(self.width, self.height)
        self.setWindowTitle(self.title)
        self.center()

        self.resultLabels()
        self.resultButtons()
        self.resultWidgetInit()
        
        self.Timer()
        self.Design()

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

    def resultLabels(self):
        titleResultLabel = QLabel("Shortest Remaining Time First", self)
        titleResultLabel.setGeometry(QRect(30+150+30,10, 900, 100))
        titleResultLabel.setStyleSheet("QWidget { color: Black}")
        titleResultLabel.setFont(QtGui.QFont('Sanserif', 30, QtGui.QFont.Bold))

    def resultButtons(self):
        backButton = QPushButton('Back to SRTF', self)
        backButton.setGeometry(QRect(150,850, 150, 50))
        #backButton.setStyleSheet("QWidget {background-color: Blue}")
        backButton.setFont(QtGui.QFont('Times New Roman',14))
        backButton.clicked.connect(self.clickedBack)

        calButton = QPushButton('Main Menu', self)
        calButton.setGeometry(QRect(1200-150-165,850, 150, 50))
        calButton.setFont(QtGui.QFont('Times New Roman',14))
        calButton.clicked.connect(self.clickedMainMenu)

    def resultWidgetInit(self):
        self.jobPoolLabel = QLabel("Job Pool", self)
        self.jobPoolLabel.setGeometry(QRect(30+130+350,80, 900, 100))
        self.jobPoolLabel.setStyleSheet("QWidget { color: Black}")
        self.jobPoolLabel.setFont(QtGui.QFont('Sanserif', 20, QtGui.QFont.Bold))

        self.rowResultTable = self.allProcess
        self.columnResultTable = 6
        self.ResultTable = QTableWidget(self.rowResultTable,self.columnResultTable,self)
        self.ResultTable.setGeometry(QRect(100,50+100, 975, 217))
        self.ResultTable.setFont(QtGui.QFont('Sanserif', 12))
        #self.FCFSResultTable.setStyleSheet("color: black;background-color: white;")

        self.ResultTable.setHorizontalHeaderLabels(("Process ID", "Arrival Time", "Burst Time", "End Time", "Turn Around Time", "Wating Time"))
        self.ResultTable.setColumnWidth(0,158)
        self.ResultTable.setColumnWidth(1,158)
        self.ResultTable.setColumnWidth(2,158)
        self.ResultTable.setColumnWidth(3,158)
        self.ResultTable.setColumnWidth(4,158)
        self.ResultTable.setColumnWidth(5,158)

        # Gantt Chart Table
        self.rowGanttChartTable = self.allProcess
        self.columnGanttChartTable = 0
        self.ganttChartTable = QTableWidget(self.rowGanttChartTable,self.columnGanttChartTable,self)
        self.ganttChartTable.setGeometry(QRect(100+50,50+100+460, 975-100, 217))
        self.ganttChartTable.setFont(QtGui.QFont('Sanserif', 12))

        self.ganttChartTable.setVerticalHeaderLabels(self.processID)

        for i in range(self.allProcess):
            self.ganttChartTable.setRowHeight(i,15)

        self.currentJobResLabel = QLabel(self)
        self.currentJobResLabel.setGeometry(QRect(100+300+20,225 + 175 + 40 + 50, 150, 50))
        self.currentJobResLabel.setFont(QtGui.QFont('Sanserif', 12, QtGui.QFont.Bold))

        self.aveWTLabel = QLabel(self)
        self.aveWTLabel.setGeometry(QRect(100+300+105+115+170+27,225 + 175 + 40+ 50, 150, 50))
        #self.aveWTLabel.setStyleSheet("QWidget { color: Green}")
        self.aveWTLabel.setFont(QtGui.QFont('Sanserif', 12, QtGui.QFont.Bold))

        self.aveTTLabel = QLabel(self)
        self.aveTTLabel.setGeometry(QRect(100+300+105+115+170+27+130+13,225 + 175 + 40+ 50, 150, 50))
        self.aveTTLabel.setFont(QtGui.QFont('Sanserif', 12, QtGui.QFont.Bold))
        
        self.CPUUtilLabel = QLabel(self)
        self.CPUUtilLabel.setGeometry(QRect(100+300+105+115+25,225 + 175 + 40 + 50, 150, 50))
        self.CPUUtilLabel.setFont(QtGui.QFont('Sanserif', 12, QtGui.QFont.Bold))

        self.currentTimeLabel = QLabel(self)
        self.currentTimeLabel.setGeometry(QRect(100+300+105+38,225 + 175 + 40 + 50, 150, 50))
        self.currentTimeLabel.setFont(QtGui.QFont('Sanserif', 12, QtGui.QFont.Bold))

        self.rowReadyQueueTable = 1
        self.columnGanttChartTable = 0
        self.readyQueueTable = QTableWidget(self.rowReadyQueueTable,self.columnGanttChartTable,self)
        self.readyQueueTable.setGeometry(QRect(100,225 + 175 + 50, 255, 80))
        self.readyQueueTable.setFont(QtGui.QFont('Sanserif', 12))

        self.readyQueueTable.setRowHeight(0,75)

        fnt = self.readyQueueTable.font()
        fnt.setPointSize(11)
        self.readyQueueTable.setFont(fnt)
        self.readyQueueTable.horizontalHeader().hide()
        self.readyQueueTable.verticalHeader().hide()

    def Design(self):
        self.queueLabel = QLabel("Ready Queue", self)
        self.queueLabel.setGeometry(QRect(100,225 + 175, 150, 50))
        self.queueLabel.setFont(QtGui.QFont('Sanserif', 13, QtGui.QFont.Bold))

        self.cpuLabel = QLabel("CPU", self)
        self.cpuLabel.setGeometry(QRect(100+300,225 + 175, 150, 50))
        self.cpuLabel.setFont(QtGui.QFont('Sanserif', 13, QtGui.QFont.Bold))

        self.currentJobLabel = QLabel("Current Job", self)
        self.currentJobLabel.setGeometry(QRect(100+300,225 + 175 + 40, 150, 50))
        self.currentJobLabel.setFont(QtGui.QFont('Sanserif', 11))

        self.currentTimeLlbl = QLabel("Current Time", self)
        self.currentTimeLlbl.setGeometry(QRect(100+300+105,225 + 175 + 40, 150, 50))
        self.currentTimeLlbl.setFont(QtGui.QFont('Sanserif', 11))

        self.cpuUtilLlbl = QLabel("CPU Utilization", self)
        self.cpuUtilLlbl.setGeometry(QRect(100+300+105+115,225 + 175 + 40, 150, 50))
        self.cpuUtilLlbl.setFont(QtGui.QFont('Sanserif', 11))

        self.AveLabel = QLabel("Average", self)
        self.AveLabel.setGeometry(QRect(100+300+105+115+170,225 + 175, 150, 50))
        self.AveLabel.setFont(QtGui.QFont('Sanserif', 13, QtGui.QFont.Bold))

        self.aveWaitingTimelbl = QLabel("Waiting Time", self)
        self.aveWaitingTimelbl.setGeometry(QRect(100+300+105+115+170,225 + 175 + 40, 150, 50))
        self.aveWaitingTimelbl.setFont(QtGui.QFont('Sanserif', 11))

        self.aveTATimelbl = QLabel("Turn Around Time", self)
        self.aveTATimelbl.setGeometry(QRect(100+300+105+115+170+130,225 + 175 + 40, 150, 50))
        self.aveTATimelbl.setFont(QtGui.QFont('Sanserif', 11))

        self.ganttChartLabel = QLabel("Gantt Chart", self)
        self.ganttChartLabel.setGeometry(QRect(100,225 + 175 + 165, 150, 50))
        self.ganttChartLabel.setFont(QtGui.QFont('Sanserif', 15, QtGui.QFont.Bold))

        self.ganttChartTimeLbl = QLabel("Time(s)", self)
        self.ganttChartTimeLbl.setGeometry(QRect(100+460,225 + 175 + 165+10, 150, 50))
        self.ganttChartTimeLbl.setFont(QtGui.QFont('Sanserif'))

    def Timer(self):
        self.start = True

        # creating a timer object
        self.timer = QTimer(self)

        # adding action to timer
        self.timer.timeout.connect(self.variables)

        # update the timer every second
        self.timer.start(1000)

    def variables(self):
        if self.start:
            # if is there process arrive in current time then add it into queue
            for row in range(self.allProcess):
                if self.timeCount == int(self.listedVal[row][1]): ## if there equal to time
                    self.queue.append([]) ## adding to queue
                    self.queue[int(len(self.queue))-1].append(self.listedVal[row][0])
                    self.queue[int(len(self.queue))-1].append(int(self.listedVal[row][1]))
                    self.queue[int(len(self.queue))-1].append(int(self.listedVal[row][2]))

            # find the lowest burst time in queue then execute that
            lowbt = 0
            loopqueue = True
            if int(len(self.queue)) > 0:
                while loopqueue != False:
                    rowbt = 0
                    while rowbt < int(len(self.queue)):
                        if int(self.queue[rowbt][2]) == lowbt:
                            self.queue[rowbt][2] = int(self.queue[rowbt][2]) - 1 # subtract 1 burst time
                            self.currentJob = self.queue[rowbt][0]
                            self.totalUsedTime += 1

                            # saving the row for gantt chart
                            for i in range(self.allProcess):
                                if self.queue[rowbt][0] == self.listedVal[i][0]:
                                    self.ganttChartRow = i

                            rowbt = int(len(self.queue))
                            loopqueue = False
                        rowbt +=1
                    lowbt += 1

                ## Getting the ready Queue
                for i in range(int(len(self.queue))):
                    self.readyQueue.append(self.queue[i][0])

            else:
                self.currentJob = ""

                # deleting the process in queue if 0 burst time
            qRow = 0
            while qRow < int(len(self.queue)):
                if int(self.queue[qRow][2]) <= 0: # if the process has 0 burst time, delete that process in queue
                    for x in range (self.allProcess): # inputing the end time process
                        if self.listedVal[x][0] == self.queue[qRow][0]:
                            self.listedVal[x][3] = self.timeCount + 1
                            self.listedVal[x][4] = int(self.listedVal[x][3]) - int(self.listedVal[x][1]) # Turn around time = End Time - Arrival Time
                            self.listedVal[x][5] = int(self.listedVal[x][4]) - int(self.listedVal[x][2]) # waiting time = Turn Around Time - Burst Time
                            self.numTerminate +=1
                    self.queue.pop(qRow)
                qRow += 1

            # getting the highest end time
            self.totalEndTime = max(l[3] for l in self.listedVal)

            if self.timeCount > 0:
                    self.cpuUtil = (self.totalUsedTime/(self.timeCount+1))*100 # formula for Cpu Utilization

            if self.timeCount == 0:
                if self.totalUsedTime > 0:
                    self.cpuUtil = 100

            #computing the average turn around time and waiting time
            totalWaitingTime = 0
            totalTurnAroundTime = 0
            for i in range(self.allProcess):
                totalWaitingTime += int(self.listedVal[i][5])
                totalTurnAroundTime += int(self.listedVal[i][4])

            self.aveWT = totalWaitingTime/self.allProcess
            self.aveTT = totalTurnAroundTime/self.allProcess


            self.updateResults()
            self.readyQueue.clear()
            self.timeCount += 1

            if self.numTerminate == self.allProcess:
                self.Donemsg.show()
                self.start = False # pause the timer
                self.updateResults()

    def updateResults(self):
        for i in range(self.rowResultTable): # inputting the End time into table
            self.ResultTable.setItem(i,0,QTableWidgetItem(str(self.listedVal[i][0])))
            self.ResultTable.setItem(i,1,QTableWidgetItem(str(self.listedVal[i][1])))
            self.ResultTable.setItem(i,2,QTableWidgetItem(str(self.listedVal[i][2])))
            self.ResultTable.setItem(i,3,QTableWidgetItem(str(self.listedVal[i][3])))
            self.ResultTable.setItem(i,4,QTableWidgetItem(str(self.listedVal[i][4])))
            self.ResultTable.setItem(i,5,QTableWidgetItem(str(self.listedVal[i][5])))

        if self.start:
            self.currentJobResLabel.setText(str(self.currentJob))
        else:
            self.currentJobResLabel.setText("")

        self.aveWTLabel.setText("%.2f" %(self.aveWT))
        self.aveTTLabel.setText("%.2f" %(self.aveTT))
        self.CPUUtilLabel.setText("%.2f" %(self.cpuUtil) + "%")
        self.currentTimeLabel.setText(str(self.timeCount))

        self.readyQueueTable.setColumnCount(int(len(self.readyQueue)))

        for i in range(int(len(self.readyQueue))):
            if i != int(len(self.readyQueue)) - 1:
                self.readyQueueItem = QTableWidgetItem(str(self.readyQueue[i]) + "-->")
            else:
                self.readyQueueItem = QTableWidgetItem(str(self.readyQueue[i]))
            self.readyQueueTable.setItem(0, i, QTableWidgetItem(self.readyQueueItem))
            self.readyQueueTable.setColumnWidth(i,10)
        
        #update gantt chart
        self.gcColumnHeader = QTableWidgetItem(str(self.timeCount))
        self.ganttChartTable.setColumnCount(self.timeCount+1)
        self.ganttChartTable.setHorizontalHeaderItem(self.timeCount,self.gcColumnHeader)

        self.ganttChartTable.setColumnWidth(self.timeCount,10)

        self.item = QTableWidgetItem(" ")
        if self.totalUsedTime > self.savedTotalUsedTime:
            self.item.setBackground(QtGui.QColor(0,0,0))
            self.ganttChartTable.setItem(self.ganttChartRow, self.timeCount, QTableWidgetItem(self.item))
        else:
            self.item.setBackground(QtGui.QColor(255,255,255))
            self.ganttChartTable.setItem(self.ganttChartRow, self.timeCount, QTableWidgetItem(self.item))

        self.savedTotalUsedTime = self.totalUsedTime # saved the last totalUsedTime



    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 10))
        
        painter.drawRect(80,100,1015,300-10) # Rec in top layer

        painter.drawRect(80,60+330,1015,170) # Rec in second layer

        painter.drawLine(80+300,60+330,80+300,550) # line between ready queue and cpu

        painter.drawLine(80+300+385,60+330,80+300+385,550) # line between cpu and average

        painter.drawRect(80,60+330 + 170,1015,275) # Bot in top layer

        painterTxt = QtGui.QPainter(self)
        painterTxt.setPen(QPen(Qt.black))
        painterTxt.translate(20, 800)
        painterTxt.rotate(-90)
        painterTxt.drawText(50, 125, "Process ID")
        painterTxt.end()
    
    def clickedBack(self):
        self.timer.stop()
        self._SRTFWin = SRTFWin()
        self._SRTFWin.show()
        self.hide()

    def clickedMainMenu(self):
        self._processSchedWin = main.processSchedWin()
        self._processSchedWin.show()
        self.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = SRTFWin()
    sys.exit(app.exec_())