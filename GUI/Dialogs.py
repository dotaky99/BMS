from PyQt5.QtWidgets import *

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