from PyQt5.QtWidgets import *
import os
from PyQt5.QtCore import *
from COPY import copy
import time

from EventLogParse import Save_Event
from LnkParse import Lnk_Parse
from BrowserParse import BrowserParser
from PrefetchParse import Prefetch_Parse
from NTFSParse import MFT_Parser, UsnJrnl_Parser
from JumpListParse import Jump_Parse


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
        self.explanation1_ = QLabel("분석에 필요한 파일을 복사합니다.\n생성된 DB가 있는 경우, 생략 가능합니다.")
        self.blank_ = QLabel()
        self.explanation2_ = QLabel("아래 시작 버튼을 누른 후, 조금만 기다려 주세요.\n복사가 완료되면 창이 종료됩니다.")

        self.progressBar = QProgressBar(self)
        self.progressBar.setRange(0,1)
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progLabel = QLabel()

        self.pushButton_ = QPushButton("시작")
        self.pushButton_.clicked.connect(self.pushButtonCopy)
        self.pushButtonFlag = True

        self.task = Thread()
        self.task.taskFinished.connect(self.onFinished)

        layout = QGridLayout()
        layout.addWidget(self.explanation1_, 0, 0)
        layout.addWidget(self.blank_, 1, 0)
        layout.addWidget(self.explanation2_, 2, 0)
        layout.addWidget(self.progressBar, 3, 0)
        layout.addWidget(self.progLabel, 4, 0)
        layout.addWidget(self.pushButton_, 5, 0)

        self.setLayout(layout)

    def pushButtonCopy(self):
        if self.pushButtonFlag:
            self.progressBar.setRange(0,0)
            self.explanation1_.setText("분석에 필요한 파일을 복사중입니다.")
            self.explanation2_.setText("복사가 완료되면 창이 종료됩니다.")
            self.progLabel.setText("잠시만 기다려주세요")
            self.task.start()
            self.pushButton_.setText("중단")
            self.pushButtonFlag = False
        else:
            if self.task.isRunning():
                self.task.terminate()
                self.task.wait()
                self.progressBar.setRange(0, 1)
                self.explanation1_.setText("파일 복사가 중단되었습니다.")
                self.explanation2_.setText("재시작을 원하시면 아래 버튼을 눌러주시고,\n복사를 원치 않으실 경우 창을 닫아주십시오.")
                self.progLabel.setText("")
                self.pushButton_.setText("재시작")
                self.pushButtonFlag = True

    def onFinished(self):
        self.pushButton_.setEnabled(False)
        self.progLabel.setText("파일 복사가 완료되었습니다.")
        self.progressBar.setRange(0,1)
        self.progressBar.setValue(1)
        time.sleep(2)
        self.close()

class Thread(QThread):
    taskFinished = pyqtSignal()
    def run(self):
        copy.file_copy()
        self.taskFinished.emit()



class Parsing(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("복사된 파일 파싱")
        self.explanation1_ = QLabel("분석에 필요한 파일을 파싱중입니다. (생성된 DB가 있는 경우, 생략 가능합니다.)\n\n파싱이 완료되면 창이 종료됩니다.")

        self.progressBar = QProgressBar(self)
        self.progressBar.setRange(0,100)
        self.progressBar.setValue(0)

        self.progLabel = QLabel()

        self.pushButton_ = QPushButton("취소")
        self.pushButton_.clicked.connect(self.pushButtonStop)

        self.task = ParsingThread()
        self.task.taskFinished.connect(self.onFinished)
        self.task.start()

        self.timerVar = QTimer()
        self.timerVar.setInterval(20000)
        self.timerVar.timeout.connect(self.progressBarTimer)
        self.timerVar.start()

        self.task.change_value.connect(self.progressBar.setValue)
        self.task.change_message.connect(self.progLabel.setText)
        self.task.change_interval.connect(self.timerVar.setInterval)

        layout = QGridLayout()
        layout.addWidget(self.explanation1_, 0, 0)
        layout.addWidget(self.progressBar, 3, 0)
        layout.addWidget(self.progLabel, 4, 0)
        layout.addWidget(self.pushButton_, 5, 0)

        self.setLayout(layout)

    def pushButtonStop(self):
        self.explanation1_.setText("파싱이 중단되었습니다. 잠시후 창이 종료됩니다.")
        self.progLabel.setText("")
        self.explanation1_.repaint()
        self.pushButton_.setEnabled(False)
        self.task.terminate()
        time.sleep(2.5)
        self.close()

    def progressBarTimer(self):
        self.times = self.progressBar.value()
        if self.times < self.task.check_time:
            self.times += 1
            self.progressBar.setValue(self.times)
            self.timeSender(self.task)
            if self.times >= self.progressBar.maximum():
                self.timerVar.stop()

    def timeSender(self, obj):
        obj.times = self.times

    def onFinished(self):
        self.pushButton_.setEnabled(False)
        self.progLabel.setText("파싱이 완료되었습니다.")
        time.sleep(2)
        self.close()



class ParsingThread(QThread):
    taskFinished = pyqtSignal()
    change_value = pyqtSignal(int)
    change_message = pyqtSignal(str)
    change_interval = pyqtSignal(int)
    check_time = 30
    times = 0
    def __init__(self):
        super().__init__()
    def run(self):
        self.change_message.emit("Parsing Event Log..")
        Save_Event.Save_Event()
        self.adjust()
        self.change_interval.emit(800)
        self.check_time = 83
        self.change_message.emit("Parsing Lnk...")
        Lnk_Parse.main()

        self.change_message.emit("Parsing Browser...")
        BrowserParser.Browser_parser()

        self.change_message.emit("Parsing Prefetch...")
        Prefetch_Parse.main()

        self.change_message.emit("Parsing JumpList...")
        Jump_Parse.main()
        self.change_interval.emit(20000)

        self.change_message.emit("Parsing $MFT...")
        MFT_Parser.parsing()
        self.adjust()

        self.check_time = 98
        self.change_message.emit("Parsing $UsnJrnl...")
        UsnJrnl_Parser.usn_parse()
        self.adjust()
        self.check_time = 100
        self.change_interval.emit(800000)
        self.change_message.emit("Parsing Registry...")
        os.system(
            "REGParse.exe COPY\REGHIVE\SYSTEM COPY\REGHIVE\SOFTWARE COPY\REGHIVE\SAM COPY\REGHIVE\\NTUSER.DAT COPY\REGHIVE\\USRCLASS.DAT")
        self.adjust()
        self.taskFinished.emit()

    def adjust(self):
        if self.times < self.check_time:
            self.change_value.emit(self.check_time)