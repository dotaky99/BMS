import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtCore import *
import sqlite3
import datetime

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

#################################################
#   tab2                                        #
#################################################
    def set_tab2(self):
        # tab2 구성
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
        query1 = "SELECT Executable_Name, Last_Executed1 from prefetch1 " \
                 "WHERE (Executable_Name LIKE 'CCleaner%' OR Executable_Name LIKE 'Cipher%' " \
                 "OR Executable_Name LIKE 'CipherShed%' OR Executable_Name LIKE 'Eraser%' " \
                 "OR Executable_Name LIKE 'SDelete%' OR Executable_Name LIKE 'SetMACE%'" \
                 "OR Executable_Name LIKE 'TrueCrypt%'  OR Executable_Name LIKE 'TimeStomp%'" \
                 "OR Executable_Name LIKE 'VeraCrypt%'  OR Executable_Name LIKE 'Wise Folder Hider%')"
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

#################################################
#   tab3                                        #
#################################################

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
        self.during.setAlignment(Qt.AlignCenter)
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
        self.datetime1 = self.input_datetime1.dateTime().toString('yyyy-MM-dd hh:mm:ss')
        self.datetime2 = self.input_datetime2.dateTime().toString('yyyy-MM-dd hh:mm:ss')
        self.timeline.clearContents()
        self.timeline_count = 0

        if self.checkbox1_1.isChecked():
            self.timeline_data1_1()
        if self.checkbox1_2.isChecked():
            self.timeline_data1_2()
        if self.checkbox1_3.isChecked():
            self.timeline_data1_3()
        if self.checkbox1_4.isChecked():
            self.timeline_data1_4()
        if self.checkbox1_5.isChecked():
            self.timeline_data1_5()
        if self.checkbox2_1.isChecked():
            self.timeline_date2_1()
        if self.checkbox2_2.isChecked():
            self.timeline_data2_2()
        if self.checkbox2_3.isChecked():
            self.timeline_data2_3()
        if self.checkbox2_4.isChecked():
            self.timeline_data2_4()
        if self.checkbox2_5.isChecked():
            self.timeline_data2_5()

        self.timeline.resizeColumnsToContents()

    # MFT 생성
    def timeline_data1_1(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query_1 = "SELECT file_path, drive, SI_M_timestamp from parsed_MFT WHERE ((file_path LIKE '/$MFT') AND " \
                "(SI_M_timestamp >= '" + self.datetime1 + "' AND SI_M_timestamp <= '" + self.datetime2 + "'))"
        cur.execute(query_1)
        rows = cur.fetchall()

        accum = self.timeline_count
        self.timeline_count = accum + len(rows)
        self.timeline.setRowCount(self.timeline_count)

        sortingEnabled = self.timeline.isSortingEnabled()
        self.timeline.setSortingEnabled(False)

        for i in range(len(rows)):
            file_path, drive, SI_M_timestamp = rows[i]
            self.timeline.setItem(accum + i, 0, QTableWidgetItem(SI_M_timestamp))
            string1 = drive + "드라이브 MFT 생성"
            string2 = " - SI_M_timestamp"
            self.timeline.setItem(accum + i, 1, QTableWidgetItem(string1))
            self.timeline.setItem(accum + i, 2, QTableWidgetItem(file_path + string2))
        self.timeline.setSortingEnabled(sortingEnabled)

        query_2 = "SELECT file_path, drive, SI_A_timestamp from parsed_MFT WHERE ((file_path LIKE '/$MFT') AND " \
                "(SI_A_timestamp >= '" + self.datetime1 + "' AND SI_A_timestamp <= '" + self.datetime2 + "'))"
        cur.execute(query_2)
        rows = cur.fetchall()
        accum = self.timeline_count
        self.timeline_count = accum + len(rows)
        self.timeline.setRowCount(self.timeline_count)

        sortingEnabled = self.timeline.isSortingEnabled()
        self.timeline.setSortingEnabled(False)

        for i in range(len(rows)):
            file_path, drive, SI_A_timestamp = rows[i]
            self.timeline.setItem(accum + i, 0, QTableWidgetItem(SI_A_timestamp))
            string1 = drive + "드라이브 MFT 생성"
            string2 = " - SI_A_timestamp"
            self.timeline.setItem(accum + i, 1, QTableWidgetItem(string1))
            self.timeline.setItem(accum + i, 2, QTableWidgetItem(file_path + string2))
        self.timeline.setSortingEnabled(sortingEnabled)

        query_3 = "SELECT file_path, drive, SI_C_timestamp from parsed_MFT WHERE ((file_path LIKE '/$MFT') AND " \
                "(SI_C_timestamp >= '" + self.datetime1 + "' AND SI_C_timestamp <= '" + self.datetime2 + "'))"
        cur.execute(query_3)
        rows = cur.fetchall()
        accum = self.timeline_count
        self.timeline_count = accum + len(rows)
        self.timeline.setRowCount(self.timeline_count)

        sortingEnabled = self.timeline.isSortingEnabled()
        self.timeline.setSortingEnabled(False)

        for i in range(len(rows)):
            file_path, drive, SI_C_timestamp = rows[i]
            self.timeline.setItem(accum + i, 0, QTableWidgetItem(SI_C_timestamp))
            string1 = drive + "드라이브 MFT 생성"
            string2 = " - SI_C_timestamp"
            self.timeline.setItem(accum + i, 1, QTableWidgetItem(string1))
            self.timeline.setItem(accum + i, 2, QTableWidgetItem(file_path + string2))
        self.timeline.setSortingEnabled(sortingEnabled)


        query_4 = "SELECT file_path, drive, SI_E_timestamp from parsed_MFT WHERE ((file_path LIKE '/$MFT') AND " \
                "(SI_E_timestamp >= '" + self.datetime1 + "' AND SI_E_timestamp <= '" + self.datetime2 + "'))"
        cur.execute(query_4)
        rows = cur.fetchall()
        accum = self.timeline_count
        self.timeline_count = accum + len(rows)
        self.timeline.setRowCount(self.timeline_count)

        sortingEnabled = self.timeline.isSortingEnabled()
        self.timeline.setSortingEnabled(False)

        for i in range(len(rows)):
            file_path, drive, SI_E_timestamp = rows[i]
            self.timeline.setItem(accum + i, 0, QTableWidgetItem(SI_E_timestamp))
            string1 = drive + "드라이브 MFT 생성"
            string2 = " - SI_E_timestamp"
            self.timeline.setItem(accum + i, 1, QTableWidgetItem(string1))
            self.timeline.setItem(accum + i, 2, QTableWidgetItem(file_path + string2))
        self.timeline.setSortingEnabled(sortingEnabled)


        query_5 = "SELECT file_path, drive, FN_M_timestamp from parsed_MFT WHERE ((file_path LIKE '/$MFT') AND " \
                "(FN_M_timestamp >= '" + self.datetime1 + "' AND FN_M_timestamp <= '" + self.datetime2 + "'))"
        cur.execute(query_5)
        rows = cur.fetchall()
        accum = self.timeline_count
        self.timeline_count = accum + len(rows)
        self.timeline.setRowCount(self.timeline_count)

        sortingEnabled = self.timeline.isSortingEnabled()
        self.timeline.setSortingEnabled(False)

        for i in range(len(rows)):
            file_path, drive, FN_M_timestamp = rows[i]
            self.timeline.setItem(accum + i, 0, QTableWidgetItem(FN_M_timestamp))
            string1 = drive + "드라이브 MFT 생성"
            string2 = " - FN_M_timestamp"
            self.timeline.setItem(accum + i, 1, QTableWidgetItem(string1))
            self.timeline.setItem(accum + i, 2, QTableWidgetItem(file_path + string2))
        self.timeline.setSortingEnabled(sortingEnabled)


        query_6 = "SELECT file_path, drive, FN_A_timestamp from parsed_MFT WHERE ((file_path LIKE '/$MFT') AND " \
                "(FN_A_timestamp >= '" + self.datetime1 + "' AND FN_A_timestamp <= '" + self.datetime2 + "'))"
        cur.execute(query_6)
        rows = cur.fetchall()
        accum = self.timeline_count
        self.timeline_count = accum + len(rows)
        self.timeline.setRowCount(self.timeline_count)

        sortingEnabled = self.timeline.isSortingEnabled()
        self.timeline.setSortingEnabled(False)

        for i in range(len(rows)):
            file_path, drive, FN_A_timestamp = rows[i]
            self.timeline.setItem(accum + i, 0, QTableWidgetItem(FN_A_timestamp))
            string1 = drive + "드라이브 MFT 생성"
            string2 = " - FN_A_timestamp"
            self.timeline.setItem(accum + i, 1, QTableWidgetItem(string1))
            self.timeline.setItem(accum + i, 2, QTableWidgetItem(file_path + string2))
        self.timeline.setSortingEnabled(sortingEnabled)


        query_7 = "SELECT file_path, drive, FN_C_timestamp from parsed_MFT WHERE ((file_path LIKE '/$MFT') AND " \
                "(FN_C_timestamp >= '" + self.datetime1 + "' AND FN_C_timestamp <= '" + self.datetime2 + "'))"
        cur.execute(query_7)
        rows = cur.fetchall()
        accum = self.timeline_count
        self.timeline_count = accum + len(rows)
        self.timeline.setRowCount(self.timeline_count)

        sortingEnabled = self.timeline.isSortingEnabled()
        self.timeline.setSortingEnabled(False)

        for i in range(len(rows)):
            file_path, drive, FN_C_timestamp = rows[i]
            self.timeline.setItem(accum + i, 0, QTableWidgetItem(FN_C_timestamp))
            string1 = drive + "드라이브 MFT 생성"
            string2 = " - FN_C_timestamp"
            self.timeline.setItem(accum + i, 1, QTableWidgetItem(string1))
            self.timeline.setItem(accum + i, 2, QTableWidgetItem(file_path + string2))
        self.timeline.setSortingEnabled(sortingEnabled)


        query_8 = "SELECT file_path, drive, FN_E_timestamp from parsed_MFT WHERE ((file_path LIKE '/$MFT') AND " \
                "(FN_E_timestamp >= '" + self.datetime1 + "' AND FN_E_timestamp <= '" + self.datetime2 + "'))"
        cur.execute(query_8)
        rows = cur.fetchall()
        accum = self.timeline_count
        self.timeline_count = accum + len(rows)
        self.timeline.setRowCount(self.timeline_count)

        sortingEnabled = self.timeline.isSortingEnabled()
        self.timeline.setSortingEnabled(False)

        for i in range(len(rows)):
            file_path, drive, FN_E_timestamp = rows[i]
            self.timeline.setItem(accum + i, 0, QTableWidgetItem(FN_E_timestamp))
            string1 = drive + "드라이브 MFT 생성"
            string2 = " - FN_E_timestamp"
            self.timeline.setItem(accum + i, 1, QTableWidgetItem(string1))
            self.timeline.setItem(accum + i, 2, QTableWidgetItem(file_path + string2))
        self.timeline.setSortingEnabled(sortingEnabled)

    # 계정 생성
    def timeline_data1_2(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query_1 = "SELECT created_on, account_name, RID_int FROM UserAccounts " \
                " WHERE (created_on >= '" + self.datetime1 + "' AND created_on <= '" + self.datetime2 + "')"
        cur.execute(query_1)
        rows = cur.fetchall()

        accum = self.timeline_count
        self.timeline_count = accum + len(rows)
        self.timeline.setRowCount(self.timeline_count)

        sortingEnabled = self.timeline.isSortingEnabled()
        self.timeline.setSortingEnabled(False)

        password_exists = []
        for i in range(len(rows)):
            created_on, name, rid = rows[i]
            # if (self.datetime1 <= created_on) and (self.datetime2 >= created_on):
            self.timeline.setItem(accum + i, 0, QTableWidgetItem(created_on))
            self.timeline.setItem(accum + i, 1, QTableWidgetItem("계정 생성"))
            self.timeline.setItem(accum + i, 2, QTableWidgetItem(name + ", SID: " + str(rid)))
        self.timeline.setSortingEnabled(sortingEnabled)
        self.set_color()

        query_2 = "SELECT last_password_change_time, account_name, RID_int FROM UserAccounts " \
                  " WHERE (last_password_change_time >= '" + self.datetime1 + "' AND last_password_change_time <= '" + self.datetime2 + "')"
        cur.execute(query_2)
        rows = cur.fetchall()

        accum = self.timeline_count
        self.timeline_count = accum + len(rows)
        self.timeline.setRowCount(self.timeline_count)

        sortingEnabled = self.timeline.isSortingEnabled()
        self.timeline.setSortingEnabled(False)

        for i in range(len(rows)):
            last_password_change_time, account_name, RID_int = rows[i]
            if last_password_change_time != None:
                self.timeline.setItem(accum + i, 0, QTableWidgetItem(last_password_change_time))
                self.timeline.setItem(accum + i, 1, QTableWidgetItem("계정 패스워드 변경"))
                self.timeline.setItem(accum + i, 2, QTableWidgetItem(account_name + ", SID: " + str(RID_int)))
            else:
                pass
        self.timeline.setSortingEnabled(sortingEnabled)
        self.set_color()


    # Windows 설치
    def timeline_data1_3(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT install_date, product_name, product_ID FROM OSInformation " \
                " WHERE (install_date >= '" + self.datetime1 + "' AND install_date <= '" + self.datetime2 + "')"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()
        accum = self.timeline_count
        self.timeline_count = accum + len(rows)
        self.timeline.setRowCount(self.timeline_count)

        sortingEnabled = self.timeline.isSortingEnabled()
        self.timeline.setSortingEnabled(False)

        for i in range(len(rows)):
            install_date, product_name, product_ID = rows[i]
            self.timeline.setItem(accum + i, 0, QTableWidgetItem(install_date))
            self.timeline.setItem(accum + i, 1, QTableWidgetItem("Windows 설치"))
            self.timeline.setItem(accum + i, 2, QTableWidgetItem(product_name + ", 제품 ID: " + product_ID))
        self.timeline.setSortingEnabled(sortingEnabled)

    # Windows 업데이트
    def timeline_data1_4(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT detailed, computer, time_created, package FROM event_log WHERE ((event_id='2' AND package IS NOT '')" \
                " AND (time_created >= '" + self.datetime1 + "' AND time_created <= '" + self.datetime2 + "'))"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()
        accum = self.timeline_count
        self.timeline_count = accum + len(rows)
        self.timeline.setRowCount(self.timeline_count)

        sortingEnabled = self.timeline.isSortingEnabled()
        self.timeline.setSortingEnabled(False)

        for i in range(len(rows)):
            detailed, computer, time_created, package = rows[i]
            self.timeline.setItem(i + accum, 0, QTableWidgetItem(time_created))
            self.timeline.setItem(i + accum, 1, QTableWidgetItem("Windows 업데이트"))
            string = "detailed: " + detailed + ", computer: " + computer + ", package: " + package
            self.timeline.setItem(i + accum, 2, QTableWidgetItem(string))
        self.timeline.setSortingEnabled(sortingEnabled)

    # 시스템 On/Off
    def timeline_data1_5(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT event_id, computer, time_created FROM event_log WHERE ((event_id = '12' OR event_id = '13') AND " \
                "(time_created >= '" + self.datetime1 + "' AND time_created <= '" + self.datetime2 + "'))"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()

        accum = self.timeline_count
        self.timeline_count = accum + len(rows)
        self.timeline.setRowCount(self.timeline_count)

        sortingEnabled = self.timeline.isSortingEnabled()
        self.timeline.setSortingEnabled(False)

        for i in range(len(rows)):
            event_id, computer, time_created = rows[i]
            self.timeline.setItem(i + accum, 0, QTableWidgetItem(time_created))
            if event_id == 12:
                self.timeline.setItem(i + accum, 1, QTableWidgetItem("시스템 On"))
            elif event_id == 13:
                self.timeline.setItem(i + accum, 1, QTableWidgetItem("시스템 Off"))
            self.timeline.setItem(i + accum, 2, QTableWidgetItem(computer))
        self.timeline.setSortingEnabled(sortingEnabled)

    # 문서 생성 및 수정
    def timeline_date2_1(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()

        query_1 = "SELECT file_name, local_base_path, target_creation_time From jumplist " \
                " WHERE ((file_name LIKE '%.pdf' OR file_name LIKE '%.hwp' OR file_name LIKE '%.docx' OR file_name LIKE '%.doc' " \
                " OR file_name LIKE '%.xlsx' OR file_name LIKE '%.csv' OR file_name LIKE '%.pptx' OR file_name LIKE '%.ppt' " \
                " OR file_name LIKE '%.txt') " \
                " AND (target_creation_time >= '" + self.datetime1 + "' AND target_creation_time <= '" + self.datetime2 + "'))"
        cur.execute(query_1)
        rows = cur.fetchall()

        accum = self.timeline_count
        self.timeline_count = accum + (len(rows))
        self.timeline.setRowCount(self.timeline_count)

        sortingEnabled = self.timeline.isSortingEnabled()
        self.timeline.setSortingEnabled(False)

        for i in range(len(rows)):
            file_name, local_base_path, target_creation_time = rows[i]
            self.timeline.setItem(accum + i, 0, QTableWidgetItem(target_creation_time))
            self.timeline.setItem(accum + i, 1, QTableWidgetItem("문서 생성"))
            self.timeline.setItem(accum + i, 2, QTableWidgetItem(file_name))
            self.timeline.setItem(accum + i, 3, QTableWidgetItem(local_base_path))

        self.timeline.setSortingEnabled(sortingEnabled)

        query_2 = "SELECT file_name, local_base_path, target_modified_time From jumplist " \
                " WHERE ((file_name LIKE '%.pdf' OR file_name LIKE '%.hwp' OR file_name LIKE '%.docx' OR file_name LIKE '%.doc' " \
                " OR file_name LIKE '%.xlsx' OR file_name LIKE '%.csv' OR file_name LIKE '%.pptx' OR file_name LIKE '%.ppt' " \
                " OR file_name LIKE '%.txt')" \
                " AND (target_modified_time >= '" + self.datetime1 + "' AND target_modified_time <= '" + self.datetime2 + "'))"
        cur.execute(query_2)
        rows = cur.fetchall()

        accum = self.timeline_count
        self.timeline_count = accum + (len(rows))
        self.timeline.setRowCount(self.timeline_count)

        sortingEnabled = self.timeline.isSortingEnabled()
        self.timeline.setSortingEnabled(False)

        for i in range(len(rows)):
            file_name, local_base_path, target_modified_time = rows[i]
            self.timeline.setItem(accum + i, 0, QTableWidgetItem(target_modified_time))
            self.timeline.setItem(accum + i, 1, QTableWidgetItem("문서 수정"))
            self.timeline.setItem(accum + i, 2, QTableWidgetItem(file_name))
            self.timeline.setItem(accum + i, 3, QTableWidgetItem(local_base_path))
        self.timeline.setSortingEnabled(sortingEnabled)

        query_3 = "SELECT file_name, local_base_path, target_accessed_time From jumplist " \
                " WHERE ((file_name LIKE '%.pdf' OR file_name LIKE '%.hwp' OR file_name LIKE '%.docx' OR file_name LIKE '%.doc' " \
                " OR file_name LIKE '%.xlsx' OR file_name LIKE '%.csv' OR file_name LIKE '%.pptx' OR file_name LIKE '%.ppt' " \
                " OR file_name LIKE '%.txt')" \
                " AND (target_accessed_time >= '" + self.datetime1 + "' AND target_accessed_time <= '" + self.datetime2 + "'))"
        cur.execute(query_3)
        rows = cur.fetchall()

        accum = self.timeline_count
        self.timeline_count = accum + (len(rows))
        self.timeline.setRowCount(self.timeline_count)

        sortingEnabled = self.timeline.isSortingEnabled()
        self.timeline.setSortingEnabled(False)

        for i in range(len(rows)):
            file_name, local_base_path, target_accessed_time = rows[i]
            self.timeline.setItem(accum + i, 0, QTableWidgetItem(target_accessed_time))
            self.timeline.setItem(accum + i, 1, QTableWidgetItem("문서 접근"))
            self.timeline.setItem(accum + i, 2, QTableWidgetItem(file_name))
            self.timeline.setItem(accum + i, 3, QTableWidgetItem(local_base_path))
        self.timeline.setSortingEnabled(sortingEnabled)

    # 안티포렌식 도구 실행
    def timeline_data2_2(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT Executable_Name, Full_Path, Last_Executed1 from prefetch1 " \
                " WHERE ((Executable_Name LIKE '%CCleaner%' OR Executable_Name LIKE 'Cipher%' " \
                " OR Executable_Name LIKE 'Eraser%' OR Executable_Name LIKE 'SDelete%' " \
                " OR Executable_Name LIKE 'SetMACE%' OR Executable_Name LIKE 'TimeStomp%'  " \
                " OR Executable_Name LIKE 'Wise Folder Hider%') " \
                " AND (Last_Executed1 >= '" + self.datetime1 + "' AND Last_Executed1 <= '" + self.datetime2 + "'))"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()
        accum = self.timeline_count
        self.timeline_count = accum + len(rows)
        self.timeline.setRowCount(self.timeline_count)

        sortingEnabled = self.timeline.isSortingEnabled()
        self.timeline.setSortingEnabled(False)

        for i in range(len(rows)):
            Executable_Name, Full_Path, Last_Executed1 = rows[i]
            self.timeline.setItem(i + accum, 0, QTableWidgetItem(Last_Executed1))
            self.timeline.setItem(i + accum, 1, QTableWidgetItem("안티포렌식 도구 실행"))
            self.timeline.setItem(i + accum, 2, QTableWidgetItem(Executable_Name))
            self.timeline.setItem(i + accum, 3, QTableWidgetItem(Full_Path))
        self.timeline.setSortingEnabled(sortingEnabled)
        self.set_color()

    # 클라우드 접근
    def timeline_data2_3(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT timestamp, Title, URL FROM cloud " \
                " WHERE (timestamp >= '" + self.datetime1 + "' AND timestamp <= '" + self.datetime2 + "')"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()
        accum = self.timeline_count
        self.timeline_count = accum + len(rows)
        self.timeline.setRowCount(self.timeline_count)

        sortingEnabled = self.timeline.isSortingEnabled()
        self.timeline.setSortingEnabled(False)

        for i in range(len(rows)):
            timestamp, Title, URL = rows[i]
            self.timeline.setItem(i + accum, 0, QTableWidgetItem(timestamp))
            self.timeline.setItem(i + accum, 1, QTableWidgetItem("클라우드 접근"))
            self.timeline.setItem(i + accum, 2, QTableWidgetItem(Title))
            self.timeline.setItem(i + accum, 3, QTableWidgetItem(URL))
        self.timeline.setSortingEnabled(sortingEnabled)
        self.set_color()

    # 저장장치 연결 및 해제
    def timeline_data2_4(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT detailed, time_created, bus_type, drive_manufac, drive_model FROM event_log WHERE ((event_id = '1006')" \
                " AND (time_created >= '" + self.datetime1 + "' AND time_created <= '" + self.datetime2 + "'))"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()
        accum = self.timeline_count
        self.timeline_count = accum + len(rows)
        self.timeline.setRowCount(self.timeline_count)

        sortingEnabled = self.timeline.isSortingEnabled()
        self.timeline.setSortingEnabled(False)

        for i in range(len(rows)):
            detailed, time_created, bus_type, drive_manufac, drive_model = rows[i]
            self.timeline.setItem(i + accum, 0, QTableWidgetItem(time_created))
            if "released" in detailed:
                self.timeline.setItem(i + accum, 1, QTableWidgetItem("USB 연결 해제"))
            else:
                self.timeline.setItem(i + accum, 1, QTableWidgetItem("USB 연결"))
            if drive_model == "NULL":
                string = "타입: " + bus_type + ", 모델명: " + drive_model
            else:
                string = "타입: " + bus_type + ", 제조사: " + drive_manufac + ", 모델명: " + drive_model
            self.timeline.setItem(i + accum, 2, QTableWidgetItem(string))
        self.timeline.setSortingEnabled(sortingEnabled)

    # 이벤트로그 삭제
    def timeline_data2_5(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT event_id, detailed, computer, time_created, sbt_usr_name, channel FROM event_log " \
                " WHERE ((event_id = '104' or event_id = '1102' AND sbt_usr_name IS NOT '' )" \
                " AND (time_created >= '" + self.datetime1 + "' AND time_created <= '" + self.datetime2 + "'))"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()
        accum = self.timeline_count
        self.timeline_count = accum + len(rows)
        self.timeline.setRowCount(self.timeline_count)

        sortingEnabled = self.timeline.isSortingEnabled()
        self.timeline.setSortingEnabled(False)

        for i in range(len(rows)):
            event_id, detailed, computer, time_created, sbt_usr_name, channel = rows[i]
            self.timeline.setItem(i + accum, 0, QTableWidgetItem(time_created))
            self.timeline.setItem(i + accum, 1, QTableWidgetItem("이벤트로그 삭제"))
            string = "detailed: " + detailed + ", computer: " + computer + ", user name: " + sbt_usr_name + ", channel: " + channel
            self.timeline.setItem(i + accum, 2, QTableWidgetItem(string))
        self.timeline.setSortingEnabled(sortingEnabled)
        self.set_color()

    def set_color(self):
        for i in range(self.timeline_count):
            for i in range(self.timeline_count):
                if self.timeline.item(i, 1).text() == "안티포렌식 도구 실행":
                    self.timeline.item(i, 1).setBackground(QtGui.QColor(255, 51, 51))
                elif self.timeline.item(i, 1).text()=="클라우드 접근":
                    self.timeline.item(i, 1).setBackground(QtGui.QColor(255, 255, 102))
                elif self.timeline.item(i, 1).text() == "이벤트로그 삭제":
                    self.timeline.itme(i, 1).setBackground(QtGui.QColor(51, 102, 225))

#################################################
#   tab4                                        #
#################################################
    # tab4 구성
    def set_tab4(self):
        self.tab4.layout = QHBoxLayout(self)
        self.set_tab4_tree()

        # item1_1 시스템 정보
        self.PC_system_table = QTableWidget(self)
        self.set_PC_system()
        self.tab4.layout.addWidget(self.PC_system_table)
        self.tab4.layout.itemAt(1).widget().setParent(None)
        # item1_2_1 계정정보 - 레지스트리
        self.PC_user_reg_table = QTableWidget(self)
        self.set_PC_user_reg()
        self.tab4.layout.addWidget(self.PC_user_reg_table)
        self.tab4.layout.itemAt(1).widget().setParent(None)
        # item1_2_2 계정정보 - 이벤트로그
        self.PC_user_evt_table = QTableWidget(self)
        self.set_PC_user_evt()
        self.tab4.layout.addWidget(self.PC_user_evt_table)
        self.tab4.layout.itemAt(1).widget().setParent(None)
        # item1_3 윈도우 업데이트
        self.PC_update_table = QTableWidget(self)
        self.set_PC_update()
        self.tab4.layout.addWidget(self.PC_update_table)
        self.tab4.layout.itemAt(1).widget().setParent(None)

        # item2_2 네트워크 - 이벤트로그
        self.network_evt_table = QTableWidget(self)
        self.set_network_evt()
        self.tab4.layout.addWidget(self.network_evt_table)
        self.tab4.layout.itemAt(1).widget().setParent(None)

        # item3_1 외부저장장치 - 레지스트리
        self.storage_reg_table = QTableWidget(self)
        self.set_storage_reg()
        self.tab4.layout.addWidget(self.storage_reg_table)
        self.tab4.layout.itemAt(1).widget().setParent(None)
        # item3_2 외부저장장치 - 이벤트로그
        self.storage_evt_table = QTableWidget(self)
        self.set_storage_evt()
        self.tab4.layout.addWidget(self.storage_evt_table)
        self.tab4.layout.itemAt(1).widget().setParent(None)

        # item4_1 검색 기록
        self.browser_search_table = QTableWidget(self)
        self.set_browser_search()
        self.tab4.layout.addWidget(self.browser_search_table)
        self.tab4.layout.itemAt(1).widget().setParent(None)
        # item4_2 다운로드 기록
        self.browser_dowload_table = QTableWidget(self)
        self.set_browser_download()
        self.tab4.layout.addWidget(self.browser_dowload_table)
        self.tab4.layout.itemAt(1).widget().setParent(None)
        # item4_3 URL 히스토리
        self.browser_url_table = QTableWidget(self)
        self.set_browser_url()
        self.tab4.layout.addWidget(self.browser_url_table)
        self.tab4.layout.itemAt(1).widget().setParent(None)
        # item4_4 로그인 기록
        self.browser_login_table = QTableWidget(self)
        self.set_browser_login()
        self.tab4.layout.addWidget(self.browser_login_table)
        self.tab4.layout.itemAt(1).widget().setParent(None)
        # item4_5 쿠키
        self.browser_cookies_table = QTableWidget(self)
        self.set_browser_cookies()
        self.tab4.layout.addWidget(self.browser_cookies_table)
        self.tab4.layout.itemAt(1).widget().setParent(None)
        # item4_6 캐시
        self.browser_cache_table = QTableWidget(self)
        self.set_browser_cache()
        self.tab4.layout.addWidget(self.browser_cache_table)
        self.tab4.layout.itemAt(1).widget().setParent(None)
        # item4_7 북마크
        self.browser_bookmark_table = QTableWidget(self)
        self.set_browser_bookmark()
        self.tab4.layout.addWidget(self.browser_bookmark_table)
        self.tab4.layout.itemAt(1).widget().setParent(None)
        # item4_8 자동완성
        self.browser_autofill_table = QTableWidget(self)
        self.set_browser_autofill()
        self.tab4.layout.addWidget(self.browser_autofill_table)
        self.tab4.layout.itemAt(1).widget().setParent(None)
        # item4_9 환경설정
        self.browser_preference_table = QTableWidget(self)
        self.set_browser_preference()
        self.tab4.layout.addWidget(self.browser_preference_table)
        self.tab4.layout.itemAt(1).widget().setParent(None)
        # item4_10 클라우드 접속기록
        self.browser_cloud_table = QTableWidget(self)
        self.set_browser_cloud()
        self.tab4.layout.addWidget(self.browser_cloud_table)
        self.tab4.layout.itemAt(1).widget().setParent(None)

        # item5_1_1 프로그램 실행 흔적 - 레지스트리 - BAM
        self.program_bam = QTableWidget(self)
        self.set_program_bam()
        self.tab4.layout.addWidget(self.program_bam)
        self.tab4.layout.itemAt(1).widget().setParent(None)
        # item5_1_2 프로그램 실행 흔적 - 레지스트리 - UserAssist
        self.program_userassist = QTableWidget(self)
        self.set_program_userassist()
        self.tab4.layout.addWidget(self.program_userassist)
        self.tab4.layout.itemAt(1).widget().setParent(None)
        # item5_1_3 프로그램 실행 흔적 - 레지스트리 - Uninstall
        self.program_uninstall = QTableWidget(self)
        self.set_program_uninstall()
        self.tab4.layout.addWidget(self.program_uninstall)
        self.tab4.layout.itemAt(1).widget().setParent(None)
        # item5_1_4 프로그램 실행 흔적 - 레지스트리 - MuiCache
        self.program_muicache = QTableWidget(self)
        self.set_program_muicache()
        self.tab4.layout.addWidget(self.program_muicache)
        self.tab4.layout.itemAt(1).widget().setParent(None)
        # item5_1_5 프로그램 실행 흔적 - 레지스트리 - FirstFolder
        self.program_firstfolder = QTableWidget(self)
        self.set_program_firstfolder()
        self.tab4.layout.addWidget(self.program_firstfolder)
        self.tab4.layout.itemAt(1).widget().setParent(None)
        # item5_1_5 프로그램 실행 흔적 - 레지스트리 - CIDSizeMRU
        self.program_cidsizemru = QTableWidget(self)
        self.set_program_cidsizemru()
        self.tab4.layout.addWidget(self.program_cidsizemru)
        self.tab4.layout.itemAt(1).widget().setParent(None)
        # item5_2 프로그램 실행 흔적 - 프리패치
        self.program_pre = QTableWidget(self)
        self.set_program_pre()
        self.tab4.layout.addWidget(self.program_pre)
        self.tab4.layout.itemAt(1).widget().setParent(None)

        # item6_1 문서실행 흔적 - 레지스트리
        self.doc_reg_table = QTableWidget(self)
        self.set_doc_reg()
        self.tab4.layout.addWidget(self.doc_reg_table)
        self.tab4.layout.itemAt(1).widget().setParent(None)
        # item6_2 문서실행 흔적 - 링크 파일
        self.doc_lnk_table = QTableWidget(self)
        self.set_doc_lnk()
        self.tab4.layout.addWidget(self.doc_lnk_table)
        self.tab4.layout.itemAt(1).widget().setParent(None)
        # item6_3 문서실행 흔적 - 점프목록
        self.doc_jmp_table = QTableWidget(self)
        self.set_doc_jmp()
        self.tab4.layout.addWidget(self.doc_jmp_table)
        self.tab4.layout.itemAt(1).widget().setParent(None)
        # item6_4 문서실행 흔적 - 프리패치
        self.doc_pre_table = QTableWidget(self)
        self.set_doc_pre()
        self.tab4.layout.addWidget(self.doc_pre_table)
        self.tab4.layout.itemAt(1).widget().setParent(None)

        # item7_1 기타실행 흔적 - 링크 파일
        self.etc_lnk_table = QTableWidget(self)
        self.set_etc_lnk()
        self.tab4.layout.addWidget(self.etc_lnk_table)
        self.tab4.layout.itemAt(1).widget().setParent(None)
        # item7_2 기타실행 흔적 - 프리패치
        self.etc_pre_table = QTableWidget(self)
        self.set_etc_pre()
        self.tab4.layout.addWidget(self.etc_pre_table)
        self.tab4.layout.itemAt(1).widget().setParent(None)
        # item7_3 기타실행 흔적 - 대화상자
        self.etc_dialog_table = QTableWidget(self)
        self.set_etc_dialog()
        self.tab4.layout.addWidget(self.etc_dialog_table)
        self.tab4.layout.itemAt(1).widget().setParent(None)

        # item8_1 이벤트 로그 삭제
        self.eventlog_delete_table = QTableWidget(self)
        self.set_eventlog_delete()
        self.tab4.layout.addWidget(self.eventlog_delete_table)
        self.tab4.layout.itemAt(1).widget().setParent(None)
        # item8_2 프로세스 강제 종료
        self.eventlog_terminate_table = QTableWidget(self)
        self.set_eventlog_terminate()
        self.tab4.layout.addWidget(self.eventlog_terminate_table)
        self.tab4.layout.itemAt(1).widget().setParent(None)
        # item8_3_1 PC 전원 기록 - 운영체제 시작 및 종료
        self.eventlog_onoff_table = QTableWidget(self)
        self.set_eventlog_onoff()
        self.tab4.layout.addWidget(self.eventlog_onoff_table)
        self.tab4.layout.itemAt(1).widget().setParent(None)
        # item8_3_2 PC 전원 기록 - 절전모드 전환 및 해제
        self.eventlog_powersaving_table = QTableWidget(self)
        self.set_eventlog_powersaving()
        self.tab4.layout.addWidget(self.eventlog_powersaving_table)
        self.tab4.layout.itemAt(1).widget().setParent(None)
        # item8_4_1 원격 - 원격 접속 기록
        self.eventlog_access1_table = QTableWidget(self)
        self.set_eventlog_access1()
        self.tab4.layout.addWidget(self.eventlog_access1_table)
        self.tab4.layout.itemAt(1).widget().setParent(None)
        # item8_4_2 원격 - 원격 실행 기록
        self.eventlog_access2_table = QTableWidget(self)
        self.set_eventlog_access2()
        self.tab4.layout.addWidget(self.eventlog_access2_table)
        self.tab4.layout.itemAt(1).widget().setParent(None)
        # item8_5 시스템 시간 변경 기록
        self.eventlog_time_table = QTableWidget(self)
        self.set_eventlog_time()
        self.tab4.layout.addWidget(self.eventlog_time_table)
        self.tab4.layout.itemAt(1).widget().setParent(None)

        # item9 폴더 열람 흔적
        self.folder_table = QTableWidget(self)
        self.set_folder()
        self.tab4.layout.addWidget(self.folder_table)
        self.tab4.layout.itemAt(1).widget().setParent(None)

        self.tab4_table = QTableWidget(self)
        self.tab4.layout.addWidget(self.tab4_table)
        self.tab4.setLayout(self.tab4.layout)

    # tab4의 tree 구성
    def set_tab4_tree(self):
        self.tree = QTreeWidget()
        self.tree.header().setVisible(False)
        self.tree.setFixedWidth(300)

        self.item1 = QTreeWidgetItem(self.tree)
        self.item1.setText(0, "PC 정보")
        self.item1_1 = QTreeWidgetItem(self.item1)
        self.item1_1.setText(0, "시스템 정보")
        self.item1_2 = QTreeWidgetItem(self.item1)
        self.item1_2.setText(0, "계정 정보")
        self.item1_2_1 = QTreeWidgetItem(self.item1_2)
        self.item1_2_1.setText(0, "레지스트리")
        self.item1_2_2 = QTreeWidgetItem(self.item1_2)
        self.item1_2_2.setText(0, "이벤트로그")
        self.item1_3 = QTreeWidgetItem(self.item1)
        self.item1_3.setText(0, "윈도우 업데이트")

        self.item2 = QTreeWidgetItem(self.tree)
        self.item2.setText(0, "네트워크")
        # self.item2_1 = QTreeWidgetItem(self.item2)
        # self.item2_1.setText(0, "레지스트리")
        self.item2_2 = QTreeWidgetItem(self.item2)
        self.item2_2.setText(0, "이벤트로그")

        self.item3 = QTreeWidgetItem(self.tree)
        self.item3.setText(0, "외부저장장치")
        self.item3_1 = QTreeWidgetItem(self.item3)
        self.item3_1.setText(0, "레지스트리")
        self.item3_2 = QTreeWidgetItem(self.item3)
        self.item3_2.setText(0, "이벤트로그")

        self.item4 = QTreeWidgetItem(self.tree)
        self.item4.setText(0, "브라우저")
        self.item4_1 = QTreeWidgetItem(self.item4)
        self.item4_1.setText(0, "검색 기록")
        self.item4_2 = QTreeWidgetItem(self.item4)
        self.item4_2.setText(0, "다운로드 기록")
        self.item4_3 = QTreeWidgetItem(self.item4)
        self.item4_3.setText(0, "URL 히스토리")
        self.item4_4 = QTreeWidgetItem(self.item4)
        self.item4_4.setText(0, "로그인 기록")
        self.item4_5 = QTreeWidgetItem(self.item4)
        self.item4_5.setText(0, "쿠키")
        self.item4_6 = QTreeWidgetItem(self.item4)
        self.item4_6.setText(0, "캐시")
        self.item4_7 = QTreeWidgetItem(self.item4)
        self.item4_7.setText(0, "북마크")
        self.item4_8 = QTreeWidgetItem(self.item4)
        self.item4_8.setText(0, "자동완성")
        self.item4_9 = QTreeWidgetItem(self.item4)
        self.item4_9.setText(0, "환경설정")
        self.item4_10 = QTreeWidgetItem(self.item4)
        self.item4_10.setText(0, "클라우드 접속기록")

        self.item5 = QTreeWidgetItem(self.tree)
        self.item5.setText(0, "프로그램 실행 흔적")
        self.item5_1 = QTreeWidgetItem(self.item5)
        self.item5_1.setText(0, "레지스트리")
        self.item5_1_1 = QTreeWidgetItem(self.item5_1)
        self.item5_1_1.setText(0, "BAM")
        self.item5_1_2 = QTreeWidgetItem(self.item5_1)
        self.item5_1_2.setText(0, "UserAssist")
        self.item5_1_3 = QTreeWidgetItem(self.item5_1)
        self.item5_1_3.setText(0, "Uninstall")
        self.item5_1_4 = QTreeWidgetItem(self.item5_1)
        self.item5_1_4.setText(0, "MuiCache")
        self.item5_1_5 = QTreeWidgetItem(self.item5_1)
        self.item5_1_5.setText(0, "FirstFolder")
        self.item5_1_6 = QTreeWidgetItem(self.item5_1)
        self.item5_1_6.setText(0, "CIDSizeMRU")
        self.item5_2 = QTreeWidgetItem(self.item5)
        self.item5_2.setText(0, "프리패치")

        self.item6 = QTreeWidgetItem(self.tree)
        self.item6.setText(0, "문서실행 흔적")
        self.item6_1 = QTreeWidgetItem(self.item6)
        self.item6_1.setText(0, "레지스트리")
        self.item6_2 = QTreeWidgetItem(self.item6)
        self.item6_2.setText(0, "링크 파일")
        self.item6_3 = QTreeWidgetItem(self.item6)
        self.item6_3.setText(0, "점프 목록")
        self.item6_4 = QTreeWidgetItem(self.item6)
        self.item6_4.setText(0, "프리패치")

        self.item7 = QTreeWidgetItem(self.tree)
        self.item7.setText(0, "기타실행 흔적")
        self.item7_1 = QTreeWidgetItem(self.item7)
        self.item7_1.setText(0, "링크 파일")
        self.item7_2 = QTreeWidgetItem(self.item7)
        self.item7_2.setText(0, "프리패치")
        self.item7_3 = QTreeWidgetItem(self.item7)
        self.item7_3.setText(0, "대화상자")

        self.item8 = QTreeWidgetItem(self.tree)
        self.item8.setText(0, "이벤트 로그")
        self.item8_1 = QTreeWidgetItem(self.item8)
        self.item8_1.setText(0, "이벤트 로그 삭제")
        self.item8_2 = QTreeWidgetItem(self.item8)
        self.item8_2.setText(0, "프로세스 강제 종료")
        self.item8_3 = QTreeWidgetItem(self.item8)
        self.item8_3.setText(0, "PC 전원 기록")
        self.item8_3_1 = QTreeWidgetItem(self.item8_3)
        self.item8_3_1.setText(0, "운영체제 시작 및 종료")
        self.item8_3_2 = QTreeWidgetItem(self.item8_3)
        self.item8_3_2.setText(0, "절전모드 전환 및 해제")
        self.item8_4 = QTreeWidgetItem(self.item8)
        self.item8_4.setText(0, "원격")
        self.item8_4_1 = QTreeWidgetItem(self.item8_4)
        self.item8_4_1.setText(0, "원격 접속 기록")
        self.item8_4_2 = QTreeWidgetItem(self.item8_4)
        self.item8_4_2.setText(0, "원격 실행 기록")
        self.item8_5 = QTreeWidgetItem(self.item8)
        self.item8_5.setText(0, "시스템 시간 변경 기록")

        self.item9 = QTreeWidgetItem(self.tree)
        self.item9.setText(0, "폴더 열람 흔적")

        self.tab4.layout.addWidget(self.tree)
        self.tree.itemClicked.connect(self.tab4_onItemClicked)

    # tab4의 tree의 item을 클릭할 시 현재 테이블을 레이아웃에서 없애고 item에 해당하는 테이블을 추가
    def tab4_onItemClicked(self, it, col):
        delete = self.tab4.layout.itemAt(1).widget()

        if it is self.item1_1:
            delete.setParent(None)
            self.tab4.layout.addWidget(self.PC_system_table)
        if it is self.item1_2_1:
            delete.setParent(None)
            self.tab4.layout.addWidget(self.PC_user_reg_table)
        if it is self.item1_2_2:
            delete.setParent(None)
            self.tab4.layout.addWidget(self.PC_user_evt_table)
        if it is self.item1_3:
            delete.setParent(None)
            self.tab4.layout.addWidget(self.PC_update_table)
        if it is self.item2_2:
            delete.setParent(None)
            self.tab4.layout.addWidget(self.network_evt_table)
        if it is self.item3_1:
            delete.setParent(None)
            self.tab4.layout.addWidget(self.storage_reg_table)
        if it is self.item3_2:
            delete.setParent(None)
            self.tab4.layout.addWidget(self.storage_evt_table)
        if it is self.item4_1:
            delete.setParent(None)
            self.tab4.layout.addWidget(self.browser_search_table)
        if it is self.item4_2:
            delete.setParent(None)
            self.tab4.layout.addWidget(self.browser_dowload_table)
        if it is self.item4_3:
            delete.setParent(None)
            self.tab4.layout.addWidget(self.browser_url_table)
        if it is self.item4_4:
            delete.setParent(None)
            self.tab4.layout.addWidget(self.browser_login_table)
        if it is self.item4_5:
            delete.setParent(None)
            self.tab4.layout.addWidget(self.browser_cookies_table)
        if it is self.item4_6:
            delete.setParent(None)
            self.tab4.layout.addWidget(self.browser_cache_table)
        if it is self.item4_7:
            delete.setParent(None)
            self.tab4.layout.addWidget(self.browser_bookmark_table)
        if it is self.item4_8:
            delete.setParent(None)
            self.tab4.layout.addWidget(self.browser_autofill_table)
        if it is self.item4_9:
            delete.setParent(None)
            self.tab4.layout.addWidget(self.browser_preference_table)
        if it is self.item4_10:
            delete.setParent(None)
            self.tab4.layout.addWidget(self.browser_cloud_table)
        if it is self.item5_1_1:
            delete.setParent(None)
            self.tab4.layout.addWidget(self.program_bam)
        if it is self.item5_1_2:
            delete.setParent(None)
            self.tab4.layout.addWidget(self.program_userassist)
        if it is self.item5_1_3:
            delete.setParent(None)
            self.tab4.layout.addWidget(self.program_uninstall)
        if it is self.item5_1_4:
            delete.setParent(None)
            self.tab4.layout.addWidget(self.program_muicache)
        if it is self.item5_1_5:
            delete.setParent(None)
            self.tab4.layout.addWidget(self.program_firstfolder)
        if it is self.item5_1_6:
            delete.setParent(None)
            self.tab4.layout.addWidget(self.program_cidsizemru)
        if it is self.item5_2:
            delete.setParent(None)
            self.tab4.layout.addWidget(self.program_pre)
        if it is self.item6_1:
            delete.setParent(None)
            self.tab4.layout.addWidget(self.doc_reg_table)
        if it is self.item6_2:
            delete.setParent(None)
            self.tab4.layout.addWidget(self.doc_lnk_table)
        if it is self.item6_3:
            delete.setParent(None)
            self.tab4.layout.addWidget(self.doc_jmp_table)
        if it is self.item6_4:
            delete.setParent(None)
            self.tab4.layout.addWidget(self.doc_pre_table)
        if it is self.item7_1:
            delete.setParent(None)
            self.tab4.layout.addWidget(self.etc_lnk_table)
        if it is self.item7_2:
            delete.setParent(None)
            self.tab4.layout.addWidget(self.etc_pre_table)
        if it is self.item7_3:
            delete.setParent(None)
            self.tab4.layout.addWidget(self.etc_dialog_table)
        if it is self.item8_1:
            delete.setParent(None)
            self.tab4.layout.addWidget(self.eventlog_delete_table)
        if it is self.item8_2:
            delete.setParent(None)
            self.tab4.layout.addWidget(self.eventlog_terminate_table)
        if it is self.item8_3_1:
            delete.setParent(None)
            self.tab4.layout.addWidget(self.eventlog_onoff_table)
        if it is self.item8_3_2:
            delete.setParent(None)
            self.tab4.layout.addWidget(self.eventlog_powersaving_table)
        if it is self.item8_4_1:
            delete.setParent(None)
            self.tab4.layout.addWidget(self.eventlog_access1_table)
        if it is self.item8_4_2:
            delete.setParent(None)
            self.tab4.layout.addWidget(self.eventlog_access2_table)
        if it is self.item8_5:
            delete.setParent(None)
            self.tab4.layout.addWidget(self.eventlog_time_table)
        if it is self.item9:
            delete.setParent(None)
            self.tab4.layout.addWidget(self.folder_table)

#################################################
#   tab4의 테이블 구성                            #
#################################################
    # item1_1 시스템 정보
    def set_PC_system(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT product_name, product_ID, system_root, owner, organization, build_lab, " \
                "timezone_name, active_time_bias, UTC, computer_name, default_user_name, last_used_user_name, " \
                "datetime(shutdown_time, '+9 hours'), datetime(install_date, '+9 hours') FROM OSInformation"
        cur.execute(query)
        rows = cur.fetchall()[0]
        conn.close()

        count = len(rows)
        self.PC_system_table.setRowCount(count)
        self.PC_system_table.setColumnCount(1)
        row_headers = ["제품명", "제품 ID", "시스템 루트", "사용자", "설치 시간",
                       "제조사", "버전", "타임존", "time_bias", "UTC",
                       "컴퓨터 이름", "기본 사용자", "마지막 사용자", "종료 시간"]
        self.PC_system_table.setVerticalHeaderLabels(row_headers)
        self.PC_system_table.horizontalHeader().setVisible(False)

        product_name, product_ID, system_root, owner, organization, build_lab, \
        timezone_name, active_time_bias, UTC, computer_name, default_user_name, last_used_user_name, \
        shutdown_time, install_date = rows
        self.PC_system_table.setItem(0, 0, QTableWidgetItem(product_name))
        self.PC_system_table.setItem(1, 0, QTableWidgetItem(product_ID))
        self.PC_system_table.setItem(2, 0, QTableWidgetItem(system_root))
        self.PC_system_table.setItem(3, 0, QTableWidgetItem(owner))
        self.PC_system_table.setItem(4, 0, QTableWidgetItem(install_date))
        self.PC_system_table.setItem(5, 0, QTableWidgetItem(organization))
        self.PC_system_table.setItem(6, 0, QTableWidgetItem(build_lab))
        self.PC_system_table.setItem(7, 0, QTableWidgetItem(timezone_name))
        self.PC_system_table.setItem(8, 0, QTableWidgetItem(str(active_time_bias)))
        self.PC_system_table.setItem(9, 0, QTableWidgetItem(str(UTC)))
        self.PC_system_table.setItem(10, 0, QTableWidgetItem(computer_name))
        self.PC_system_table.setItem(11, 0, QTableWidgetItem(default_user_name))
        self.PC_system_table.setItem(12, 0, QTableWidgetItem(last_used_user_name))
        self.PC_system_table.setItem(13, 0, QTableWidgetItem(shutdown_time))

        self.PC_system_table.resizeColumnsToContents()

    # item1_2_1 계정정보 - 레지스트리
    def set_PC_user_reg(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT RID_int, account_name, complete_account_name, logon_failure_count, logon_success_count, comment, homedir, " \
                "datetime(last_login_time, '+9 hours'), datetime(last_password_change_time, '+9 hours'), " \
                "datetime(expires_on, '+9 hours'), datetime(last_incorrect_password_time, '+9 hours'), " \
                "datetime(created_on, '+9 hours') FROM UserAccounts"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()

        count = len(rows)
        self.PC_user_reg_table.setRowCount(count)
        self.PC_user_reg_table.setColumnCount(12)
        column_headers = ["RID", "계정 생성 시간", "계정명", "전체 계정명", "로그인 실패 횟수", "로그인 성공 횟수", "설명", "홈 디렉토리",
                          "마지막 로그인", "마지막 패스워드 변경",
                          "만료", "마지막 패스워드 불일치"]
        self.PC_user_reg_table.setHorizontalHeaderLabels(column_headers)

        for i in range(count):
            RID_int, account_name, complete_account_name, logon_failure_count, logon_success_count, comment, homedir, \
            last_login_time, last_password_change_time, expires_on, last_incorrect_password_time, created_on = rows[
                i]
            self.PC_user_reg_table.setItem(i, 0, QTableWidgetItem(str(RID_int)))
            self.PC_user_reg_table.setItem(i, 1, QTableWidgetItem(created_on))
            self.PC_user_reg_table.setItem(i, 2, QTableWidgetItem(account_name))
            self.PC_user_reg_table.setItem(i, 3, QTableWidgetItem(complete_account_name))
            self.PC_user_reg_table.setItem(i, 4, QTableWidgetItem(str(logon_failure_count)))
            self.PC_user_reg_table.setItem(i, 5, QTableWidgetItem(str(logon_success_count)))
            self.PC_user_reg_table.setItem(i, 6, QTableWidgetItem(comment))
            self.PC_user_reg_table.setItem(i, 7, QTableWidgetItem(homedir))
            self.PC_user_reg_table.setItem(i, 8, QTableWidgetItem(last_login_time))
            self.PC_user_reg_table.setItem(i, 9, QTableWidgetItem(last_password_change_time))
            self.PC_user_reg_table.setItem(i, 10, QTableWidgetItem(expires_on))
            self.PC_user_reg_table.setItem(i, 11, QTableWidgetItem(last_incorrect_password_time))

    # item1_2_2 계정정보 - 이벤트로그
    def set_PC_user_evt(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT event_id, detailed, computer, sbt_usr_name, trg_usr_name, display_name, mem_sid, " \
                "datetime(time_created, '+9 hours') FROM event_log " \
                "WHERE (event_id LIKE '1004' OR event_id LIKE '1005' OR event_id LIKE '4624'" \
                "OR event_id LIKE '4625' OR event_id LIKE '4720' OR event_id LIKE '4724' OR event_id LIKE '4726'" \
                "OR event_id LIKE '4732' OR event_id LIKE '4733' OR event_id LIKE '4738')"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()

        count = len(rows)
        self.PC_user_evt_table.setRowCount(count)
        self.PC_user_evt_table.setColumnCount(8)
        column_headers = ["Event_ID", "Detailed", "Time_Created", "Computer", "Sbt_User_Name",
                          "Trg_User_Name", "Display", "Mem_Sid"]
        self.PC_user_evt_table.setHorizontalHeaderLabels(column_headers)

        for i in range(count):
            event_id, detailed, computer, sbt_usr_name, trg_usr_name, display_name, mem_sid, time_created = rows[i]
            self.PC_user_evt_table.setItem(i, 0, QTableWidgetItem(str(event_id)))
            self.PC_user_evt_table.setItem(i, 1, QTableWidgetItem(detailed))
            self.PC_user_evt_table.setItem(i, 2, QTableWidgetItem(time_created))
            self.PC_user_evt_table.setItem(i, 3, QTableWidgetItem(computer))
            self.PC_user_evt_table.setItem(i, 4, QTableWidgetItem(sbt_usr_name))
            self.PC_user_evt_table.setItem(i, 5, QTableWidgetItem(trg_usr_name))
            self.PC_user_evt_table.setItem(i, 6, QTableWidgetItem(display_name))
            self.PC_user_evt_table.setItem(i, 7, QTableWidgetItem(mem_sid))

    # item1_3 윈도우 업데이트
    def set_PC_update(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT detailed, computer, package, datetime(time_created, '+9 hours') " \
                "FROM event_log WHERE event_id LIKE '2'"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()

        count = len(rows)
        self.PC_update_table.setRowCount(count)
        self.PC_update_table.setColumnCount(5)
        column_headers = ["Detailed", "Time_Created", "Computer", "Package", "출처"]
        self.PC_update_table.setHorizontalHeaderLabels(column_headers)

        for i in range(count):
            detailed, computer, package, time_created, = rows[i]
            self.PC_update_table.setItem(i, 0, QTableWidgetItem(detailed))
            self.PC_update_table.setItem(i, 1, QTableWidgetItem(time_created))
            self.PC_update_table.setItem(i, 2, QTableWidgetItem(computer))
            self.PC_update_table.setItem(i, 3, QTableWidgetItem(package))
            self.PC_update_table.setItem(i, 4, QTableWidgetItem("eventlog: id == 2"))

    # item2_2 네트워크 - 이벤트로그
    def set_network_evt(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT event_id, detailed, computer, net_name, guid, conn_mode, reason, datetime(time_created, '+9 hours') " \
                "FROM event_log WHERE (event_id = '10000' AND net_name IS NOT '') OR (event_id = '10001' AND net_name IS NOT '') OR event_id = '8003';"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()

        count = len(rows)
        self.network_evt_table.setRowCount(count)
        self.network_evt_table.setColumnCount(8)
        column_headers = ["이벤트 아이디", "내용", "컴퓨터 이름", "이벤트 생성날짜", "네트워크 이름", "네트워크 GUID", "연결 방식", "해제 이유"]
        self.network_evt_table.setHorizontalHeaderLabels(column_headers)

        for i in range(count):
            event_id, detailed, computer, net_name, guid, conn_mode, reason, time_created = rows[i]
            self.network_evt_table.setItem(i, 0, QTableWidgetItem(str(event_id)))
            self.network_evt_table.setItem(i, 1, QTableWidgetItem(detailed))
            self.network_evt_table.setItem(i, 2, QTableWidgetItem(computer))
            self.network_evt_table.setItem(i, 3, QTableWidgetItem(time_created))
            self.network_evt_table.setItem(i, 4, QTableWidgetItem(net_name))
            self.network_evt_table.setItem(i, 5, QTableWidgetItem(guid))
            self.network_evt_table.setItem(i, 6, QTableWidgetItem(conn_mode))
            self.network_evt_table.setItem(i, 7, QTableWidgetItem(reason))

    # item3_1 외부저장장치 - 레지스트리
    def set_storage_reg(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT GUID, label, vendor_name, product_name, version, serial_num, " \
                "datetime(first_connected, '+9 hours'), datetime(last_connected, '+9 hours') FROM Connected_USB"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()

        count = len(rows)
        self.storage_reg_table.setRowCount(count)
        self.storage_reg_table.setColumnCount(8)
        column_headers = ["GUID", "라벨", "제조사", "제품명", "버전", "시리얼 번호", "최초 연결", "마지막 연결"]
        self.storage_reg_table.setHorizontalHeaderLabels(column_headers)

        for i in range(count):
            GUID, label, vendor_name, product_name, version, serial_num, first_connected, last_connected = rows[i]
            self.storage_reg_table.setItem(i, 0, QTableWidgetItem(GUID))
            self.storage_reg_table.setItem(i, 1, QTableWidgetItem(label))
            self.storage_reg_table.setItem(i, 2, QTableWidgetItem(vendor_name))
            self.storage_reg_table.setItem(i, 3, QTableWidgetItem(product_name))
            self.storage_reg_table.setItem(i, 4, QTableWidgetItem(version))
            self.storage_reg_table.setItem(i, 5, QTableWidgetItem(product_name))
            self.storage_reg_table.setItem(i, 6, QTableWidgetItem(first_connected))
            self.storage_reg_table.setItem(i, 7, QTableWidgetItem(last_connected))

    # item3_2 외부저장장치 - 이벤트로그
    def set_storage_evt(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT event_id, detailed, computer, bus_type, drive_manufac, drive_serial, drive_model," \
                "drive_location, datetime(time_created, '+9 hours') FROM event_log WHERE event_id LIKE '1006'"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()

        count = len(rows)
        self.storage_evt_table.setRowCount(count)
        self.storage_evt_table.setColumnCount(9)
        column_headers = ["이벤트 아이디", "내용", "컴퓨터 이름", "Time_Created", "Bus_Type", "제조사", "시리얼 번호", "Drive_Model",
                          "Drive_Location"]
        self.storage_evt_table.setHorizontalHeaderLabels(column_headers)

        for i in range(count):
            event_id, detailed, computer, bus_type, drive_manufac, drive_serial, drive_model, drive_location, time_created = \
            rows[i]
            self.storage_evt_table.setItem(i, 0, QTableWidgetItem(str(event_id)))
            self.storage_evt_table.setItem(i, 1, QTableWidgetItem(detailed))
            self.storage_evt_table.setItem(i, 2, QTableWidgetItem(computer))
            self.storage_evt_table.setItem(i, 3, QTableWidgetItem(time_created))
            self.storage_evt_table.setItem(i, 4, QTableWidgetItem(bus_type))
            self.storage_evt_table.setItem(i, 5, QTableWidgetItem(drive_manufac))
            self.storage_evt_table.setItem(i, 6, QTableWidgetItem(drive_serial))
            self.storage_evt_table.setItem(i, 7, QTableWidgetItem(drive_model))
            self.storage_evt_table.setItem(i, 8, QTableWidgetItem(drive_location))

    # item4_1 검색 기록
    def set_browser_search(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT type, keyword, datetime(timestamp, '+9 hours') FROM keyword;"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()

        count = len(rows)
        self.browser_search_table.setRowCount(count)
        self.browser_search_table.setColumnCount(3)
        column_headers = ["타입", "시간", "키워드"]
        self.browser_search_table.setHorizontalHeaderLabels(column_headers)

        for i in range(count):
            type, keyword, timestamp = rows[i]
            self.browser_search_table.setItem(i, 0, QTableWidgetItem(type))
            self.browser_search_table.setItem(i, 1, QTableWidgetItem(timestamp))
            self.browser_search_table.setItem(i, 2, QTableWidgetItem(keyword))

        self.browser_search_table.resizeColumnsToContents()

    # item4_2 다운로드 기록
    def set_browser_download(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT type, url, status, path, interrupt_reason, danger_type, opened, etag, " \
                "datetime(timestamp, '+9 hours'), datetime(last_modified, '+9 hours') from download;"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()

        count = len(rows)
        self.browser_dowload_table.setRowCount(count)
        self.browser_dowload_table.setColumnCount(10)
        column_headers = ["타입", "시간", "url", "상태", "경로", "실패 이유", "위험 파일", "opened", "etag", "last_modified"]
        self.browser_dowload_table.setHorizontalHeaderLabels(column_headers)

        for i in range(count):
            type, url, status, path, interrupt_reason, danger_type, opened, etag, \
            timestamp, last_modified = rows[i]
            self.browser_dowload_table.setItem(i, 0, QTableWidgetItem(type))
            self.browser_dowload_table.setItem(i, 1, QTableWidgetItem(timestamp))
            self.browser_dowload_table.setItem(i, 2, QTableWidgetItem(url))
            self.browser_dowload_table.setItem(i, 3, QTableWidgetItem(status))
            self.browser_dowload_table.setItem(i, 4, QTableWidgetItem(path))
            self.browser_dowload_table.setItem(i, 5, QTableWidgetItem(interrupt_reason))
            self.browser_dowload_table.setItem(i, 6, QTableWidgetItem(danger_type))
            self.browser_dowload_table.setItem(i, 7, QTableWidgetItem(opened))
            self.browser_dowload_table.setItem(i, 8, QTableWidgetItem(etag))
            self.browser_dowload_table.setItem(i, 9, QTableWidgetItem(last_modified))

    # item4_3 URL 히스토리
    def set_browser_url(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT url, title, source, visit_duration, visit_count, typed_count, url_hidden, transition, " \
                "datetime(timestamp, '+9 hours') from url;"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()

        count = len(rows)
        self.browser_url_table.setRowCount(count)
        self.browser_url_table.setColumnCount(9)
        column_headers = ["시간", "url", "제목", "source", "머문 시간", "방문 횟수", "검색 횟수", "url hidden", "접근 방식"]
        self.browser_url_table.setHorizontalHeaderLabels(column_headers)

        for i in range(count):
            url, title, source, visit_duration, visit_count, typed_count, url_hidden, transition, timestamp = rows[
                i]
            self.browser_url_table.setItem(i, 0, QTableWidgetItem(timestamp))
            self.browser_url_table.setItem(i, 1, QTableWidgetItem(url))
            self.browser_url_table.setItem(i, 2, QTableWidgetItem(title))
            self.browser_url_table.setItem(i, 3, QTableWidgetItem(source))
            self.browser_url_table.setItem(i, 4, QTableWidgetItem(visit_duration))
            self.browser_url_table.setItem(i, 5, QTableWidgetItem(visit_count))
            self.browser_url_table.setItem(i, 6, QTableWidgetItem(typed_count))
            self.browser_url_table.setItem(i, 7, QTableWidgetItem(url_hidden))
            self.browser_url_table.setItem(i, 8, QTableWidgetItem(transition))

    # item4_4 로그인 기록
    def set_browser_login(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT type, url, name, data, password_element, password_value," \
                "datetime(timestamp, '+9 hours') from login;"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()

        count = len(rows)
        self.browser_login_table.setRowCount(count)
        self.browser_login_table.setColumnCount(7)
        column_headers = ["type", "시간", "로그인 url", "id임을 나타내는 값", "id 또는 계정", "password임을 나타내는 값", "password"]
        self.browser_login_table.setHorizontalHeaderLabels(column_headers)

        for i in range(count):
            type, url, name, data, password_element, password_value, timestamp = rows[i]
            self.browser_login_table.setItem(i, 0, QTableWidgetItem(type))
            self.browser_login_table.setItem(i, 1, QTableWidgetItem(timestamp))
            self.browser_login_table.setItem(i, 2, QTableWidgetItem(url))
            self.browser_login_table.setItem(i, 3, QTableWidgetItem(name))
            self.browser_login_table.setItem(i, 4, QTableWidgetItem(data))
            self.browser_login_table.setItem(i, 5, QTableWidgetItem(password_element))
            self.browser_login_table.setItem(i, 6, QTableWidgetItem(str(password_value)))

    # item4_5 쿠키
    def set_browser_cookies(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT type, url, title, value, datetime(timestamp, '+9 hours') from cookies;"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()

        count = len(rows)
        self.browser_cookies_table.setRowCount(count)
        self.browser_cookies_table.setColumnCount(5)
        column_headers = ["type", "시간", "url", "title", "value"]
        self.browser_cookies_table.setHorizontalHeaderLabels(column_headers)

        for i in range(count):
            type, url, title, value, timestamp = rows[i]
            self.browser_cookies_table.setItem(i, 0, QTableWidgetItem(type))
            self.browser_cookies_table.setItem(i, 1, QTableWidgetItem(timestamp))
            self.browser_cookies_table.setItem(i, 2, QTableWidgetItem(url))
            self.browser_cookies_table.setItem(i, 3, QTableWidgetItem(title))
            self.browser_cookies_table.setItem(i, 4, QTableWidgetItem(value))

    # item4_6 캐시
    def set_browser_cache(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT url, status, value, etag, server_name, data_location, all_http_headers, " \
                "datetime(timestamp, '+9 hours'), datetime(last_modified, '+9 hours') from cache;"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()

        count = len(rows)
        self.browser_cache_table.setRowCount(count)
        self.browser_cache_table.setColumnCount(9)
        column_headers = ["시간", "url", "상태", "파일", "etag", "마지막 수정", "서버", "데이터 위치", "http 트래픽"]
        self.browser_cache_table.setHorizontalHeaderLabels(column_headers)

        for i in range(count):
            url, status, value, etag, server_name, data_location, all_http_headers, timestamp, last_modified = rows[
                i]
            self.browser_cache_table.setItem(i, 0, QTableWidgetItem(timestamp))
            self.browser_cache_table.setItem(i, 1, QTableWidgetItem(url))
            self.browser_cache_table.setItem(i, 2, QTableWidgetItem(status))
            self.browser_cache_table.setItem(i, 3, QTableWidgetItem(value))
            self.browser_cache_table.setItem(i, 4, QTableWidgetItem(etag))
            self.browser_cache_table.setItem(i, 5, QTableWidgetItem(last_modified))
            self.browser_cache_table.setItem(i, 6, QTableWidgetItem(server_name))
            self.browser_cache_table.setItem(i, 7, QTableWidgetItem(data_location))
            self.browser_cache_table.setItem(i, 8, QTableWidgetItem(all_http_headers))

    # item4_7 북마크
    def set_browser_bookmark(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT type, url, title, value, datetime(timestamp, '+9 hours') from bookmark;"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()

        count = len(rows)
        self.browser_bookmark_table.setRowCount(count)
        self.browser_bookmark_table.setColumnCount(5)
        column_headers = ["type", "시간", "url", "타이틀", "parent value"]
        self.browser_bookmark_table.setHorizontalHeaderLabels(column_headers)

        for i in range(count):
            type, url, title, value, timestamp = rows[i]
            self.browser_bookmark_table.setItem(i, 0, QTableWidgetItem(type))
            self.browser_bookmark_table.setItem(i, 1, QTableWidgetItem(timestamp))
            self.browser_bookmark_table.setItem(i, 2, QTableWidgetItem(url))
            self.browser_bookmark_table.setItem(i, 3, QTableWidgetItem(title))
            self.browser_bookmark_table.setItem(i, 4, QTableWidgetItem(value))

    # item4_8 자동완성
    def set_browser_autofill(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT type, status, value, datetime(timestamp, '+9 hours') from autofill;"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()

        count = len(rows)
        self.browser_autofill_table.setRowCount(count)
        self.browser_autofill_table.setColumnCount(4)
        column_headers = ["type", "시간", "id/email", "value"]
        self.browser_autofill_table.setHorizontalHeaderLabels(column_headers)

        for i in range(count):
            type, status, value, timestamp = rows[i]
            self.browser_autofill_table.setItem(i, 0, QTableWidgetItem(type))
            self.browser_autofill_table.setItem(i, 1, QTableWidgetItem(timestamp))
            self.browser_autofill_table.setItem(i, 2, QTableWidgetItem(status))
            self.browser_autofill_table.setItem(i, 3, QTableWidgetItem(value))

    # item4_9 환경설정
    def set_browser_preference(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT type, url, status, data, datetime(timestamp, '+9 hours') FROM preference;"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()

        count = len(rows)
        self.browser_preference_table.setRowCount(count)
        self.browser_preference_table.setColumnCount(5)
        column_headers = ["type", "시간", "url", "status", "data"]
        self.browser_preference_table.setHorizontalHeaderLabels(column_headers)

        for i in range(count):
            type, url, status, data, timestamp = rows[i]
            self.browser_preference_table.setItem(i, 0, QTableWidgetItem(type))
            self.browser_preference_table.setItem(i, 1, QTableWidgetItem(timestamp))
            self.browser_preference_table.setItem(i, 2, QTableWidgetItem(url))
            self.browser_preference_table.setItem(i, 3, QTableWidgetItem(status))
            self.browser_preference_table.setItem(i, 4, QTableWidgetItem(data))

    # item4_10 클라우드 접속기록
    def set_browser_cloud(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT url, title, datetime(timestamp, '+9 hours') FROM cloud;"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()

        count = len(rows)
        self.browser_cloud_table.setRowCount(count)
        self.browser_cloud_table.setColumnCount(3)
        column_headers = ["시간", "url", "title"]
        self.browser_cloud_table.setHorizontalHeaderLabels(column_headers)

        for i in range(count):
            url, title, timestamp = rows[i]
            self.browser_cloud_table.setItem(i, 0, QTableWidgetItem(timestamp))
            self.browser_cloud_table.setItem(i, 1, QTableWidgetItem(url))
            self.browser_cloud_table.setItem(i, 2, QTableWidgetItem(title))

    # item5_1_1 프로그램 실행 흔적 - 레지스트리 - BAM
    def set_program_bam(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT SID, program_path, datetime(last_executed, '+9 hours') FROM BAM;"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()

        count = len(rows)
        self.program_bam.setRowCount(count)
        self.program_bam.setColumnCount(3)
        column_headers = ["사용자", "프로그램", "마지막 실행"]
        self.program_bam.setHorizontalHeaderLabels(column_headers)

        for i in range(count):
            SID, program_path, last_executed = rows[i]
            self.program_bam.setItem(i, 0, QTableWidgetItem(SID))
            self.program_bam.setItem(i, 1, QTableWidgetItem(program_path))
            self.program_bam.setItem(i, 2, QTableWidgetItem(last_executed))

    # item5_1_2 프로그램 실행 흔적 - 레지스트리 - UserAssist
    def set_program_userassist(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT name, run_count, datetime(last_executed, '+9 hours') FROM UserAssist_CEB;"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()

        count = len(rows)
        self.program_userassist.setRowCount(count)
        self.program_userassist.setColumnCount(3)
        column_headers = ["프로그램", "실행 횟수", "마지막 실행"]
        self.program_userassist.setHorizontalHeaderLabels(column_headers)

        for i in range(count):
            name, run_count, last_executed = rows[i]
            self.program_userassist.setItem(i, 0, QTableWidgetItem(name))
            self.program_userassist.setItem(i, 1, QTableWidgetItem(run_count))
            self.program_userassist.setItem(i, 2, QTableWidgetItem(last_executed))

    # item5_1_3 프로그램 실행 흔적 - 레지스트리 - Uninstall
    def set_program_uninstall(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT name, version, install_location, publisher, type, datetime(install_date, '+9 hours') FROM Uninstall;"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()

        count = len(rows)
        self.program_uninstall.setRowCount(count)
        self.program_uninstall.setColumnCount(6)
        column_headers = ["프로그램", "버전", "경로", "제조사", "타입", "설치일"]
        self.program_uninstall.setHorizontalHeaderLabels(column_headers)

        for i in range(count):
            name, version, install_location, publisher, type, install_date = rows[i]
            self.program_uninstall.setItem(i, 0, QTableWidgetItem(name))
            self.program_uninstall.setItem(i, 1, QTableWidgetItem(version))
            self.program_uninstall.setItem(i, 2, QTableWidgetItem(install_location))
            self.program_uninstall.setItem(i, 3, QTableWidgetItem(publisher))
            self.program_uninstall.setItem(i, 4, QTableWidgetItem(type))
            self.program_uninstall.setItem(i, 5, QTableWidgetItem(install_date))

    # item5_1_4 프로그램 실행 흔적 - 레지스트리 - MuiCache
    def set_program_muicache(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT name, path FROM MuiCache;"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()

        count = len(rows)
        self.program_muicache.setRowCount(count)
        self.program_muicache.setColumnCount(2)
        column_headers = ["프로그램", "경로"]
        self.program_muicache.setHorizontalHeaderLabels(column_headers)

        for i in range(count):
            name, path = rows[i]
            self.program_muicache.setItem(i, 0, QTableWidgetItem(name))
            self.program_muicache.setItem(i, 1, QTableWidgetItem(path))

    # item5_1_5 프로그램 실행 흔적 - 레지스트리 - FirstFolder
    def set_program_firstfolder(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT program_name, folder, mru, datetime(opened_on, '+9 hours') FROM FirstFolder;"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()

        count = len(rows)
        self.program_firstfolder.setRowCount(count)
        self.program_firstfolder.setColumnCount(4)
        column_headers = ["프로그램", "폴더", "mru", "실행 시간"]
        self.program_firstfolder.setHorizontalHeaderLabels(column_headers)

        for i in range(count):
            program_name, folder, mru, opened_on = rows[i]
            self.program_firstfolder.setItem(i, 0, QTableWidgetItem(program_name))
            self.program_firstfolder.setItem(i, 1, QTableWidgetItem(folder))
            self.program_firstfolder.setItem(i, 2, QTableWidgetItem(mru))
            self.program_firstfolder.setItem(i, 3, QTableWidgetItem(opened_on))

    # item5_1_6 프로그램 실행 흔적 - 레지스트리 - CIDSizeMRU
    def set_program_cidsizemru(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT program_name, mru, datetime(opened_on, '+9 hours') FROM CIDSizeMRU;"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()

        count = len(rows)
        self.program_cidsizemru.setRowCount(count)
        self.program_cidsizemru.setColumnCount(3)
        column_headers = ["프로그램", "mru", "실행 시간"]
        self.program_cidsizemru.setHorizontalHeaderLabels(column_headers)

        for i in range(count):
            program_name, mru, opened_on = rows[i]
            self.program_cidsizemru.setItem(i, 0, QTableWidgetItem(program_name))
            self.program_cidsizemru.setItem(i, 1, QTableWidgetItem(mru))
            self.program_cidsizemru.setItem(i, 2, QTableWidgetItem(opened_on))

    # item5_2 프로그램 실행 흔적 - 프리패치
    def set_program_pre(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT Executable_Name, Run_Count, " \
                "datetime(Last_Executed1, '+9 hours'), datetime(Last_Executed2, '+9 hours'), " \
                "datetime(Last_Executed3, '+9 hours'), datetime(Last_Executed4, '+9 hours'), " \
                "datetime(Last_Executed5, '+9 hours'), datetime(Last_Executed6, '+9 hours'), " \
                "datetime(Last_Executed7, '+9 hours'), datetime(Last_Executed8, '+9 hours') FROM prefetch1"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()

        count = len(rows)
        self.program_pre.setRowCount(count)
        self.program_pre.setColumnCount(10)
        column_headers = ["프로그램", "실행 횟수", "최근 실행 시간1", "최근 실행 시간2", "최근 실행 시간3",
                          "최근 실행 시간4", "최근 실행 시간5", "최근 실행 시간6", "최근 실행 시간7", "최근 실행 시간8"]
        self.program_pre.setHorizontalHeaderLabels(column_headers)

        for i in range(count):
            executable_name, run_count, last_executed1, last_executed2, last_executed3, \
            last_executed4, last_executed5, last_executed6, last_executed7, last_executed8 = rows[i]
            self.program_pre.setItem(i, 0, QTableWidgetItem(executable_name))
            self.program_pre.setItem(i, 1, QTableWidgetItem(str(run_count)))
            self.program_pre.setItem(i, 2, QTableWidgetItem(last_executed1))
            self.program_pre.setItem(i, 3, QTableWidgetItem(last_executed2))
            self.program_pre.setItem(i, 4, QTableWidgetItem(last_executed3))
            self.program_pre.setItem(i, 5, QTableWidgetItem(last_executed4))
            self.program_pre.setItem(i, 6, QTableWidgetItem(last_executed5))
            self.program_pre.setItem(i, 7, QTableWidgetItem(last_executed6))
            self.program_pre.setItem(i, 8, QTableWidgetItem(last_executed7))
            self.program_pre.setItem(i, 9, QTableWidgetItem(last_executed8))

    # item6_1 문서실행 흔적 - 레지스트리
    def set_doc_reg(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT program, lnk, datetime(opened_on, '+9 hours') FROM RecentDocs WHERE (program LIKE '%.pdf' OR program LIKE '%.hwp' " \
                "OR program LIKE '%.docx' OR program LIKE '%.doc' OR program LIKE '%.xlsx' OR program LIKE '%.csv' " \
                "OR program LIKE '%.pptx' OR program LIKE '%.ppt' OR program LIKE '%.txt')"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()

        count = len(rows)
        self.doc_reg_table.setRowCount(count)
        self.doc_reg_table.setColumnCount(3)
        column_headers = ["파일", "링크 파일", "접근 시간"]
        self.doc_reg_table.setHorizontalHeaderLabels(column_headers)

        for i in range(count):
            program, lnk, opened_on = rows[i]
            self.doc_reg_table.setItem(i, 0, QTableWidgetItem(program))
            self.doc_reg_table.setItem(i, 1, QTableWidgetItem(lnk))
            self.doc_reg_table.setItem(i, 2, QTableWidgetItem(opened_on))

    # item6_2 문서실행 흔적 - 링크 파일
    def set_doc_lnk(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT file_name, lnk_file_full_path, file_flags, file_size, local_base_path, show_command, " \
                "drive_serial_number, drive_type, volume_label, icon_location, machine_info, " \
                "datetime(target_creation_time, '+9 hours'), datetime(target_modified_time, '+9 hours'), " \
                "datetime(target_accessed_time, '+9 hours') from lnk_files " \
                "WHERE ((local_base_path LIKE '%.pdf' OR local_base_path LIKE '%.hwp' OR local_base_path LIKE '%.docx'" \
                "OR local_base_path LIKE '%.doc' OR local_base_path LIKE '%.xlsx' OR local_base_path LIKE '%.csv'" \
                "OR local_base_path LIKE '%.pptx' OR local_base_path LIKE '%.ppt' OR local_base_path LIKE '%.txt')" \
                "AND lnk_file_full_path LIKE '%Recent%')"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()

        count = len(rows)
        self.doc_lnk_table.setRowCount(count)
        self.doc_lnk_table.setColumnCount(14)
        column_headers = ["파일", "경로", "File_Flags", "크기", "Local_Base_Path", "Show_Command",
                          "생성", "수정", "접근", "Drive_Serial_Number",
                          "Drive_Type", "Volume_Label", "Icon_Location", "Machine_Info"]
        self.doc_lnk_table.setHorizontalHeaderLabels(column_headers)

        for i in range(count):
            file_name, lnk_file_full_path, file_flags, file_size, local_base_path, show_command, \
            drive_serial_number, drive_type, volume_label, icon_location, machine_info, \
            target_creation_time, target_modified_time, target_accessed_time = rows[i]
            self.doc_lnk_table.setItem(i, 0, QTableWidgetItem(file_name))
            self.doc_lnk_table.setItem(i, 1, QTableWidgetItem(lnk_file_full_path))
            self.doc_lnk_table.setItem(i, 2, QTableWidgetItem(file_flags))
            self.doc_lnk_table.setItem(i, 3, QTableWidgetItem(file_size))
            self.doc_lnk_table.setItem(i, 4, QTableWidgetItem(local_base_path))
            self.doc_lnk_table.setItem(i, 5, QTableWidgetItem(show_command))
            self.doc_lnk_table.setItem(i, 6, QTableWidgetItem(target_creation_time))
            self.doc_lnk_table.setItem(i, 7, QTableWidgetItem(target_modified_time))
            self.doc_lnk_table.setItem(i, 8, QTableWidgetItem(target_accessed_time))
            self.doc_lnk_table.setItem(i, 9, QTableWidgetItem(drive_serial_number))
            self.doc_lnk_table.setItem(i, 10, QTableWidgetItem(drive_type))
            self.doc_lnk_table.setItem(i, 11, QTableWidgetItem(volume_label))
            self.doc_lnk_table.setItem(i, 12, QTableWidgetItem(icon_location))
            self.doc_lnk_table.setItem(i, 13, QTableWidgetItem(machine_info))

    # item6_3 문서실행 흔적 - 점프 목록
    def set_doc_jmp(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT file_name, lnk_counter, local_base_path, file_size, file_flags, show_command, icon, description, volume_label, drive_type, " \
                "datetime(target_creation_time, '+9 hours'), datetime(target_modified_time, '+9 hours'), datetime(target_accessed_time, '+9 hours')" \
                " FROM jumplist WHERE (local_base_path LIKE '%.pdf' OR local_base_path LIKE '%.hwp' OR local_base_path LIKE '%.docx' " \
                "OR local_base_path LIKE '%.doc' OR local_base_path LIKE '%.xlsx' OR local_base_path LIKE '%.csv' OR local_base_path LIKE '%.pptx' " \
                "OR local_base_path LIKE '%.ppt' OR local_base_path LIKE '%.txt')"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()

        count = len(rows)
        self.doc_jmp_table.setRowCount(count)
        self.doc_jmp_table.setColumnCount(13)
        column_headers = ["file_name", "lnk_counter", "local_base_path", "file_size", "file_flags",
                          "target_created_time",
                          "target_modified_time", "target_accessed_time", "show_command", "icon", "description",
                          "volume_label", "drive_type"]
        self.doc_jmp_table.setHorizontalHeaderLabels(column_headers)

        for i in range(count):
            file_name, lnk_counter, local_base_path, file_size, file_flags, show_command, icon, description, volume_label, drive_type, \
            target_creation_time, target_modified_time, target_accessed_time, = rows[i]
            self.doc_jmp_table.setItem(i, 0, QTableWidgetItem(file_name))
            self.doc_jmp_table.setItem(i, 1, QTableWidgetItem(lnk_counter))
            self.doc_jmp_table.setItem(i, 2, QTableWidgetItem(local_base_path))
            self.doc_jmp_table.setItem(i, 3, QTableWidgetItem(file_size))
            self.doc_jmp_table.setItem(i, 4, QTableWidgetItem(file_flags))
            self.doc_jmp_table.setItem(i, 5, QTableWidgetItem(target_creation_time))
            self.doc_jmp_table.setItem(i, 6, QTableWidgetItem(target_modified_time))
            self.doc_jmp_table.setItem(i, 7, QTableWidgetItem(target_accessed_time))
            self.doc_jmp_table.setItem(i, 8, QTableWidgetItem(show_command))
            self.doc_jmp_table.setItem(i, 9, QTableWidgetItem(icon))
            self.doc_jmp_table.setItem(i, 10, QTableWidgetItem(description))
            self.doc_jmp_table.setItem(i, 11, QTableWidgetItem(volume_label))
            self.doc_jmp_table.setItem(i, 12, QTableWidgetItem(drive_type))

    # item6_4 문서실행 흔적 - 프리패치
    def set_doc_pre(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT FILENAME, PATH from prefetch2 WHERE (FILENAME LIKE '%.pdf' OR FILENAME LIKE '%.hwp' OR FILENAME LIKE '%.docx' " \
                "OR FILENAME LIKE '%.doc' OR FILENAME LIKE '%.xlsx' OR FILENAME LIKE '%.csv' OR FILENAME LIKE '%.pptx' " \
                "OR FILENAME LIKE '%.ppt' OR FILENAME LIKE '%.txt')"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()

        count = len(rows)
        self.doc_pre_table.setRowCount(count)
        self.doc_pre_table.setColumnCount(2)
        column_headers = ["파일", "경로"]
        self.doc_pre_table.setHorizontalHeaderLabels(column_headers)

        for i in range(count):
            file_name, path = rows[i]
            self.doc_pre_table.setItem(i, 0, QTableWidgetItem(file_name))
            self.doc_pre_table.setItem(i, 1, QTableWidgetItem(path))

    # item7_1 기타실행 흔적 - 링크 파일
    def set_etc_lnk(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT file_name, lnk_file_full_path, file_flags, file_size, local_base_path, show_command, " \
                "drive_serial_number, drive_type, volume_label, icon_location, machine_info, " \
                "datetime(target_creation_time, '+9 hours'), datetime(target_modified_time, '+9 hours'), " \
                "datetime(target_accessed_time, '+9 hours') FROM lnk_files " \
                "WHERE((local_base_path LIKE '%.jpg' OR local_base_path LIKE '%.jpeg' OR local_base_path LIKE '%.gif' " \
                "OR local_base_path LIKE '%.bmp' OR local_base_path LIKE '%.png' OR local_base_path LIKE '%.raw' " \
                "OR local_base_path LIKE '%.tiff' OR local_base_path LIKE '%.wav' OR local_base_path LIKE '%.wma' " \
                "OR local_base_path LIKE '%.mp3' OR local_base_path LIKE '%.mp4' OR local_base_path LIKE '%.mkv' " \
                "OR local_base_path LIKE '%.avi' OR local_base_path LIKE '%.flv' OR local_base_path LIKE '%.mov' " \
                "OR local_base_path LIKE '%.zip' OR local_base_path LIKE '%.7z' OR local_base_path LIKE '%.alz' " \
                "OR local_base_path LIKE '%.egg' OR local_base_path LIKE '%.rar')" \
                "AND file_flags not LIKE '%DIRECTORY%' AND lnk_file_full_path LIKE '%Recent%')"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()

        count = len(rows)
        self.etc_lnk_table.setRowCount(count)
        self.etc_lnk_table.setColumnCount(14)
        column_headers = ["파일", "LNK 경로", "Flags", "크기", "Local_Base_Path", "Show_Command",
                          "생성", "수정", "접근", "Drive_Serial_Number",
                          "Drive_Type", "Volume_Label", "Icon_Location", "Machine_Info"]
        self.etc_lnk_table.setHorizontalHeaderLabels(column_headers)

        for i in range(count):
            file_name, lnk_file_full_path, file_flags, file_size, local_base_path, show_command, \
            drive_serial_number, drive_type, volume_label, icon_location, machine_info, \
            target_creation_time, target_modified_time, target_accessed_time = rows[i]
            self.etc_lnk_table.setItem(i, 0, QTableWidgetItem(file_name))
            self.etc_lnk_table.setItem(i, 1, QTableWidgetItem(lnk_file_full_path))
            self.etc_lnk_table.setItem(i, 2, QTableWidgetItem(file_flags))
            self.etc_lnk_table.setItem(i, 3, QTableWidgetItem(file_size))
            self.etc_lnk_table.setItem(i, 4, QTableWidgetItem(local_base_path))
            self.etc_lnk_table.setItem(i, 5, QTableWidgetItem(show_command))
            self.etc_lnk_table.setItem(i, 6, QTableWidgetItem(target_creation_time))
            self.etc_lnk_table.setItem(i, 7, QTableWidgetItem(target_modified_time))
            self.etc_lnk_table.setItem(i, 8, QTableWidgetItem(target_accessed_time))
            self.etc_lnk_table.setItem(i, 9, QTableWidgetItem(drive_serial_number))
            self.etc_lnk_table.setItem(i, 10, QTableWidgetItem(drive_type))
            self.etc_lnk_table.setItem(i, 11, QTableWidgetItem(volume_label))
            self.etc_lnk_table.setItem(i, 12, QTableWidgetItem(icon_location))
            self.etc_lnk_table.setItem(i, 13, QTableWidgetItem(machine_info))

    # item7_2 기타실행 흔적 - 프리패치
    def set_etc_pre(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT FILENAME, PATH from prefetch2  WHERE (FILENAME LIKE '%.jpg' OR FILENAME LIKE '%.jpeg' OR FILENAME LIKE '%.gif' " \
                "OR FILENAME LIKE '%.bmp' OR FILENAME LIKE '%.png' OR FILENAME LIKE '%.raw' OR FILENAME LIKE '%.tiff' " \
                "OR FILENAME LIKE '%.wav' OR FILENAME LIKE '%.wma' OR FILENAME LIKE '%.mp3' OR FILENAME LIKE '%.mp4' " \
                "OR FILENAME LIKE '%.mkv' OR FILENAME LIKE '%.avi' OR FILENAME LIKE '%.flv' OR FILENAME LIKE '%.mov' " \
                "OR FILENAME LIKE '%.zip' OR FILENAME LIKE '%.7z' OR FILENAME LIKE '%.alz' OR FILENAME LIKE '%.egg' " \
                "OR FILENAME LIKE '%.rar')"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()

        count = len(rows)
        self.etc_pre_table.setRowCount(count)
        self.etc_pre_table.setColumnCount(2)
        column_headers = ["파일", "경로"]
        self.etc_pre_table.setHorizontalHeaderLabels(column_headers)

        for i in range(count):
            file_name, path = rows[i]
            self.etc_pre_table.setItem(i, 0, QTableWidgetItem(file_name))
            self.etc_pre_table.setItem(i, 1, QTableWidgetItem(path))

    # item7_3 기타실행 흔적 - 대화상자
    def set_etc_dialog(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT program, mru, datetime(opened_on, '+9 hours') FROM Legacy;"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()

        count = len(rows)
        self.etc_dialog_table.setRowCount(count)
        self.etc_dialog_table.setColumnCount(3)
        column_headers = ["프로그램", "최근 실행 순서", "시간"]
        self.etc_dialog_table.setHorizontalHeaderLabels(column_headers)

        for i in range(count):
            program, mru, opened_on = rows[i]
            self.etc_dialog_table.setItem(i, 0, QTableWidgetItem(program))
            self.etc_dialog_table.setItem(i, 1, QTableWidgetItem(str(mru)))
            self.etc_dialog_table.setItem(i, 2, QTableWidgetItem(opened_on))

    # item8_1 이벤트 로그 삭제
    def set_eventlog_delete(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT event_id, detailed, computer, sbt_usr_name, channel, " \
                "datetime(time_created, '+9 hours') FROM event_log WHERE event_id == '104' or event_id == '1102';"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()

        count = len(rows)
        self.eventlog_delete_table.setRowCount(count)
        self.eventlog_delete_table.setColumnCount(6)
        column_headers = ["이벤트 아이디", "내용", "컴퓨터 아이디", "이벤트 생성날짜", "주체이름", "채널"]
        self.eventlog_delete_table.setHorizontalHeaderLabels(column_headers)

        for i in range(count):
            event_id, detailed, computer, sbt_usr_name, channel, time_created = rows[i]
            self.eventlog_delete_table.setItem(i, 0, QTableWidgetItem(str(event_id)))
            self.eventlog_delete_table.setItem(i, 1, QTableWidgetItem(detailed))
            self.eventlog_delete_table.setItem(i, 2, QTableWidgetItem(computer))
            self.eventlog_delete_table.setItem(i, 3, QTableWidgetItem(time_created))
            self.eventlog_delete_table.setItem(i, 4, QTableWidgetItem(sbt_usr_name))
            self.eventlog_delete_table.setItem(i, 5, QTableWidgetItem(channel))

    # item8_2 프로세스 강제 종료
    def set_eventlog_terminate(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT event_id, detailed, computer, app_name, app_version, app_path, " \
                "datetime(time_created, '+9 hours') FROM event_log WHERE event_id == '1002' AND app_name IS NOT '';"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()

        count = len(rows)
        self.eventlog_terminate_table.setRowCount(count)
        self.eventlog_terminate_table.setColumnCount(7)
        column_headers = ["이벤트 아이디", "내용", "컴퓨터 아이디", "이벤트 생성날짜", "프로세스 이름", "프로그램 버전", "경로"]
        self.eventlog_terminate_table.setHorizontalHeaderLabels(column_headers)

        for i in range(count):
            event_id, detailed, computer, app_name, app_version, app_path, time_created = rows[i]
            self.eventlog_terminate_table.setItem(i, 0, QTableWidgetItem(str(event_id)))
            self.eventlog_terminate_table.setItem(i, 1, QTableWidgetItem(detailed))
            self.eventlog_terminate_table.setItem(i, 2, QTableWidgetItem(computer))
            self.eventlog_terminate_table.setItem(i, 3, QTableWidgetItem(time_created))
            self.eventlog_terminate_table.setItem(i, 4, QTableWidgetItem(app_name))
            self.eventlog_terminate_table.setItem(i, 5, QTableWidgetItem(app_version))
            self.eventlog_terminate_table.setItem(i, 6, QTableWidgetItem(app_path))

    # item8_3_1 PC 전원 기록 - 운영체제 시작 및 종료
    def set_eventlog_onoff(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT event_id, detailed, computer, " \
                "datetime(time_created, '+9 hours') FROM event_log WHERE event_id = '12' OR event_id = '13';"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()

        count = len(rows)
        self.eventlog_onoff_table.setRowCount(count)
        self.eventlog_onoff_table.setColumnCount(4)
        column_headers = ["이벤트 아이디", "내용", "컴퓨터 아이디", "이벤트 생성날짜"]
        self.eventlog_onoff_table.setHorizontalHeaderLabels(column_headers)

        for i in range(count):
            event_id, detailed, computer, time_created = rows[i]
            self.eventlog_onoff_table.setItem(i, 0, QTableWidgetItem(str(event_id)))
            self.eventlog_onoff_table.setItem(i, 1, QTableWidgetItem(detailed))
            self.eventlog_onoff_table.setItem(i, 2, QTableWidgetItem(computer))
            self.eventlog_onoff_table.setItem(i, 3, QTableWidgetItem(time_created))

    # item8_3_2 PC 전원 기록 - 절전모드 전환 및 해제
    def set_eventlog_powersaving(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT event_id, detailed, computer, datetime(time_created, '+9 hours'), " \
                "datetime(sleep_time, '+9 hours'), datetime(wake_time, '+9 hours') " \
                "FROM event_log WHERE event_id = '1' OR (event_id = '42' AND source IS 'System.evtx')"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()

        count = len(rows)
        self.eventlog_powersaving_table.setRowCount(count)
        self.eventlog_powersaving_table.setColumnCount(6)
        column_headers = ["이벤트 아이디", "내용", "컴퓨터 아이디", "이벤트 생성날짜", "전환시간", "복귀시간"]
        self.eventlog_powersaving_table.setHorizontalHeaderLabels(column_headers)

        for i in range(count):
            event_id, detailed, computer, time_created, sleep_time, wake_time = rows[i]
            self.eventlog_powersaving_table.setItem(i, 0, QTableWidgetItem(str(event_id)))
            self.eventlog_powersaving_table.setItem(i, 1, QTableWidgetItem(detailed))
            self.eventlog_powersaving_table.setItem(i, 2, QTableWidgetItem(computer))
            self.eventlog_powersaving_table.setItem(i, 3, QTableWidgetItem(time_created))
            self.eventlog_powersaving_table.setItem(i, 4, QTableWidgetItem(sleep_time))
            self.eventlog_powersaving_table.setItem(i, 5, QTableWidgetItem(wake_time))

    # item8_4_1 원격 - 원격 접속 기록
    def set_eventlog_access1(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT event_id, detailed, computer, remo_conn_user, remo_conn_addr, remo_conn_local, local_manager_sess_id, " \
                "datetime(time_created, '+9 hours') FROM event_log WHERE event_id = '261' or event_id = '1149' or event_id = '24' or event_id = '25';"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()

        count = len(rows)
        self.eventlog_access1_table.setRowCount(count)
        self.eventlog_access1_table.setColumnCount(8)
        column_headers = ["이벤트 아이디", "내용", "컴퓨터 아이디", "이벤트 생성날짜", "로그인 계정", "들어온 IP", "내 컴퓨터 이름", "세션 ID"]
        self.eventlog_access1_table.setHorizontalHeaderLabels(column_headers)

        for i in range(count):
            event_id, detailed, computer, remo_conn_user, remo_conn_addr, remo_conn_local, local_manager_sess_id, time_created = \
            rows[i]
            self.eventlog_access1_table.setItem(i, 0, QTableWidgetItem(str(event_id)))
            self.eventlog_access1_table.setItem(i, 1, QTableWidgetItem(detailed))
            self.eventlog_access1_table.setItem(i, 2, QTableWidgetItem(computer))
            self.eventlog_access1_table.setItem(i, 3, QTableWidgetItem(time_created))
            self.eventlog_access1_table.setItem(i, 4, QTableWidgetItem(remo_conn_user))
            self.eventlog_access1_table.setItem(i, 5, QTableWidgetItem(remo_conn_addr))
            self.eventlog_access1_table.setItem(i, 6, QTableWidgetItem(remo_conn_local))
            self.eventlog_access1_table.setItem(i, 7, QTableWidgetItem(local_manager_sess_id))

    # item8_4_2 원격 - 원격 실행 기록
    def set_eventlog_access2(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT event_id, detailed, computer, rdp_name, rdp_value, rdp_custom_level, rdp_domain, rdp_session, sec_id, " \
                "datetime(time_created, '+9 hours') FROM event_log where (event_id = '1024' AND rdp_value IS NOT  '') or (event_id = '1026' AND rdp_value IS NOT '') or event_id = '1025' or event_id = '1027' or event_id = '1028' or event_id = '1102';"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()

        count = len(rows)
        self.eventlog_access2_table.setRowCount(count)
        self.eventlog_access2_table.setColumnCount(10)
        column_headers = ["이벤트 아이디", "내용", "컴퓨터 아이디", "이벤트 생성날짜", "서버 이름", "서버 주소", "커스텀 레벨", "도메인 이름", "세션 ID",
                          "계정 SID"]
        self.eventlog_access2_table.setHorizontalHeaderLabels(column_headers)

        for i in range(count):
            event_id, detailed, computer, rdp_name, rdp_value, rdp_custom_level, rdp_domain, rdp_session, sec_id, time_created = \
            rows[i]
            self.eventlog_access2_table.setItem(i, 0, QTableWidgetItem(str(event_id)))
            self.eventlog_access2_table.setItem(i, 1, QTableWidgetItem(detailed))
            self.eventlog_access2_table.setItem(i, 2, QTableWidgetItem(computer))
            self.eventlog_access2_table.setItem(i, 3, QTableWidgetItem(time_created))
            self.eventlog_access2_table.setItem(i, 4, QTableWidgetItem(rdp_name))
            self.eventlog_access2_table.setItem(i, 5, QTableWidgetItem(rdp_value))
            self.eventlog_access2_table.setItem(i, 6, QTableWidgetItem(rdp_custom_level))
            self.eventlog_access2_table.setItem(i, 7, QTableWidgetItem(rdp_domain))
            self.eventlog_access2_table.setItem(i, 8, QTableWidgetItem(rdp_session))
            self.eventlog_access2_table.setItem(i, 9, QTableWidgetItem(sec_id))

    # item8_5 시스템 시간 변경  기록
    def set_eventlog_time(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT event_id, detailed, computer, reason, old_bias, new_bias, sbt_usr_name, sys_prv_time, sys_new_time, " \
                "datetime(time_created, '+9 hours') FROM event_log where (event_id = '1' AND reason IS NOT '') OR event_id = '22' OR event_id = '4616';"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()

        count = len(rows)
        self.eventlog_time_table.setRowCount(count)
        self.eventlog_time_table.setColumnCount(10)
        column_headers = ["이벤트 아이디", "내용", "컴퓨터 아이디", "이벤트 생성날짜", "이유", "전 표준시간", "후 표준시간", "주체이름", "전 시간", "후 시간"]
        self.eventlog_time_table.setHorizontalHeaderLabels(column_headers)

        for i in range(count):
            event_id, detailed, computer, reason, old_bias, new_bias, sbt_usr_name, sys_prv_time, sys_new_time, time_created = \
            rows[i]
            self.eventlog_time_table.setItem(i, 0, QTableWidgetItem(str(event_id)))
            self.eventlog_time_table.setItem(i, 1, QTableWidgetItem(detailed))
            self.eventlog_time_table.setItem(i, 2, QTableWidgetItem(computer))
            self.eventlog_time_table.setItem(i, 3, QTableWidgetItem(time_created))
            self.eventlog_time_table.setItem(i, 4, QTableWidgetItem(reason))
            self.eventlog_time_table.setItem(i, 5, QTableWidgetItem(old_bias))
            self.eventlog_time_table.setItem(i, 6, QTableWidgetItem(new_bias))
            self.eventlog_time_table.setItem(i, 7, QTableWidgetItem(sbt_usr_name))
            self.eventlog_time_table.setItem(i, 8, QTableWidgetItem(sys_prv_time))
            self.eventlog_time_table.setItem(i, 9, QTableWidgetItem(sys_new_time))

    # item9 폴더 열람 흔적
    def set_folder(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        query = "SELECT file_name, lnk_file_full_path, file_flags, file_size, local_base_path, show_command, " \
                "drive_serial_number, drive_type, volume_label, icon_location, machine_info, droid_file, droid_vol, known_guid, " \
                "datetime(target_creation_time, '+9 hours'), datetime(target_modified_time, '+9 hours'), datetime(target_accessed_time, '+9 hours')" \
                " FROM lnk_files WHERE file_flags LIKE '%DIRECTORY%'"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()

        count = len(rows)
        self.folder_table.setRowCount(count)
        self.folder_table.setColumnCount(17)
        column_headers = ["File_Name", "Lnk_File_Path", "Flags", "Size", "Local_Base_Path", "Show_Command", \
                          "Target_Created_Time", "Target_Modified_Time", "Target_Accessed_Time",
                          "Drive_Serial_Number",
                          "Drive_Type", "Volume_Label", "Icon_Location", "Machine_Info", "Droid_File", "Droid_Vol",
                          "Known_Guid"]
        self.folder_table.setHorizontalHeaderLabels(column_headers)

        for i in range(count):
            file_name, lnk_file_full_path, file_flags, file_size, local_base_path, show_command, \
            drive_serial_number, drive_type, volume_label, icon_location, machine_info, droid_file, droid_vol, known_guid, \
            target_creation_time, target_modified_time, target_accessed_time = rows[i]
            self.folder_table.setItem(i, 0, QTableWidgetItem(file_name))
            self.folder_table.setItem(i, 1, QTableWidgetItem(lnk_file_full_path))
            self.folder_table.setItem(i, 2, QTableWidgetItem(file_flags))
            self.folder_table.setItem(i, 3, QTableWidgetItem(file_size))
            self.folder_table.setItem(i, 4, QTableWidgetItem(local_base_path))
            self.folder_table.setItem(i, 5, QTableWidgetItem(show_command))
            self.folder_table.setItem(i, 6, QTableWidgetItem(target_creation_time))
            self.folder_table.setItem(i, 7, QTableWidgetItem(target_modified_time))
            self.folder_table.setItem(i, 8, QTableWidgetItem(target_accessed_time))
            self.folder_table.setItem(i, 9, QTableWidgetItem(drive_serial_number))
            self.folder_table.setItem(i, 10, QTableWidgetItem(drive_type))
            self.folder_table.setItem(i, 11, QTableWidgetItem(volume_label))
            self.folder_table.setItem(i, 12, QTableWidgetItem(icon_location))
            self.folder_table.setItem(i, 13, QTableWidgetItem(machine_info))
            self.folder_table.setItem(i, 14, QTableWidgetItem(droid_file))
            self.folder_table.setItem(i, 15, QTableWidgetItem(droid_vol))
            self.folder_table.setItem(i, 16, QTableWidgetItem(known_guid))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywidget = MyWidget()
    mywidget.show()
    sys.exit(app.exec_())