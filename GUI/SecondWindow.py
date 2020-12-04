import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import Tabs
import Dialogs

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Believe Me Sister' # 실행 프로그램의 이름
        # 실행 프로그램의 시작 위치 설정
        # self.left = 100
        # self.top = 100
        # self.width = 1000
        # self.height = 700
        self.showMaximized();
        self.initUI()
        # UTC 변환
        self.UTC = None
        self.init_UTC()
        self.widget = Tabs.MyWidget(self, self.UTC)
        self.setCentralWidget(self.widget)

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon('bob.png')) # 실행 프로그램 대표 이미지
        # self.setGeometry(self.left, self.top, self.width, self.height) # 실행 프로그램의 시작 위치
        self.make_menubar() # 메뉴바 만들기
        self.show()

    def make_menubar(self):
        menuBar = self.menuBar()

        # 파일 메뉴
        self.Filemenu = menuBar.addMenu("파일")
        self.exitAction = QAction(QIcon('exit.png'), 'Exit', self)
        self.exitAction.setStatusTip('Exit application')
        self.exitAction.triggered.connect(qApp.quit) # 프로그램 종료와 연결

        # 보기 메뉴
        self.Viewmenu = menuBar.addMenu("보기")
        self.viewAction1 = QAction(QIcon('view1.png'), 'UTC 설정', self)
        self.viewAction1.setStatusTip('set UTC')
        self.viewAction1.triggered.connect(self.View1Action_open) # UTC 설정

        # 도움말 메뉴
        self.Helpmenu = menuBar.addMenu("도움말")
        self.helpAction = QAction(QIcon('help.png'), '도움말', self)
        self.helpAction.setStatusTip('Information about Tool')
        self.helpAction.triggered.connect(self.HelpAction_open) # 도움말

        self.MenuList()

    def MenuList(self):
        self.FileAct = [self.exitAction]
        self.ViewAct = [self.viewAction1]
        self.HelpAct = [self.helpAction]

        for i in self.FileAct:
            self.Filemenu.addAction(i)
        for i in self.ViewAct:
            self.Viewmenu.addAction(i)
        for i in self.HelpAct:
            self.Helpmenu.addAction(i)

    def View1Action_open(self):
        try:
            dlg = Dialogs.UTCDialog(self)
            dlg.exec()
            self.UTC = dlg.UTC
            self.widget = Tabs.MyWidget(self, self.UTC)
            self.setCentralWidget(self.widget)
        except:
            pass

    def HelpAction_open(self):
        Dialogs.HelpDialog(self)
        QLabel(self)

    def init_UTC(self):
        dlg = Dialogs.UTCDialog(self)
        dlg.exec()
        self.UTC = dlg.UTC

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())