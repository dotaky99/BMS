import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import Tabs

class UTCDialog(QDialog):
    def __init__(self, parent):
        super(UTCDialog, self).__init__(parent)
        self.setupUI()
        self.UTC = None

    def setupUI(self):
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('UTC 설정')
        layout = QBoxLayout(QBoxLayout.TopToBottom, parent = self)
        self.setLayout(layout)
        label = QLabel()
        self.combobox = QComboBox()
        self.combobox.addItems(["UTC-12", "UTC-11", "UTC-10", "UTC-9", "UTC-8", "UTC-7", "UTC-6",
                    "UTC-5", "UTC-4", "UTC-3", "UTC-2", "UTC-1", "UTC+0", "UTC+1",
                    "UTC+2", "UTC+3", "UTC+4", "UTC+5", "UTC+6", "UTC+7", "UTC+8",
                    "UTC+9", "UTC+10", "UTC+11", "UTC+12", "UTC+13"])
        layout.addWidget(self.combobox)
        layout.addWidget(label)
        self.button = QPushButton("확인", self) # 버튼 텍스트
        self.button.move(190, 250) # 버튼 위치
        self.button.clicked.connect(self.buttonClicked) # 클릭 시 실행할 function
        self.show()

    def buttonClicked(self):
        self.UTC = self.combobox.currentText().split("UTC")[1]
        print(self.UTC)
        self.close()

class HelpDialog(QDialog):
    def __init__(self, parent):
        super(HelpDialog, self).__init__(parent)
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('도움말')

        # text 삽입
        self.text = QTextBrowser(self)
        self.text.append("BoB 프로젝트 '언니만 미도>3<' 팀의 결과물입니다.")
        self.text.resize(300, 300)
        self.show()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Believe Me Sister' # 실행 프로그램의 이름
        # 실행 프로그램의 시작 위치 설정
        self.left = 100
        self.top = 100
        self.width = 1000
        self.height = 700
        self.initUI()
        self.dialog = QDialog()
        self.widget = Tabs.MyWidget(self)
        self.setCentralWidget(self.widget)

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon('bob.png')) # 실행 프로그램 대표 이미지
        self.setGeometry(self.left, self.top, self.width, self.height) # 실행 프로그램의 시작 위치
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
        UTCDialog(self)

    def HelpAction_open(self):
        HelpDialog(self)
        QLabel(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())