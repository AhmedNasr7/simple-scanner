from PyQt5.uic import loadUiType
import sys
from os import path
from PyQt5.QtWidgets import *
import PyQt5.QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from tokenizer import *
from results_table import *


#FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "main.ui"))


class MainApp(QMainWindow):

    def __init__(self, parent= None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        #self.setupUi(self)
        self.setup_Ui()
        self.init_Buttons()

    def setup_Ui(self):
        self.setFixedSize(867, 526)
        self.create_widgets()
        self.center_window()
        #self.setFixedSize(self.window_width, self.window_height)

        self.setWindowTitle('Compiler Scanner')


    def create_widgets(self):
        self.textBox = QTextEdit(self)
        self.textBox.move(20, 20)
        self.textBox.setFixedSize(621, 441)
        self.tokenize_button = QPushButton('Tokenize', self)
        self.tokenize_button.move(700, 50)
        self.tokenize_button.setFixedSize(121, 31)
        


    def center_window(self):

        # centering window
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def init_Buttons(self):
        self.tokenize_button.clicked.connect(self.tokenize)


    def tokenize(self):
        code_text = self.textBox.toPlainText()
        self.tokenizer = Tokenizer(code_text)
        self.tokenizer.pass_data_signal.connect(self.receive_data)
        self.tokenizer.error_signal.connect(self.show_msgBox)
        self.tokenizer.tokenize()


    @pyqtSlot(list)
    def receive_data(self, tokens_list):
        self.display_results(tokens_list)


    
    def display_results(self, tokens_list):
        tablemodel = TableView(tokens_list)
        self.table = ResultsTable(tablemodel)
        self.table.show()

    
    @pyqtSlot(str)
    def show_msgBox(self, msg):
        print(msg)
        self.msgBox = QMessageBox()
        self.msgBox.setWindowTitle("Error!")
        self.msgBox.setIcon(QMessageBox.Warning)
        self.msgBox.setText(msg)
        self.msgBox.setStandardButtons(QMessageBox.Ok)
        self.msgBox.exec_()  
        



def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()