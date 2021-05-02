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

SJF_values = ['p1', 3, 4, 0, 0, 0, 'p2', 5, 9, 0, 0, 0, 'p3', 8, 4, 0, 0, 0, 'p4', 0, 7, 0, 0, 0, 'p5', 12, 6, 0, 0, 0]

# SJF Result Window
class SJF_ResultWin(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "Shortest Job First Result"
        
        self.width = 1200
        self.height = 950

        #self.setStyleSheet("background-color: black;")

        ## Initializing variables
        global SJF_values
        self.SJF_valTables = SJF_values
        self.values = self.SJF_valTables
        self.lengthSJF_valTables = len(self.values)

        self.allProcess = int(self.lengthSJF_valTables/6)

        self.listedVal = []

        for i in range(self.allProcess): # adding 2d array
            self.listedVal.append([])

        self.indexVal = 0
        for row in range(self.allProcess): # Converting the values to 2d array
            for col in range(6):
                self.listedVal[row].append(self.values[self.indexVal])
                self.indexVal += 1

        self.currentJob = ""

        self.SimulationSpeed = 1
        self.totalEndTime = 0
        self.queue = []
        self.readyQueue = []
        self.curJobQueue = []
        self.savedQueue = []

        self.processID = []
        i = 0 # PID starts with 0 index
        while i < self.lengthSJF_valTables:
            self.processID.append(self.SJF_valTables[i])
            i += 6
        #print(self.processID)

        self.savedTotalUsedTime = 0
        self.ganttChartRow = 0
        self.totalUsedTime = 0

        self.cpuUtil = 0
        self.aveTT = 0
        self.aveWT = 0

        self.numTerminate = 0

        self.timeCount = 0

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

        #print(self.SJF_valTables)

    def resultLabels(self):
        titleResultLabel = QLabel("Shortest Job First", self)
        titleResultLabel.setGeometry(QRect(30+150+125+55,10, 900, 100))
        titleResultLabel.setStyleSheet("QWidget { color: Black}")
        titleResultLabel.setFont(QtGui.QFont('Sanserif', 30, QtGui.QFont.Bold))

    def resultButtons(self):
        backButton = QPushButton('Back to SJF', self)
        backButton.setGeometry(QRect(150,850, 150, 50))
        #backButton.setStyleSheet("QWidget {background-color: Blue}")
        backButton.setFont(QtGui.QFont('Times New Roman',14))
        backButton.clicked.connect(self.clickedBackSJF)

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
        #self.ResultTable.setStyleSheet("color: black;background-color: white;")
        self.ResultTable.setStyleSheet("background: rgb(160,200,170);")

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
        timer = QTimer(self)

        # adding action to timer
        timer.timeout.connect(self.variables)

        # update the timer every second
        timer.start(1000)
        
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
                    while rowbt < int(len(self.queue)): # finding the lowest burst time
                        if int(self.queue[rowbt][2]) == lowbt:
                            if int(len(self.curJobQueue)) > 0:
                                curjob = 0
                                while curjob < int(len(self.queue)):
                                    if self.queue[curjob][0] == self.curJobQueue[0]:
                                        self.queue[curjob][2] = int(self.queue[curjob][2]) - 1 # subtract 1 burst time
                                
                                        self.currentJob = self.queue[curjob][0]
                                        self.totalUsedTime += 1

                                        # saving the row for gantt chart
                                        for i in range(self.allProcess):
                                            if self.queue[curjob][0] == self.listedVal[i][0]:
                                                self.ganttChartRow = i

                                        # putting the current job to the top of queue
                                        for i in range(3):
                                            self.savedQueue.append(self.queue[curjob][i])
                                        self.queue.pop(curjob)
                                        self.queue.insert(0,[])
                                        for i in range(3):
                                            self.queue[0].append(self.savedQueue[i])

                                        self.savedQueue.clear()

                                        curjob = int(len(self.queue))
                                    curjob += 1
                            else:
                                self.queue[rowbt][2] = int(self.queue[rowbt][2]) - 1 # subtract 1 burst time

                                for i in range(3):
                                    self.curJobQueue.append(self.queue[rowbt][i])
                                
                                self.currentJob = self.queue[rowbt][0]
                                
                                self.totalUsedTime += 1

                                # saving the row for gantt chart
                                for i in range(self.allProcess):
                                    if self.queue[rowbt][0] == self.listedVal[i][0]:
                                        self.ganttChartRow = i

                                # putting the current job to the top of queue
                                for i in range(3):
                                    self.savedQueue.append(self.queue[rowbt][i])
                                self.queue.pop(rowbt)
                                self.queue.insert(0,[])
                                for i in range(3):
                                    self.queue[0].append(self.savedQueue[i])

                                self.savedQueue.clear()

                            rowbt = int(len(self.queue))
                            loopqueue = False
                        rowbt +=1
                    lowbt += 1

                ## Getting the ready Queue
                for i in range(int(len(self.queue))):
                    self.readyQueue.append(self.queue[i][0])

            else:
                self.currentJob = ""
                    
            qRow = 0
            while qRow < int(len(self.queue)):
                if int(self.queue[qRow][2]) <= 0: # if the process has 0 burst time, delete that process in queue
                    for x in range (self.allProcess): # inputing the end time process
                        if self.listedVal[x][0] == self.queue[qRow][0]: # if process id is same as in queue, then input it in specific process
                            self.listedVal[x][3] = self.timeCount + 1
                            self.listedVal[x][4] = int(self.listedVal[x][3]) - int(self.listedVal[x][1]) # Turn around time = End Time - Arrival Time
                            self.listedVal[x][5] = int(self.listedVal[x][4]) - int(self.listedVal[x][2]) # waiting time = Turn Around Time - Burst Time
                            self.numTerminate +=1
                    self.queue.pop(qRow)
                    self.curJobQueue.clear()
                qRow += 1

            ### updating the values
            totalWaitingTime = 0
            totalTurnAroundTime = 0
            for i in range(self.allProcess): #computing the average turn around time
                totalWaitingTime += int(self.listedVal[i][5])
                totalTurnAroundTime += int(self.listedVal[i][4])
            
            self.aveWT = totalWaitingTime/self.allProcess
            self.aveTT = totalTurnAroundTime/self.allProcess

            # getting the highest end time
            self.totalEndTime = max(l[3] for l in self.listedVal)

            if self.timeCount > 0:
                self.cpuUtil = (self.totalUsedTime/(self.timeCount+1))*100 # formula for Cpu Utilization

            if self.timeCount == 0:
                if self.totalUsedTime > 0:
                    self.cpuUtil = 100

            #if self.numTerminate != self.allProcess:
            self.updateResults()
            self.readyQueue.clear()
            self.timeCount += 1
            
            if self.numTerminate == self.allProcess:
                #self.Donemsg.show()
                self.start = False # pause the timer
                self.updateResults()
            #loop = False

    # update the table
    def updateResults(self):
        for i in range(self.rowResultTable): # inputting the End time into table
            for j in range(6):
                self.ResultTable.setItem(i,j,QTableWidgetItem(str(self.listedVal[i][j])))

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

    def clickedBackSJF(self):
        #self.Donemsg.hide()
        self._SJFWin = SJFWin()
        self._SJFWin.show()
        self.hide()

    def clickedMainMenu(self):
        self._processSchedWin = main.processSchedWin()
        self._processSchedWin.show()
        self.hide()

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

stylesheet = """
    SJF_ResultWin {
        background-image: url(Icons/sjpbg1.jpg);
        background-repeat: no-repeat;
        background-position: center;
    }
"""
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet)
    ex = SJF_ResultWin()
    sys.exit(app.exec_())