import sys
from os import path
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, \
    QPushButton, QCheckBox, QGridLayout, QDesktopWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot


class ResultsTable(QMainWindow):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.initUI()

    def initUI(self):
        self.setMinimumSize(500,500)
        self.tableview = QTableView(self)
        self.tableview.setModel(self.model)
        self.tableview.setFixedSize(400, 400)
        self.setWindowTitle('Lexical Results')
        self.center_window()


        # size policy
        self.tableview.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        #tableview.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum) # ---
        self.tableview.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)# ++

    

        
    def center_window(self):

        # centering window
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())


class TableView(QAbstractTableModel):
    
    def __init__(self, tokens, parent = None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        #super().__init__()
        
        self.__rows = []
        self.__headers = ['Token', 'Type']
        for token_obj in tokens:
            self.__rows.append((token_obj.value(), token_obj.type()))

        
    def init_ui(self):
        pass
    def rowCount(self, parent):
        return len(self.__rows)
        
    def columnCount(self, parent):
        return len(self.__headers)

    def data(self, index, role):
        if role != Qt.DisplayRole:
            return QVariant()
        # What's the value of the cell at the given index?
        return self.__rows[index.row()][index.column()]

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole or orientation != Qt.Horizontal:
            return QVariant()
        return self.__headers[section]
      


'''
if __name__ == '__main__':
    app = QApplication([])
    model = ResultsTable()
    view = QTableView()
    view.setModel(model)
    view.setFixedSize(500, 500)
    view.show()
    app.exec_()
'''

