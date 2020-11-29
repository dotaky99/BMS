import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtCore import *
import sqlite3

class Tab2():
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
        text1_4_n = []  # DRM 정보
        query = "SELECT name, version, install_location, publisher, install_date FROM Uninstall " \
                "WHERE name LIKE 'Oracle VM VirtualBox%' OR name LIKE 'VMware Workstation';"
        cur.execute(query)
        list = cur.fetchall()
        for l in range(len(list)):
            text1_4_n.append(QLabel(
                "이름 : " + list[l][0] + ", 버전: " + list[l][1] + ", 경로: " + list[l][2] + ", 제조사: " + list[l][
                    3] + ", 최초 실행 시각: " + list[l][4] + ", 삭제 여부 : ", self))

        ####추가####
        conn1 = sqlite3.connect("Believe_Me_Sister.db")
        cur1 = conn1.cursor()
        text1_6_n = []  # 안티포렌식 정보

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
        #text2_7 = QLabel("<b> * 네트워크  <b>  :  ", self) #필요 없을 것 같아
        text2_8 = QLabel("<b> * 계정  <b>  :  ", self)
        text2_1_1 = QLabel(list[0] + " (" + list[6] + ")", self)
        text2_2_1 = QLabel(list[4] + " (UTC +00)", self)
        text2_3_1 = QLabel(list[10], self)
        # text4_2 = QLabel(string4, self)
        text2_5_1 = QLabel(list[7] + " (UTC" + f"{list[9]:+03d}" + ")", self)

        text2_6_n = []
        query = "SELECT serial_num, random_yn, UIID, vendor_name, product_name, version, label, GUID, " \
                "first_connected, last_connected FROM Connected_USB"
        cur.execute(query)
        list = cur.fetchall()
        for l in range(len(list)):
            string = "시리얼 넘버: " + list[l][0] + ", GUID: " + list[l][7] + ", UIID: " + list[l][2] + ", 최초 연결: " + list[l][
                8] + ", 마지막 연결: " + list[l][9]
            text2_6_n.append(QLabel(string))

        text2_8_n = []
        query = "SELECT account_name, created_on FROM UserAccounts"
        cur.execute(query)
        list = cur.fetchall()
        for l in range(len(list)):
            text2_8_n.append(QLabel(list[l][0] + ", 생성: " + list[l][1]))

        vbox2.addWidget(text2_1, 0, 0)  # 윈도우 버전
        vbox2.addWidget(text2_2, 1, 0)  # 윈도우 설치 시각
        vbox2.addWidget(text2_3, 2, 0)  # 컴퓨터 이름
        vbox2.addWidget(text2_4, 3, 0)  # 작업 그룹
        vbox2.addWidget(text2_5, 4, 0)  # 표준 시간대
        vbox2.addWidget(text2_6, 5, 0)  # USB
        #vbox2.addWidget(text2_7, 10, 0)  # 네트워크
        vbox2.addWidget(text2_8, 11, 0)  # 계정
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
