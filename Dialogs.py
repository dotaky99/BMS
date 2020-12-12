from PyQt5.QtWidgets import *
import os
from COPY import copy


class UTCDialog(QDialog):
    def __init__(self, parent):
        super(UTCDialog, self).__init__(parent)
        self.setupUI()
        self.UTC = None

    def setupUI(self):
        self.setWindowTitle('UTC 설정')
        self.resize(300, 300)
        self.center()
        layout = QBoxLayout(QBoxLayout.TopToBottom, parent = self)
        self.setLayout(layout)
        label = QLabel()
        self.combobox = QComboBox()
        self.combobox.addItems(["UTC-12", "UTC-11", "UTC-10", "UTC-9", "UTC-8", "UTC-7", "UTC-6",
                    "UTC-5", "UTC-4", "UTC-3", "UTC-2", "UTC-1", "UTC+0", "UTC+1",
                    "UTC+2", "UTC+3", "UTC+4", "UTC+5", "UTC+6", "UTC+7", "UTC+8",
                    "UTC+9", "UTC+10", "UTC+11", "UTC+12", "UTC+13", "UTC+14"])
        layout.addWidget(self.combobox)
        layout.addWidget(label)
        self.button = QPushButton("확인", self) # 버튼 텍스트
        self.button.move(190, 250) # 버튼 위치
        self.button.clicked.connect(self.buttonClicked) # 클릭 시 실행할 function
        self.show()

    def buttonClicked(self):
        self.UTC = self.combobox.currentText().split("UTC")[1]
        self.close()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


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


class MemoryDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("메모리 덤프")
        self.explanation1 = QLabel("메모리는 시스템이 활성화되어 있는 동안 시스템 런타임 상태의")
        self.explanation2 = QLabel("중요 정보를 포함하고 있습니다.")
        self.blank = QLabel()
        self.question = QLabel("추후 분석을 위해 메모리를 덤프하시겠습니까?")

        self.yn = None
        self.checkbox1 = QCheckBox("예")
        self.checkbox2 = QCheckBox("아니오")
        self.checkbox1.setChecked(True)
        self.checkbox1.stateChanged.connect(self.checkbox1_state)
        self.checkbox2.stateChanged.connect(self.checkbox2_state)

        self.pushButton = QPushButton("다음")
        self.pushButton.clicked.connect(self.pushButtonClicked)

        layout = QGridLayout()
        layout.addWidget(self.explanation1, 0, 0)
        layout.addWidget(self.explanation2, 1, 0)
        layout.addWidget(self.blank, 2, 0)
        layout.addWidget(self.question, 3, 0)
        layout.addWidget(self.checkbox1, 4, 0)
        layout.addWidget(self.checkbox2, 5, 0)
        layout.addWidget(self.pushButton, 6, 0)
        self.setLayout(layout)

    def checkbox1_state(self):
        if self.checkbox1.isChecked():
            self.checkbox2.setChecked(False)
        else:
            self.checkbox2.setChecked(True)

    def checkbox2_state(self):
        if self.checkbox2.isChecked():
            self.checkbox1.setChecked(False)
        else:
            self.checkbox1.setChecked(True)

    def pushButtonClicked(self):
        if self.checkbox1.isChecked():
            os.system("COPY\DumpIt.exe") ######################### 경로 수정
            self.yn = 1
        else:
            self.yn = 0
        self.close()


class FileCopy(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("파일 복사")
        self.explanation1_ = QLabel("분석에 필요한 파일을 복사중입니다.")
        self.blank_ = QLabel()
        self.explanation2_ = QLabel("아래 버튼을 누른 후, 조금만 기다려 주세요.\nDB가 생성되면 창이 종료됩니다.")

        self.pushButton_ = QPushButton("시작")
        self.pushButton_.clicked.connect(self.pushButtonCopy)

        layout = QGridLayout()
        layout.addWidget(self.explanation1_, 0, 0)
        layout.addWidget(self.blank_, 1, 0)
        layout.addWidget(self.explanation2_, 2, 0)
        layout.addWidget(self.pushButton_, 3, 0)
        self.setLayout(layout)

    def pushButtonCopy(self):
        copy.main()
        self.close()