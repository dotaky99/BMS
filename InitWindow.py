import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
import SecondWindow
import Dialogs

form_class = uic.loadUiType("Initial Window.ui")[0]
class InitWindow(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("PreAn")
        self.pushButton.clicked.connect(self.buttonFunction)
        self.qPixmap = QPixmap()
        self.qPixmap.load("BoB.png")
        self.logo.setPixmap(self.qPixmap)

    def buttonFunction(self) :
        dlg = Dialogs.MemoryDialog()
        dlg.exec_()
        file = Dialogs.FileCopy()
        file.exec_()
        file2 = Dialogs.Parsing()
        file2.exec_()
        self.hide()
        self.window2 = SecondWindow.MainWindow()
        self.window2.show()


if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = InitWindow()
    myWindow.show()
    app.exec_()