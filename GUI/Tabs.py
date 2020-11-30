import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtCore import *
import sqlite3
from GUI import Tab2, Tab3, Tab4

class MyWidget(QWidget):
    def __init__(self, parent):
        super(MyWidget, self).__init__(parent)
        self.setGeometry(100, 100, 1500, 700)
        self.initUI()

    def initUI(self):
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tabs = QTabWidget()
        self.tabs.addTab(self.tab2, "확인 사항")
        self.tabs.addTab(self.tab3, "타임라인")
        self.tabs.addTab(self.tab4, "데이터")

        Tab2.Tab2.set_tab2(self)
        Tab3.Tab3.set_tab3(self)
        Tab4.Tab4.set_tab4(self)

        total_layout = QVBoxLayout()
        total_layout.addWidget(self.tabs)
        self.setLayout(total_layout)

# def set_color(self):
#     for i in range(self.timeline_count):
#         # if self.timeline.item(1, i) == "안티포렌식 도구 실행":
#         #     self.timeline.item(1, i).setBackground(QtGui.QColor(125, 0, 0))
#         self.timeline.item(1, i).setBackground(Qt.red)
#         # self.timeline.item(1, i).setBackground(QtGui.QColor(125, 0, 0))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywidget = MyWidget()
    mywidget.show()
    sys.exit(app.exec_())