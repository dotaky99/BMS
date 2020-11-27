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
        item4.setText(0, "프리패치")

        item5 = QTreeWidgetItem(tree)
        item5.setText(0, "프로그램/파일")
        item5_1 = QTreeWidgetItem(item5)
        item5_1.setText(0, "프로그램")
        item5_2 = QTreeWidgetItem(item5)
        item5_2.setText(0, "파일")

        item6 = QTreeWidgetItem(tree)
        item6.setText(0, "이벤트 로그")
        item6_1 = QTreeWidgetItem(item6)
        item6_1.setText(0, "이벤트 로그 삭제")
        item6_2 = QTreeWidgetItem(item6)
        item6_2.setText(0, "프로세스 강제 종료")
        item6_3 = QTreeWidgetItem(item6)
        item6_3.setText(0, "PC ON/OFF")
        item6_4 = QTreeWidgetItem(item6)
        item6_4.setText(0, "절전 모드")
        item6_5 = QTreeWidgetItem(item6)
        item6_5.setText(0, "원격 접속 기록")

        self.prefetch_table = QTableWidget(self)
        self.set_prefetch_data()

        self.tab4.layout.addWidget(tree)
        self.tab4.layout.addWidget(self.prefetch_table)
        self.tab4.setLayout(self.tab4.layout)

    def set_prefetch_data(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()

        query = "SELECT Executable_Name, Run_Count FROM prefetch1"
        cur.execute(query)
        rows = cur.fetchall()

        last_executed_rows = []
        for i in range(1, 9):
            query = "SELECT datetime(Last_Executed" + str(i) + ", ' +9 hours') FROM prefetch1"
            #query = "SELECT datetime(Last_Executed" + str(i) + ", '" + self.UTC + " hours') FROM prefetch1"
            cur.execute(query)
            last_executed_rows.append(cur.fetchall())
        last_executed_rows = list(zip(*last_executed_rows))

        conn.close()

        count = len(rows)
        self.prefetch_table.setRowCount(count)
        self.prefetch_table.setColumnCount(11)
        column_headers = ["Executable_Name", "run count", "last executed time1", "last executed time2",
                          "last executed time3", "last executed time4", "last executed time5", "last executed time6",
                          "last executed time7", "last executed time8"]
        self.prefetch_table.setHorizontalHeaderLabels(column_headers)

        for i in range(count):
            executable_name, run_count = rows[i]
            last_executed1, last_executed2, last_executed3, last_executed4,\
            last_executed5, last_executed6, last_executed7, last_executed8 = last_executed_rows[i]

            #self.prefetch_table.setItem(i, 0, QTableWidgetItem(file_name))
            self.prefetch_table.setItem(i, 1, QTableWidgetItem(executable_name))
            self.prefetch_table.setItem(i, 2, QTableWidgetItem(str(run_count)))

            self.prefetch_table.setItem(i, 3, QTableWidgetItem(last_executed1[0]))
            self.prefetch_table.setItem(i, 4, QTableWidgetItem(last_executed2[0]))
            self.prefetch_table.setItem(i, 5, QTableWidgetItem(last_executed3[0]))
            self.prefetch_table.setItem(i, 6, QTableWidgetItem(last_executed4[0]))
            self.prefetch_table.setItem(i, 7, QTableWidgetItem(last_executed5[0]))
            self.prefetch_table.setItem(i, 8, QTableWidgetItem(last_executed6[0]))
            self.prefetch_table.setItem(i, 9, QTableWidgetItem(last_executed7[0]))
            self.prefetch_table.setItem(i, 10, QTableWidgetItem(last_executed8[0]))

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