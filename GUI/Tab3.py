import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtCore import *
import sqlite3

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
    self.timebutton.clicked.connect(set_timeline)
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
    accum = self.timeline_count
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
    conn = sqlite3.connect("Believe_Me_Sister.db")
    cur = conn.cursor()
    query = "SELECT event_id, detailed, computer, time_created, sbt_usr_name, channel FROM event_log " \
            "WHERE (event_id LIKE '104' or event_id LIKE '1102' AND sbt_usr_name IS NOT '')"
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
