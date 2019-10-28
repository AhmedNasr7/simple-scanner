from PyQt5.uic import loadUiType
import sys
from os import path
from PyQt5.QtWidgets import *
import PyQt5.QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from tokenizer import *



FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "main.ui"))


class MainApp(QMainWindow, FORM_CLASS):

    def __init__(self, parent= None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setup_Ui()
        self.init_Buttons()

    def setup_Ui(self):
        self.center_window()

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
        




def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()