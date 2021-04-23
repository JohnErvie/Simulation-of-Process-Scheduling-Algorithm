import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

lista = ['aa', 'ab', 'ac']
listb = ['ba', 'bb', 'bc']
listc = ['ca', 'cb', 'cc']
mystruct = {'A':lista, 'B':listb, 'C':listc}

class MyTable(QTableWidget):
    def __init__(self, thestruct, *args):
        QTableWidget.__init__(self, *args)
        self.data = thestruct
        self.setmydata()

    def setmydata(self):
        '''
        n = 0
        for key in self.data:
            m = 0
            for item in self.data[key]:
                newitem = QTableWidgetItem(item)
                if key == 'A':
                    newitem.setBackground(QtGui.QColor(100,100,150))
                elif key == 'B':
                    newitem.setBackground(QtGui.QColor(100,150,100))
                else:
                    newitem.setBackground(QtGui.QColor(150,100,100))
                self.setItem(m, n, QTableWidgetItem('ab').setBackground(QtGui.QColor(100,100,150)))
                m += 1
            n += 1
        '''
        item = QTableWidgetItem(" ")
        item.setBackground(QtGui.QColor(255,0,0))
        self.setItem(0, 1, QTableWidgetItem(item))

def main(args):
    app = QApplication(args)
    table = MyTable(mystruct, 5, 3)
    table.show()
    sys.exit(app.exec_())

if __name__=="__main__":
    main(sys.argv)