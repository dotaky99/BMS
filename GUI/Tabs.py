import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtCore import *
import sqlite3

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

        self.set_tab2()
        self.set_tab3()
        self.set_tab4()

        total_layout = QVBoxLayout()
        total_layout.addWidget(self.tabs)
        self.setLayout(total_layout)
        #self.UTC = "+9"     # 수정할 것.

####tab2 구성####
    def set_tab2(self):
        self.tab2.layout = QVBoxLayout()


####수집 전 확인 사항####
        groupbox1 = QGroupBox("수집 전 확인 사항")
        vbox1 = QGridLayout()
        text1_1 = QLabel("<b> * DRM  <b>  :  ", self)
        text1_2 = QLabel("<b> * 매체제어  <b>  :  ", self)
        text1_3 = QLabel("<b> * 디스크 암호화  <b>  :  ", self)
        text1_4 = QLabel("<b> * VM  <b>  :  ", self)
        text1_5 = QLabel("<b> * 정보 저장 매체  <b>  :  ", self)
        text1_6 = QLabel("<b> * 안티포렌식  <b>  :  ", self)
        text1_7 = QLabel("<b> * 볼륨 섀도우  :  <b>")

        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        text1_4_n = [] # DRM 정보
        query = "SELECT name, version, install_location, publisher, install_date FROM Uninstall " \
                "WHERE name LIKE 'Oracle VM VirtualBox%' OR name LIKE 'VMware Workstation';"
        cur.execute(query)
        list = cur.fetchall()
        for l in range(len(list)):
            text1_4_n.append(QLabel("이름 : " + list[l][0] + ", 버전: " + list[l][1] + ", 경로: " + list[l][2] + ", 제조사: " + list[l][3] + ", 최초 실행 시각: " + list[l][4] + ", 삭제 여부 : ", self))

####추가####
        conn1 = sqlite3.connect("Believe_Me_Sister.db")
        cur1 = conn1.cursor()
        text1_6_n = [] # 안티포렌식 정보

        ## 설치o, 실행o
        query1 = "SELECT Executable_Name, Last_Executed1 from prefetch1 " \
                 "WHERE (Executable_Name LIKE 'CCleaner%' OR Executable_Name LIKE 'Cipher%' " \
                 "OR Executable_Name LIKE 'CipherShed%' OR Executable_Name LIKE 'Eraser%' " \
                 "OR Executable_Name LIKE 'SDelete%' OR Executable_Name LIKE 'SetMACE%'" \
                 "OR Executable_Name LIKE 'TrueCrypt%'  OR Executable_Name LIKE 'TimeStomp%'" \
                 "OR Executable_Name LIKE 'VeraCrypt%'  OR Executable_Name LIKE 'Wise Folder Hider%')"


        ## 설치x, 실행o

        ## 설치o, 실행o

        cur1.execute(query1)
        list1 = cur1.fetchall()
        for l in range(len(list1)):
            text1_6_n.append(QLabel("이름 : " + list1[l][0] + ", 마지막 실행 시각: " + list1[l][1] + ", 삭제 여부 : ", self))


        vbox1.addWidget(text1_1, 0, 0)
        vbox1.addWidget(text1_2, 1, 0)
        vbox1.addWidget(text1_3, 2, 0)
        vbox1.addWidget(text1_4, 3, 0)
        vbox1.addWidget(text1_5, 5, 0)
        vbox1.addWidget(text1_6, 6, 0)
        vbox1.addWidget(text1_7, 7 + len(list1), 0)

        vbox1.addWidget(text1_4_n[0], 3, 1)

####추가####
        for i in range(len(list1)):
            vbox1.addWidget(text1_6_n[i], 6 + i, 1)

        groupbox1.setLayout(vbox1)


##PC 정보##
        groupbox2 = QGroupBox("PC 정보")
        vbox2 = QGridLayout()

        query = "SELECT * FROM OSInformation;"
        cur.execute(query)
        list = cur.fetchall()[0]

        text2_1 = QLabel("<b> * 윈도우 버전  <b>  :  ", self)
        text2_2 = QLabel("<b> * 윈도우 설치 시각  <b>  :  ", self)
        text2_3 = QLabel("<b> * 컴퓨터 이름  <b>  :  ", self)
        text2_4 = QLabel("<b> * 작업 그룹  <b>  :  ", self)
        text2_5 = QLabel("<b> * 표준 시간대  <b>  :  ", self)
        text2_6 = QLabel("<b> * usb  <b>  :  ", self)
        text2_7 = QLabel("<b> * 네트워크  <b>  :  ", self)
        text2_8 = QLabel("<b> * 계정  <b>  :  ", self)
        text2_1_1 = QLabel(list[0] + " (" + list[6] + ")", self)
        text2_2_1 = QLabel(list[4] + " (UTC +00)", self)
        text2_3_1 = QLabel(list[10], self)
        # text4_2 = QLabel(string4, self)
        text2_5_1 = QLabel(list[7] + " (UTC"+ f"{list[9]:+03d}" + ")", self)

        text2_6_n = []
        query = "SELECT serial_num, random_yn, UIID, vendor_name, product_name, version, label, GUID, " \
                "first_connected, last_connected FROM Connected_USB"
        cur.execute(query)
        list = cur.fetchall()
        for l in range(len(list)):
            string = "시리얼 넘버: " + list[l][0] + ", GUID: " + list[l][7] + ", UIID: " + list[l][2] + ", 최초 연결: " + list[l][8] + ", 마지막 연결: " + list[l][9]
            text2_6_n.append(QLabel(string))

        text2_8_n = []
        query = "SELECT account_name, created_on FROM UserAccounts"
        cur.execute(query)
        list = cur.fetchall()
        for l in range(len(list)):
            text2_8_n.append(QLabel(list[l][0] + ", 생성: " + list[l][1]))


        vbox2.addWidget(text2_1, 0, 0) # 윈도우 버전
        vbox2.addWidget(text2_2, 1, 0) # 윈도우 설치 시각
        vbox2.addWidget(text2_3, 2, 0) # 컴퓨터 이름
        vbox2.addWidget(text2_4, 3, 0) # 작업 그룹
        vbox2.addWidget(text2_5, 4, 0) # 표준 시간대
        vbox2.addWidget(text2_6, 5, 0) # USB
        vbox2.addWidget(text2_7, 10, 0) # 네트워크
        vbox2.addWidget(text2_8, 11, 0) # 계정
        vbox2.addWidget(text2_1_1, 0, 1)
        vbox2.addWidget(text2_2_1, 1, 1)
        vbox2.addWidget(text2_3_1, 2, 1)
        vbox2.addWidget(text2_5_1, 4, 1)
        vbox2.addWidget(text2_6_n[0], 5, 1)
        # vbox2.addWidget(text2_6_n[1], 6, 1)
        # vbox2.addWidget(text2_6_n[2], 7, 1)
        # vbox2.addWidget(text2_6_n[3], 8, 1)
        # vbox2.addWidget(text2_6_n[4], 9, 1)
        vbox2.addWidget(text2_8_n[0], 11, 1)
        vbox2.addWidget(text2_8_n[1], 12, 1)
        vbox2.addWidget(text2_8_n[2], 13, 1)
        vbox2.addWidget(text2_8_n[3], 14, 1)
        vbox2.addWidget(text2_8_n[4], 15, 1)
        groupbox2.setLayout(vbox2)

        self.tab2.layout.addWidget(groupbox1)
        self.tab2.layout.addWidget(groupbox2)

        self.tab2.setLayout(self.tab2.layout)


    def set_tab3(self):
        # tab3 구성
        self.tab3.layout = QGridLayout(self)

        self.box1 = QVBoxLayout()
        self.checkbox1_1 = QCheckBox("MFT 생성")
        self.checkbox1_2 = QCheckBox("계정 생성")
        self.checkbox1_3 = QCheckBox("Windows 설치")
        self.checkbox1_4 = QCheckBox("Windows 업데이트")
        self.checkbox1_5 = QCheckBox("시스템 On/Off")
        self.box1.addWidget(self.checkbox1_1)
        self.box1.addWidget(self.checkbox1_2)
        self.box1.addWidget(self.checkbox1_3)
        self.box1.addWidget(self.checkbox1_4)
        self.box1.addWidget(self.checkbox1_5)

        self.box2 = QVBoxLayout()
        self.checkbox2_1 = QCheckBox("문서 생성 및 수정")
        self.checkbox2_2 = QCheckBox("안티포렌식 도구 실행")
        self.checkbox2_3 = QCheckBox("클라우드 접근")
        self.checkbox2_4 = QCheckBox("저장장치 연결 및 해제")
        self.checkbox2_5 = QCheckBox("이벤트로그 삭제")
        self.box2.addWidget(self.checkbox2_1)
        self.box2.addWidget(self.checkbox2_2)
        self.box2.addWidget(self.checkbox2_3)
        self.box2.addWidget(self.checkbox2_4)
        self.box2.addWidget(self.checkbox2_5)

        self.box4 = QHBoxLayout()
        self.box4.addLayout(self.box1)
        self.box4.addLayout(self.box2)

        self.box3 = QHBoxLayout()
        self.input_datetime1 = QDateTimeEdit()
        self.input_datetime2 = QDateTimeEdit()
        self.currentDateTime = QDateTime.currentDateTime()
        self.input_datetime1.setDateTime(self.currentDateTime)
        self.input_datetime2.setDateTime(self.currentDateTime)
        self.input_datetime1.setCalendarPopup(True)
        self.input_datetime2.setCalendarPopup(True)
        self.during = QLabel(" ~ ")
        self.timebutton = QPushButton("적용")
        self.timebutton.clicked.connect(self.set_timeline)
        self.box3.addWidget(self.input_datetime1)
        self.box3.addWidget(self.during)
        self.box3.addWidget(self.input_datetime2)
        self.box3.addWidget(self.timebutton)

        self.timeline = QTableWidget(self)
        self.timeline.setSortingEnabled(True)
        self.timeline.setColumnCount(4)
        headers = ["시간", "행위", "세부 사항", "경로"]
        self.timeline.setHorizontalHeaderLabels(headers)

        self.tab3.layout.addLayout(self.box3, 0, 0)
        self.tab3.layout.addLayout(self.box4, 1, 0)
        self.tab3.layout.addWidget(self.timeline, 2, 0)
        self.tab3.setLayout(self.tab3.layout)

    def set_timeline(self):
        self.datetime1 = self.input_datetime1.dateTime()
        self.datetime2 = self.input_datetime2.dateTime()
        self.timeline.clearContents()
        self.timeline_count = 0

        if self.checkbox1_1.isChecked():
            print("1_1")
        if self.checkbox1_2.isChecked():
            self.timeline_data1_2()
        if self.checkbox1_3.isChecked():
            self.timeline_data1_3()
        if self.checkbox1_4.isChecked():
            self.timeline_data1_4()
        if self.checkbox1_5.isChecked():
            self.timeline_data1_5()
        if self.checkbox2_1.isChecked():
            print("2_1")
        if self.checkbox2_2.isChecked():
            self.timeline_data2_2()
        if self.checkbox2_3.isChecked():
            self.timeline_data2_3()
        if self.checkbox2_4.isChecked():
            self.timeline_data2_4()
        if self.checkbox2_5.isChecked():
            self.timeline_data2_5()

        self.timeline.resizeColumnsToContents()

    # 계정 생성
    def timeline_data1_2(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT created_on, last_password_change_time, account_name, RID_int FROM UserAccounts"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()
        accum = self.timeline_count
        self.timeline_count = accum + len(rows)
        self.timeline.setRowCount(self.timeline_count)
        password_exists = []
        for i in range(len(rows)):
            created_on, last_password, name, rid = rows[i]
            self.timeline.setItem(accum + i, 0, QTableWidgetItem(created_on))
            self.timeline.setItem(accum + i, 1, QTableWidgetItem("계정 생성"))
            self.timeline.setItem(accum + i, 2, QTableWidgetItem(name + ", SID: " + str(rid)))
            if last_password != None:
                password_exists.append(i)

        accum = self.timeline_count
        self.timeline_count = accum + len(password_exists)
        self.timeline.setRowCount(self.timeline_count)
        cnt = 0
        for p in password_exists:
            created_on, last_password, name, rid = rows[p]
            self.timeline.setItem(accum + cnt, 0, QTableWidgetItem(last_password))
            self.timeline.setItem(accum + cnt, 1, QTableWidgetItem("계정 패스워드 변경"))
            self.timeline.setItem(accum + cnt, 2, QTableWidgetItem(name + ", SID: " + str(rid)))
            cnt = cnt + 1

    # Windows 설치
    def timeline_data1_3(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT install_date, product_name, product_ID FROM OSInformation"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()
        accum = self.timeline_count
        self.timeline_count = accum + len(rows)
        self.timeline.setRowCount(self.timeline_count)
        time, name, id = rows[0]
        self.timeline.setItem(accum, 0, QTableWidgetItem(time))
        self.timeline.setItem(accum, 1, QTableWidgetItem("Windows 설치"))
        self.timeline.setItem(accum, 2, QTableWidgetItem(name + ", 제품 ID: " + id))

    # Windows 업데이트
    def timeline_data1_4(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT detailed, computer, time_created, package FROM event_log where event_id='2' AND package IS NOT '';"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()
        accum = self.timeline_count
        self.timeline_count = accum + len(rows)
        self.timeline.setRowCount(self.timeline_count)
        for i in range(len(rows)):
            detailed, computer, time, package = rows[i]
            self.timeline.setItem(i + accum, 0, QTableWidgetItem(time))
            self.timeline.setItem(i + accum, 1, QTableWidgetItem("Windows 업데이트"))
            string = "detailed: " + detailed + ", computer: " + computer + ", package: " + package
            self.timeline.setItem(i + accum, 2, QTableWidgetItem(string))

    # 시스템 On/Off
    def timeline_data1_5(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT event_id, computer, time_created FROM event_log WHERE event_id = '12' OR event_id = '13'"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()

        accum = self.timeline_count
        self.timeline_count = accum + len(rows)
        self.timeline.setRowCount(self.timeline_count)
        for i in range(len(rows)):
            event_id, computer, time = rows[i]
            self.timeline.setItem(i + accum, 0, QTableWidgetItem(time))
            if event_id == 12:
                self.timeline.setItem(i + accum, 1, QTableWidgetItem("시스템 On"))
            elif event_id == 13:
                self.timeline.setItem(i + accum, 1, QTableWidgetItem("시스템 Off"))
            self.timeline.setItem(i + accum, 2, QTableWidgetItem(computer))

    # 안티포렌식 도구 실행
    def timeline_data2_2(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        # query = 'SELECT Executable_Name, Full_Path, Last_Executed1, Last_Executed2, Last_Executed3, Last_Executed4, Last_Executed5, Last_Executed6, Last_Executed7, Last_Executed8 from prefetch1 WHERE (Executable_Name LIKE "CCleaner%" OR Executable_Name LIKE "Cipher%" OR Executable_Name LIKE "CipherShed%" OR Executable_Name LIKE "Eraser%" OR Executable_Name LIKE "SDelete%" OR Executable_Name LIKE "SetMACE%"  OR Executable_Name LIKE "TrueCrypt%"  OR Executable_Name LIKE "TimeStomp%"  OR Executable_Name LIKE "VeraCrypt%"  OR Executable_Name LIKE "Wise Folder Hider%")'
        query = 'SELECT Executable_Name, Full_Path, Last_Executed1 from prefetch1 WHERE (Executable_Name LIKE "CCleaner%" OR Executable_Name LIKE "Cipher%" OR Executable_Name LIKE "CipherShed%" OR Executable_Name LIKE "Eraser%" OR Executable_Name LIKE "SDelete%" OR Executable_Name LIKE "SetMACE%"  OR Executable_Name LIKE "TrueCrypt%"  OR Executable_Name LIKE "TimeStomp%"  OR Executable_Name LIKE "VeraCrypt%"  OR Executable_Name LIKE "Wise Folder Hider%")'
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()
        accum = self.timeline_count
        self.timeline_count = accum + len(rows)
        self.timeline.setRowCount(self.timeline_count)
        for i in range(len(rows)):
            name, path, time = rows[i]
            self.timeline.setItem(i + accum, 0, QTableWidgetItem(time))
            self.timeline.setItem(i + accum, 1, QTableWidgetItem("안티포렌식 도구 실행"))
            self.timeline.setItem(i + accum, 2, QTableWidgetItem(name))
            self.timeline.setItem(i + accum, 3, QTableWidgetItem(path))

    # 클라우드 접근
    def timeline_data2_3(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT timestamp, Title, URL FROM cloud"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()
        accum = self.timeline_count
        self.timeline_count = accum + len(rows)
        self.timeline.setRowCount(self.timeline_count)
        for i in range(len(rows)):
            time, title, url = rows[i]
            self.timeline.setItem(i + accum, 0, QTableWidgetItem(time))
            self.timeline.setItem(i + accum, 1, QTableWidgetItem("클라우드 접근"))
            self.timeline.setItem(i + accum, 2, QTableWidgetItem(title))
            self.timeline.setItem(i + accum, 3, QTableWidgetItem(url))

    # 저장장치 연결 및 해제
    def timeline_data2_4(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT detailed, time_created, bus_type, drive_manufac, drive_model FROM event_log WHERE event_id = '1006';"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()
        accum = self.timeline_countㄴ
        self.timeline_count = accum + len(rows)
        self.timeline.setRowCount(self.timeline_count)
        for i in range(len(rows)):
            detailed, time, bus_type, manufac, model = rows[i]
            self.timeline.setItem(i + accum, 0, QTableWidgetItem(time))
            if "released" in detailed:
                self.timeline.setItem(i + accum, 1, QTableWidgetItem("USB 연결 해제"))
            else:
                self.timeline.setItem(i + accum, 1, QTableWidgetItem("USB 연결"))
            if manufac == "NULL":
                string = "타입: " + bus_type + ", 모델명: " + model
            else:
                string = "타입: " + bus_type + ", 제조사: " + manufac + ", 모델명: " + model
            self.timeline.setItem(i + accum, 2, QTableWidgetItem(string))

    # 이벤트로그 삭제
    def timeline_data2_5(self):
        conn = sqlite3.connect("BBelieve_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT event_id, detailed, computer, time_created, sbt_usr_name, channel FROM event_log WHERE event_id = '104' or event_id = '1102' AND sbt_usr_name IS NOT '';"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()
        accum = self.timeline_count
        self.timeline_count = accum + len(rows)
        self.timeline.setRowCount(self.timeline_count)
        for i in range(len(rows)):
            event_id, detailed, computer, time, usr_name, channel = rows[i]
            self.timeline.setItem(i + accum, 0, QTableWidgetItem(time))
            self.timeline.setItem(i + accum, 1, QTableWidgetItem("이벤트로그 삭제"))
            string = "detailed: " + detailed + ", computer: " + computer + ", user name: " + usr_name + ", channel: " + channel
            self.timeline.setItem(i + accum, 2, QTableWidgetItem(string))

    def set_tab4(self):
        # tab 4 구성
        self.tab4.layout = QHBoxLayout(self)

        tree = QTreeWidget()
        tree.header().setVisible(False)
        tree.setFixedWidth(300)

        item1 = QTreeWidgetItem(tree)
        item1.setText(0, "PC 정보")
        item1_1 = QTreeWidgetItem(item1)
        item1_1.setText(0, "시스템 정보")
        item1_2 = QTreeWidgetItem(item1)
        item1_2.setText(0, "계정 정보")
        item1_3 = QTreeWidgetItem(item1)
        item1_3.setText(0, "네트워크")
        item1_4 = QTreeWidgetItem(item1)
        item1_4.setText(0, "윈도우 업데이트")
        item1_5 = QTreeWidgetItem(item1)
        item1_5.setText(0, "디스크 정보")

        item2 = QTreeWidgetItem(tree)
        item2.setText(0, "외부저장장치")
        item2_1 = QTreeWidgetItem(item2)
        item2_1.setText(0, "레지스트리")
        item2_2 = QTreeWidgetItem(item2)
        item2_2.setText(0, "이벤트로그")

        item3 = QTreeWidgetItem(tree)
        item3.setText(0, "브라우저")
        item3_1 = QTreeWidgetItem(item3)
        item3_1.setText(0, "검색 기록")
        item3_2 = QTreeWidgetItem(item3)
        item3_2.setText(0, "다운로드 기록")
        item3_3 = QTreeWidgetItem(item3)
        item3_3.setText(0, "URL 히스토리")
        item3_4 = QTreeWidgetItem(item3)
        item3_4.setText(0, "로그인 기록")
        item3_5 = QTreeWidgetItem(item3)
        item3_5.setText(0, "클라우드 접속 기록")
        item3_6 = QTreeWidgetItem(item3)
        item3_6.setText(0, "쿠키")
        item3_7 = QTreeWidgetItem(item3)
        item3_7.setText(0, "캐시")
        item3_8 = QTreeWidgetItem(item3)
        item3_8.setText(0, "북마크")
        item3_9 = QTreeWidgetItem(item3)
        item3_9.setText(0, "자동완성")

        item4 = QTreeWidgetItem(tree)
        item4.setText(0, "프로그램 실행 흔적")
        item4_1 = QTreeWidgetItem(item4)
        item4_1.setText(0, "레지스트리")
        item4_2 = QTreeWidgetItem(item4)
        item4_2.setText(0, "프리패치")


        item5 = QTreeWidgetItem(tree)
        item5.setText(0, "문서 실행 흔적")
        item5_1 = QTreeWidgetItem(item5)
        item5_1.setText(0, "레지스트리")
        item5_2 = QTreeWidgetItem(item5)
        item5_2.setText(0, "링크 파일")
        item5_3 = QTreeWidgetItem(item5)
        item5_3.setText(0, "점프 목록")
        item5_4 = QTreeWidgetItem(item5)
        item5_4.setText(0, "프리패치")

        item6 = QTreeWidgetItem(tree)
        item6.setText(0, "기타 실행 흔적")
        item6_1 = QTreeWidgetItem(item6)
        item6_1.setText(0, "링크 파일")
        item6_2 = QTreeWidgetItem(item6)
        item6_2.setText(0, "프리패치")

        item7 = QTreeWidgetItem(tree)
        item7.setText(0, "이벤트 로그")
        item7_1 = QTreeWidgetItem(item7)
        item7_1.setText(0, "이벤트 로그 삭제")
        item7_2 = QTreeWidgetItem(item7)
        item7_2.setText(0, "프로세스 강제 종료")
        item7_3 = QTreeWidgetItem(item7)
        item7_3.setText(0, "PC ON/OFF")
        item7_4 = QTreeWidgetItem(item7)
        item7_4.setText(0, "절전 모드")
        item7_5 = QTreeWidgetItem(item7)
        item7_5.setText(0, "원격 접속 기록")

#### PC 정보 중 시스템 정보####
        # self.pc_system_table = QTableWidget(self)
        # self.PC_System()
        #
        # self.tab4.layout.addWidget(tree)
        # self.tab4.layout.addWidget(self.pc_system_table)
        # self.tab4.setLayout(self.tab4.layout)

#### PC 정보 중 사용자 정보####
        # self.pc_user_table = QTableWidget(self)
        # self.PC_User()
        #
        # self.tab4.layout.addWidget(tree)
        # self.tab4.layout.addWidget(self.pc_user_table)
        # self.tab4.setLayout(self.tab4.layout)

#### PC 정보 중 네트워크 정보####
        # self.pc_network_table = QTableWidget(self)
        # self.PC_Network()
        #
        # self.tab4.layout.addWidget(tree)
        # self.tab4.layout.addWidget(self.pc_network_table)
        # self.tab4.setLayout(self.tab4.layout)

#### PC 정보 중 윈도우 업데이트 정보####
        # self.pc_window_update_table = QTableWidget(self)
        # self.PC_Window_Update()
        #
        # self.tab4.layout.addWidget(tree)
        # self.tab4.layout.addWidget(self.pc_window_update_table)
        # self.tab4.setLayout(self.tab4.layout)

#### 외부저장장치 중 레지스트리 정보####
        # self.external_registry_table = QTableWidget(self)
        # self.External_Registry()
        #
        # self.tab4.layout.addWidget(tree)
        # self.tab4.layout.addWidget(self.external_registry_table)
        # self.tab4.setLayout(self.tab4.layout)

#### 외부저장장치 중 이벤트 로그 정보####
        # self.external_event_log_table = QTableWidget(self)
        # self.External_Event_Log()
        #
        # self.tab4.layout.addWidget(tree)
        # self.tab4.layout.addWidget(self.external_event_log_table)
        # self.tab4.setLayout(self.tab4.layout)

#### 브라우저 중 검색 정보####
        # self.browser_search_table = QTableWidget(self)
        # self.Browser_Search()
        #
        # self.tab4.layout.addWidget(tree)
        # self.tab4.layout.addWidget(self.browser_search_table)
        # self.tab4.setLayout(self.tab4.layout)

#### 브라우저 중 다운로드 기록 정보####
        # self.browser_download_table = QTableWidget(self)
        # self.Browser_Download()
        #
        # self.tab4.layout.addWidget(tree)
        # self.tab4.layout.addWidget(self.browser_download_table)
        # self.tab4.setLayout(self.tab4.layout)

#### 브라우저 중 히스토리 정보####
        # self.browser_history_table = QTableWidget(self)
        # self.Browser_History()
        #
        # self.tab4.layout.addWidget(tree)
        # self.tab4.layout.addWidget(self.browser_history_table)
        # self.tab4.setLayout(self.tab4.layout)

#### 브라우저 중 로그인 기록 정보####
        # self.browser_login_table = QTableWidget(self)
        # self.Browser_Login()
        #
        # self.tab4.layout.addWidget(tree)
        # self.tab4.layout.addWidget(self.browser_login_table)
        # self.tab4.setLayout(self.tab4.layout)

#### 브라우저 중 클라우드 접속 기록 정보####
        # self.browser_cloud_table = QTableWidget(self)
        # self.Browser_Cloud()
        #
        # self.tab4.layout.addWidget(tree)
        # self.tab4.layout.addWidget(self.browser_cloud_table)
        # self.tab4.setLayout(self.tab4.layout)

#### 브라우저 중 쿠키 정보####
        # self.browser_cookie_table = QTableWidget(self)
        # self.Browser_Cookie()
        #
        # self.tab4.layout.addWidget(tree)
        # self.tab4.layout.addWidget(self.browser_cookie_table)
        # self.tab4.setLayout(self.tab4.layout)

#### 브라우저 중 캐시 정보####
        # self.browser_cache_table = QTableWidget(self)
        # self.Browser_Cache()
        #
        # self.tab4.layout.addWidget(tree)
        # self.tab4.layout.addWidget(self.browser_cache_table)
        # self.tab4.setLayout(self.tab4.layout)

#### 브라우저 중 북마크 정보####
        # self.browser_bookmark_table = QTableWidget(self)
        # self.Browser_Bookmark()
        #
        # self.tab4.layout.addWidget(tree)
        # self.tab4.layout.addWidget(self.browser_bookmark_table)
        # self.tab4.setLayout(self.tab4.layout)

#### 브라우저 중 자동완성 정보####
        # self.browser_autofill_table = QTableWidget(self)
        # self.Browser_Autofill()
        #
        # self.tab4.layout.addWidget(tree)
        # self.tab4.layout.addWidget(self.browser_autofill_table)
        # self.tab4.setLayout(self.tab4.layout)

#### 프로그램 실행 흔적 중 레지스트리####
        # self.program_registry_table = QTableWidget(self)
        # self.Program_Registry()
        #
        # self.tab4.layout.addWidget(tree)
        # self.tab4.layout.addWidget(self.program_registry_table)
        # self.tab4.setLayout(self.tab4.layout)

#### 프로그램 실행 흔적 중 프리패치####
        # self.program_prefetch_table = QTableWidget(self)
        # self.Program_Prefetch()
        #
        # self.tab4.layout.addWidget(tree)
        # self.tab4.layout.addWidget(self.program_prefetch_table)
        # self.tab4.setLayout(self.tab4.layout)

#### 문서 실행 흔적 중 레지스트리####
        # self.document_registry_table = QTableWidget(self)
        # self.Document_Registry()
        #
        # self.tab4.layout.addWidget(tree)
        # self.tab4.layout.addWidget(self.document_registry_table)
        # self.tab4.setLayout(self.tab4.layout)

#### 문서 실행 흔적 중 링크 파일####
        # self.document_lnk_table = QTableWidget(self)
        # self.Document_Lnk()
        #
        # self.tab4.layout.addWidget(tree)
        # self.tab4.layout.addWidget(self.document_lnk_table)
        # self.tab4.setLayout(self.tab4.layout)

#### 문서 실행 흔적 중 점프 목록####
        # self.document_jumplist_table = QTableWidget(self)
        # self.Document_Jumplist()
        #
        # self.tab4.layout.addWidget(tree)
        # self.tab4.layout.addWidget(self.document_jumplist_table)
        # self.tab4.setLayout(self.tab4.layout)

#### 문서 실행 흔적 중 프리패치####
        # self.document_prefetch_table = QTableWidget(self)
        # self.Document_Prefetch()
        #
        # self.tab4.layout.addWidget(tree)
        # self.tab4.layout.addWidget(self.document_prefetch_table)
        # self.tab4.setLayout(self.tab4.layout)

#### 폴더 열람 흔적 중 링크 파일####
        # self.folder_lnk_table = QTableWidget(self)
        # self.Folder_Lnk()
        #
        # self.tab4.layout.addWidget(tree)
        # self.tab4.layout.addWidget(self.folder_lnk_table)
        # self.tab4.setLayout(self.tab4.layout)

#### 기타 실행 흔적 중 링크 파일####
        # self.etc_lnk_table = QTableWidget(self)
        # self.Etc_Lnk()
        #
        # self.tab4.layout.addWidget(tree)
        # self.tab4.layout.addWidget(self.etc_lnk_table)
        # self.tab4.setLayout(self.tab4.layout)

#### 기타 실행 흔적 중 프리패치####
        # self.etc_prefetch_table = QTableWidget(self)
        # self.Etc_Prefetch()
        #
        # self.tab4.layout.addWidget(tree)
        # self.tab4.layout.addWidget(self.etc_prefetch_table)
        # self.tab4.setLayout(self.tab4.layout)

#### 이벤트 로그 흔적 중 이벤트 로그 삭제####
        # self.event_eventdel_table = QTableWidget(self)
        # self.Event_Eventdel()
        #
        # self.tab4.layout.addWidget(tree)
        # self.tab4.layout.addWidget(self.event_eventdel_table)
        # self.tab4.setLayout(self.tab4.layout)

#### 이벤트 로그 흔적 중 프로세스 강제 종료####
        # self.event_process_table = QTableWidget(self)
        # self.Event_Process()
        #
        # self.tab4.layout.addWidget(tree)
        # self.tab4.layout.addWidget(self.event_process_table)
        # self.tab4.setLayout(self.tab4.layout)

#### 이벤트 로그 흔적 중 PC ON/OFF 파일####
        # self.event_pc_table = QTableWidget(self)
        # self.Event_PC()
        #
        # self.tab4.layout.addWidget(tree)
        # self.tab4.layout.addWidget(self.event_pc_table)
        # self.tab4.setLayout(self.tab4.layout)

#### 이벤트 로그 흔적 중 절전 모드####
        # self.event_powersave_table = QTableWidget(self)
        # self.Event_Powersave()
        #
        # self.tab4.layout.addWidget(tree)
        # self.tab4.layout.addWidget(self.event_powersave_table)
        # self.tab4.setLayout(self.tab4.layout)

#### 이벤트 로그 흔적 중 원격 접속 기록####
        self.event_remote_table = QTableWidget(self)
        self.Event_Remote()

        self.tab4.layout.addWidget(tree)
        self.tab4.layout.addWidget(self.event_remote_table)
        self.tab4.setLayout(self.tab4.layout)

#### PC 정보 중 시스템 정보 테이블####
    # def PC_System(self):
    #     conn = sqlite3.connect("Believe_Me_Sister.db")
    #     cur = conn.cursor()
    #     query = "SELECT RID, RID_int, last_login_time, last_password_change_time, expires_on," \
    #             "last_incorrect_password_time, logon_failure_count, logon_success_count, account_name," \
    #             "complete_account_name, comment, homedir, created_on FROM UserAccounts"
    #     cur.execute(query)
    #     rows = cur.fetchall()
    #
    #     conn.close()
    #
    #     count = len(rows)
    #     self.pc_system_table.setRowCount(count)
    #     self.pc_system_table.setColumnCount(13)
    #     column_headers = ["RID", "RID_int", "last_login_time", "last_password_change_time", "expires_on", \
    #             "last_incorrect_password_time", "logon_failure_count", "logon_success_count", "account_name", \
    #             "complete_account_name", "comment", "homedir", "created_on"]
    #     self.pc_system_table.setHorizontalHeaderLabels(column_headers)
    #
    #     for i in range(count):
    #         RID, RID_int, last_login_time, last_password_change_time, expires_on, last_incorrect_password_time,\
    #         logon_failure_count, logon_success_count, account_name,complete_account_name, comment,\
    #         homedir, created_on = rows[i]
    #
    #         self.pc_system_table.setItem(i, 0, QTableWidgetItem(RID))
    #         self.pc_system_table.setItem(i, 1, QTableWidgetItem(RID_int))
    #         self.pc_system_table.setItem(i, 2, QTableWidgetItem(last_login_time))
    #         self.pc_system_table.setItem(i, 3, QTableWidgetItem(last_password_change_time))
    #         self.pc_system_table.setItem(i, 4, QTableWidgetItem(expires_on))
    #         self.pc_system_table.setItem(i, 5, QTableWidgetItem(last_incorrect_password_time))
    #         self.pc_system_table.setItem(i, 6, QTableWidgetItem(logon_failure_count))
    #         self.pc_system_table.setItem(i, 7, QTableWidgetItem(logon_success_count))
    #         self.pc_system_table.setItem(i, 8, QTableWidgetItem(account_name))
    #         self.pc_system_table.setItem(i, 9, QTableWidgetItem(complete_account_name))
    #         self.pc_system_table.setItem(i, 10, QTableWidgetItem(comment))
    #         self.pc_system_table.setItem(i, 11, QTableWidgetItem(homedir))
    #         self.pc_system_table.setItem(i, 12, QTableWidgetItem(created_on))

#### PC 정보 중 사용자 정보 테이블####
#### event_id가 안 나옴ㅠㅠ
    # def PC_User(self):
    #     conn = sqlite3.connect("Believe_Me_Sister.db")
    #     cur = conn.cursor()
    #     query = "SELECT event_id, detailed, time_created, computer, sbt_usr_name, trg_usr_name, display_name, mem_sid," \
    #             "source FROM event_log WHERE (event_id LIKE '1004' OR event_id LIKE '1005' OR event_id LIKE '4624'" \
    #             "OR event_id LIKE '4625' OR event_id LIKE '4720' OR event_id LIKE '4724' OR event_id LIKE '4726'" \
    #             "OR event_id LIKE '4732' OR event_id LIKE '4733' OR event_id LIKE '4738')"
    #
    #     cur.execute(query)
    #     rows = cur.fetchall()
    #
    #     conn.close()
    #
    #     count = len(rows)
    #     self.pc_user_table.setRowCount(count)
    #     self.pc_user_table.setColumnCount(9)
    #     column_headers = ["Event_ID", "Detailed", "Time_Created", "Computer", "Sbt_User_Name", \
    #             "Trg_User_Name", "Display", "Mem_Sid", "Source"]
    #     self.pc_user_table.setHorizontalHeaderLabels(column_headers)
    #
    #     for i in range(count):
    #         event_id, detailed, time_created, computer, sbt_usr_name, trg_usr_name, display_name, mem_sid, source = rows[i]
    #
    #         self.pc_user_table.setItem(i, 0, QTableWidgetItem(event_id))
    #         self.pc_user_table.setItem(i, 1, QTableWidgetItem(detailed))
    #         self.pc_user_table.setItem(i, 2, QTableWidgetItem(time_created))
    #         self.pc_user_table.setItem(i, 3, QTableWidgetItem(computer))
    #         self.pc_user_table.setItem(i, 4, QTableWidgetItem(sbt_usr_name))
    #         self.pc_user_table.setItem(i, 5, QTableWidgetItem(trg_usr_name))
    #         self.pc_user_table.setItem(i, 6, QTableWidgetItem(display_name))
    #         self.pc_user_table.setItem(i, 7, QTableWidgetItem(mem_sid))
    #         self.pc_user_table.setItem(i, 8, QTableWidgetItem(source))

#### PC 정보 중 네트워크 정보 테이블####
#### event_id가 안 나옴ㅠㅠ
    # def PC_Network(self):
    #     conn = sqlite3.connect("Believe_Me_Sister.db")
    #     cur = conn.cursor()
    #     query = "SELECT event_id, detailed, computer, time_created, net_name, guid, conn_mode, reason, source " \
    #             "FROM event_log WHERE (event_id LIKE '10000' AND net_name IS NOT '') OR (event_id LIKE '10001' AND net_name IS NOT '')" \
    #             "OR event_id LIKE '8003'"
    #
    #     cur.execute(query)
    #     rows = cur.fetchall()
    #
    #     conn.close()
    #
    #     count = len(rows)
    #     self.pc_network_table.setRowCount(count)
    #     self.pc_network_table.setColumnCount(9)
    #     column_headers = ["Event_ID", "Detailed", "Computer", "Time_Created", "Net_Name", "Guid", "Conn_Mode", "Reason", "Source"]
    #     self.pc_network_table.setHorizontalHeaderLabels(column_headers)
    #
    #     for i in range(count):
    #         event_id, detailed, computer, time_created, net_name, guid, conn_mode, reason, source = rows[i]
    #
    #         self.pc_network_table.setItem(i, 0, QTableWidgetItem(event_id))
    #         self.pc_network_table.setItem(i, 1, QTableWidgetItem(detailed))
    #         self.pc_network_table.setItem(i, 2, QTableWidgetItem(computer))
    #         self.pc_network_table.setItem(i, 3, QTableWidgetItem(time_created))
    #         self.pc_network_table.setItem(i, 4, QTableWidgetItem(net_name))
    #         self.pc_network_table.setItem(i, 5, QTableWidgetItem(guid))
    #         self.pc_network_table.setItem(i, 6, QTableWidgetItem(conn_mode))
    #         self.pc_network_table.setItem(i, 7, QTableWidgetItem(reason))
    #         self.pc_network_table.setItem(i, 8, QTableWidgetItem(source))

#### PC 정보 중 윈도우 업데이트 정보 테이블####
#### event_id가 안 나옴ㅠㅠ
    # def PC_Window_Update(self):
    #     conn = sqlite3.connect("Believe_Me_Sister.db")
    #     cur = conn.cursor()
    #     query = "SELECT event_id, detailed, time_created, computer, package, source FROM event_log WHERE event_id LIKE '2'"
    #
    #     cur.execute(query)
    #     rows = cur.fetchall()
    #
    #     conn.close()
    #
    #     count = len(rows)
    #     self.pc_window_update_table.setRowCount(count)
    #     self.pc_window_update_table.setColumnCount(6)
    #     column_headers = ["Event_ID", "Detailed", "Time_Created", "Computer", "Package", "Source"]
    #     self.pc_window_update_table.setHorizontalHeaderLabels(column_headers)
    #
    #     for i in range(count):
    #         event_id, detailed, time_created, computer, package, source = rows[i]
    #
    #         self.pc_window_update_table.setItem(i, 0, QTableWidgetItem(event_id))
    #         self.pc_window_update_table.setItem(i, 1, QTableWidgetItem(detailed))
    #         self.pc_window_update_table.setItem(i, 2, QTableWidgetItem(time_created))
    #         self.pc_window_update_table.setItem(i, 3, QTableWidgetItem(computer))
    #         self.pc_window_update_table.setItem(i, 4, QTableWidgetItem(package))
    #         self.pc_window_update_table.setItem(i, 5, QTableWidgetItem(source))

#### 외부저장장치 중 레지스트리 테이블####
    # def External_Registry(self):
    #     conn = sqlite3.connect("Believe_Me_Sister.db")
    #     cur = conn.cursor()
    #     query = "SELECT GUID, label, first_connected, last_connected, vendor_name, product_name, version, serial_num, " \
    #             "random_yn FROM Connected_USB"
    #
    #     cur.execute(query)
    #     rows = cur.fetchall()
    #
    #     conn.close()
    #
    #     count = len(rows)
    #     self.external_registry_table.setRowCount(count)
    #     self.external_registry_table.setColumnCount(9)
    #     column_headers = ["GUID", "Label", "First_Connect", "Last_Connect", "Vendor_Name", "Product", "Version", "Serial_Num", "Random_yn"]
    #     self.external_registry_table.setHorizontalHeaderLabels(column_headers)
    #
    #     for i in range(count):
    #         GUID, label, first_connected, last_connected, vendor_name, product_name, version, serial_num, random_yn = rows[i]
    #
    #         self.external_registry_table.setItem(i, 0, QTableWidgetItem(GUID))
    #         self.external_registry_table.setItem(i, 1, QTableWidgetItem(label))
    #         self.external_registry_table.setItem(i, 2, QTableWidgetItem(first_connected))
    #         self.external_registry_table.setItem(i, 3, QTableWidgetItem(last_connected))
    #         self.external_registry_table.setItem(i, 4, QTableWidgetItem(vendor_name))
    #         self.external_registry_table.setItem(i, 5, QTableWidgetItem(product_name))
    #         self.external_registry_table.setItem(i, 6, QTableWidgetItem(version))
    #         self.external_registry_table.setItem(i, 7, QTableWidgetItem(serial_num))
    #         self.external_registry_table.setItem(i, 8, QTableWidgetItem(random_yn))

#### 외부저장장치 중 이벤트 로그 테이블####
#### event_id가 안 나옴ㅠㅠ
    # def External_Event_Log(self):
    #     conn = sqlite3.connect("Believe_Me_Sister.db")
    #     cur = conn.cursor()
    #     query = "SELECT event_id, detailed, computer, time_created, bus_type, drive_manufac, drive_serial, drive_model," \
    #             "drive_location, source FROM event_log WHERE event_id LIKE '1006'"
    #
    #     cur.execute(query)
    #     rows = cur.fetchall()
    #
    #     conn.close()
    #
    #     count = len(rows)
    #     self.external_event_log_table.setRowCount(count)
    #     self.external_event_log_table.setColumnCount(10)
    #     column_headers = ["Event_ID", "Detailed", "Computer", "Time_Created", "Bus_Type", "Drive_Manfac", "Drive_Serial",
    #                       "Drive_Model", "Drive_Location", "Source"]
    #     self.external_event_log_table.setHorizontalHeaderLabels(column_headers)
    #
    #     for i in range(count):
    #         event_id, detailed, computer, time_created, bus_type, drive_manufac, drive_serial, drive_model, \
    #         drive_location, source = rows[i]
    #
    #         self.external_event_log_table.setItem(i, 0, QTableWidgetItem(event_id))
    #         self.external_event_log_table.setItem(i, 1, QTableWidgetItem(detailed))
    #         self.external_event_log_table.setItem(i, 2, QTableWidgetItem(computer))
    #         self.external_event_log_table.setItem(i, 3, QTableWidgetItem(time_created))
    #         self.external_event_log_table.setItem(i, 4, QTableWidgetItem(bus_type))
    #         self.external_event_log_table.setItem(i, 5, QTableWidgetItem(drive_manufac))
    #         self.external_event_log_table.setItem(i, 6, QTableWidgetItem(drive_serial))
    #         self.external_event_log_table.setItem(i, 7, QTableWidgetItem(drive_model))
    #         self.external_event_log_table.setItem(i, 8, QTableWidgetItem(drive_location))
    #         self.external_event_log_table.setItem(i, 9, QTableWidgetItem(source))

#### 브라우저 중 검색 테이블####
    # def Browser_Search(self):
    #     conn = sqlite3.connect("Believe_Me_Sister.db")
    #     cur = conn.cursor()
    #     query = "SELECT keyword, timestamp from keyword"
    #
    #     cur.execute(query)
    #     rows = cur.fetchall()
    #
    #     conn.close()
    #
    #     count = len(rows)
    #     self.browser_search_table.setRowCount(count)
    #     self.browser_search_table.setColumnCount(2)
    #     column_headers = ["Keyword", "TimeStamp"]
    #     self.browser_search_table.setHorizontalHeaderLabels(column_headers)
    #
    #     for i in range(count):
    #         keyword, timestamp = rows[i]
    #
    #         self.browser_search_table.setItem(i, 0, QTableWidgetItem(keyword))
    #         self.browser_search_table.setItem(i, 1, QTableWidgetItem(timestamp))

#### 브라우저 중 다운로드 테이블####
#### 다운로드 한 파일 이름 추가하기!
    # def Browser_Download(self):
    #     conn = sqlite3.connect("Believe_Me_Sister.db")
    #     cur = conn.cursor()
    #     query = "SELECT timestamp, url, status, path, interrupt_reason, danger_type, opened, etag, last_modified from download"
    #
    #     cur.execute(query)
    #     rows = cur.fetchall()
    #
    #     conn.close()
    #
    #     count = len(rows)
    #     self.browser_download_table.setRowCount(count)
    #     self.browser_download_table.setColumnCount(9)
    #     column_headers = ["TimeStamp", "URL", "Status", "Path", "Interrup_Reason","Danger_Type", "Opend", "etag", "Last_Modified"]
    #     self.browser_download_table.setHorizontalHeaderLabels(column_headers)
    #
    #     for i in range(count):
    #         timestamp, url, status, path, interrupt_reason, danger_type, opened, etag, last_modified = rows[i]
    #
    #         self.browser_download_table.setItem(i, 0, QTableWidgetItem(timestamp))
    #         self.browser_download_table.setItem(i, 1, QTableWidgetItem(url))
    #         self.browser_download_table.setItem(i, 2, QTableWidgetItem(status))
    #         self.browser_download_table.setItem(i, 3, QTableWidgetItem(path))
    #         self.browser_download_table.setItem(i, 4, QTableWidgetItem(interrupt_reason))
    #         self.browser_download_table.setItem(i, 5, QTableWidgetItem(danger_type))
    #         self.browser_download_table.setItem(i, 6, QTableWidgetItem(opened))
    #         self.browser_download_table.setItem(i, 7, QTableWidgetItem(etag))
    #         self.browser_download_table.setItem(i, 8, QTableWidgetItem(last_modified))

#### 브라우저 중 히스토리 테이블####
#### visit_count, type_count, url_hidden 안 나옴ㅠㅠ
    # def Browser_History(self):
    #     conn = sqlite3.connect("Believe_Me_Sister.db")
    #     cur = conn.cursor()
    #     query = "SELECT title, timestamp, url, source, visit_duration, visit_count, typed_count, url_hidden, transition from url"
    #
    #     cur.execute(query)
    #     rows = cur.fetchall()
    #
    #     conn.close()
    #
    #     count = len(rows)
    #     self.browser_history_table.setRowCount(count)
    #     self.browser_history_table.setColumnCount(9)
    #     column_headers = ["Title", "TimeStamp", "URL", "Source", "Visit_Duration","Visit_Count", "Typed_Count", "URL_Hidden",
    #                       "Trasition"]
    #     self.browser_history_table.setHorizontalHeaderLabels(column_headers)
    #
    #     for i in range(count):
    #         title, timestamp, url, source, visit_duration, visit_count, typed_count, url_hidden, transition = rows[i]
    #
    #         self.browser_history_table.setItem(i, 0, QTableWidgetItem(title))
    #         self.browser_history_table.setItem(i, 1, QTableWidgetItem(timestamp))
    #         self.browser_history_table.setItem(i, 2, QTableWidgetItem(url))
    #         self.browser_history_table.setItem(i, 3, QTableWidgetItem(source))
    #         self.browser_history_table.setItem(i, 4, QTableWidgetItem(visit_duration))
    #         self.browser_history_table.setItem(i, 5, QTableWidgetItem(visit_count))
    #         self.browser_history_table.setItem(i, 6, QTableWidgetItem(typed_count))
    #         self.browser_history_table.setItem(i, 7, QTableWidgetItem(url_hidden))
    #         self.browser_history_table.setItem(i, 8, QTableWidgetItem(transition))

#### 브라우저 중 로그인 테이블####
#### password_value는 bytes라고 UI에서 못 보여줌ㅠㅠ
    # def Browser_Login(self):
    #     conn = sqlite3.connect("Believe_Me_Sister.db")
    #     cur = conn.cursor()
    #     query = "SELECT url, timestamp, name, data, password_element from login"
    #
    #     cur.execute(query)
    #     rows = cur.fetchall()
    #
    #     conn.close()
    #
    #     count = len(rows)
    #     self.browser_login_table.setRowCount(count)
    #     self.browser_login_table.setColumnCount(5)
    #     column_headers = ["URL", "TimeStamp", "Name", "Date", "Password_Element"]
    #     self.browser_login_table.setHorizontalHeaderLabels(column_headers)
    #
    #     for i in range(count):
    #         url, timestamp, name, data, password_element = rows[i]
    #
    #         self.browser_login_table.setItem(i, 0, QTableWidgetItem(url))
    #         self.browser_login_table.setItem(i, 1, QTableWidgetItem(timestamp))
    #         self.browser_login_table.setItem(i, 2, QTableWidgetItem(name))
    #         self.browser_login_table.setItem(i, 3, QTableWidgetItem(data))
    #         self.browser_login_table.setItem(i, 4, QTableWidgetItem(password_element))

#### 브라우저 중 클라우드 테이블####
    # def Browser_Cloud(self):
    #     conn = sqlite3.connect("Believe_Me_Sister.db")
    #     cur = conn.cursor()
    #     query = "SELECT title, url, timestamp FROM cloud"
    #
    #     cur.execute(query)
    #     rows = cur.fetchall()
    #
    #     conn.close()
    #
    #     count = len(rows)
    #     self.browser_cloud_table.setRowCount(count)
    #     self.browser_cloud_table.setColumnCount(3)
    #     column_headers = ["Title", "URL", "TimeStamp"]
    #     self.browser_cloud_table.setHorizontalHeaderLabels(column_headers)
    #
    #     for i in range(count):
    #         title, url, timestamp = rows[i]
    #
    #         self.browser_cloud_table.setItem(i, 0, QTableWidgetItem(title))
    #         self.browser_cloud_table.setItem(i, 1, QTableWidgetItem(url))
    #         self.browser_cloud_table.setItem(i, 2, QTableWidgetItem(timestamp))

#### 브라우저 중 쿠키 테이블####
    # def Browser_Cookie(self):
    #     conn = sqlite3.connect("Believe_Me_Sister.db")
    #     cur = conn.cursor()
    #     query = "SELECT title, url, timestamp, value from cookies"
    #
    #     cur.execute(query)
    #     rows = cur.fetchall()
    #
    #     conn.close()
    #
    #     count = len(rows)
    #     self.browser_cookie_table.setRowCount(count)
    #     self.browser_cookie_table.setColumnCount(4)
    #     column_headers = ["Title", "URL", "TimeStamp", "Value"]
    #     self.browser_cookie_table.setHorizontalHeaderLabels(column_headers)
    #
    #     for i in range(count):
    #         title, url, timestamp, value = rows[i]
    #
    #         self.browser_cookie_table.setItem(i, 0, QTableWidgetItem(title))
    #         self.browser_cookie_table.setItem(i, 1, QTableWidgetItem(url))
    #         self.browser_cookie_table.setItem(i, 2, QTableWidgetItem(timestamp))
    #         self.browser_cookie_table.setItem(i, 3, QTableWidgetItem(value))

#### 브라우저 중 캐시 테이블####
#### timestamp가 캐시 생성 시간이라 그랬는데 마지막 수정시간이랑 시간대가 안 맞음
    # def Browser_Cache(self):
    #     conn = sqlite3.connect("Believe_Me_Sister.db")
    #     cur = conn.cursor()
    #     query = "SELECT value, url, server_name, status, etag, timestamp, last_modified, data_location," \
    #             " all_http_headers from cache"
    #
    #     cur.execute(query)
    #     rows = cur.fetchall()
    #
    #     conn.close()
    #
    #     count = len(rows)
    #     self.browser_cache_table.setRowCount(count)
    #     self.browser_cache_table.setColumnCount(9)
    #     column_headers = ["Value", "URL", "Server_Name", "Status", "etag", "Created_Time", "Last_Modified_Time", "Date_Location",
    #                       "All_HTTP_Headers"]
    #     self.browser_cache_table.setHorizontalHeaderLabels(column_headers)
    #
    #     for i in range(count):
    #         value, url, server_name, status, etag, timestamp, last_modified, data_location, all_http_headers = rows[i]
    #
    #         self.browser_cache_table.setItem(i, 0, QTableWidgetItem(value))
    #         self.browser_cache_table.setItem(i, 1, QTableWidgetItem(url))
    #         self.browser_cache_table.setItem(i, 2, QTableWidgetItem(server_name))
    #         self.browser_cache_table.setItem(i, 3, QTableWidgetItem(status))
    #         self.browser_cache_table.setItem(i, 4, QTableWidgetItem(etag))
    #         self.browser_cache_table.setItem(i, 5, QTableWidgetItem(timestamp))
    #         self.browser_cache_table.setItem(i, 6, QTableWidgetItem(last_modified))
    #         self.browser_cache_table.setItem(i, 7, QTableWidgetItem(data_location))
    #         self.browser_cache_table.setItem(i, 8, QTableWidgetItem(all_http_headers))

#### 브라우저 중 북마크 테이블####
    # def Browser_Bookmark(self):
    #     conn = sqlite3.connect("Believe_Me_Sister.db")
    #     cur = conn.cursor()
    #     query = "SELECT title, url, timestamp from bookmark"
    #
    #     cur.execute(query)
    #     rows = cur.fetchall()
    #
    #     conn.close()
    #
    #     count = len(rows)
    #     self.browser_bookmark_table.setRowCount(count)
    #     self.browser_bookmark_table.setColumnCount(3)
    #     column_headers = ["Title", "URL", "TimeStamp"]
    #     self.browser_bookmark_table.setHorizontalHeaderLabels(column_headers)
    #
    #     for i in range(count):
    #         title, url, timestamp = rows[i]
    #
    #         self.browser_bookmark_table.setItem(i, 0, QTableWidgetItem(title))
    #         self.browser_bookmark_table.setItem(i, 1, QTableWidgetItem(url))
    #         self.browser_bookmark_table.setItem(i, 2, QTableWidgetItem(timestamp))

#### 브라우저 중 자동완성 테이블####
    # def Browser_Autofill(self):
    #     conn = sqlite3.connect("Believe_Me_Sister.db")
    #     cur = conn.cursor()
    #     query = "SELECT value, status, timestamp from autofill"
    #
    #     cur.execute(query)
    #     rows = cur.fetchall()
    #
    #     conn.close()
    #
    #     count = len(rows)
    #     self.browser_autofill_table.setRowCount(count)
    #     self.browser_autofill_table.setColumnCount(3)
    #     column_headers = ["Value", "Status", "TimeStamp"]
    #     self.browser_autofill_table.setHorizontalHeaderLabels(column_headers)
    #
    #     for i in range(count):
    #         value, status, timestamp = rows[i]
    #
    #         self.browser_autofill_table.setItem(i, 0, QTableWidgetItem(value))
    #         self.browser_autofill_table.setItem(i, 1, QTableWidgetItem(status))
    #         self.browser_autofill_table.setItem(i, 2, QTableWidgetItem(timestamp))

#### 프로그램 실행 흔적 중 레지스트리 테이블####
#### 여러 개의 SQL문 중 Uninstall에서 가져오는 것만 사용함!
    # def Program_Registry(self):
    #     conn = sqlite3.connect("Believe_Me_Sister.db")
    #     cur = conn.cursor()
    #     query = "SELECT name, version, install_date, install_location, publisher, type FROM Uninstall"
    #
    #     cur.execute(query)
    #     rows = cur.fetchall()
    #
    #     conn.close()
    #
    #     count = len(rows)
    #     self.program_registry_table.setRowCount(count)
    #     self.program_registry_table.setColumnCount(6)
    #     column_headers = ["Name", "Version", "Install_Date", "Install_Location", "Publisher", "Type"]
    #     self.program_registry_table.setHorizontalHeaderLabels(column_headers)
    #
    #     for i in range(count):
    #         name, version, install_date, install_location, publisher, type = rows[i]
    #
    #         self.program_registry_table.setItem(i, 0, QTableWidgetItem(name))
    #         self.program_registry_table.setItem(i, 1, QTableWidgetItem(version))
    #         self.program_registry_table.setItem(i, 2, QTableWidgetItem(install_date))
    #         self.program_registry_table.setItem(i, 3, QTableWidgetItem(install_location))
    #         self.program_registry_table.setItem(i, 4, QTableWidgetItem(publisher))
    #         self.program_registry_table.setItem(i, 5, QTableWidgetItem(type))


####프로그램 실행 흔적 중 프리패치 테이블####
    # def Program_Prefetch(self):
    #     conn = sqlite3.connect("Believe_Me_Sister.db")
    #     cur = conn.cursor()
    #
    #     query = "SELECT Executable_Name, Run_Count FROM prefetch1"
    #     cur.execute(query)
    #     rows = cur.fetchall()
    #
    #     last_executed_rows = []
    #     for i in range(1, 9):
    #         query = "SELECT datetime(Last_Executed" + str(i) + ", '+9 hours') From Prefetch1"
    #         cur.execute(query)
    #         time = cur.fetchall()
    #         last_executed_rows.append(time)
    #     last_executed_rows = list(zip(*last_executed_rows))
    #
    #     conn.close()
    #
    #     count = len(rows)
    #     self.program_prefetch_table.setRowCount(count)
    #     self.program_prefetch_table.setColumnCount(10)
    #     column_headers = ["Executable_Name", "run count", "last executed time1", "last executed time2",
    #                       "last executed time3", "last executed time4", "last executed time5", "last executed time6",
    #                       "last executed time7", "last executed time8"]
    #     self.program_prefetch_table.setHorizontalHeaderLabels(column_headers)
    #
    #     for i in range(count):
    #         executable_name, run_count = rows[i]
    #         last_executed1, last_executed2, last_executed3, last_executed4,\
    #         last_executed5, last_executed6, last_executed7, last_executed8 = last_executed_rows[i]
    #
    #         self.program_prefetch_table.setItem(i, 0, QTableWidgetItem(executable_name))
    #         self.program_prefetch_table.setItem(i, 1, QTableWidgetItem(str(run_count)))
    #
    #         self.program_prefetch_table.setItem(i, 2, QTableWidgetItem(last_executed1[0]))
    #         self.program_prefetch_table.setItem(i, 3, QTableWidgetItem(last_executed2[0]))
    #         self.program_prefetch_table.setItem(i, 4, QTableWidgetItem(last_executed3[0]))
    #         self.program_prefetch_table.setItem(i, 5, QTableWidgetItem(last_executed4[0]))
    #         self.program_prefetch_table.setItem(i, 6, QTableWidgetItem(last_executed5[0]))
    #         self.program_prefetch_table.setItem(i, 7, QTableWidgetItem(last_executed6[0]))
    #         self.program_prefetch_table.setItem(i, 8, QTableWidgetItem(last_executed7[0]))
    #         self.program_prefetch_table.setItem(i, 9, QTableWidgetItem(last_executed8[0]))

#### 문서 실행 흔적 중 레지스트리 테이블####
#### opened_on이 접근 시간일까?
    # def Document_Registry(self):
    #     conn = sqlite3.connect("Believe_Me_Sister.db")
    #     cur = conn.cursor()
    #     query = "SELECT program, opened_on FROM RecentDocs WHERE (program LIKE '%.pdf' OR program LIKE '%.hwp' " \
    #             "OR program LIKE '%.docx' OR program LIKE '%.doc' OR program LIKE '%.xlsx' OR program LIKE '%.csv' " \
    #             "OR program LIKE '%.pptx' OR program LIKE '%.ppt' OR program LIKE '%.txt')"
    #
    #     cur.execute(query)
    #     rows = cur.fetchall()
    #
    #     conn.close()
    #
    #     count = len(rows)
    #     self.document_registry_table.setRowCount(count)
    #     self.document_registry_table.setColumnCount(2)
    #     column_headers = ["Program", "Accessed_Time"]
    #     self.document_registry_table.setHorizontalHeaderLabels(column_headers)
    #
    #     for i in range(count):
    #         program, opened_on = rows[i]
    #
    #         self.document_registry_table.setItem(i, 0, QTableWidgetItem(program))
    #         self.document_registry_table.setItem(i, 1, QTableWidgetItem(opened_on))

#### 문서 실행 흔적 중 링크 파일 테이블####
    # def Document_Lnk(self):
    #     conn = sqlite3.connect("Believe_Me_Sister.db")
    #     cur = conn.cursor()
    #     query = "SELECT file_name, lnk_file_full_path, file_flags, file_size, local_base_path, show_command," \
    #             "target_creation_time, target_modified_time, target_accessed_time, drive_serial_number, drive_type," \
    #             "volume_label, icon_location, machine_info from lnk_files " \
    #             "WHERE ((local_base_path LIKE '%.pdf' OR local_base_path LIKE '%.hwp' OR local_base_path LIKE '%.docx'" \
    #             "OR local_base_path LIKE '%.doc' OR local_base_path LIKE '%.xlsx' OR local_base_path LIKE '%.csv'" \
    #             "OR local_base_path LIKE '%.pptx' OR local_base_path LIKE '%.ppt' OR local_base_path LIKE '%.txt')" \
    #             "AND lnk_file_full_path LIKE '%Recent%')"
    #
    #     cur.execute(query)
    #     rows = cur.fetchall()
    #
    #     conn.close()
    #
    #     count = len(rows)
    #     self.document_lnk_table.setRowCount(count)
    #     self.document_lnk_table.setColumnCount(14)
    #     column_headers = ["File_Name", "Lnk_File_Path", "File_Flags", "Size", "Local_Base_Path", "Show_Command",
    #                       "Target_Created_Time", "Target_Modified_Time", "Target_Accessed_Timed", "Drive_Serial_Number",
    #                       "Drive_Type", "Volume_Label", "Icon_Location", "Machine_Info"]
    #     self.document_lnk_table.setHorizontalHeaderLabels(column_headers)
    #
    #     for i in range(count):
    #         file_name, lnk_file_full_path, file_flags, file_size, local_base_path, show_command,\
    #         target_creation_time, target_modified_time, target_accessed_time, drive_serial_number, drive_type,\
    #         volume_label, icon_location, machine_info = rows[i]
    #
    #         self.document_lnk_table.setItem(i, 0, QTableWidgetItem(file_name))
    #         self.document_lnk_table.setItem(i, 1, QTableWidgetItem(lnk_file_full_path))
    #         self.document_lnk_table.setItem(i, 2, QTableWidgetItem(file_flags))
    #         self.document_lnk_table.setItem(i, 3, QTableWidgetItem(file_size))
    #         self.document_lnk_table.setItem(i, 4, QTableWidgetItem(local_base_path))
    #         self.document_lnk_table.setItem(i, 5, QTableWidgetItem(show_command))
    #         self.document_lnk_table.setItem(i, 6, QTableWidgetItem(target_creation_time))
    #         self.document_lnk_table.setItem(i, 7, QTableWidgetItem(target_modified_time))
    #         self.document_lnk_table.setItem(i, 8, QTableWidgetItem(target_accessed_time))
    #         self.document_lnk_table.setItem(i, 9, QTableWidgetItem(drive_serial_number))
    #         self.document_lnk_table.setItem(i, 10, QTableWidgetItem(drive_type))
    #         self.document_lnk_table.setItem(i, 11, QTableWidgetItem(volume_label))
    #         self.document_lnk_table.setItem(i, 12, QTableWidgetItem(icon_location))
    #         self.document_lnk_table.setItem(i, 13, QTableWidgetItem(machine_info))

# #### 문서 실행 흔적 중 점프 목록 테이블####
# #### DB에 없는듯?
#     def Document_Jumplist(self):
#         conn = sqlite3.connect("Believe_Me_Sister.db")
#         cur = conn.cursor()
#         query = ""
#
#         cur.execute(query)
#         rows = cur.fetchall()
#
#         conn.close()
#
#         count = len(rows)
#         self.document_jumplist_table.setRowCount(count)
#         self.document_jumplist_table.setColumnCount(14)
#         column_headers = []
#         self.document_jumplist_table.setHorizontalHeaderLabels(column_headers)
#
#         for i in range(count):
#             = rows[i]
#
#             self.document_jumplist_table.setItem(i, 0, QTableWidgetItem())
#             self.document_jumplist_table.setItem(i, 1, QTableWidgetItem())
#             self.document_jumplist_table.setItem(i, 2, QTableWidgetItem())
#             self.document_jumplist_table.setItem(i, 3, QTableWidgetItem())
#             self.document_jumplist_table.setItem(i, 4, QTableWidgetItem())
#             self.document_jumplist_table.setItem(i, 5, QTableWidgetItem())
#             self.document_jumplist_table.setItem(i, 6, QTableWidgetItem())
#             self.document_jumplist_table.setItem(i, 7, QTableWidgetItem())
#             self.document_jumplist_table.setItem(i, 8, QTableWidgetItem())
#             self.document_jumplist_table.setItem(i, 9, QTableWidgetItem())
#             self.document_jumplist_table.setItem(i, 10, QTableWidgetItem())
#             self.document_jumplist_table.setItem(i, 11, QTableWidgetItem())
#             self.document_jumplist_table.setItem(i, 12, QTableWidgetItem())
#             self.document_jumplist_table.setItem(i, 13, QTableWidgetItem())


####문서 실행 흔적 중 프리패치 테이블####
    # def Document_Prefetch(self):
    #     conn = sqlite3.connect("Believe_Me_Sister.db")
    #     cur = conn.cursor()
    #     query = "SELECT FILENAME, PATH from prefetch2 WHERE (FILENAME LIKE '%.pdf' OR FILENAME LIKE '%.hwp' OR FILENAME LIKE '%.docx' " \
    #             "OR FILENAME LIKE '%.doc' OR FILENAME LIKE '%.xlsx' OR FILENAME LIKE '%.csv' OR FILENAME LIKE '%.pptx' " \
    #             "OR FILENAME LIKE '%.ppt' OR FILENAME LIKE '%.txt')"
    #     cur.execute(query)
    #     rows = cur.fetchall()
    #
    #     conn.close()
    #
    #     count = len(rows)
    #     self.document_prefetch_table.setRowCount(count)
    #     self.document_prefetch_table.setColumnCount(2)
    #     column_headers = ["File Name", "Path"]
    #     self.document_prefetch_table.setHorizontalHeaderLabels(column_headers)
    #
    #     for i in range(count):
    #         file_name, path = rows[i]
    #
    #         self.document_prefetch_table.setItem(i, 0, QTableWidgetItem(file_name))
    #         self.document_prefetch_table.setItem(i, 1, QTableWidgetItem(path))

#### 폴더 열람 흔적 링크 파일 테이블####
    # def Folder_Lnk(self):
    #     conn = sqlite3.connect("Believe_Me_Sister.db")
    #     cur = conn.cursor()
    #     query = "SELECT file_name, lnk_file_full_path, file_flags, file_size, local_base_path, show_command," \
    #             "target_creation_time, target_modified_time, target_accessed_time, drive_serial_number, drive_type," \
    #             "volume_label, icon_location, machine_info, droid_file, droid_vol, known_guid FROM lnk_files " \
    #             "WHERE file_flags LIKE '%DIRECTORY%'"
    #
    #     cur.execute(query)
    #     rows = cur.fetchall()
    #
    #     conn.close()
    #
    #     count = len(rows)
    #     self.folder_lnk_table.setRowCount(count)
    #     self.folder_lnk_table.setColumnCount(17)
    #     column_headers = ["File_Name", "Lnk_File_Path", "Flags", "Size", "Local_Base_Path", "Show_Command", \
    #             "Target_Created_Time", "Target_Modified_Time", "Target_Accessed_Time", "Drive_Serial_Number", "Drive_Type", \
    #             "Volume_Label", "Icon_Location", "Machine_Info", "Droid_File", "Droid_Vol", "Known_Guid"]
    #     self.folder_lnk_table.setHorizontalHeaderLabels(column_headers)
    #
    #     for i in range(count):
    #         file_name, lnk_file_full_path, file_flags, file_size, local_base_path, show_command, target_creation_time, \
    #         target_modified_time, target_accessed_time, drive_serial_number, drive_type, volume_label, icon_location,\
    #         machine_info, droid_file, droid_vol, known_guid = rows[i]
    #
    #         self.folder_lnk_table.setItem(i, 0, QTableWidgetItem(file_name))
    #         self.folder_lnk_table.setItem(i, 1, QTableWidgetItem(lnk_file_full_path))
    #         self.folder_lnk_table.setItem(i, 2, QTableWidgetItem(file_flags))
    #         self.folder_lnk_table.setItem(i, 3, QTableWidgetItem(file_size))
    #         self.folder_lnk_table.setItem(i, 4, QTableWidgetItem(local_base_path))
    #         self.folder_lnk_table.setItem(i, 5, QTableWidgetItem(show_command))
    #         self.folder_lnk_table.setItem(i, 6, QTableWidgetItem(target_creation_time))
    #         self.folder_lnk_table.setItem(i, 7, QTableWidgetItem(target_modified_time))
    #         self.folder_lnk_table.setItem(i, 8, QTableWidgetItem(target_accessed_time))
    #         self.folder_lnk_table.setItem(i, 9, QTableWidgetItem(drive_serial_number))
    #         self.folder_lnk_table.setItem(i, 10, QTableWidgetItem(drive_type))
    #         self.folder_lnk_table.setItem(i, 11, QTableWidgetItem(volume_label))
    #         self.folder_lnk_table.setItem(i, 12, QTableWidgetItem(icon_location))
    #         self.folder_lnk_table.setItem(i, 13, QTableWidgetItem(machine_info))
    #         self.folder_lnk_table.setItem(i, 14, QTableWidgetItem(droid_file))
    #         self.folder_lnk_table.setItem(i, 15, QTableWidgetItem(droid_vol))
    #         self.folder_lnk_table.setItem(i, 16, QTableWidgetItem(known_guid))

#### 기타 실행 흔적 중 링크 파일 테이블####
    # def Etc_Lnk(self):
    #     conn = sqlite3.connect("Believe_Me_Sister.db")
    #     cur = conn.cursor()
    #     query = "SELECT file_name, lnk_file_full_path, file_flags, file_size, local_base_path, show_command," \
    #             "target_creation_time, target_modified_time, target_accessed_time, drive_serial_number, drive_type," \
    #             "volume_label, icon_location, machine_info FROM lnk_files " \
    #             "WHERE((local_base_path LIKE '%.jpg' OR local_base_path LIKE '%.jpeg' OR local_base_path LIKE '%.gif' " \
    #             "OR local_base_path LIKE '%.bmp' OR local_base_path LIKE '%.png' OR local_base_path LIKE '%.raw' " \
    #             "OR local_base_path LIKE '%.tiff' OR local_base_path LIKE '%.wav' OR local_base_path LIKE '%.wma' " \
    #             "OR local_base_path LIKE '%.mp3' OR local_base_path LIKE '%.mp4' OR local_base_path LIKE '%.mkv' " \
    #             "OR local_base_path LIKE '%.avi' OR local_base_path LIKE '%.flv' OR local_base_path LIKE '%.mov' " \
    #             "OR local_base_path LIKE '%.zip' OR local_base_path LIKE '%.7z' OR local_base_path LIKE '%.alz' " \
    #             "OR local_base_path LIKE '%.egg' OR local_base_path LIKE '%.rar')" \
    #             "AND file_flags not LIKE '%DIRECTORY%' AND lnk_file_full_path LIKE '%Recent%')"
    #
    #     cur.execute(query)
    #     rows = cur.fetchall()
    #
    #     conn.close()
    #
    #     count = len(rows)
    #     self.etc_lnk_table.setRowCount(count)
    #     self.etc_lnk_table.setColumnCount(14)
    #     column_headers = ["File_Name", "Lnk_File_Path", "Flags", "Size", "Local_Base_Path", "Show_Command", \
    #             "Target_Created_Time", "Target_Modified_Time", "Target_Accessed_Time", "Drive_Serial_Number", "Drive_Type", \
    #             "Volume_Label", "Icon_Location", "Machine_Info"]
    #     self.etc_lnk_table.setHorizontalHeaderLabels(column_headers)
    #
    #     for i in range(count):
    #         file_name, lnk_file_full_path, file_flags, file_size, local_base_path, show_command, target_creation_time, \
    #         target_modified_time, target_accessed_time, drive_serial_number, drive_type, volume_label, icon_location,\
    #         machine_info = rows[i]
    #
    #         self.etc_lnk_table.setItem(i, 0, QTableWidgetItem(file_name))
    #         self.etc_lnk_table.setItem(i, 1, QTableWidgetItem(lnk_file_full_path))
    #         self.etc_lnk_table.setItem(i, 2, QTableWidgetItem(file_flags))
    #         self.etc_lnk_table.setItem(i, 3, QTableWidgetItem(file_size))
    #         self.etc_lnk_table.setItem(i, 4, QTableWidgetItem(local_base_path))
    #         self.etc_lnk_table.setItem(i, 5, QTableWidgetItem(show_command))
    #         self.etc_lnk_table.setItem(i, 6, QTableWidgetItem(target_creation_time))
    #         self.etc_lnk_table.setItem(i, 7, QTableWidgetItem(target_modified_time))
    #         self.etc_lnk_table.setItem(i, 8, QTableWidgetItem(target_accessed_time))
    #         self.etc_lnk_table.setItem(i, 9, QTableWidgetItem(drive_serial_number))
    #         self.etc_lnk_table.setItem(i, 10, QTableWidgetItem(drive_type))
    #         self.etc_lnk_table.setItem(i, 11, QTableWidgetItem(volume_label))
    #         self.etc_lnk_table.setItem(i, 12, QTableWidgetItem(icon_location))
    #         self.etc_lnk_table.setItem(i, 13, QTableWidgetItem(machine_info))


####기타 실행 흔적 중 프리패치 테이블####
    # def Etc_Prefetch(self):
    #     conn = sqlite3.connect("Believe_Me_Sister.db")
    #     cur = conn.cursor()
    #     query = "SELECT FILENAME, PATH from prefetch2  WHERE (FILENAME LIKE '%.jpg' OR FILENAME LIKE '%.jpeg' OR FILENAME LIKE '%.gif' " \
    #             "OR FILENAME LIKE '%.bmp' OR FILENAME LIKE '%.png' OR FILENAME LIKE '%.raw' OR FILENAME LIKE '%.tiff' " \
    #             "OR FILENAME LIKE '%.wav' OR FILENAME LIKE '%.wma' OR FILENAME LIKE '%.mp3' OR FILENAME LIKE '%.mp4' " \
    #             "OR FILENAME LIKE '%.mkv' OR FILENAME LIKE '%.avi' OR FILENAME LIKE '%.flv' OR FILENAME LIKE '%.mov' " \
    #             "OR FILENAME LIKE '%.zip' OR FILENAME LIKE '%.7z' OR FILENAME LIKE '%.alz' OR FILENAME LIKE '%.egg' " \
    #             "OR FILENAME LIKE '%.rar')"
    #     cur.execute(query)
    #     rows = cur.fetchall()
    #
    #     conn.close()
    #
    #     count = len(rows)
    #     self.etc_prefetch_table.setRowCount(count)
    #     self.etc_prefetch_table.setColumnCount(2)
    #     column_headers = ["File Name", "Path"]
    #     self.etc_prefetch_table.setHorizontalHeaderLabels(column_headers)
    #
    #     for i in range(count):
    #         file_name, path = rows[i]
    #
    #         self.etc_prefetch_table.setItem(i, 0, QTableWidgetItem(file_name))
    #         self.etc_prefetch_table.setItem(i, 1, QTableWidgetItem(path))

#### 이벤트 로그 흔적 중 이벤트 로그 삭제 테이블####
#### event_id 안 보임ㅠㅠ
    # def Event_Eventdel(self):
    #     conn = sqlite3.connect("Believe_Me_Sister.db")
    #     cur = conn.cursor()
    #     query = "SELECT event_id, detailed, computer, time_created, sbt_usr_name, channel, source FROM event_log " \
    #             "WHERE (event_id LIKE '104' OR event_id LIKE '1102')"
    #
    #     cur.execute(query)
    #     rows = cur.fetchall()
    #
    #     conn.close()
    #
    #     count = len(rows)
    #     self.event_eventdel_table.setRowCount(count)
    #     self.event_eventdel_table.setColumnCount(7)
    #     column_headers = ["Event_ID", "Detailed", "Computer", "Created_Time", "Sbt_User_Name", "Channel", "Source"]
    #     self.event_eventdel_table.setHorizontalHeaderLabels(column_headers)
    #
    #     for i in range(count):
    #         event_id, detailed, computer, time_created, sbt_usr_name, channel, source = rows[i]
    #
    #         self.event_eventdel_table.setItem(i, 0, QTableWidgetItem(event_id))
    #         self.event_eventdel_table.setItem(i, 1, QTableWidgetItem(detailed))
    #         self.event_eventdel_table.setItem(i, 2, QTableWidgetItem(computer))
    #         self.event_eventdel_table.setItem(i, 3, QTableWidgetItem(time_created))
    #         self.event_eventdel_table.setItem(i, 4, QTableWidgetItem(sbt_usr_name))
    #         self.event_eventdel_table.setItem(i, 5, QTableWidgetItem(channel))
    #         self.event_eventdel_table.setItem(i, 6, QTableWidgetItem(source))

#### 이벤트 로그 흔적 중 프로세스 강제 종료 테이블####
#### event_id 안 보임ㅠㅠ
    # def Event_Process(self):
    #     conn = sqlite3.connect("Believe_Me_Sister.db")
    #     cur = conn.cursor()
    #     query = "SELECT event_id, detailed, computer, time_created, app_name, app_version, app_path " \
    #             "FROM event_log WHERE (event_id LIKE '1002' AND app_name IS NOT '')"
    #
    #     cur.execute(query)
    #     rows = cur.fetchall()
    #
    #     conn.close()
    #
    #     count = len(rows)
    #     self.event_process_table.setRowCount(count)
    #     self.event_process_table.setColumnCount(7)
    #     column_headers = ["Event_ID", "Detailed", "Computer", "Created_Time", "App_Name", "App_Version", "App_Path"]
    #     self.event_process_table.setHorizontalHeaderLabels(column_headers)
    #
    #     for i in range(count):
    #         event_id, detailed, computer, time_created, app_name, app_version, app_path = rows[i]
    #
    #         self.event_process_table.setItem(i, 0, QTableWidgetItem(event_id))
    #         self.event_process_table.setItem(i, 1, QTableWidgetItem(detailed))
    #         self.event_process_table.setItem(i, 2, QTableWidgetItem(computer))
    #         self.event_process_table.setItem(i, 3, QTableWidgetItem(time_created))
    #         self.event_process_table.setItem(i, 4, QTableWidgetItem(app_name))
    #         self.event_process_table.setItem(i, 5, QTableWidgetItem(app_version))
    #         self.event_process_table.setItem(i, 6, QTableWidgetItem(app_path))

#### 이벤트 로그 흔적 PC ON/OFF 종료 테이블####
#### event_id 안 보임ㅠㅠ
    # def Event_PC(self):
    #     conn = sqlite3.connect("Believe_Me_Sister.db")
    #     cur = conn.cursor()
    #     query = "SELECT event_id, detailed, computer, time_created FROM event_log " \
    #             "WHERE (event_id LIKE '12' OR event_id LIKE '13')"
    #
    #     cur.execute(query)
    #     rows = cur.fetchall()
    #
    #     conn.close()
    #
    #     count = len(rows)
    #     self.event_pc_table.setRowCount(count)
    #     self.event_pc_table.setColumnCount(4)
    #     column_headers = ["Event_ID", "Detailed", "Computer", "Created_Time"]
    #     self.event_pc_table.setHorizontalHeaderLabels(column_headers)
    #
    #     for i in range(count):
    #         event_id, detailed, computer, time_created = rows[i]
    #
    #         self.event_pc_table.setItem(i, 0, QTableWidgetItem(event_id))
    #         self.event_pc_table.setItem(i, 1, QTableWidgetItem(detailed))
    #         self.event_pc_table.setItem(i, 2, QTableWidgetItem(computer))
    #         self.event_pc_table.setItem(i, 3, QTableWidgetItem(time_created))

#### 이벤트 로그 흔적 절전모드 종료 테이블####
#### event_id 안 보임ㅠㅠ
    # def Event_Powersave(self):
    #     conn = sqlite3.connect("Believe_Me_Sister.db")
    #     cur = conn.cursor()
    #     query = "SELECT event_id, detailed, computer, time_created, sleep_time, wake_time " \
    #             "FROM event_log WHERE (event_id LIKE '1' OR (event_id LIKE '42' AND source IS 'System.evtx'))"
    #
    #     cur.execute(query)
    #     rows = cur.fetchall()
    #
    #     conn.close()
    #
    #     count = len(rows)
    #     self.event_powersave_table.setRowCount(count)
    #     self.event_powersave_table.setColumnCount(6)
    #     column_headers = ["Event_ID", "Detailed", "Computer", "Created_Time", "Sleep_Time", "Wake_Time"]
    #     self.event_powersave_table.setHorizontalHeaderLabels(column_headers)
    #
    #     for i in range(count):
    #         event_id, detailed, computer, time_created, sleep_time, wake_time = rows[i]
    #
    #         self.event_powersave_table.setItem(i, 0, QTableWidgetItem(event_id))
    #         self.event_powersave_table.setItem(i, 1, QTableWidgetItem(detailed))
    #         self.event_powersave_table.setItem(i, 2, QTableWidgetItem(computer))
    #         self.event_powersave_table.setItem(i, 3, QTableWidgetItem(time_created))
    #         self.event_powersave_table.setItem(i, 4, QTableWidgetItem(sleep_time))
    #         self.event_powersave_table.setItem(i, 5, QTableWidgetItem(wake_time))

#### 이벤트 로그 흔적 원격 접속 테이블####
#### event_id 안 보임ㅠㅠ
#### 일단 원격 접속 당한 것만 해놨음!
    def Event_Remote(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT event_id, detailed, computer, time_created, remo_conn_user, remo_conn_addr, remo_conn_local," \
                "local_manager_sess_id FROM event_log WHERE (event_id LIKE '261' OR event_id LIKE '1149' OR event_id LIKE '24' " \
                "OR event_id LIKE '25')"

        cur.execute(query)
        rows = cur.fetchall()

        conn.close()

        count = len(rows)
        self.event_remote_table.setRowCount(count)
        self.event_remote_table.setColumnCount(8)
        column_headers = ["Event_ID", "Detailed", "Computer", "Created_Time", "Remote_Conn_User", "Remote_Conn_Addr",
                          "Remote_Conn_Local", "Local_Manager_Sess_ID"]
        self.event_remote_table.setHorizontalHeaderLabels(column_headers)

        for i in range(count):
            event_id, detailed, computer, time_created, remo_conn_user, remo_conn_addr, remo_conn_local,\
            local_manager_sess_id = rows[i]

            self.event_remote_table.setItem(i, 0, QTableWidgetItem(event_id))
            self.event_remote_table.setItem(i, 1, QTableWidgetItem(detailed))
            self.event_remote_table.setItem(i, 2, QTableWidgetItem(computer))
            self.event_remote_table.setItem(i, 3, QTableWidgetItem(time_created))
            self.event_remote_table.setItem(i, 4, QTableWidgetItem(remo_conn_user))
            self.event_remote_table.setItem(i, 5, QTableWidgetItem(remo_conn_addr))
            self.event_remote_table.setItem(i, 6, QTableWidgetItem(remo_conn_local))
            self.event_remote_table.setItem(i, 7, QTableWidgetItem(local_manager_sess_id))

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