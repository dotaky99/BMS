import os, sys
import re
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QColor
from PyQt5.QtCore import *
import sqlite3
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.dates as mdates


class MyWidget(QWidget):
    def __init__(self, parent, UTC):
        super(MyWidget, self).__init__(parent)
        self.setGeometry(100, 100, 1500, 700)
        try:
            self.UTC = "'" + UTC + " hours'"
            self.UTC_int = int(UTC)
        except:
            self.UTC = "'+0 hours'"  # UTC 선택 안하고 창 종료 시 0으로 설정
            self.UTC_int = 0
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
        # self.set_tab4()

        total_layout = QVBoxLayout()
        total_layout.addWidget(self.tabs)
        self.setLayout(total_layout)

#################################################
#   tab2                                        #
#################################################
    # tab2 구성
    def set_tab2(self):
        self.tab2.layout = QVBoxLayout()
        self.set_PCinfo()
        self.set_checklist()
        self.tab2.setLayout(self.tab2.layout)

    # tab2 수집 전 확인 사항
    def set_checklist(self):
        self.groupbox1 = QGroupBox("수집 전 확인 사항")
        self.vbox1 = QVBoxLayout()

        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        # DRM - fasoo
        try:
            # 설치 + 실행
            query1_1_1 = "SELECT a.name, a.version, a.publisher, b.Full_Path, " \
                       "datetime(a.install_date," + self.UTC + "), datetime(b.Last_Executed1," + self.UTC + ") FROM Uninstall a, Prefetch1 b " \
                       "WHERE name like '%fasoo%' AND Executable_Name LIKE '%fasoo%'"
            cur.execute(query1_1_1)
            rows1_1_1 = cur.fetchall()
            if len(rows1_1_1) < 1:
                # 설치
                query1_1_2 = "SELECT name, version, publisher, install_location, datetime(install_date," + self.UTC + ") FROM Uninstall WHERE name like '%fasoo%'"
                cur.execute(query1_1_2)
                rows1_1_2 = cur.fetchall()
                if len(rows1_1_2)<1:
                    # 실행
                    query1_1_3 = "SELECT Executable_Name, Full_Path, datetime(Last_Executed1," + self.UTC + ") FROM Prefetch1 WHERE Executable_Name like '%fasoo%'"
                    cur.execute(query1_1_3)
                    rows1_1_3 = cur.fetchall()
                else:
                    rows1_1_3 = ''
            else:
                rows1_1_2 = ''
                rows1_1_3 = ''
        except:
            rows1_1_1 = ''
            rows1_1_2 = ''
            rows1_1_3 = ''
            pass

        # DRM - SoftcampDS
        try:
            # 설치 + 실행
            query1_2_1 = "SELECT a.name, a.version, a.publisher, b.Full_Path, " \
                       "datetime(a.install_date," + self.UTC + "), datetime(b.Last_Executed1," + self.UTC + ") FROM Uninstall a, Prefetch1 b " \
                       "WHERE name like '%SoftcampDS%' AND Executable_Name LIKE '%SoftcampDS%'"
            cur.execute(query1_2_1)
            rows1_2_1 = cur.fetchall()
            if len(rows1_2_1) < 1:
                # 설치
                query1_2_2 = "SELECT name, version, publisher, install_location, datetime(install_date," + self.UTC + ") FROM Uninstall WHERE name like '%SoftcampDS%'"
                cur.execute(query1_2_2)
                rows1_2_2 = cur.fetchall()
                if len(rows1_2_2)<1:
                    # 실행
                    query1_2_3 = "SELECT Executable_Name, Full_Path, datetime(Last_Executed1," + self.UTC + ") FROM Prefetch1 WHERE Executable_Name like '%SoftcampDS%'"
                    cur.execute(query1_2_3)
                    rows1_2_3 = cur.fetchall()
                else:
                    rows1_2_3 = ''
            else:
                rows1_2_2 = ''
                rows1_2_3 = ''
        except:
            rows1_2_1 = ''
            rows1_2_2 = ''
            rows1_2_3 = ''
            pass

        # DRM - SDSLanuc
        try:
            # 설치 + 실행
            query1_3_1 = "SELECT a.name, a.version, a.publisher, b.Full_Path, " \
                       "datetime(a.install_date," + self.UTC + "), datetime(b.Last_Executed1," + self.UTC + ") FROM Uninstall a, Prefetch1 b " \
                       "WHERE name like '%SDSLanuc%' AND Executable_Name LIKE '%SDSLanuc%'"
            cur.execute(query1_3_1)
            rows1_3_1 = cur.fetchall()
            if len(rows1_3_1) < 1:
                # 설치
                query1_3_2 = "SELECT name, version, publisher, install_location, datetime(install_date," + self.UTC + ") FROM Uninstall WHERE name like '%SDSLanuc%'"
                cur.execute(query1_3_2)
                rows1_3_2 = cur.fetchall()
                if len(rows1_3_2)<1:
                    # 실행
                    query1_3_3 = "SELECT Executable_Name, Full_Path, datetime(Last_Executed1," + self.UTC + ") FROM Prefetch1 WHERE Executable_Name like '%SDSLanuc%'"
                    cur.execute(query1_3_3)
                    rows1_3_3 = cur.fetchall()
                else:
                    rows1_3_3 = ''
            else:
                rows1_3_2 = ''
                rows1_3_3 = ''
        except:
            rows1_3_1 = ''
            rows1_3_2 = ''
            rows1_3_3 = ''
            pass

        # DRM - DocumentSAFER
        try:
            # 설치 + 실행
            query1_4_1 = "SELECT a.name, a.version, a.publisher, b.Full_Path, " \
                       "datetime(a.install_date," + self.UTC + "), datetime(b.Last_Executed1," + self.UTC + ") FROM Uninstall a, Prefetch1 b " \
                       "WHERE name like '%DocumentSAFER%' AND Executable_Name LIKE '%DocumentSAFER%'"
            cur.execute(query1_4_1)
            rows1_4_1 = cur.fetchall()
            if len(rows1_4_1) < 1:
                # 설치
                query1_4_2 = "SELECT name, version, publisher, install_location, datetime(install_date," + self.UTC + ") FROM Uninstall WHERE name like '%DocumentSAFER%'"
                cur.execute(query1_4_2)
                rows1_4_2 = cur.fetchall()
                if len(rows1_4_2)<1:
                    # 실행
                    query1_4_3 = "SELECT Executable_Name, Full_Path, datetime(Last_Executed1," + self.UTC + ") FROM Prefetch1 WHERE Executable_Name like '%DocumentSAFER%'"
                    cur.execute(query1_4_3)
                    rows1_4_3 = cur.fetchall()
                else:
                    rows1_4_3 = ''
            else:
                rows1_4_2 = ''
                rows1_4_3 = ''
        except:
            rows1_4_1 = ''
            rows1_4_2 = ''
            rows1_4_3 = ''
            pass

        # 매체제어
        # Symantec이 설치되었는지 확인
        symantec = []
        try:
            GetRegKey_command = 'RegistryParse\\GetRegKey.exe COPY\\REGHIVE\\SYSTEM COPY\\REGHIVE\\SOFTWARE COPY\\REGHIVE\\SAM REGHIVE\\NTUSER.DAT COPY\\REGHIVE\\USRCLASS.DAT '
            GetRegValue_command = 'RegistryParse\\GetRegValue.exe COPY\\REGHIVE\\SYSTEM COPY\\REGHIVE\\SOFTWARE COPY\\REGHIVE\\SAM REGHIVE\\NTUSER.DAT COPY\\REGHIVE\\USRCLASS.DAT '
            input = 'SOFTWARE "Symantec\\Symantec Endpoint Protection\\CurrentVersion"'
            result1 = os.popen(GetRegKey_command + input).read()
            input = 'SOFTWARE "Wow6432Node\\Symantec\\Symantec Endpoint Protection\\CurrentVersion"'
            result2 = os.popen(GetRegKey_command + input).read()
            if result1 == 1 or result2 == 1:    # 시만텍이 있는 경우
                symantec.append("Symantec")
                input = 'SOFTWARE "Symantec\\Symantec Endpoint Protection\\CurrentVersion\\public-opstate" ASRunningStatus'
                result1 = os.popen(GetRegValue_command + input).read()
                input = 'SOFTWARE "Wow6432Node\\Symantec\\Symantec Endpoint Protection\\CurrentVersion\\public-opstate" ASRunningStatus'
                result2 = os.popen(GetRegValue_command + input).read()
                if result1 == 1 or result2 == 2:    # 시만텍이 실행중인 경우
                    symantec.append("실행중")
                else:
                    symantec.append("")
        except:
            pass

        # 디스크 암호화 - CipherShed
        try:
            # 설치 + 실행
            query3_1_1 = "SELECT a.name, a.version, a.publisher, b.Full_Path, " \
                       "datetime(a.install_date," + self.UTC + "), datetime(b.Last_Executed1," + self.UTC + ") FROM Uninstall a, Prefetch1 b " \
                       "WHERE name like 'CipherShed%' AND Executable_Name LIKE 'CipherShed%'"
            cur.execute(query3_1_1)
            rows3_1_1 = cur.fetchall()
            if len(rows3_1_1) < 1:
                # 설치
                query3_1_2 = "SELECT name, version, publisher, install_location, datetime(install_date," + self.UTC + ") FROM Uninstall WHERE name like 'CipherShed%'"
                cur.execute(query3_1_2)
                rows3_1_2 = cur.fetchall()
                if len(rows3_1_2)<1:
                    # 실행
                    query3_1_3 = "SELECT Executable_Name, Full_Path, datetime(Last_Executed1," + self.UTC + ") FROM Prefetch1 WHERE Executable_Name like 'CihperShed%'"
                    cur.execute(query3_1_3)
                    rows3_1_3 = cur.fetchall()
                else:
                    rows3_1_3 = ''
            else:
                rows3_1_2 = ''
                rows3_1_3 = ''
        except:
            rows3_1_1 = ''
            rows3_1_2 = ''
            rows3_1_3 = ''
            pass

        # 디스크 암호화 - TrueCrypt
        try:
            # 설치 + 실행
            query3_2_1 = "SELECT a.name, a.version, a.publisher, b.Full_Path, " \
                       "datetime(a.install_date," + self.UTC + "), datetime(b.Last_Executed1," + self.UTC + ") FROM Uninstall a, Prefetch1 b " \
                        "WHERE name like 'VeraCrypt%' AND Executable_Name likE 'TrueCrypt%'"
            cur.execute(query3_2_1)
            rows3_2_1 = cur.fetchall()
            if len(rows3_2_1) < 1:
                # 설치
                query3_2_2 = "SELECT name, version, publisher, install_location, datetime(install_date," + self.UTC + ") FROM Uninstall WHERE name like 'TrueCrypt%'"
                cur.execute(query3_2_2)
                rows3_2_2 = cur.fetchall()
                if len(rows3_2_2)<1:
                    # 실행
                    query3_2_3 = "SELECT Executable_Name, Full_Path, datetime(Last_Executed1," + self.UTC + ") FROM Prefetch1 WHERE Executable_Name like 'TrueCrypt%'"
                    cur.execute(query3_2_3)
                    rows3_2_3 = cur.fetchall()
                else:
                    rows3_2_3 = ''
            else:
                rows3_2_2 = ''
                rows3_2_3 = ''
        except:
            rows3_2_1 = ''
            rows3_2_2 = ''
            rows3_2_3 = ''
            pass

        # 디스크 암호화 - VeraCrypt
        try:
            # 설치 + 실행
            query3_3_1 = "SELECT a.name, a.version, b.Full_Path, a.publisher,  " \
                       "datetime(a.install_date," + self.UTC + "), datetime(b.Last_Executed1," + self.UTC + ") FROM Uninstall a, Prefetch1 b " \
                       "WHERE name like 'VeraCrypt%' AND Executable_Name likE 'VeraCrypt%'"
            cur.execute(query3_3_1)
            rows3_3_1 = cur.fetchall()

            if len(rows3_3_1) < 1:
                # 설치
                query3_3_2 = "SELECT name, version, publisher, install_location, datetime(install_date," + self.UTC + ") FROM Uninstall WHERE name like 'VeraCrypt%'"
                cur.execute(query3_3_2)
                rows3_3_2 = cur.fetchall()
                if len(rows3_3_2) < 1:
                    # 실행
                    query3_3_3 = "SELECT Executable_Name, Full_Path, datetime(Last_Executed1," + self.UTC + ") FROM Prefetch1 WHERE Executable_Name like 'VeraCrypt%'"
                    cur.execute(query3_3_3)
                    rows3_3_3 = cur.fetchall()
                else:
                    rows3_3_3 = ''
            else:
                rows3_3_2 = ''
                rows3_3_3 = ''

        except:
            rows3_3_1 = ''
            rows3_3_2 = ''
            rows3_3_3 = ''
            pass

        # 안티포렌식 - CCleaner
        try:
            # 설치 + 실행
            query4_1_1 = "SELECT a.name, a.version,  b.Full_Path, a.publisher," \
                       "datetime(a.install_date," + self.UTC + "), datetime(b.Last_Executed1," + self.UTC + ") FROM Uninstall a, Prefetch1 b " \
                       "WHERE name like 'CCleaner%' AND Executable_Name LIKE 'CCleaner%'"
            cur.execute(query4_1_1)
            rows4_1_1 = cur.fetchall()
            if len(rows4_1_1) < 1:
                # 설치
                query4_1_2 = "SELECT name, version,  install_location, publisher, datetime(install_date," + self.UTC + ") FROM Uninstall WHERE name like 'CCleaner%'"
                cur.execute(query4_1_2)
                rows4_1_2 = cur.fetchall()
                if len(rows4_1_2) < 1:
                    # 실행
                    query4_1_3 = "SELECT Executable_Name, Full_Path, datetime(Last_Executed1," + self.UTC + ") FROM Prefetch1 WHERE Executable_Name like 'CCleaner%'"
                    cur.execute(query4_1_3)
                    rows4_1_3 = cur.fetchall()
                else:
                    rows4_1_3 = ''
            else:
                rows4_1_2 = ''
                rows4_1_3 = ''
        except:
            rows4_1_1 = ''
            rows4_1_2 = ''
            rows4_1_3 = ''
            pass

        # 안티포렌식 - Cipher
        try:
            # 설치 + 실행
            query4_2_1 = "SELECT a.name, a.version, b.Full_Path, a.publisher, " \
                       "datetime(a.install_date," + self.UTC + "), datetime(b.Last_Executed1," + self.UTC + ") FROM Uninstall a, Prefetch1 b " \
                       "WHERE name like 'Cipher%' AND Executable_Name LIKE 'Cipher%'"
            cur.execute(query4_2_1)
            rows4_2_1 = cur.fetchall()
            if len(rows4_2_1) < 1:
                # 설치
                query4_2_2 = "SELECT name, version, install_location, publisher,  datetime(install_date," + self.UTC + ") FROM Uninstall WHERE name like 'Cipher%'"
                cur.execute(query4_2_2)
                rows4_2_2 = cur.fetchall()
                if len(rows4_2_2) < 1:
                    # 실행
                    query4_2_3 = "SELECT Executable_Name, Full_Path, datetime(Last_Executed1," + self.UTC + ") FROM Prefetch1 WHERE Executable_Name like 'Cipher%'"
                    cur.execute(query4_2_3)
                    rows4_2_3 = cur.fetchall()
                else:
                    rows4_2_3 = ''
            else:
                rows4_2_2 = ''
                rows4_2_3 = ''
        except:
            rows4_2_1 = ''
            rows4_2_2 = ''
            rows4_2_3 = ''
            pass

        # 안티포렌식 - Eraser
        try:
        # 설치 + 실행
            query4_3_1 = "SELECT a.name, a.version, b.Full_Path, a.publisher, " \
                       "datetime(a.install_date," + self.UTC + "), datetime(b.Last_Executed1," + self.UTC + ") FROM Uninstall a, Prefetch1 b " \
                       "WHERE name like 'Eraser%' AND Executable_Name LIKE 'Eraser%'"
            cur.execute(query4_3_1)
            rows4_3_1 = cur.fetchall()
            if len(rows4_3_1) < 1:
                # 설치
                query4_3_2 = "SELECT name, version, publisher, install_location, datetime(install_date," + self.UTC + ") FROM Uninstall WHERE name like 'Eraser%'"
                cur.execute(query4_3_2)
                rows4_3_2 = cur.fetchall()
                if len(rows4_3_2)<1:
                    # 실행
                    query4_3_3 = "SELECT Executable_Name, Full_Path, datetime(Last_Executed1," + self.UTC + ") FROM Prefetch1 WHERE Executable_Name like 'Eraser%'"
                    cur.execute(query4_3_3)
                    rows4_3_3 = cur.fetchall()
                else:
                    rows4_3_3 = ''
            else:
                rows4_3_2 = ''
                rows4_3_3 = ''
        except:
            rows4_3_1 = ''
            rows4_3_2 = ''
            rows4_3_3 = ''
            pass

        # 안티포렌식 - SDelete
        try:
            # 설치 + 실행
            query4_4_1 = "SELECT a.name, a.version,b.Full_Path,  a.publisher, " \
                       "datetime(a.install_date," + self.UTC + "), datetime(b.Last_Executed1," + self.UTC + ") FROM Uninstall a, Prefetch1 b " \
                       "WHERE name like 'SDelete%' AND Executable_Name LIKE 'SDelete%'"
            cur.execute(query4_4_1)
            rows4_4_1 = cur.fetchall()
            if len(rows4_4_1) < 1:
                # 설치
                query4_4_2 = "SELECT name, version, publisher, install_location, datetime(install_date," + self.UTC + ") FROM Uninstall WHERE name like 'SDelete%'"
                cur.execute(query4_4_2)
                rows4_4_2 = cur.fetchall()
                if len(rows4_4_2) < 1:
                    # 실행
                    query4_4_3 = "SELECT Executable_Name, Full_Path, datetime(Last_Executed1," + self.UTC + ") FROM Prefetch1 WHERE Executable_Name like 'SDelete%'"
                    cur.execute(query4_4_3)
                    rows4_4_3 = cur.fetchall()
                else:
                    rows4_4_3 = ''
            else:
                rows4_4_2 = ''
                rows4_4_3 = ''
        except:
            rows4_4_1 = ''
            rows4_4_2 = ''
            rows4_4_3 = ''
            pass

        # 안티포렌식 - TimeStomp
        try:
            # 설치 + 실행
            query4_5_1 = "SELECT a.name, a.version, b.Full_Path, a.publisher, " \
                       "datetime(a.install_date," + self.UTC + "), datetime(b.Last_Executed1," + self.UTC + ") FROM Uninstall a, Prefetch1 b " \
                       "WHERE name like 'TimeStomp%' AND Executable_Name LIKE 'TimeStomp%'"
            cur.execute(query4_5_1)
            rows4_5_1 = cur.fetchall()
            if len(rows4_5_1) < 1:
                # 설치
                query4_5_2 = "SELECT name, version, publisher, install_location, datetime(install_date," + self.UTC + ") FROM Uninstall WHERE name like 'TimeStomp%'"
                cur.execute(query4_5_2)
                rows4_5_2 = cur.fetchall()
                if len(rows4_5_2) < 1:
                    # 실행
                    query4_5_3 = "SELECT Executable_Name, Full_Path, datetime(Last_Executed1," + self.UTC + ") FROM Prefetch1 WHERE Executable_Name like 'TimeStomp%'"
                    cur.execute(query4_5_3)
                    rows4_5_3 = cur.fetchall()
                else:
                    rows4_5_3 = ''
            else:
                rows4_5_2 = ''
                rows4_5_3 = ''
        except:
            rows4_5_1 = ''
            rows4_5_2 = ''
            rows4_5_3 = ''
            pass

        # 안티포렌식 - Wise Folder Hider
        try:
            # 설치 + 실행
            query4_6_1 = "SELECT a.name, a.version, b.Full_Path, a.publisher," \
                       "datetime(a.install_date," + self.UTC + "), datetime(b.Last_Executed1," + self.UTC + ") FROM Uninstall a, Prefetch1 b " \
                       "WHERE name like 'Wise Folder Hider%' AND Executable_Name LIKE 'Wise Folder Hider%'"
            cur.execute(query4_6_1)
            rows4_6_1 = cur.fetchall()
            if len(rows4_6_1) < 1:
                # 설치
                query4_6_2 = "SELECT name, version, publisher, install_location, datetime(install_date," + self.UTC + ") FROM Uninstall WHERE name like 'Wise Folder Hider%'"
                cur.execute(query4_6_2)
                rows4_6_2 = cur.fetchall()
                if len(rows4_6_2) < 1:
                    # 실행
                    query4_6_3 = "SELECT Executable_Name, Full_Path, datetime(Last_Executed1," + self.UTC + ") FROM Prefetch1 WHERE Executable_Name like 'Wise Folder Hider%'"
                    cur.execute(query4_6_3)
                    rows4_6_3 = cur.fetchall()
                else:
                    rows4_6_3 = ''
            else:
                rows4_6_2 = ''
                rows4_6_3 = ''
        except:
            rows4_6_1 = ''
            rows4_6_2 = ''
            rows4_6_3 = ''
            pass


        # VM - virtualbox
        try:
            # 설치 + 실행
            query5_1_1 = "SELECT a.name, a.version, b.Full_Path, a.publisher," \
                         "datetime(a.install_date," + self.UTC + "), datetime(b.Last_Executed1," + self.UTC + ") FROM Uninstall a, Prefetch1 b " \
                         "WHERE name like '%virtualbox%' AND Executable_Name LIKE '%virtualbox%'"
            cur.execute(query5_1_1)
            rows5_1_1 = cur.fetchall()
            if len(rows5_1_1) < 1:
                # 설치
                query5_1_2 = "SELECT name, version, publisher, install_location, datetime(install_date," + self.UTC + ") FROM Uninstall WHERE name like '%virtualbox%'"
                cur.execute(query5_1_2)
                rows5_1_2 = cur.fetchall()
                if len(rows5_1_2) < 1:
                    # 실행
                    query5_1_3 = "SELECT Executable_Name, Full_Path, datetime(Last_Executed1," + self.UTC + ") FROM Prefetch1 WHERE Executable_Name like '%virtualbox%'"
                    cur.execute(query5_1_3)
                    rows5_1_3 = cur.fetchall()
                else:
                    rows5_1_3 = ''
            else:
                rows5_1_2 = ''
                rows5_1_3 = ''
        except:
            rows5_1_1 = ''
            rows5_1_2 = ''
            rows5_1_3 = ''
            pass

        # VM - VMWARE
        try:
            # 설치 + 실행
            query5_2_1 = "SELECT a.name, a.version, b.Full_Path, a.publisher," \
                         "datetime(a.install_date," + self.UTC + "), datetime(b.Last_Executed1," + self.UTC + ") FROM Uninstall a, Prefetch1 b " \
                         "WHERE name like '%VMWARE%' AND Executable_Name LIKE '%VMWARE%'"
            cur.execute(query5_2_1)
            rows5_2_1 = cur.fetchall()
            if len(rows5_2_1) < 1:
                # 설치
                query5_2_2 = "SELECT name, version, publisher, install_location, datetime(install_date," + self.UTC + ") FROM Uninstall WHERE name like '%VMWARE%'"
                cur.execute(query5_2_2)
                rows5_2_2 = cur.fetchall()
                if len(rows5_2_2) < 1:
                    # 실행
                    query5_2_3 = "SELECT Executable_Name, Full_Path, datetime(Last_Executed1," + self.UTC + ") FROM Prefetch1 WHERE Executable_Name like '%VMWARE%'"
                    cur.execute(query5_2_3)
                    rows5_2_3 = cur.fetchall()
                else:
                    rows5_2_3 = ''
            else:
                rows5_2_2 = ''
                rows5_2_3 = ''
        except:
            rows5_2_1 = ''
            rows5_2_2 = ''
            rows5_2_3 = ''
            pass

    # 삭제 여부 확인
        query3_1 ="SELECT is_in_use from parsed_MFT WHERE file_path like '%CipherShed.exe' and src='File record'"
        cur.execute(query3_1)
        del3_1 = cur.fetchall()
        if (len(del3_1))<1:
            del3_1 = [('?')]

        query3_2 = "SELECT is_in_use from parsed_MFT WHERE file_path like '%TrueCrypt.exe' and src='File record'"
        cur.execute(query3_2)
        del3_2 = cur.fetchall()
        if (len(del3_2)) < 1:
            del3_2 = [('?')]

        query3_3 = "SELECT is_in_use from parsed_MFT WHERE file_path like '%VeraCrypt.exe' and src='File record'"
        cur.execute(query3_3)
        del3_3 = cur.fetchall()
        if(len(del3_3)) < 1:
            del3_3 = [('?')]

        query4_1 = "SELECT is_in_use from parsed_MFT WHERE file_path like '%CCleaner.exe' and src='File record'"
        cur.execute(query4_1)
        del4_1 = cur.fetchall()
        if(len(del4_1)) < 1:
            del4_1 = [('?')]

        query4_2 = "SELECT is_in_use from parsed_MFT WHERE file_path like '%Cipher.exe' and src='File record'"
        cur.execute(query4_2)
        del4_2 = cur.fetchall()
        if(len(del4_2)) < 1:
            del4_2 = [('?')]

        query4_3 = "SELECT is_in_use from parsed_MFT WHERE file_path like '%Eraser.exe' and src='File record'"
        cur.execute(query4_3)
        del4_3 = cur.fetchall()
        if(len(del4_3)) < 1:
            del4_3 = [('?')]

        query4_4 = "SELECT is_in_use from parsed_MFT WHERE file_path like '%SDelete.exe' and src='File record'"
        cur.execute(query4_4)
        del4_4 = cur.fetchall()
        if(len(del4_4)) < 1:
            del4_4 = [('?')]

        query4_5 = "SELECT is_in_use from parsed_MFT WHERE file_path like '%TimeStomp.exe' and src='File record'"
        cur.execute(query4_5)
        del4_5 = cur.fetchall()
        if(len(del4_5)) < 1:
            del4_5 = [('?')]

        query4_6 = "SELECT is_in_use from parsed_MFT WHERE file_path like '%Wise Folder Hider.exe' and src='File record'"
        cur.execute(query4_6)
        del4_6 = cur.fetchall()
        if(len(del4_6)) < 1:
            del4_6 = [('?')]

        query5_1 = "SELECT is_in_use from parsed_MFT WHERE file_path like '%VirtualBox.exe' and src='File record'"
        cur.execute(query5_1)
        del5_1 = cur.fetchall()
        if(len(del5_1)) < 1:
            del5_1 = [('?')]

        query5_2 = "SELECT is_in_use from parsed_MFT WHERE file_path like '%VMWare.exe' and src='File record'"
        cur.execute(query5_2)
        del5_2 = cur.fetchall()
        if(len(del5_2)) < 1:
            del5_2 = [('?')]

        self.tab2_table = QTableWidget(self)
        count = len(rows1_1_1) + len(rows1_1_2) + len(rows1_1_3) \
                + len(rows1_2_1) + len(rows1_2_2) + len(rows1_2_3) \
                + len(rows1_3_1) + len(rows1_3_2) + len(rows1_3_3) \
                + len(rows1_4_1) + len(rows1_4_2) + len(rows1_4_3) \
                + len(symantec)\
                + len(rows3_1_1) + len(rows3_1_2) + len(rows3_1_3) \
                + len(rows3_2_1) + len(rows3_2_2) + len(rows3_2_3) \
                + len(rows3_3_1) + len(rows3_3_2) + len(rows3_3_3) \
                + len(rows4_1_1) + len(rows4_1_2) + len(rows4_1_3) \
                + len(rows4_2_1) + len(rows4_2_2) + len(rows4_2_3) \
                + len(rows4_3_1) + len(rows4_3_2) + len(rows4_3_3) \
                + len(rows4_4_1) + len(rows4_4_2) + len(rows4_4_3) \
                + len(rows4_5_1) + len(rows4_5_2) + len(rows4_5_3) \
                + len(rows4_6_1) + len(rows4_6_2) + len(rows4_6_3) \
                + len(rows5_1_1) + len(rows5_1_2) + len(rows5_1_3) \
                + len(rows5_2_1) + len(rows5_2_2) + len(rows5_2_3) \
                + 5

        self.tab2_table.setRowCount(count)
        self.tab2_table.setColumnCount(8)
        column_headers = ["", "프로그램", "버전", "설치 경로", "제조사", "설치 시각", "실행 시각", "존재 여부"]
        self.tab2_table.setHorizontalHeaderLabels(column_headers)
        tab2_accum = 0

        # DRM
        self.color_tab2_table("DRM", tab2_accum)
        try:
            if len(rows1_1_1) >= 1:
                # 설치 + 실행
                for i in range(len(rows1_1_1)):
                    name, version, Full_Path, publisher, install_date, Last_Executed1 = rows1_1_1[i]
                    self.tab2_table.setItem(i + tab2_accum + 1, 1, QTableWidgetItem(name))
                    self.tab2_table.setItem(i + tab2_accum + 1, 2, QTableWidgetItem(version))
                    self.tab2_table.setItem(i + tab2_accum + 1, 3, QTableWidgetItem(Full_Path))
                    self.tab2_table.setItem(i + tab2_accum + 1, 4, QTableWidgetItem(publisher))
                    self.tab2_table.setItem(i + tab2_accum + 1, 5, QTableWidgetItem(install_date))
                    self.tab2_table.setItem(i + tab2_accum + 1, 6, QTableWidgetItem(Last_Executed1))
                rows1_1 = rows1_1_1
            elif len(rows1_1_2) >= 1:
                # 설치
                for i in range(len(rows1_1_2)):
                    name, version, publisher, install_location, install_date = rows1_1_2[i]
                    self.tab2_table.setItem(i + tab2_accum + 1, 1, QTableWidgetItem(name))
                    self.tab2_table.setItem(i + tab2_accum + 1, 2, QTableWidgetItem(version))
                    self.tab2_table.setItem(i + tab2_accum + 1, 3, QTableWidgetItem(publisher))
                    self.tab2_table.setItem(i + tab2_accum + 1, 4, QTableWidgetItem(install_location))
                    self.tab2_table.setItem(i + tab2_accum + 1, 5, QTableWidgetItem(install_date))
                rows1_1 = rows1_1_2
            elif len(rows1_1_3) >= 1:
                # 실행
                for i in range(len(rows1_1_3)):
                    Executable_Name, Full_Path, Last_Executed1 = rows1_1_3[i]
                    self.tab2_table.setItem(i + tab2_accum + 1, 1, QTableWidgetItem(Executable_Name))
                    self.tab2_table.setItem(i + tab2_accum + 1, 3, QTableWidgetItem(Full_Path))
                    self.tab2_table.setItem(i + tab2_accum + 1, 6, QTableWidgetItem(Last_Executed1))
                rows1_1 = rows1_1_3
            else:
                rows1_1 = ''
        except:
            pass
        tab2_accum = tab2_accum + len(rows1_1)

        try:
            if len(rows1_2_1) >= 1:
                # 설치 + 실행
                for i in range(len(rows1_2_1)):
                    name, version, Full_Path, publisher, install_date, Last_Executed1 = rows1_2_1[i]
                    self.tab2_table.setItem(i + tab2_accum + 1, 1, QTableWidgetItem(name))
                    self.tab2_table.setItem(i + tab2_accum + 1, 2, QTableWidgetItem(version))
                    self.tab2_table.setItem(i + tab2_accum + 1, 3, QTableWidgetItem(Full_Path))
                    self.tab2_table.setItem(i + tab2_accum + 1, 4, QTableWidgetItem(publisher))
                    self.tab2_table.setItem(i + tab2_accum + 1, 5, QTableWidgetItem(install_date))
                    self.tab2_table.setItem(i + tab2_accum + 1, 6, QTableWidgetItem(Last_Executed1))
                rows1_2 = rows1_2_1
            elif len(rows1_2_2) >= 1:
                # 설치
                for i in range(len(rows1_2_2)):
                    name, version, publisher, install_location, install_date = rows1_2_2[i]
                    self.tab2_table.setItem(i + tab2_accum + 1, 1, QTableWidgetItem(name))
                    self.tab2_table.setItem(i + tab2_accum + 1, 2, QTableWidgetItem(version))
                    self.tab2_table.setItem(i + tab2_accum + 1, 3, QTableWidgetItem(publisher))
                    self.tab2_table.setItem(i + tab2_accum + 1, 4, QTableWidgetItem(install_location))
                    self.tab2_table.setItem(i + tab2_accum + 1, 5, QTableWidgetItem(install_date))
                rows1_2 = rows1_2_2
            elif len(rows1_2_3) >= 1:
                # 실행
                for i in range(len(rows1_2_3)):
                    Executable_Name, Full_Path, Last_Executed1 = rows1_2_3[i]
                    self.tab2_table.setItem(i + tab2_accum + 1, 1, QTableWidgetItem(Executable_Name))
                    self.tab2_table.setItem(i + tab2_accum + 1, 3, QTableWidgetItem(Full_Path))
                    self.tab2_table.setItem(i + tab2_accum + 1, 6, QTableWidgetItem(Last_Executed1))
                rows1_2 = rows1_2_3
            else:
                rows1_2 = ''
        except:
            pass
        tab2_accum = tab2_accum + len(rows1_2)

        try:
            if len(rows1_3_1) >= 1:
                # 설치 + 실행
                for i in range(len(rows1_3_1)):
                    name, version, Full_Path, publisher, install_date, Last_Executed1 = rows1_3_1[i]
                    self.tab2_table.setItem(i + tab2_accum + 1, 1, QTableWidgetItem(name))
                    self.tab2_table.setItem(i + tab2_accum + 1, 2, QTableWidgetItem(version))
                    self.tab2_table.setItem(i + tab2_accum + 1, 3, QTableWidgetItem(Full_Path))
                    self.tab2_table.setItem(i + tab2_accum + 1, 4, QTableWidgetItem(publisher))
                    self.tab2_table.setItem(i + tab2_accum + 1, 5, QTableWidgetItem(install_date))
                    self.tab2_table.setItem(i + tab2_accum + 1, 6, QTableWidgetItem(Last_Executed1))
                rows1_3 = rows1_3_1
            elif len(rows1_3_2) >= 1:
                # 설치
                for i in range(len(rows1_3_2)):
                    name, version, publisher, install_location, install_date = rows1_3_2[i]
                    self.tab2_table.setItem(i + tab2_accum + 1, 1, QTableWidgetItem(name))
                    self.tab2_table.setItem(i + tab2_accum + 1, 2, QTableWidgetItem(version))
                    self.tab2_table.setItem(i + tab2_accum + 1, 3, QTableWidgetItem(publisher))
                    self.tab2_table.setItem(i + tab2_accum + 1, 4, QTableWidgetItem(install_location))
                    self.tab2_table.setItem(i + tab2_accum + 1, 5, QTableWidgetItem(install_date))
                rows1_3 = rows1_3_2
            elif len(rows1_3_3) >= 1:
                # 실행
                for i in range(len(rows1_3_3)):
                    Executable_Name, Full_Path, Last_Executed1 = rows1_3_3[i]
                    self.tab2_table.setItem(i + tab2_accum + 1, 1, QTableWidgetItem(Executable_Name))
                    self.tab2_table.setItem(i + tab2_accum + 1, 3, QTableWidgetItem(Full_Path))
                    self.tab2_table.setItem(i + tab2_accum + 1, 6, QTableWidgetItem(Last_Executed1))
                rows1_3 = rows1_3_3
            else:
                rows1_3 = ''
        except:
            pass
        tab2_accum = tab2_accum + len(rows1_3)

        try:
            if len(rows1_4_1) >= 1:
                # 설치 + 실행
                for i in range(len(rows1_4_1)):
                    name, version, Full_Path, publisher, install_date, Last_Executed1 = rows1_4_1[i]
                    self.tab2_table.setItem(i + tab2_accum + 1, 1, QTableWidgetItem(name))
                    self.tab2_table.setItem(i + tab2_accum + 1, 2, QTableWidgetItem(version))
                    self.tab2_table.setItem(i + tab2_accum + 1, 3, QTableWidgetItem(Full_Path))
                    self.tab2_table.setItem(i + tab2_accum + 1, 4, QTableWidgetItem(publisher))
                    self.tab2_table.setItem(i + tab2_accum + 1, 5, QTableWidgetItem(install_date))
                    self.tab2_table.setItem(i + tab2_accum + 1, 6, QTableWidgetItem(Last_Executed1))
                rows1_4 = rows1_4_1
            elif len(rows1_4_2) >= 1:
                # 설치
                for i in range(len(rows1_4_2)):
                    name, version, publisher, install_location, install_date = rows1_4_2[i]
                    self.tab2_table.setItem(i + tab2_accum + 1, 1, QTableWidgetItem(name))
                    self.tab2_table.setItem(i + tab2_accum + 1, 2, QTableWidgetItem(version))
                    self.tab2_table.setItem(i + tab2_accum + 1, 3, QTableWidgetItem(publisher))
                    self.tab2_table.setItem(i + tab2_accum + 1, 4, QTableWidgetItem(install_location))
                    self.tab2_table.setItem(i + tab2_accum + 1, 5, QTableWidgetItem(install_date))
                rows1_4 = rows1_4_2
            elif len(rows1_4_3) >= 1:
                # 실행
                for i in range(len(rows1_4_3)):
                    Executable_Name, Full_Path, Last_Executed1 = rows1_4_3[i]
                    self.tab2_table.setItem(i + tab2_accum + 1, 1, QTableWidgetItem(Executable_Name))
                    self.tab2_table.setItem(i + tab2_accum + 1, 3, QTableWidgetItem(Full_Path))
                    self.tab2_table.setItem(i + tab2_accum + 1, 6, QTableWidgetItem(Last_Executed1))
                rows1_4 = rows1_4_3
            else:
                rows1_4 = ''
        except:
            pass
        tab2_accum = tab2_accum + len(rows1_4) + 1

        # 매체제어
        self.color_tab2_table("매체제어", tab2_accum)
        try:
            program, execute = symantec
            self.tab2_table.setItem(tab2_accum + 1, 1, QTableWidgetItem(program))
            self.tab2_table.setItem(tab2_accum + 1, 3, QTableWidgetItem(execute))
        except:
            pass
        tab2_accum = tab2_accum + len(symantec) + 1

        # 디스크 암호화
        self.color_tab2_table("디스크 암호화", tab2_accum)
        try:
            if len(rows3_1_1) >= 1:
                # 설치 + 실행
                for i in range(len(rows3_1_1)):
                    name, version, Full_Path, publisher, install_date, Last_Executed1 = rows3_1_1[i]
                    self.tab2_table.setItem(i + tab2_accum + 1, 1, QTableWidgetItem(name))
                    self.tab2_table.setItem(i + tab2_accum + 1, 2, QTableWidgetItem(version))
                    self.tab2_table.setItem(i + tab2_accum + 1, 3, QTableWidgetItem(Full_Path))
                    self.tab2_table.setItem(i + tab2_accum + 1, 4, QTableWidgetItem(publisher))
                    self.tab2_table.setItem(i + tab2_accum + 1, 5, QTableWidgetItem(install_date))
                    self.tab2_table.setItem(i + tab2_accum + 1, 6, QTableWidgetItem(Last_Executed1))
                    self.tab2_table.setItem(i + tab2_accum + 1, 7, QTableWidgetItem(del3_1[0]))
                rows3_1 = rows3_1_1
            elif len(rows3_1_2) >= 1:
                # 설치
                for i in range(len(rows3_1_2)):
                    name, version, publisher, install_location, install_date = rows3_1_2[i]
                    self.tab2_table.setItem(i + tab2_accum + 1, 1, QTableWidgetItem(name))
                    self.tab2_table.setItem(i + tab2_accum + 1, 2, QTableWidgetItem(version))
                    self.tab2_table.setItem(i + tab2_accum + 1, 3, QTableWidgetItem(publisher))
                    self.tab2_table.setItem(i + tab2_accum + 1, 4, QTableWidgetItem(install_location))
                    self.tab2_table.setItem(i + tab2_accum + 1, 5, QTableWidgetItem(install_date))
                    self.tab2_table.setItem(i + tab2_accum + 1, 7, QTableWidgetItem(del3_1[0]))
                rows3_1 = rows3_1_2
            elif len(rows3_1_3) >=1:
                # 실행
                for i in range(len(rows3_1_3)):
                    Executable_Name, Full_Path, Last_Executed1 = rows3_1_3[i]
                    self.tab2_table.setItem(i + tab2_accum + 1, 1, QTableWidgetItem(Executable_Name))
                    self.tab2_table.setItem(i + tab2_accum + 1, 3, QTableWidgetItem(Full_Path))
                    self.tab2_table.setItem(i + tab2_accum + 1, 6, QTableWidgetItem(Last_Executed1))
                    self.tab2_table.setItem(i + tab2_accum + 1, 7, QTableWidgetItem(del3_1[0][0]))
                rows3_1 = rows3_1_3
            else:
                rows3_1 = ''

        except:
            rows3_1 = ''
            pass
        tab2_accum = tab2_accum + len(rows3_1)

        try:
            if len(rows3_2_1) >= 1:
                # 설치 + 실행
                for i in range(len(rows3_2_1)):
                    name, version, Full_Path, publisher, install_date, Last_Executed1 = rows3_2_1[i]
                    self.tab2_table.setItem(i + tab2_accum + 1, 1, QTableWidgetItem(name))
                    self.tab2_table.setItem(i + tab2_accum + 1, 2, QTableWidgetItem(version))
                    self.tab2_table.setItem(i + tab2_accum + 1, 3, QTableWidgetItem(Full_Path))
                    self.tab2_table.setItem(i + tab2_accum + 1, 4, QTableWidgetItem(publisher))
                    self.tab2_table.setItem(i + tab2_accum + 1, 5, QTableWidgetItem(install_date))
                    self.tab2_table.setItem(i + tab2_accum + 1, 6, QTableWidgetItem(Last_Executed1))
                    self.tab2_table.setItem(i + tab2_accum + 1, 7, QTableWidgetItem(del3_2[0][0]))
                rows3_2 = rows3_2_1
            elif len(rows3_2_2) >= 1:
                # 설치
                for i in range(len(rows3_2_2)):
                    name, version, publisher, install_location, install_date = rows3_2_2[i]
                    self.tab2_table.setItem(i + tab2_accum + 1, 1, QTableWidgetItem(name))
                    self.tab2_table.setItem(i + tab2_accum + 1, 2, QTableWidgetItem(version))
                    self.tab2_table.setItem(i + tab2_accum + 1, 3, QTableWidgetItem(publisher))
                    self.tab2_table.setItem(i + tab2_accum + 1, 4, QTableWidgetItem(install_location))
                    self.tab2_table.setItem(i + tab2_accum + 1, 5, QTableWidgetItem(install_date))
                    self.tab2_table.setItem(i + tab2_accum + 1, 7, QTableWidgetItem(del3_2[0][0]))
                rows3_2 = rows3_2_2
            elif len(rows3_2_3) >= 1:
                # 실행
                for i in range(len(rows3_2_3)):
                    Executable_Name, Full_Path, Last_Executed1 = rows3_2_3[i]
                    self.tab2_table.setItem(i + tab2_accum + 1, 1, QTableWidgetItem(Executable_Name))
                    self.tab2_table.setItem(i + tab2_accum + 1, 3, QTableWidgetItem(Full_Path))
                    self.tab2_table.setItem(i + tab2_accum + 1, 6, QTableWidgetItem(Last_Executed1))
                    self.tab2_table.setItem(i + tab2_accum + 1, 7, QTableWidgetItem(del3_2[0][0]))
                rows3_2 = rows3_2_3
            else:
                rows3_2 = ''

        except:
            rows3_2 = ''
            pass
        tab2_accum = tab2_accum + len(rows3_2)

        try:
            if len(rows3_3_1) >= 1:
                # 설치 + 실행
                for i in range(len(rows3_3_1)):
                    name, version, Full_Path, publisher, install_date, Last_Executed1 = rows3_3_1[i]
                    self.tab2_table.setItem(i + tab2_accum + 1, 1, QTableWidgetItem(name))
                    self.tab2_table.setItem(i + tab2_accum + 1, 2, QTableWidgetItem(version))
                    self.tab2_table.setItem(i + tab2_accum + 1, 3, QTableWidgetItem(Full_Path))
                    self.tab2_table.setItem(i + tab2_accum + 1, 4, QTableWidgetItem(publisher))
                    self.tab2_table.setItem(i + tab2_accum + 1, 5, QTableWidgetItem(install_date))
                    self.tab2_table.setItem(i + tab2_accum + 1, 6, QTableWidgetItem(Last_Executed1))
                    self.tab2_table.setItem(i + tab2_accum + 1, 7, QTableWidgetItem(del3_3[0][0]))
                rows3_3 = rows3_3_1
            elif len(rows3_3_2) >= 1:
                # 설치
                for i in range(len(rows3_3_2)):
                    name, version, publisher, install_location, install_date = rows3_3_2[i]
                    self.tab2_table.setItem(i + tab2_accum + 1, 1, QTableWidgetItem(name))
                    self.tab2_table.setItem(i + tab2_accum + 1, 2, QTableWidgetItem(version))
                    self.tab2_table.setItem(i + tab2_accum + 1, 3, QTableWidgetItem(publisher))
                    self.tab2_table.setItem(i + tab2_accum + 1, 4, QTableWidgetItem(install_location))
                    self.tab2_table.setItem(i + tab2_accum + 1, 5, QTableWidgetItem(install_date))
                    self.tab2_table.setItem(i + tab2_accum + 1, 7, QTableWidgetItem(del3_3[0][0]))
                rows3_3 = rows3_3_2
            elif len(rows3_3_3) >= 1:
                #실행
                for i in range(len(rows3_3_3)):
                    Executable_Name, Full_Path, Last_Executed1 = rows3_3_3[i]
                    self.tab2_table.setItem(i + tab2_accum + 1, 1, QTableWidgetItem(Executable_Name))
                    self.tab2_table.setItem(i + tab2_accum + 1, 3, QTableWidgetItem(Full_Path))
                    self.tab2_table.setItem(i + tab2_accum + 1, 6, QTableWidgetItem(Last_Executed1))
                    self.tab2_table.setItem(i + tab2_accum + 1, 7, QTableWidgetItem(del3_3[0][0]))
                rows3_3 = rows3_3_3
            else:
                rows3_3 = ''
        except:
            rows3_3 = ''
            pass
        tab2_accum = tab2_accum + len(rows3_3) + 1

        # 안티포렌식
        self.color_tab2_table("안티포렌식", tab2_accum)
        try:
            if len(rows4_1_1) >= 1:
                # 설치 + 실행
                for i in range(len(rows4_1_1)):
                    name, version, Full_Path, publisher, install_date, Last_Executed1 = rows4_1_1[i]
                    self.tab2_table.setItem(i + tab2_accum + 1, 1, QTableWidgetItem(name))
                    self.tab2_table.setItem(i + tab2_accum + 1, 2, QTableWidgetItem(version))
                    self.tab2_table.setItem(i + tab2_accum + 1, 3, QTableWidgetItem(Full_Path))
                    self.tab2_table.setItem(i + tab2_accum + 1, 4, QTableWidgetItem(publisher))
                    self.tab2_table.setItem(i + tab2_accum + 1, 5, QTableWidgetItem(install_date))
                    self.tab2_table.setItem(i + tab2_accum + 1, 6, QTableWidgetItem(Last_Executed1))
                    self.tab2_table.setItem(i + tab2_accum + 1, 7, QTableWidgetItem(del4_1[0][0]))
                rows4_1 = rows4_1_1
            elif len(rows4_1_2) >= 1:
                # 설치
                for i in range(len(rows4_1_2)):
                    name, version, install_location, publisher, install_date = rows4_1_2[i]
                    self.tab2_table.setItem(i + tab2_accum + 1, 1, QTableWidgetItem(name))
                    self.tab2_table.setItem(i + tab2_accum + 1, 2, QTableWidgetItem(version))
                    self.tab2_table.setItem(i + tab2_accum + 1, 3, QTableWidgetItem(install_location))
                    self.tab2_table.setItem(i + tab2_accum + 1, 4, QTableWidgetItem(publisher))
                    self.tab2_table.setItem(i + tab2_accum + 1, 5, QTableWidgetItem(install_date))
                    self.tab2_table.setItem(i + tab2_accum + 1, 7, QTableWidgetItem(del4_1[0][0]))
                rows4_1 = rows4_1_2
            elif len(rows4_1_3) >= 1:
                # 실행
                for i in range(len(rows4_1_3)):
                    Executable_Name, Full_Path, Last_Executed1 = rows4_1_3[i]
                    self.tab2_table.setItem(i + tab2_accum + 1, 1, QTableWidgetItem(Executable_Name))
                    self.tab2_table.setItem(i + tab2_accum + 1, 3, QTableWidgetItem(Full_Path))
                    self.tab2_table.setItem(i + tab2_accum + 1, 6, QTableWidgetItem(Last_Executed1))
                    self.tab2_table.setItem(i + tab2_accum + 1, 7, QTableWidgetItem(del4_1[0][0]))
                rows4_1 = rows4_1_3
            else:
                rows4_1 = ''

        except:
            rows4_1 = ''
            pass
        tab2_accum = tab2_accum + len(rows4_1)

        try:
            if len(rows4_2_1) >= 1:
                # 설치 + 실행
                for i in range(len(rows4_2_1)):
                    name, version, Full_Path, publisher, install_date, Last_Executed1 = rows4_2_1[i]
                    self.tab2_table.setItem(i + tab2_accum + 1, 1, QTableWidgetItem(name))
                    self.tab2_table.setItem(i + tab2_accum + 1, 2, QTableWidgetItem(version))
                    self.tab2_table.setItem(i + tab2_accum + 1, 3, QTableWidgetItem(Full_Path))
                    self.tab2_table.setItem(i + tab2_accum + 1, 4, QTableWidgetItem(publisher))
                    self.tab2_table.setItem(i + tab2_accum + 1, 5, QTableWidgetItem(install_date))
                    self.tab2_table.setItem(i + tab2_accum + 1, 6, QTableWidgetItem(Last_Executed1))
                    self.tab2_table.setItem(i + tab2_accum + 1, 7, QTableWidgetItem(del4_2[0][0]))
                rows4_2 = rows4_2_1
            elif len(rows4_2_2) >= 1:
                # 설치
                for i in range(len(rows4_2_2)):
                    name, version, publisher, install_location, install_date = rows4_2_2[i]
                    self.tab2_table.setItem(i + tab2_accum + 1, 1, QTableWidgetItem(name))
                    self.tab2_table.setItem(i + tab2_accum + 1, 2, QTableWidgetItem(version))
                    self.tab2_table.setItem(i + tab2_accum + 1, 3, QTableWidgetItem(publisher))
                    self.tab2_table.setItem(i + tab2_accum + 1, 4, QTableWidgetItem(install_location))
                    self.tab2_table.setItem(i + tab2_accum + 1, 5, QTableWidgetItem(install_date))
                    self.tab2_table.setItem(i + tab2_accum + 1, 7, QTableWidgetItem(del4_2[0][0]))
                rows4_2 = rows4_2_2
            elif len(rows4_2_3) >= 1:
                # 실행
                for i in range(len(rows4_2_3)):
                    Executable_Name, Full_Path, Last_Executed1 = rows4_2_3[i]
                    self.tab2_table.setItem(i + tab2_accum + 1, 1, QTableWidgetItem(Executable_Name))
                    self.tab2_table.setItem(i + tab2_accum + 1, 3, QTableWidgetItem(Full_Path))
                    self.tab2_table.setItem(i + tab2_accum + 1, 6, QTableWidgetItem(Last_Executed1))
                    self.tab2_table.setItem(i + tab2_accum + 1, 7, QTableWidgetItem(del4_2[0][0]))
                rows4_2 = rows4_2_3
            else:
                rows4_2 = ''

        except:
            rows4_2 = ''
            pass
        tab2_accum = tab2_accum + len(rows4_2)

        try:
            if len(rows4_3_1) >= 1:
                # 설치 + 실행
                for i in range(len(rows4_3_1)):
                    name, version, Full_Path, publisher, install_date, Last_Executed1 = rows4_3_1[i]
                    self.tab2_table.setItem(i + tab2_accum + 1, 1, QTableWidgetItem(name))
                    self.tab2_table.setItem(i + tab2_accum + 1, 2, QTableWidgetItem(version))
                    self.tab2_table.setItem(i + tab2_accum + 1, 3, QTableWidgetItem(Full_Path))
                    self.tab2_table.setItem(i + tab2_accum + 1, 4, QTableWidgetItem(publisher))
                    self.tab2_table.setItem(i + tab2_accum + 1, 5, QTableWidgetItem(install_date))
                    self.tab2_table.setItem(i + tab2_accum + 1, 6, QTableWidgetItem(Last_Executed1))
                    self.tab2_table.setItem(i + tab2_accum + 1, 7, QTableWidgetItem(del4_3[0][0]))
                rows4_3 = rows4_3_1
            elif len(rows4_3_2) >= 1:
                # 설치
                for i in range(len(rows4_3_2)):
                    name, version, publisher, install_location, install_date = rows4_3_2[i]
                    self.tab2_table.setItem(i + tab2_accum + 1, 1, QTableWidgetItem(name))
                    self.tab2_table.setItem(i + tab2_accum + 1, 2, QTableWidgetItem(version))
                    self.tab2_table.setItem(i + tab2_accum + 1, 3, QTableWidgetItem(publisher))
                    self.tab2_table.setItem(i + tab2_accum + 1, 4, QTableWidgetItem(install_location))
                    self.tab2_table.setItem(i + tab2_accum + 1, 5, QTableWidgetItem(install_date))
                    self.tab2_table.setItem(i + tab2_accum + 1, 7, QTableWidgetItem(del4_3[0][0]))
                rows4_3 = rows4_3_2
            elif len(rows4_3_3) >= 1:
                # 실행
                for i in range(len(rows4_3_3)):
                    Executable_Name, Full_Path, Last_Executed1 = rows4_3_3[i]
                    self.tab2_table.setItem(i + tab2_accum + 1, 1, QTableWidgetItem(Executable_Name))
                    self.tab2_table.setItem(i + tab2_accum + 1, 3, QTableWidgetItem(Full_Path))
                    self.tab2_table.setItem(i + tab2_accum + 1, 6, QTableWidgetItem(Last_Executed1))
                    self.tab2_table.setItem(i + tab2_accum + 1, 7, QTableWidgetItem(del4_3[0][0]))
                rows4_3 = rows4_3_3
            else:
                rows4_3 = ''
        except:
            rows4_3 = ''
            pass
        tab2_accum = tab2_accum + len(rows4_3)

        try:
            if len(rows4_4_1) >= 1:
                # 설치 + 실행
                for i in range(len(rows4_4_1)):
                    name, version, Full_Path, publisher, install_date, Last_Executed1 = rows4_4_1[i]
                    self.tab2_table.setItem(i + tab2_accum + 1, 1, QTableWidgetItem(name))
                    self.tab2_table.setItem(i + tab2_accum + 1, 2, QTableWidgetItem(version))
                    self.tab2_table.setItem(i + tab2_accum + 1, 3, QTableWidgetItem(Full_Path))
                    self.tab2_table.setItem(i + tab2_accum + 1, 4, QTableWidgetItem(publisher))
                    self.tab2_table.setItem(i + tab2_accum + 1, 5, QTableWidgetItem(install_date))
                    self.tab2_table.setItem(i + tab2_accum + 1, 6, QTableWidgetItem(Last_Executed1))
                    self.tab2_table.setItem(i + tab2_accum + 1, 7, QTableWidgetItem(del4_4[0][0]))
                rows4_4 = rows4_4_1
            elif len(rows4_4_2) >= 1:
                # 설치
                for i in range(len(rows4_4_2)):
                    name, version, publisher, install_location, install_date = rows4_4_2[i]
                    self.tab2_table.setItem(i + tab2_accum + 1, 1, QTableWidgetItem(name))
                    self.tab2_table.setItem(i + tab2_accum + 1, 2, QTableWidgetItem(version))
                    self.tab2_table.setItem(i + tab2_accum + 1, 3, QTableWidgetItem(publisher))
                    self.tab2_table.setItem(i + tab2_accum + 1, 4, QTableWidgetItem(install_location))
                    self.tab2_table.setItem(i + tab2_accum + 1, 5, QTableWidgetItem(install_date))
                    self.tab2_table.setItem(i + tab2_accum + 1, 7, QTableWidgetItem(del4_4[0][0]))
                rows4_4 = rows4_4_2
            elif len(rows4_4_3) >= 1:
                # 실행
                for i in range(len(rows4_4_3)):
                    Executable_Name, Full_Path, Last_Executed1 = rows4_4_3[i]
                    self.tab2_table.setItem(i + tab2_accum + 1, 1, QTableWidgetItem(Executable_Name))
                    self.tab2_table.setItem(i + tab2_accum + 1, 3, QTableWidgetItem(Full_Path))
                    self.tab2_table.setItem(i + tab2_accum + 1, 6, QTableWidgetItem(Last_Executed1))
                    self.tab2_table.setItem(i + tab2_accum + 1, 7, QTableWidgetItem(del4_4[0][0]))
                rows4_4 = rows4_4_3
            else:
                rows4_4 = ''

        except:
            rows4_4 = ''
            pass
        tab2_accum = tab2_accum + len(rows4_4)

        try:
            if len(rows4_5_1) >= 1:
                # 설치 + 실행
                for i in range(len(rows4_5_1)):
                    name, version, Full_Path, publisher, install_date, Last_Executed1 = rows4_5_1[i]
                    self.tab2_table.setItem(i + tab2_accum + 1, 1, QTableWidgetItem(name))
                    self.tab2_table.setItem(i + tab2_accum + 1, 2, QTableWidgetItem(version))
                    self.tab2_table.setItem(i + tab2_accum + 1, 3, QTableWidgetItem(Full_Path))
                    self.tab2_table.setItem(i + tab2_accum + 1, 4, QTableWidgetItem(publisher))
                    self.tab2_table.setItem(i + tab2_accum + 1, 5, QTableWidgetItem(install_date))
                    self.tab2_table.setItem(i + tab2_accum + 1, 6, QTableWidgetItem(Last_Executed1))
                    self.tab2_table.setItem(i + tab2_accum + 1, 7, QTableWidgetItem(del4_5[0][0]))
                rows4_5 = rows4_5_1
            elif len(rows4_5_2) >= 1:
                # 설치
                for i in range(len(rows4_5_2)):
                    name, version, publisher, install_location, install_date = rows4_5_2[i]
                    self.tab2_table.setItem(i + tab2_accum + 1, 1, QTableWidgetItem(name))
                    self.tab2_table.setItem(i + tab2_accum + 1, 2, QTableWidgetItem(version))
                    self.tab2_table.setItem(i + tab2_accum + 1, 3, QTableWidgetItem(publisher))
                    self.tab2_table.setItem(i + tab2_accum + 1, 4, QTableWidgetItem(install_location))
                    self.tab2_table.setItem(i + tab2_accum + 1, 5, QTableWidgetItem(install_date))
                    self.tab2_table.setItem(i + tab2_accum + 1, 7, QTableWidgetItem(del4_5[0][0]))
                rows4_5 = rows4_5_2
            elif len(rows4_5_3) >= 1:
                # 실행
                for i in range(len(rows4_5_3)):
                    Executable_Name, Full_Path, Last_Executed1 = rows4_5_3[i]
                    self.tab2_table.setItem(i + tab2_accum + 1, 1, QTableWidgetItem(Executable_Name))
                    self.tab2_table.setItem(i + tab2_accum + 1, 3, QTableWidgetItem(Full_Path))
                    self.tab2_table.setItem(i + tab2_accum + 1, 6, QTableWidgetItem(Last_Executed1))
                    self.tab2_table.setItem(i + tab2_accum + 1, 7, QTableWidgetItem(del4_5[0][0]))
                rows4_5 = rows4_5_3
            else:
                rows4_5 = ''

        except:
            rows4_5 = ''
            pass
        tab2_accum = tab2_accum + len(rows4_5)

        try:
            if len(rows4_6_1) >= 1:
                # 설치 + 실행
                for i in range(len(rows4_6_1)):
                    name, version, Full_Path, publisher, install_date, Last_Executed1 = rows4_6_1[i]
                    self.tab2_table.setItem(i + tab2_accum + 1, 1, QTableWidgetItem(name))
                    self.tab2_table.setItem(i + tab2_accum + 1, 2, QTableWidgetItem(version))
                    self.tab2_table.setItem(i + tab2_accum + 1, 3, QTableWidgetItem(Full_Path))
                    self.tab2_table.setItem(i + tab2_accum + 1, 4, QTableWidgetItem(publisher))
                    self.tab2_table.setItem(i + tab2_accum + 1, 5, QTableWidgetItem(install_date))
                    self.tab2_table.setItem(i + tab2_accum + 1, 6, QTableWidgetItem(Last_Executed1))
                    self.tab2_table.setItem(i + tab2_accum + 1, 7, QTableWidgetItem(del4_6[0][0]))
                rows4_6 = rows4_6_1
            elif len(rows4_6_2) >= 1:
                # 설치
                for i in range(len(rows4_6_2)):
                    name, version, publisher, install_location, install_date = rows4_6_2[i]
                    self.tab2_table.setItem(i + tab2_accum + 1, 1, QTableWidgetItem(name))
                    self.tab2_table.setItem(i + tab2_accum + 1, 2, QTableWidgetItem(version))
                    self.tab2_table.setItem(i + tab2_accum + 1, 3, QTableWidgetItem(publisher))
                    self.tab2_table.setItem(i + tab2_accum + 1, 4, QTableWidgetItem(install_location))
                    self.tab2_table.setItem(i + tab2_accum + 1, 5, QTableWidgetItem(install_date))
                    self.tab2_table.setItem(i + tab2_accum + 1, 7, QTableWidgetItem(del4_6[0][0]))
                rows4_6 = rows4_6_2
            elif len(rows4_6_3) >= 1:
                # 실행
                for i in range(len(rows4_6_3)):
                    Executable_Name, Full_Path, Last_Executed1 = rows4_6_3[i]
                    self.tab2_table.setItem(i + tab2_accum + 1, 1, QTableWidgetItem(Executable_Name))
                    self.tab2_table.setItem(i + tab2_accum + 1, 3, QTableWidgetItem(Full_Path))
                    self.tab2_table.setItem(i + tab2_accum + 1, 6, QTableWidgetItem(Last_Executed1))
                    self.tab2_table.setItem(i + tab2_accum + 1, 7, QTableWidgetItem(del4_6[0][0]))
                rows4_6 = rows4_6_3
            else:
                rows4_6 = ''
        except:
            rows4_6 = ''
            pass
        tab2_accum = tab2_accum + len(rows4_6)+1

        # VM
        self.color_tab2_table("VM", tab2_accum)
        try:
            if len(rows5_1_1) >= 1:
                # 설치 + 실행
                for i in range(len(rows5_1_1)):
                    name, version, Full_Path, publisher, install_date, Last_Executed1 = rows5_1_1[i]
                    self.tab2_table.setItem(i + tab2_accum + 1, 1, QTableWidgetItem(name))
                    self.tab2_table.setItem(i + tab2_accum + 1, 2, QTableWidgetItem(version))
                    self.tab2_table.setItem(i + tab2_accum + 1, 3, QTableWidgetItem(Full_Path))
                    self.tab2_table.setItem(i + tab2_accum + 1, 4, QTableWidgetItem(publisher))
                    self.tab2_table.setItem(i + tab2_accum + 1, 5, QTableWidgetItem(install_date))
                    self.tab2_table.setItem(i + tab2_accum + 1, 6, QTableWidgetItem(Last_Executed1))
                    self.tab2_table.setItem(i + tab2_accum + 1, 7, QTableWidgetItem(del5_1[0][0]))
                rows5_1 = rows5_1_1
            elif len(rows5_1_2) >= 1:
                # 설치
                for i in range(len(rows5_1_2)):
                    name, version, publisher, install_location, install_date = rows5_1_2[i]
                    self.tab2_table.setItem(i + tab2_accum + 1, 1, QTableWidgetItem(name))
                    self.tab2_table.setItem(i + tab2_accum + 1, 2, QTableWidgetItem(version))
                    self.tab2_table.setItem(i + tab2_accum + 1, 3, QTableWidgetItem(publisher))
                    self.tab2_table.setItem(i + tab2_accum + 1, 4, QTableWidgetItem(install_location))
                    self.tab2_table.setItem(i + tab2_accum + 1, 5, QTableWidgetItem(install_date))
                    self.tab2_table.setItem(i + tab2_accum + 1, 7, QTableWidgetItem(del5_1[0][0]))
                rows5_1 = rows5_1_2
            elif len(rows5_1_3) >= 1:
                # 실행
                for i in range(len(rows5_1_3)):
                    Executable_Name, Full_Path, Last_Executed1 = rows5_1_3[i]
                    self.tab2_table.setItem(i + tab2_accum + 1, 1, QTableWidgetItem(Executable_Name))
                    self.tab2_table.setItem(i + tab2_accum + 1, 3, QTableWidgetItem(Full_Path))
                    self.tab2_table.setItem(i + tab2_accum + 1, 6, QTableWidgetItem(Last_Executed1))
                    self.tab2_table.setItem(i + tab2_accum + 1, 7, QTableWidgetItem(del5_1[0][0]))
                rows5_1 = rows5_1_3
            else:
                rows5_1 = ''
        except:
            rows5_1 = ''
            pass
        tab2_accum = tab2_accum + len(rows5_1)

        try:
            if len(rows5_2_1) >= 1:
                # 설치 + 실행
                for i in range(len(rows5_2_1)):
                    name, version, Full_Path, publisher, install_date, Last_Executed1 = rows5_2_1[i]
                    self.tab2_table.setItem(i + tab2_accum + 1, 1, QTableWidgetItem(name))
                    self.tab2_table.setItem(i + tab2_accum + 1, 2, QTableWidgetItem(version))
                    self.tab2_table.setItem(i + tab2_accum + 1, 3, QTableWidgetItem(Full_Path))
                    self.tab2_table.setItem(i + tab2_accum + 1, 4, QTableWidgetItem(publisher))
                    self.tab2_table.setItem(i + tab2_accum + 1, 5, QTableWidgetItem(install_date))
                    self.tab2_table.setItem(i + tab2_accum + 1, 6, QTableWidgetItem(Last_Executed1))
                    self.tab2_table.setItem(i + tab2_accum + 1, 7, QTableWidgetItem(del5_2[0][0]))
                rows5_2 = rows5_2_1
            elif len(rows5_2_2) >= 1:
                # 설치
                for i in range(len(rows5_2_2)):
                    name, version, publisher, install_location, install_date = rows5_2_2[i]
                    self.tab2_table.setItem(i + tab2_accum + 1, 1, QTableWidgetItem(name))
                    self.tab2_table.setItem(i + tab2_accum + 1, 2, QTableWidgetItem(version))
                    self.tab2_table.setItem(i + tab2_accum + 1, 3, QTableWidgetItem(publisher))
                    self.tab2_table.setItem(i + tab2_accum + 1, 4, QTableWidgetItem(install_location))
                    self.tab2_table.setItem(i + tab2_accum + 1, 5, QTableWidgetItem(install_date))
                    self.tab2_table.setItem(i + tab2_accum + 1, 7, QTableWidgetItem(del5_2[0][0]))
                rows5_2 = rows5_2_2
            elif len(rows5_2_3) >= 1:
                # 실행
                for i in range(len(rows5_2_3)):
                    Executable_Name, Full_Path, Last_Executed1 = rows5_2_3[i]
                    self.tab2_table.setItem(i + tab2_accum + 1, 1, QTableWidgetItem(Executable_Name))
                    self.tab2_table.setItem(i + tab2_accum + 1, 3, QTableWidgetItem(Full_Path))
                    self.tab2_table.setItem(i + tab2_accum + 1, 6, QTableWidgetItem(Last_Executed1))
                    self.tab2_table.setItem(i + tab2_accum + 1, 7, QTableWidgetItem(del5_2[0][0]))
                rows5_2 = rows5_2_3
            else:
                rows5_2 = ''
        except:
            rows5_2 = ''
            pass


        self.tab2_table.verticalHeader().hide()
        self.tab2_table.setColumnWidth(0, self.width()*3/30)
        self.tab2_table.setColumnWidth(1, self.width()*4/30)
        self.tab2_table.setColumnWidth(2, self.width()*2/30)
        self.tab2_table.setColumnWidth(3, self.width()*13/30)
        self.tab2_table.setColumnWidth(4, self.width()*3/30)
        self.tab2_table.setColumnWidth(5, self.width()*4/30)
        self.tab2_table.setColumnWidth(6, self.width()*4/30)
        self.tab2_table.setColumnWidth(7, self.width()*3/30)

        self.vbox1.addWidget(self.tab2_table)
        self.groupbox1.setLayout(self.vbox1)
        self.tab2.layout.addWidget(self.groupbox1)

    # tab2_table의 라인 컬러링
    def color_tab2_table(self, string, accum):
        self.tab2_table.setItem(accum, 0, QTableWidgetItem(string))
        self.tab2_table.setItem(accum, 1, QTableWidgetItem(""))
        self.tab2_table.setItem(accum, 2, QTableWidgetItem(""))
        self.tab2_table.setItem(accum, 3, QTableWidgetItem(""))
        self.tab2_table.setItem(accum, 4, QTableWidgetItem(""))
        self.tab2_table.setItem(accum, 5, QTableWidgetItem(""))
        self.tab2_table.setItem(accum, 6, QTableWidgetItem(""))
        self.tab2_table.setItem(accum, 7, QTableWidgetItem(""))
        self.tab2_table.item(accum, 0).setBackground(QtGui.QColor(229, 243, 255))
        self.tab2_table.item(accum, 1).setBackground(QtGui.QColor(229, 243, 255))
        self.tab2_table.item(accum, 2).setBackground(QtGui.QColor(229, 243, 255))
        self.tab2_table.item(accum, 3).setBackground(QtGui.QColor(229, 243, 255))
        self.tab2_table.item(accum, 4).setBackground(QtGui.QColor(229, 243, 255))
        self.tab2_table.item(accum, 5).setBackground(QtGui.QColor(229, 243, 255))
        self.tab2_table.item(accum, 6).setBackground(QtGui.QColor(229, 243, 255))
        self.tab2_table.item(accum, 7).setBackground(QtGui.QColor(229, 243, 255))

    # tab2 요약 정보
    def set_PCinfo(self):
        self.groupbox2 = QGroupBox("요약 정보")
        self.vbox2 = QVBoxLayout()
        self.tab2_tree = QTreeWidget()
        self.tab2_tree.header().setVisible(False)

        pubIP = os.popen("curl ifconfig.me").read()
        string5 = "공인 IP : " + str(pubIP)

        # 윈도우 버전, 윈도우 설치 시각, 컴퓨터 이름, 표준 시간대, 공인IP, 시스템 시간 변경, 표준시간대 변경
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT product_name, product_ID, build_lab, computer_name, " \
                    "timezone_name, UTC, " \
                    "datetime(install_date, " + self.UTC + ") FROM OSInformation;"
            cur.execute(query)
            rows = cur.fetchall()[0]

            string1 = "윈도우 버전:\t" + rows[0] + ", " + rows[1] + ", " + rows[2]
            string2 = "윈도우 설치 시간:\t " + rows[6]
            string3 = "컴퓨터 이름:\t" + rows[3]
            string4 = "표준 시간대:\t" + rows[4] + " (UTC " + str(rows[5]) + ")"

        except:
            string1 = "윈도우 버전"
            string2 = "윈도우 설치 시간"
            string3 = "컴퓨터 이름"
            string4 = "표준 시간대"
        # 최대 절전모드 여부 확인
        try:
            GetRegKey_command = 'RegistryParse\\GetRegKey.exe COPY\\REGHIVE\\SYSTEM COPY\\REGHIVE\\SOFTWARE COPY\\REGHIVE\\SAM REGHIVE\\NTUSER.DAT COPY\\REGHIVE\\USRCLASS.DAT '
            GetRegValue_command = 'RegistryParse\\GetRegValue.exe COPY\\REGHIVE\\SYSTEM COPY\\REGHIVE\\SOFTWARE COPY\\REGHIVE\\SAM REGHIVE\\NTUSER.DAT COPY\\REGHIVE\\USRCLASS.DAT '
            input = 'SYSTEM "ControlSet001\\Control\\Power"'
            result1 = os.popen(GetRegKey_command + input).read()
            if "True" in result1:
                input = 'SYSTEM "ControlSet001\\Control\\Power" HibernateEnabled'
                result2 = os.popen(GetRegValue_command + input).read()
                if result2 == 1:
                    hibernation = "ON"
                else:
                    hibernation = "OFF"
            else:
                print(input + "의 경로를 찾을 수 없습니다")
        except:
            pass

        self.text0 = QTreeWidgetItem(self.tab2_tree)
        self.text0.setText(0, "PC 정보")
        self.text1 = QTreeWidgetItem(self.text0)
        self.text1.setText(0, string1)
        self.text2 = QTreeWidgetItem(self.text0)
        self.text2.setText(0, string2)
        self.text3 = QTreeWidgetItem(self.text0)
        self.text3.setText(0, string3)
        self.text4 = QTreeWidgetItem(self.text0)
        self.text4.setText(0, string4)
        self.hibernate = QTreeWidgetItem(self.text0)
        self.hibernate.setText(0, "최대 절전모드 : " + hibernation)
        self.vss = QTreeWidgetItem(self.text0)
        self.vss.setText(0, "볼륨 섀도우 카피")
        self.text5 = QTreeWidgetItem(self.tab2_tree)
        self.text5.setText(0, "MFT 생성 시간")
        self.text6 = QTreeWidgetItem(self.tab2_tree)
        self.text6.setText(0, "계정")
        self.text7 = QTreeWidgetItem(self.tab2_tree)
        self.text7.setText(0, "USB")
        self.text8 = QTreeWidgetItem(self.tab2_tree)
        self.text8.setText(0, "네트워크")
        self.text8_1 = QTreeWidgetItem(self.text8)
        self.text8_1.setText(0, string5)
        self.text9 = QTreeWidgetItem(self.tab2_tree)
        self.text9.setText(0, "시간 변경")

        # Volume Shadows Copy
        try:
            query = 'select file_path from parsed_MFT where file_path like "%system volume Information%" and (file_path like "%{%}{%}" or file_path like "%{%}")'
            cur.execute(query)
            rows = cur.fetchall()
            self.vss_content = []
            for i in range(len(rows)):
                file_path = rows[i]
                string = file_path[0].split('/')[-1]
                self.vss_content.append(QTreeWidgetItem(self.vss))
                self.vss_content[i].setText(0, string)
        except:
            pass

        # MFT 생성 시간 + (MFT 생성 vs 시스템 설치)
        c_mft_time = ''
        try:
            win_install = re.search('[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}', string2)
            win_install = win_install.group()
            query = "SELECT drive, datetime(SI_M_timestamp, " + self.UTC + ") FROM parsed_MFT WHERE file_path LIKE '/$MFT'"
            cur.execute(query)
            rows = cur.fetchall()
            self.text5_content = []
            for i in range(len(rows)):
                drive, SI_M_timestamp = rows[i]
                flag = 0
                print(drive)
                if drive == 'C':
                    c_mft_time = SI_M_timestamp
                    if datetime.strptime(SI_M_timestamp, "%Y-%m-%d %H:%M:%S") > datetime.strptime(win_install, "%Y-%m-%d %H:%M:%S"):
                        string = drive + ":\ : " + SI_M_timestamp + "\t ※윈도우 설치시간과 MFT 생성 시간이 논리적 모순입니다."
                        flag = 1
                        # 윈도우 설치 -> mft 생성 => 이상함!
                    else :
                        string = drive + ":\ : " + SI_M_timestamp # 정상(C에 대해서만)
                else :
                    string = drive + ":\ : " + SI_M_timestamp
                self.text5_content.append(QTreeWidgetItem(self.text5))
                if flag == 1:
                    self.text5_content[i].setBackground(0, QColor(255, 153, 128))
                self.text5_content[i].setText(0, string)

        except:
            pass

        # 계정 + (계정 vs 시스템 설치) + (계정 vs mft 생성)
        try:
            query = 'SELECT datetime(install_date, ' + self.UTC + ') FROM OSInformation;'
            cur.execute(query)
            win_inst = cur.fetchone()

            query = "SELECT account_name, RID_int, datetime(created_on, " + self.UTC + "), " \
                    "datetime(last_login_time, " + self.UTC + ") FROM UserAccounts"
            cur.execute(query)
            rows = cur.fetchall()

            self.text6_content = []
            for i in range(len(rows)):
                string = QTextEdit()
                flag = 0
                account_name, RID_int, created_on, last_login_time = rows[i]
                # 사용자가 생성한 계정
                try:
                    query = 'SELECT SI_C_timestamp FROM parsed_MFT WHERE file_path="/Users/' + account_name + '" and is_dir="Y"'
                    cur.execute(query)
                    acc_folder = cur.fetchone()
                except:
                    acc_folder = ''
                if int(RID_int) > 1000:
                    if last_login_time == None:
                        if datetime.strptime(win_inst[0], "%Y-%m-%d %H:%M:%S") > datetime.strptime(created_on,"%Y-%m-%d %H:%M:%S"):
                            string = account_name + "(" + str(RID_int) + ")" + "\t생성: " + created_on + "\t마지막 로그인: " + str(last_login_time)
                            flag = 1
                        else:
                            string = account_name + "(" + str(RID_int) + ")" + "\t생성: " + created_on + "\t마지막 로그인: " + str(last_login_time)

                    else: # 사용자가 생성한 계정에 로그인 기록이 존재
                        # 윈도우 설치 시간이 계정 생성 시간 이후인 경우
                        if datetime.strptime(win_inst[0], "%Y-%m-%d %H:%M:%S") > datetime.strptime(created_on, "%Y-%m-%d %H:%M:%S")\
                                or datetime.strptime(c_mft_time, "%Y-%m-%d %H:%M:%S") > datetime.strptime(created_on, "%Y-%m-%d %H:%M:%S"):
                            string = account_name + "(" + str(RID_int) + ")" + "\t생성: " + created_on + "\t마지막 로그인: " + str(last_login_time) + "\t계정 폴더 생성 시간: " + acc_folder[0] + "\t ※윈도우 설치시간 또는 MFT 생성 시간과 계정 생성 시간이 논리적 모순입니다."
                            flag = 1
                        else:
                            string = account_name + "(" + str(RID_int) + ")" + "\t생성: " + created_on + "\t마지막 로그인: " + str(last_login_time) + "\t계정 폴더 생성 시간: " + acc_folder[0]

                # 시스템이 생성한 계정
                else:
                    if last_login_time == None:
                        if datetime.strptime(win_inst[0], "%Y-%m-%d %H:%M:%S") > datetime.strptime(created_on,"%Y-%m-%d %H:%M:%S"):
                            string = account_name + "(" + str(RID_int) + ")" + "\t생성: " + created_on + "\t마지막 로그인: " + str(last_login_time)
                            flag = 1
                        else:
                            string = account_name + "(" + str(RID_int) + ")" + "\t생성: " + created_on + "\t마지막 로그인: " + str(last_login_time)

                    else: # 시스템이 생성한 계정에 로그인 기록이 존재
                        if datetime.strptime(win_inst[0], "%Y-%m-%d %H:%M:%S") > datetime.strptime(created_on,"%Y-%m-%d %H:%M:%S"):
                            string = account_name + "(" + str(RID_int) + ")" + "\t생성: " + created_on + "\t마지막 로그인: " + str(last_login_time) + "\t ※윈도우 설치시간과 계정 생성 시간이 논리적 모순입니다."
                            flag = 1
                        else:
                            string = account_name + "(" + str(RID_int) + ")" + "\t생성: " + created_on + "\t마지막 로그인: " + str(last_login_time)

                self.text6_content.append(QTreeWidgetItem(self.text6))
                if flag == 1:
                    self.text6_content[i].setBackground(0, QColor(255, 153, 128))
                self.text6_content[i].setText(0, string)
        except:
            pass

        # USB
        try:
            query = "SELECT serial_num, random_yn, GUID, vendor_name, product_name, version, label, first_connected, last_connected FROM Connected_USB"
            cur.execute(query)
            rows = cur.fetchall()
            self.text7_content = []
            for i in range(len(rows)):
                serial_num, random_yn, GUID, vendor_name, product_name, version, label, first_connected, last_connected = rows[i]
                string = None
                if random_yn == 0:   # serial_num이 PnP Manager가 부여한 랜덤 번호가 아니라면 serial_num를 출력함
                    string = vendor_name + " " + product_name + " " + version + " / GUID: " + GUID + ", 시리얼 번호: " + str(serial_num) + ", 최초 연결: " + first_connected + ", 마지막 연결: " + last_connected
                elif random_yn == 1: # serial_num이 PnP Manager가 부여한 랜덤 번호라면 serial_num를 출력하지 않음
                    string = vendor_name + " " + product_name + " " + version + " / GUID: " + GUID + ", 최초 연결: " + first_connected + ", 마지막 연결: " + last_connected
                self.text7_content.append(QTreeWidgetItem(self.text7))
                self.text7_content[i].setText(0, string)

        except:
            pass

        # 네트워크
        try:
            query = "SELECT description, ip, default_gateway, lease_obtained_time, lease_terminates_time FROM Network"
            cur.execute(query)
            rows = cur.fetchall()
            self.text8_content = []
            for i in range(len(rows)):
                description, ip, default_gateway, lease_obtained_time, lease_terminates_time = rows[i]
                self.text8_content.append(QTreeWidgetItem(self.text8))
                string = "네트워크 : " + str(description) + ", ip: " + str(ip) + ", 게이트웨이: " + str(default_gateway) + ", 할당: " + str(lease_obtained_time) + ", 만료: " + str(lease_terminates_time)
                self.text8_content[i].setText(0, string)
        except:
            pass

        # 시스템 시간 변경
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT datetime(a.time_created, " + self.UTC + "), a.sbt_usr_name, " \
                    "datetime(a.sys_prv_time, " + self.UTC + "), datetime(a.sys_new_time, " + self.UTC + ") FROM event_log a, UserAccounts b " \
                    "WHERE (event_id LIKE 4616) AND (a.sbt_usr_name = b.account_name)"
            cur.execute(query)
            rows = cur.fetchall()
            conn.close()
            self.text9_1_content = []
            for i in range(len(rows)):
                time_created, sbt_usr_name, sys_prv_time, sys_new_time = rows[i]
                string = "시스템 시간 변경 발생시간 : " + time_created + ", 계정명 : " + sbt_usr_name+ ", 전 : " + sys_prv_time + " -> 후 : " + sys_new_time + "\t ※시스템 시간이 변경되었습니다."
                self.text9_1_content.append(QTreeWidgetItem(self.text9))
                self.text9_1_content[i].setBackground(0, QColor(255, 153, 128))
                self.text9_1_content[i].setText(0, string)

        except:
            pass

        #표준 시간대 변경
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT datetime(time_created, " + self.UTC + "),new_bias, old_bias " \
                    "FROM event_log WHERE event_id LIKE 22"
            cur.execute(query)
            rows = cur.fetchall()
            self.text9_2_content = []
            for i in range(len(rows)):
                time_created, new_bias, old_bias = rows[i]
                old = "UTC+" + str(int(old_bias) / 60 * -1) if int(old_bias) < 0 else "UTC" + str(
                    int(old_bias) / 60 * -1)
                new = "UTC+" + str(int(new_bias) / 60 * -1) if int(new_bias) < 0 else "UTC" + str(
                    int(new_bias) / 60 * -1)
                string = "표준 시간대 변경 발생 시간 : " + str(time_created) + " " + str(old) + " -> " + str(new) + "\t ※표준 시간대가 변경되었습니다."
                self.text9_2_content.append(QTreeWidgetItem(self.text9))
                self.text9_2_content[i].setBackground(0, QColor(255, 153, 128))
                self.text9_2_content[i].setText(0, string)

        except:
            pass

        self.vbox2.addWidget(self.tab2_tree)
        self.groupbox2.setLayout(self.vbox2)
        self.tab2.layout.addWidget(self.groupbox2)


#################################################
#   tab3                                        #
#################################################
    # tab3 구성
    def set_tab3(self):
        self.tab3.layout = QGridLayout(self)

        self.box1 = QVBoxLayout()
        self.checkbox1_1 = QCheckBox("MFT 생성")
        self.checkbox1_2 = QCheckBox("계정 생성")
        self.checkbox1_3 = QCheckBox("Windows 설치 / Windows 업데이트")
        self.checkbox1_4 = QCheckBox("시간 변경")
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

        self.timeline_tab1 = QWidget()
        self.timeline_tab2 = QWidget()
        self.timeline_tabs = QTabWidget()
        self.timeline_tabs.addTab(self.timeline_tab1, "테이블")
        self.timeline_tabs.addTab(self.timeline_tab2, "그래프")

        self.tab3.layout.addLayout(self.box3, 0, 0)
        self.tab3.layout.addLayout(self.box4, 1, 0)
        self.tab3.layout.addWidget(self.timeline_tabs, 2, 0)
        self.set_timeline_tab1()
        self.set_timeline_tab2()
        self.tab3.setLayout(self.tab3.layout)


#################################################
#   tab3의 tab2                                 #
#################################################
    # tab3의 타임라인 그래프 + 테이블 구성
    def set_timeline_tab2(self):
        self.timeline_tab2.layout = QHBoxLayout()

        fig = plt.Figure()
        self.ax = fig.add_subplot(111)
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
        self.ax2 = self.ax.twinx()
        self.canvas = FigureCanvas(fig)
        self.canvas.draw()
        self.canvas.mpl_connect('button_press_event', self.timeline_click)

        self.print_graph_button = QPushButton("그래프 출력")
        self.print_graph_button.clicked.connect(self.set_graph)
        self.graph_layout = QVBoxLayout()
        self.time_label = QLabel()

        self.internet_table = QTableWidget(self)
        self.internet_table.setColumnCount(3)
        column_headers = ["시간", "URL", "제목"]
        self.internet_table.setHorizontalHeaderLabels(column_headers)
        self.internet_table.setColumnWidth(0, self.width() * 2 / 15)
        self.internet_table.setColumnWidth(1, self.width() * 4 / 11)
        self.internet_table.setColumnWidth(2, self.width() * 3 / 11)

        self.document_table = QTableWidget(self)
        self.document_table.setColumnCount(3)
        column_headers = ["시간", "타입", "파일"]
        self.document_table.setHorizontalHeaderLabels(column_headers)
        self.document_table.setColumnWidth(0, self.width() * 2 / 15)
        self.document_table.setColumnWidth(1, self.width() * 1 / 17)
        self.document_table.setColumnWidth(2, self.width() * 8 / 14)

        self.graph_layout.addWidget(self.print_graph_button)
        self.graph_layout.addWidget(self.time_label)
        self.graph_layout.addWidget(self.internet_table)
        self.graph_layout.addWidget(self.document_table)

        self.timeline_tab2.layout.addWidget(self.canvas)
        self.timeline_tab2.layout.addLayout(self.graph_layout)
        self.timeline_tab2.setLayout(self.timeline_tab2.layout)

    # 그래프 출력
    def set_graph(self):
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        start = self.input_datetime1.dateTime().toPyDateTime() + timedelta(hours=-self.UTC_int)
        end = self.input_datetime2.dateTime().toPyDateTime() + timedelta(hours=-self.UTC_int)
        interval = (end - start) / 10

        # times 리스트 생성
        self.times = []  # str: 쿼리에서 string 타입의 시간이 필요함. self.times는 self.times2, self.times3보다 1 더 길음. (쿼리 사용을 위함)
        self.times2 = []  # datetime: matplot 사용시 datetime 타입으로 인자를 넘겨야 함
        index = start
        for i in range(10):
            self.times.append(index.strftime("%Y-%m-%d %H:%M:%S"))
            self.times2.append(index)
            index = index + interval
        self.times.append(end.strftime("%Y-%m-%d %H:%M:%S"))
        self.times3 = []  # float: datetime 객체는 matplot에서 float 타입으로 출력됨.
        for t in self.times2:
            self.times3.append(mdates.date2num(t))

        # 인터넷 접속 데이터 생성
        self.internet_data = []
        try:
            for t in range(10):
                query = "SELECT visit_count FROM url WHERE (timestamp >= '" + self.times[t] + "') AND (timestamp <= '" + self.times[t+1] + "')"
                cur.execute(query)
                rows = cur.fetchall()
                self.internet_data.append(len(rows))
        except:
            pass

        # 문서 생성/접근/수정 데이터 생성
        self.document_data = []
        try:
            for t in range(10):
                query = "SELECT OBJID_timestamp FROM parsed_MFT WHERE " \
                        "((FN_M_timestamp >= '" + self.times[t] + "' AND FN_M_timestamp < '" + self.times[t+1] + "') OR " \
                        "(FN_A_timestamp >= '" + self.times[t] + "' AND FN_A_timestamp < '" + self.times[t+1] + "') OR " \
                        "(FN_C_timestamp >= '" + self.times[t] + "' AND FN_C_timestamp < '" + self.times[t+1] + "'))"
                cur.execute(query)
                rows = cur.fetchall()
                self.document_data.append(len(rows))
        except:
            pass
        conn.close()

        # 마우스 클릭 위치 계산을 위한 변수
        self.times3_max = max(self.times3)
        self.times3_min = min(self.times3)
        times3_tmp = [(t - self.times3_min) / (self.times3_max - self.times3_min) for t in self.times3]
        internet_max = max(self.internet_data)
        internet_min = min(self.internet_data)
        internet_data_tmp = [(i - internet_min) / (internet_max - internet_min) for i in self.internet_data]
        document_max = max(self.document_data)
        document_min = min(self.document_data)
        document_data_tmp = [(d - document_min) / (document_max - document_min) for d in self.document_data]
        self.points1 = list(zip(times3_tmp, internet_data_tmp))
        self.points2 = list(zip(times3_tmp, document_data_tmp))
        if internet_max > document_max:
            self.MAX = internet_max
        else:
            self.MAX = document_max
        if internet_min < document_min:
            self.MIN = internet_min
        else:
            self.MIN = document_min

        self.ax.cla()
        self.ax2.cla()
        line1 = self.ax.plot(self.times2, self.internet_data, color="lightskyblue", label="Internet")
        line2 = self.ax2.plot(self.times2, self.document_data, color="sandybrown", label="Documnets Create/Modify/Access")
        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        self.ax.legend(lines, labels, loc="upper left")
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
        self.canvas.draw()

    # 그래프 클릭 시 거리 계산
    def distance(self, a, b):
        return (sum([(k[0] - k[1]) ** 2 for k in zip(a, b)]) ** 0.5)

    # 그래프 클릭 시 이벤트
    def timeline_click(self, event):
        if event.inaxes is None:
            return

        try:
            x = (event.xdata - self.times3_min) / (self.times3_max - self.times3_min)
            y = (event.ydata - self.MIN) / (self.MAX - self.MIN)
            dists1 = [self.distance([x, y], p) for p in self.points1]
            dists2 = [self.distance([x, y], p) for p in self.points2]
            if min(dists1) > min(dists2):
                dists = dists2
            else:
                dists = dists1

            if min(dists) > (self.times3_max - self.times3_min) / 100:  # 클릭 범위 지정. 나누는 숫자가 작을 수록 클릭 가능 범위 커짐.
                return                                                  # (self.times3_max - self.times3_min)은 범위의 크기에 유동적으로 클릭 범위를 조정하기 위함.

            index = dists.index(min(dists))
            start_label = (self.times2[index] + timedelta(hours=self.UTC_int)).strftime("%Y-%m-%d %H:%M:%S")
            end_label = (self.times2[index] + timedelta(hours=(self.UTC_int + 1))).strftime("%Y-%m-%d %H:%M:%S")
            self.time_label.setText(start_label + " ~ " + end_label)
            self.set_internet_table(index)
            self.set_document_table(index)
        except:
            pass

    # tab3 타임라인의 그래프 - 인터넷 테이블
    def set_internet_table(self, index):
        try:
            self.internet_table.clearContents()
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT datetime(timestamp, " + self.UTC + "), url, title FROM url " \
                    "WHERE (timestamp >= '" + self.times[index] + "') AND (timestamp <= '" + self.times[index + 1] + "')"
            cur.execute(query)
            rows = cur.fetchall()
            conn.close()

            count = len(rows)
            self.internet_table.setRowCount(count)
            for i in range(count):
                timestamp, url, title = rows[i]
                self.internet_table.setItem(i, 0, QTableWidgetItem(timestamp))
                self.internet_table.setItem(i, 1, QTableWidgetItem(url))
                self.internet_table.setItem(i, 2, QTableWidgetItem(title))

            self.internet_table.sortItems(0, QtCore.Qt.AscendingOrder)
        except:
            pass

    # tab3 타임라인의 그래프 - 문서 테이블
    def set_document_table(self, index):
        try:
            self.document_table.clearContents()
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT datetime(FN_C_timestamp, " + self.UTC + "), file_path FROM parsed_MFT " \
                    "WHERE (FN_C_timestamp >= '" + self.times[index] + "') AND (FN_C_timestamp <= '" + self.times[index+1] + "')"
            cur.execute(query)
            creation_rows = cur.fetchall()
            query = "SELECT datetime(FN_M_timestamp, " + self.UTC + "), file_path FROM parsed_MFT " \
                    "WHERE (FN_M_timestamp >= '" + self.times[index] + "') AND (FN_M_timestamp <= '" + self.times[index + 1] + "')"
            cur.execute(query)
            modified_rows = cur.fetchall()
            query = "SELECT datetime(FN_A_timestamp, " + self.UTC + "), file_path FROM parsed_MFT " \
                    "WHERE (FN_A_timestamp >= '" + self.times[index] + "') AND (FN_A_timestamp <= '" + self.times[index + 1] + "')"
            cur.execute(query)
            accessed_rows = cur.fetchall()
            conn.close()

            count = len(creation_rows) + len(modified_rows) + len(accessed_rows)
            self.document_table.setRowCount(count)

            for i in range(len(creation_rows)):  # 문서 생성
                time, file = creation_rows[i]
                self.document_table.setItem(i, 0, QTableWidgetItem(time))
                self.document_table.setItem(i, 1, QTableWidgetItem("생성"))
                self.document_table.setItem(i, 2, QTableWidgetItem(file))
            accum = len(creation_rows)
            for i in range(len(modified_rows)):  # 문서 수정
                time, file = modified_rows[i]
                self.document_table.setItem(i + accum, 0, QTableWidgetItem(time))
                self.document_table.setItem(i + accum, 1, QTableWidgetItem("수정"))
                self.document_table.setItem(i + accum, 2, QTableWidgetItem(file))
            accum = accum + len(modified_rows)
            for i in range(len(accessed_rows)):  # 문서 접근
                time, file = accessed_rows[i]
                self.document_table.setItem(i + accum, 0, QTableWidgetItem(time))
                self.document_table.setItem(i + accum, 1, QTableWidgetItem("접근"))
                self.document_table.setItem(i + accum, 2, QTableWidgetItem(file))

            self.document_table.sortItems(0, QtCore.Qt.AscendingOrder)
        except:
            pass


#################################################
#   tab3의 tab1                                 #
#################################################
    # tab3의 tab1 구성 (search line, 테이블)
    def set_timeline_tab1(self):
        self.timeline_tab1.layout = QVBoxLayout()

        self.timeline_search = QLineEdit(self)
        self.timeline_search.setPlaceholderText("Search ...")
        self.timeline_search.textChanged.connect(self.search_timeline)

        self.timeline = QTableWidget(self)
        self.timeline.setSortingEnabled(True)
        self.timeline.setColumnCount(4)
        headers = ["시간", "행위", "세부 사항", "경로"]
        self.timeline.setHorizontalHeaderLabels(headers)
        self.timeline.setColumnWidth(0, self.width() * 3 / 20)
        self.timeline.setColumnWidth(1, self.width() * 3 / 20)
        self.timeline.setColumnWidth(2, self.width() * 8 / 20)
        self.timeline.setColumnWidth(3, self.width() * 10 / 20)

        self.timeline_tab1.layout.addWidget(self.timeline_search)
        self.timeline_tab1.layout.addWidget(self.timeline)
        self.timeline_tab1.setLayout(self.timeline_tab1.layout)

    # tab3의 타임라인 구성
    def set_timeline(self):
        self.datetime1 = (self.input_datetime1.dateTime().toPyDateTime() + timedelta(hours = -self.UTC_int)).strftime("%Y-%m-%d %H:%M:%S")
        self.datetime2 = (self.input_datetime2.dateTime().toPyDateTime() + timedelta(hours = -self.UTC_int)).strftime("%Y-%m-%d %H:%M:%S")
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

    # tab3의 타임라인 필터링
    def search_timeline(self, s):
        for i in range(self.timeline.rowCount()):
            self.timeline.hideRow(i)

        items = self.timeline.findItems(s, Qt.MatchContains)
        for item in items:
            self.timeline.showRow(item.row())

    # 타임라인 - MFT 생성
    def timeline_data1_1(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query_1 = "SELECT file_path, drive, datetime(SI_M_timestamp," + self.UTC + ") from parsed_MFT WHERE ((file_path LIKE '/$MFT') AND " \
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
                string1 = drive + ":\ $SI 수정"
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
                string1 = drive + ":\ $SI 접근"
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
                string1 = drive + ":\ $SI 생성"
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
                string1 = drive + ":\ $SI mft 변경"
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
                string1 = drive + ":\ $FN 수정"
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
                string1 = drive + ":\ $FN 접근"
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
                string1 = drive + ":\ $FN 생성"
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
                string1 = drive + ":\ $FN mft 변경"
                string2 = " - FN_E_timestamp"
                self.timeline.setItem(accum + i, 1, QTableWidgetItem(string1))
                self.timeline.setItem(accum + i, 2, QTableWidgetItem(file_path + string2))
            self.timeline.setSortingEnabled(sortingEnabled)
        except:
            pass

    # 타임라인 - 계정 생성
    def timeline_data1_2(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query_1 = "SELECT datetime(created_on," + self.UTC + "), account_name, RID_int FROM UserAccounts " \
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

            query_2 = "SELECT datetime(last_password_change_time," + self.UTC + "), account_name, RID_int FROM UserAccounts " \
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
        except:
            pass

    # 타임라인 - Windows 설치, Windows 업데이트
    def timeline_data1_3(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT datetime(install_date," + self.UTC + "), product_name, product_ID FROM OSInformation " \
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

        except:
            pass

        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT detailed, computer, datetime(time_created," + self.UTC + "), package FROM event_log WHERE ((event_id='2' AND package IS NOT '')" \
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
        except:
            pass

    # 타임라인 - 시간 변경, 표준시간대 변경
    def timeline_data1_4(self):
        try:
            conn = sqlite3.connect('Believe_Me_Sister.db')
            cur = conn.cursor()
            query1 = "SELECT datetime(a.time_created," + self.UTC + "), a.detailed, " \
                    "a.sbt_usr_name, datetime(a.sys_prv_time, " + self.UTC + "), " \
                    "datetime(a.sys_new_time, " + self.UTC + ") FROM event_log a, UserAccounts b WHERE ((event_id LIKE 4616) " \
                    "AND (a.sbt_usr_name LIKE b.account_name) " \
                    "AND (time_created >= '" + self.datetime1 + "' AND time_created <= '" + self.datetime2 + "'))"
            cur.execute(query1)
            rows = cur.fetchall()
            conn.close()
            accum = self.timeline_count
            self.timeline_count = accum + len(rows)
            self.timeline.setRowCount(self.timeline_count)

            sortingEnabled = self.timeline.isSortingEnabled()
            self.timeline.setSortingEnabled(False)

            for i in range(len(rows)):
                time_created, detailed, sbt_usr_name, sys_prv_time, sys_new_time = rows[i]
                self.timeline.setItem(i + accum, 0, QTableWidgetItem(time_created))
                self.timeline.setItem(i + accum, 1, QTableWidgetItem("시스템 시간 변경"))
                string = "계정 이름: " + sbt_usr_name + ", 변경 전 시간: " + sys_prv_time + ", 변경 후 시간: " + sys_new_time
                self.timeline.setItem(i + accum, 2, QTableWidgetItem(string))
            self.timeline.setSortingEnabled(sortingEnabled)
            self.set_color()

            query2 = "SELECT datetime(time_created, " + self.UTC + "), detailed, new_bias, old_bias FROM event_log WHERE event_id LIKE 22"
            cur.execute(query2)
            rows = cur.fetchall()
            conn.close()
            accum = self.timeline_count
            self.timeline_count = accum + len(rows)
            self.timeline.setRowCount(self.timeline_count)

            sortingEnabled = self.timeline.isSortingEnabled()
            self.timeline.setSortingEnabled(False)

            for i in range(len(rows)):
                time_created, detailed, new_bias, old_bias = rows[i]
                self.timeline.setItem(i + accum, 0, QTableWidgetItem(time_created))
                self.timeline.setItem(i + accum, 1, QTableWidgetItem("표준시간대 변경"))
                string = "detailed : " + detailed + ", old_bias : " + old_bias + ", new bias : " + new_bias
                self.timeline.setItem(i+accum, 2, QTableWidgetItem(string))
            self.timeline.setSortingEnabled(sortingEnabled)
            self.set_color()
        except:
            pass

    # 타임라인 - 시스템 On/Off
    def timeline_data1_5(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT event_id, computer, datetime(time_created," + self.UTC + ") FROM event_log WHERE ((event_id = '12' OR event_id = '13') AND " \
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
        except:
            pass

    # 타임라인 - 문서 생성 및 수정
    def timeline_date2_1(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()

            query_1 = "SELECT file_name, local_base_path, datetime(target_creation_time, " + self.UTC + ") From jumplist " \
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

            query_2 = "SELECT file_name, local_base_path, datetime(target_modified_time, " + self.UTC + ") From jumplist " \
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

            query_3 = "SELECT file_name, local_base_path, datetime(target_accessed_time, " + self.UTC + ") From jumplist " \
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
        except:
            pass

    # 타임라인 - 안티포렌식 도구 실행
    def timeline_data2_2(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT Executable_Name, Full_Path, datetime(Last_Executed1," + self.UTC + ") from prefetch1 " \
                    " WHERE ((Executable_Name LIKE '%CCleaner%' OR Executable_Name LIKE 'Cipher%' " \
                    " OR Executable_Name LIKE 'Eraser%' OR Executable_Name LIKE 'SDelete%' " \
                    " OR Executable_Name LIKE 'SetMACE%' OR Executable_Name LIKE 'TimeStomp%'  " \
                    " OR Executable_Name LIKE 'Wise Folder Hider%') " \
                    " AND (Last_Executed1 >= '" + self.datetime1 + "' AND (Last_Executed1 <= '" + self.datetime2 + "')))"

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
        except:
            pass

    # 타임라인 - 클라우드 접근
    def timeline_data2_3(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT datetime(timestamp," + self.UTC + "), Title, URL FROM cloud " \
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
        except:
            pass

    # 타임라인 - 저장장치 연결 및 해제
    def timeline_data2_4(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT detailed, datetime(time_created," + self.UTC + "), bus_type, drive_manufac, drive_model FROM event_log WHERE ((event_id = '1006')" \
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
        except:
            pass

    # 타임라인 - 이벤트로그 삭제
    def timeline_data2_5(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT event_id, detailed, computer, datetime(time_created," + self.UTC + "), sbt_usr_name, channel FROM event_log " \
                    "WHERE (event_id = '104' or (event_id = '1102' AND sbt_usr_name IS NOT '' )" \
                    "AND (time_created >= '" + self.datetime1 + "' AND time_created <= '" + self.datetime2 + "'))"
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
        except:
            pass

    # tab3의 타임라인 컬러링
    def set_color(self):
        for i in range(self.timeline_count):
            for i in range(self.timeline_count):
                if self.timeline.item(i, 1).text() == "안티포렌식 도구 실행":
                    self.timeline.item(i, 1).setBackground(QtGui.QColor(255, 51, 51))
                elif self.timeline.item(i, 1).text() == "클라우드 접근":
                    self.timeline.item(i, 1).setBackground(QtGui.QColor(255, 255, 102))
                elif self.timeline.item(i, 1).text() == "이벤트로그 삭제":
                    self.timeline.item(i, 1).setBackground(QtGui.QColor(51, 102, 225))
                elif self.timeline.item(i, 1).text() == "시스템 시간 변경":
                    self.timeline.item(i, 1).setBackground(QtGui.QColor(255, 128, 0))
                elif self.timeline.item(i, 1).text() == "표준 시간대 변경":
                    self.timeline.item(i, 1).setBackground(QtGui.QColor(0, 128, 255))


#################################################
#   tab4                                        #
#################################################
    # tab4 구성
    def set_tab4(self):
        self.tab4.layout = QHBoxLayout(self)
        self.rightlayout = QVBoxLayout(self)
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
        # item2_1 네트워크 - 무선랜 접속 기록
        self.network_wireless = QTableWidget(self)
        self.set_network_wireless()
        self.tab4.layout.addWidget(self.network_wireless)
        self.tab4.layout.itemAt(1).widget().setParent(None)
        # item2_1_2 네트워크 - 인터페이스
        self.network_interface = QTableWidget(self)
        self.set_network_interface()
        self.tab4.layout.addWidget(self.network_interface)
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
        # item5_1_6 프로그램 실행 흔적 - 레지스트리 - CIDSizeMRU
        self.program_cidsizemru = QTableWidget(self)
        self.set_program_cidsizemru()
        self.tab4.layout.addWidget(self.program_cidsizemru)
        self.tab4.layout.itemAt(1).widget().setParent(None)
        # item5_1_7 프로그램 실행 흔적 - 레지스트리 - Legacy
        self.etc_dialog_table = QTableWidget(self)
        self.set_etc_dialog()
        self.tab4.layout.addWidget(self.etc_dialog_table)
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

        # item9_1 전체 파일 및 폴더
        self.file_and_folder_table = QTableWidget(self)
        self.set_file_and_folder()
        self.tab4.layout.addWidget(self.file_and_folder_table)
        self.tab4.layout.itemAt(1).widget().setParent(None)
        # item9_2 삭제된 파일 및 폴더
        self.del_file_and_folder_table = QTableWidget(self)
        self.set_del_file_and_folder()
        self.tab4.layout.addWidget(self.del_file_and_folder_table)
        self.tab4.layout.itemAt(1).widget().setParent(None)
        # item9_3 파일 변경 사항
        self.modified_file_table = QTableWidget(self)
        self.set_modified_file()
        self.tab4.layout.addWidget(self.modified_file_table)
        self.tab4.layout.itemAt(1).widget().setParent(None)
        # item9_4 최근 폴더 열람 흔적
        self.recent_folder_table = QTableWidget(self)
        self.set_recent_folder()
        self.tab4.layout.addWidget(self.recent_folder_table)
        self.tab4.layout.itemAt(1).widget().setParent(None)

        self.search = QLineEdit(self)
        self.search.setPlaceholderText("Search ...")
        self.rightlayout.addWidget(self.search)
        self.tab4_table = QTableWidget(self)
        self.rightlayout.addWidget(self.tab4_table)
        self.tab4.layout.addLayout(self.rightlayout)
        self.tab4.setLayout(self.tab4.layout)

        self.search.textChanged.connect(self.search_keyword)

    # tab4의 테이블 필터링 기능
    def search_keyword(self, s):
        items = self.rightlayout.itemAt(1).widget().findItems(s, Qt.MatchContains)

        for i in range(self.rightlayout.itemAt(1).widget().rowCount()):
            self.rightlayout.itemAt(1).widget().hideRow(i)

        for item in items:
            self.rightlayout.itemAt(1).widget().showRow(item.row())

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
        self.item1_2_1.setText(0, "Registry")
        self.item1_2_2 = QTreeWidgetItem(self.item1_2)
        self.item1_2_2.setText(0, "Event Log")
        self.item1_3 = QTreeWidgetItem(self.item1)
        self.item1_3.setText(0, "윈도우 업데이트")

        self.item2 = QTreeWidgetItem(self.tree)
        self.item2.setText(0, "네트워크")
        self.item2_1 = QTreeWidgetItem(self.item2)
        self.item2_1.setText(0, "무선랜 접속 기록")
        self.item2_1_2 = QTreeWidgetItem(self.item2)
        self.item2_1_2.setText(0, "인터페이스")
        self.item2_2 = QTreeWidgetItem(self.item2)
        self.item2_2.setText(0, "Event Log")

        self.item3 = QTreeWidgetItem(self.tree)
        self.item3.setText(0, "외부저장장치")
        self.item3_1 = QTreeWidgetItem(self.item3)
        self.item3_1.setText(0, "Registry")
        self.item3_2 = QTreeWidgetItem(self.item3)
        self.item3_2.setText(0, "Event Log")

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

        self.item55 = QTreeWidgetItem(self.tree)
        self.item55.setText(0, "실행 흔적")
        self.item5 = QTreeWidgetItem(self.item55)
        self.item5.setText(0, "프로그램 실행 흔적")
        self.item5_1 = QTreeWidgetItem(self.item5)
        self.item5_1.setText(0, "Registry")
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
        self.item5_1_7 = QTreeWidgetItem(self.item5_1)
        self.item5_1_7.setText(0, "Legacy")
        self.item5_2 = QTreeWidgetItem(self.item5)
        self.item5_2.setText(0, "Prefetch")

        self.item6 = QTreeWidgetItem(self.item55)
        self.item6.setText(0, "문서실행 흔적")
        self.item6_1 = QTreeWidgetItem(self.item6)
        self.item6_1.setText(0, "Registry")
        self.item6_2 = QTreeWidgetItem(self.item6)
        self.item6_2.setText(0, "LNK File")
        self.item6_3 = QTreeWidgetItem(self.item6)
        self.item6_3.setText(0, "Jumplist")
        self.item6_4 = QTreeWidgetItem(self.item6)
        self.item6_4.setText(0, "Prefetch")

        self.item7 = QTreeWidgetItem(self.item55)
        self.item7.setText(0, "기타실행 흔적")
        self.item7_1 = QTreeWidgetItem(self.item7)
        self.item7_1.setText(0, "LNK File")
        self.item7_2 = QTreeWidgetItem(self.item7)
        self.item7_2.setText(0, "Prefetch")

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
        self.item8_4.setText(0, "RDP")
        self.item8_4_1 = QTreeWidgetItem(self.item8_4)
        self.item8_4_1.setText(0, "RDP 접속 기록")
        self.item8_4_2 = QTreeWidgetItem(self.item8_4)
        self.item8_4_2.setText(0, "RDP 실행 기록")
        self.item8_5 = QTreeWidgetItem(self.item8)
        self.item8_5.setText(0, "시스템 시간 변경 기록")

        self.item9 = QTreeWidgetItem(self.tree)
        self.item9.setText(0, "파일 및 폴더")
        self.item9_1 = QTreeWidgetItem(self.item9)
        self.item9_1.setText(0, "전체 파일 및 폴더")
        self.item9_2 = QTreeWidgetItem(self.item9)
        self.item9_2.setText(0, "삭제된 파일 및 폴더")
        self.item9_3 = QTreeWidgetItem(self.item9)
        self.item9_3.setText(0, "파일 변경 사항")
        self.item9_4 = QTreeWidgetItem(self.item9)
        self.item9_4.setText(0, "최근 열람 폴더 흔적")

        self.tab4.layout.addWidget(self.tree)
        self.tree.itemClicked.connect(self.tab4_onItemClicked)

    # tab4의 tree의 아이템을 클릭할 시 레이아웃에서 현재 테이블을 클릭한 아이템의 테이블로 교체
    def tab4_onItemClicked(self, it, col):
        delete = self.rightlayout.itemAt(1).widget()

        if it is self.item1_1:
            delete.setParent(None)
            self.rightlayout.addWidget(self.PC_system_table)
            self.search.clear()
        if it is self.item1_2_1:
            delete.setParent(None)
            self.rightlayout.addWidget(self.PC_user_reg_table)
            self.search.clear()
        if it is self.item1_2_2:
            delete.setParent(None)
            self.rightlayout.addWidget(self.PC_user_evt_table)
            self.search.clear()
        if it is self.item1_3:
            delete.setParent(None)
            self.rightlayout.addWidget(self.PC_update_table)
            self.search.clear()
        if it is self.item2_1:
            delete.setParent(None)
            self.rightlayout.addWidget(self.network_wireless)
            self.search.clear()
        if it is self.item2_1_2:
            delete.setParent(None)
            self.rightlayout.addWidget(self.network_interface)
            self.search.clear()
        if it is self.item2_2:
            delete.setParent(None)
            self.rightlayout.addWidget(self.network_evt_table)
            self.search.clear()
        if it is self.item3_1:
            delete.setParent(None)
            self.rightlayout.addWidget(self.storage_reg_table)
            self.search.clear()
        if it is self.item3_2:
            delete.setParent(None)
            self.rightlayout.addWidget(self.storage_evt_table)
            self.search.clear()
        if it is self.item4_1:
            delete.setParent(None)
            self.rightlayout.addWidget(self.browser_search_table)
            self.search.clear()
        if it is self.item4_2:
            delete.setParent(None)
            self.rightlayout.addWidget(self.browser_dowload_table)
            self.search.clear()
        if it is self.item4_3:
            delete.setParent(None)
            self.rightlayout.addWidget(self.browser_url_table)
            self.search.clear()
        if it is self.item4_4:
            delete.setParent(None)
            self.rightlayout.addWidget(self.browser_login_table)
            self.search.clear()
        if it is self.item4_5:
            delete.setParent(None)
            self.rightlayout.addWidget(self.browser_cookies_table)
            self.search.clear()
        if it is self.item4_6:
            delete.setParent(None)
            self.rightlayout.addWidget(self.browser_cache_table)
            self.search.clear()
        if it is self.item4_7:
            delete.setParent(None)
            self.rightlayout.addWidget(self.browser_bookmark_table)
            self.search.clear()
        if it is self.item4_8:
            delete.setParent(None)
            self.rightlayout.addWidget(self.browser_autofill_table)
            self.search.clear()
        if it is self.item4_9:
            delete.setParent(None)
            self.rightlayout.addWidget(self.browser_preference_table)
            self.search.clear()
        if it is self.item4_10:
            delete.setParent(None)
            self.rightlayout.addWidget(self.browser_cloud_table)
            self.search.clear()
        if it is self.item5_1_1:
            delete.setParent(None)
            self.rightlayout.addWidget(self.program_bam)
            self.search.clear()
        if it is self.item5_1_2:
            delete.setParent(None)
            self.rightlayout.addWidget(self.program_userassist)
            self.search.clear()
        if it is self.item5_1_3:
            delete.setParent(None)
            self.rightlayout.addWidget(self.program_uninstall)
            self.search.clear()
        if it is self.item5_1_4:
            delete.setParent(None)
            self.rightlayout.addWidget(self.program_muicache)
            self.search.clear()
        if it is self.item5_1_5:
            delete.setParent(None)
            self.rightlayout.addWidget(self.program_firstfolder)
            self.search.clear()
        if it is self.item5_1_6:
            delete.setParent(None)
            self.rightlayout.addWidget(self.program_cidsizemru)
            self.search.clear()
        if it is self.item5_1_7:
            delete.setParent(None)
            self.rightlayout.addWidget(self.etc_dialog_table)
            self.search.clear()
        if it is self.item5_2:
            delete.setParent(None)
            self.rightlayout.addWidget(self.program_pre)
            self.search.clear()
        if it is self.item6_1:
            delete.setParent(None)
            self.rightlayout.addWidget(self.doc_reg_table)
            self.search.clear()
        if it is self.item6_2:
            delete.setParent(None)
            self.rightlayout.addWidget(self.doc_lnk_table)
            self.search.clear()
        if it is self.item6_3:
            delete.setParent(None)
            self.rightlayout.addWidget(self.doc_jmp_table)
            self.search.clear()
        if it is self.item6_4:
            delete.setParent(None)
            self.rightlayout.addWidget(self.doc_pre_table)
            self.search.clear()
        if it is self.item7_1:
            delete.setParent(None)
            self.rightlayout.addWidget(self.etc_lnk_table)
            self.search.clear()
        if it is self.item7_2:
            delete.setParent(None)
            self.rightlayout.addWidget(self.etc_pre_table)
            self.search.clear()
        if it is self.item8_1:
            delete.setParent(None)
            self.rightlayout.addWidget(self.eventlog_delete_table)
            self.search.clear()
        if it is self.item8_2:
            delete.setParent(None)
            self.rightlayout.addWidget(self.eventlog_terminate_table)
            self.search.clear()
        if it is self.item8_3_1:
            delete.setParent(None)
            self.rightlayout.addWidget(self.eventlog_onoff_table)
            self.search.clear()
        if it is self.item8_3_2:
            delete.setParent(None)
            self.rightlayout.addWidget(self.eventlog_powersaving_table)
            self.search.clear()
        if it is self.item8_4_1:
            delete.setParent(None)
            self.rightlayout.addWidget(self.eventlog_access1_table)
            self.search.clear()
        if it is self.item8_4_2:
            delete.setParent(None)
            self.rightlayout.addWidget(self.eventlog_access2_table)
            self.search.clear()
        if it is self.item8_5:
            delete.setParent(None)
            self.rightlayout.addWidget(self.eventlog_time_table)
            self.search.clear()
        if it is self.item9_1:
            delete.setParent(None)
            self.rightlayout.addWidget(self.file_and_folder_table)
            self.search.clear()
        if it is self.item9_2:
            delete.setParent(None)
            self.rightlayout.addWidget(self.del_file_and_folder_table)
            self.search.clear()
        if it is self.item9_3:
            delete.setParent(None)
            self.rightlayout.addWidget(self.modified_file_table)
            self.search.clear()
        if it is self.item9_4:
            delete.setParent(None)
            self.rightlayout.addWidget(self.recent_folder_table)
            self.search.clear()


#################################################
#   tab4의 테이블 구성                            #
#################################################
    # item1_1 시스템 정보
    def set_PC_system(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT product_name, product_ID, system_root, owner, organization, build_lab, " \
                    "timezone_name, active_time_bias, UTC, computer_name, default_user_name, last_used_user_name, " \
                    "datetime(shutdown_time, " + self.UTC + "), datetime(install_date, " + self.UTC + ") FROM OSInformation"
            cur.execute(query)
            rows = cur.fetchall()
            conn.close()

            count = len(rows)
            self.PC_system_table.setRowCount(count)
            self.PC_system_table.setColumnCount(14)
            column_headers = ["제품명", "제품 ID", "시스템 루트", "사용자", "설치 시간",
                           "제조사", "버전", "타임존", "time_bias", "UTC",
                           "컴퓨터 이름", "기본 사용자", "마지막 사용자", "종료 시간"]
            self.PC_system_table.setHorizontalHeaderLabels(column_headers)

            for i in range(len(rows)):
                product_name, product_ID, system_root, owner, organization, build_lab, \
                timezone_name, active_time_bias, UTC, computer_name, default_user_name, last_used_user_name, \
                shutdown_time, install_date = rows[i]
                self.PC_system_table.setItem(i, 0, QTableWidgetItem(product_name))
                self.PC_system_table.setItem(i, 1, QTableWidgetItem(product_ID))
                self.PC_system_table.setItem(i, 2, QTableWidgetItem(system_root))
                self.PC_system_table.setItem(i, 3, QTableWidgetItem(owner))
                self.PC_system_table.setItem(i, 4, QTableWidgetItem(install_date))
                self.PC_system_table.setItem(i, 5, QTableWidgetItem(organization))
                self.PC_system_table.setItem(i, 6, QTableWidgetItem(build_lab))
                self.PC_system_table.setItem(i, 7, QTableWidgetItem(timezone_name))
                self.PC_system_table.setItem(i, 8, QTableWidgetItem(str(active_time_bias)))
                self.PC_system_table.setItem(i, 9, QTableWidgetItem(str(UTC)))
                self.PC_system_table.setItem(i, 10, QTableWidgetItem(computer_name))
                self.PC_system_table.setItem(i, 11, QTableWidgetItem(default_user_name))
                self.PC_system_table.setItem(i, 12, QTableWidgetItem(last_used_user_name))
                self.PC_system_table.setItem(i, 13, QTableWidgetItem(shutdown_time))

            self.PC_system_table.resizeColumnsToContents()

        except:
            pass

    # item1_2_1 계정정보 - 레지스트리
    def set_PC_user_reg(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT RID_int, account_name, complete_account_name, logon_failure_count, logon_success_count, comment, homedir, " \
                    "datetime(last_login_time, " + self.UTC + "), datetime(last_password_change_time, " + self.UTC + "), " \
                    "datetime(expires_on, " + self.UTC + "), datetime(last_incorrect_password_time, " + self.UTC + "), " \
                    "datetime(created_on, " + self.UTC + ") FROM UserAccounts"
            cur.execute(query)
            rows = cur.fetchall()
            conn.close()

            count = len(rows)
            self.PC_user_reg_table.setRowCount(count)
            self.PC_user_reg_table.setColumnCount(12)
            column_headers = ["RID", "계정 생성 시간", "계정명", "전체 계정명", "로그인 실패 횟수", "로그인 성공 횟수", "설명", "홈 디렉토리",
                              "마지막 로그인 시간", "마지막 패스워드 변경 시간",
                              "만료", "마지막 패스워드 불일치 시간"]
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

                self.PC_user_reg_table.setColumnWidth(0, self.width() * 2 / 30)
                self.PC_user_reg_table.setColumnWidth(1, self.width() * 4 / 30)
                self.PC_user_reg_table.setColumnWidth(2, self.width() * 3 / 30)
                self.PC_user_reg_table.setColumnWidth(3, self.width() * 3 / 30)
                self.PC_user_reg_table.setColumnWidth(4, self.width() * 4 / 30)
                self.PC_user_reg_table.setColumnWidth(5, self.width() * 4 / 30)
                self.PC_user_reg_table.setColumnWidth(6, self.width() * 6 / 30)
                self.PC_user_reg_table.setColumnWidth(7, self.width() * 3 / 30)
                self.PC_user_reg_table.setColumnWidth(8, self.width() * 4 / 30)
                self.PC_user_reg_table.setColumnWidth(9, self.width() * 5 / 30)
                self.PC_user_reg_table.setColumnWidth(10, self.width() * 3 / 30)
                self.PC_user_reg_table.setColumnWidth(11, self.width() * 5 / 30)

        except:
            pass

    # item1_2_2 계정정보 - 이벤트로그
    def set_PC_user_evt(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT event_id, detailed, computer, sbt_usr_name, trg_usr_name, display_name, mem_sid, " \
                    "datetime(time_created, " + self.UTC + "), source FROM event_log " \
                    "WHERE (event_id LIKE '1004' OR event_id LIKE '1005' OR event_id LIKE '4624'" \
                    "OR event_id LIKE '4625' OR event_id LIKE '4720' OR event_id LIKE '4724' OR event_id LIKE '4726'" \
                    "OR event_id LIKE '4732' OR event_id LIKE '4733' OR event_id LIKE '4738')"
            cur.execute(query)
            rows = cur.fetchall()
            conn.close()

            count = len(rows)
            self.PC_user_evt_table.setRowCount(count)
            self.PC_user_evt_table.setColumnCount(9)
            column_headers = ["이벤트 아이디", "상세설명", "행위 발생 시간", "컴퓨터 이름", "주체 이름",
                              "타겟 이름", "Display", "Mem_Sid", "출처"]
            self.PC_user_evt_table.setHorizontalHeaderLabels(column_headers)

            for i in range(count):
                event_id, detailed, computer, sbt_usr_name, trg_usr_name, display_name, mem_sid, time_created, source = rows[i]
                self.PC_user_evt_table.setItem(i, 0, QTableWidgetItem(str(event_id)))
                self.PC_user_evt_table.setItem(i, 1, QTableWidgetItem(detailed))
                self.PC_user_evt_table.setItem(i, 2, QTableWidgetItem(time_created))
                self.PC_user_evt_table.setItem(i, 3, QTableWidgetItem(computer))
                self.PC_user_evt_table.setItem(i, 4, QTableWidgetItem(sbt_usr_name))
                self.PC_user_evt_table.setItem(i, 5, QTableWidgetItem(trg_usr_name))
                self.PC_user_evt_table.setItem(i, 6, QTableWidgetItem(display_name))
                self.PC_user_evt_table.setItem(i, 7, QTableWidgetItem(mem_sid))
                self.PC_user_evt_table.setItem(i, 8, QTableWidgetItem(source))

            self.PC_user_evt_table.setColumnWidth(0, self.width() * 3 / 30)
            self.PC_user_evt_table.setColumnWidth(1, self.width() * 6 / 30)
            self.PC_user_evt_table.setColumnWidth(2, self.width() * 4 / 30)
            self.PC_user_evt_table.setColumnWidth(3, self.width() * 4 / 30)
            self.PC_user_evt_table.setColumnWidth(4, self.width() * 5 / 30)
            self.PC_user_evt_table.setColumnWidth(5, self.width() * 3 / 30)
            self.PC_user_evt_table.setColumnWidth(6, self.width() * 3 / 30)
            self.PC_user_evt_table.setColumnWidth(7, self.width() * 3 / 30)
            self.PC_user_evt_table.setColumnWidth(8, self.width() * 5 / 30)
        except:
            pass

    # item1_3 윈도우 업데이트
    def set_PC_update(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT event_id, detailed, computer, package, datetime(time_created, " + self.UTC + "), source " \
                    "FROM event_log WHERE event_id LIKE '2'"
            cur.execute(query)
            rows = cur.fetchall()
            conn.close()

            count = len(rows)
            self.PC_update_table.setRowCount(count)
            self.PC_update_table.setColumnCount(6)
            column_headers = ["이벤트 로그", "상세설명", "행위 발생 시간", "컴퓨터 이름", "업데이트 내용", "출처"]
            self.PC_update_table.setHorizontalHeaderLabels(column_headers)

            for i in range(count):
                event_id, detailed, computer, package, time_created, source = rows[i]
                self.PC_update_table.setItem(i, 0, QTableWidgetItem(str(event_id)))
                self.PC_update_table.setItem(i, 1, QTableWidgetItem(detailed))
                self.PC_update_table.setItem(i, 2, QTableWidgetItem(time_created))
                self.PC_update_table.setItem(i, 3, QTableWidgetItem(computer))
                self.PC_update_table.setItem(i, 4, QTableWidgetItem(package))
                self.PC_update_table.setItem(i, 5, QTableWidgetItem(source))

            self.PC_update_table.setColumnWidth(0, self.width() * 3 / 30)
            self.PC_update_table.setColumnWidth(1, self.width() * 10 / 30)
            self.PC_update_table.setColumnWidth(2, self.width() * 4 / 30)
            self.PC_update_table.setColumnWidth(3, self.width() * 4 / 30)
            self.PC_update_table.setColumnWidth(4, self.width() * 3 / 30)
            self.PC_update_table.setColumnWidth(5, self.width() * 3 / 30)

        except:
            pass

    # item2_1 네트워크 - 무선랜 접속 기록
    def set_network_wireless(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT profile_name, description, GUID, default_gateway_mac, dns_suffix, " \
                    "datetime(created_time, " + self.UTC + "), datetime(last_connected_time, " + self.UTC + ") FROM Wireless;"
            cur.execute(query)
            rows = cur.fetchall()
            conn.close()

            count = len(rows)
            self.network_wireless.setRowCount(count)
            self.network_wireless.setColumnCount(7)
            column_headers = ["프로필", "상세", "GUID", "게이트웨이 맥주소", "DNS 접미사", "최초 연결", "마지막 연결"]
            self.network_wireless.setHorizontalHeaderLabels(column_headers)

            for i in range(count):
                profile_name, description, GUID, default_gateway_mac, dns_suffix, created, last_connected = rows[i]
                self.network_wireless.setItem(i, 0, QTableWidgetItem(profile_name))
                self.network_wireless.setItem(i, 1, QTableWidgetItem(description))
                self.network_wireless.setItem(i, 2, QTableWidgetItem(GUID))
                self.network_wireless.setItem(i, 3, QTableWidgetItem(default_gateway_mac))
                self.network_wireless.setItem(i, 4, QTableWidgetItem(dns_suffix))
                self.network_wireless.setItem(i, 5, QTableWidgetItem(created))
                self.network_wireless.setItem(i, 6, QTableWidgetItem(last_connected))
        except:
            pass

    # item2_1_2 네트워크 - 인터페이스
    def set_network_interface(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT description, GUID, ip, subnet_mask, default_gateway, dhcp_use, dhcp_server, dns_server, domain, " \
                    "datetime(lease_obtained_time, " + self.UTC + "), datetime(lease_terminates_time, " + self.UTC + ") FROM Network;"
            cur.execute(query)
            rows = cur.fetchall()
            conn.close()

            count = len(rows)
            self.network_interface.setRowCount(count)
            self.network_interface.setColumnCount(11)
            column_headers = ["설명", "GUID", "ip", "서브넷 마스크", "기본 게이트웨이", "DHCP 사용", "DHCP 서버", "DNS 서버", "도메인", "할당 시간", "만료 시간"]
            self.network_interface.setHorizontalHeaderLabels(column_headers)

            for i in range(count):
                description, GUID, ip, subnet_mask, default_gateway, dhcp_use, dhcp_server, dns_server, domain, \
                lease_obtained_time, lease_terminates_time = rows[i]
                if dhcp_use == 1:
                    dhcp_use = "사용"
                elif dhcp_use == 0:
                    dhcp_use = "사용 안 함"
                self.network_interface.setItem(i, 0, QTableWidgetItem(description))
                self.network_interface.setItem(i, 1, QTableWidgetItem(GUID))
                self.network_interface.setItem(i, 2, QTableWidgetItem(ip))
                self.network_interface.setItem(i, 3, QTableWidgetItem(subnet_mask))
                self.network_interface.setItem(i, 4, QTableWidgetItem(default_gateway))
                self.network_interface.setItem(i, 5, QTableWidgetItem(dhcp_use))
                self.network_interface.setItem(i, 6, QTableWidgetItem(dhcp_server))
                self.network_interface.setItem(i, 7, QTableWidgetItem(dns_server))
                self.network_interface.setItem(i, 8, QTableWidgetItem(domain))
                self.network_interface.setItem(i, 9, QTableWidgetItem(lease_obtained_time))
                self.network_interface.setItem(i, 10, QTableWidgetItem(lease_terminates_time))
        except:
            pass

    # item2_2 네트워크 - 이벤트로그
    def set_network_evt(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT event_id, detailed, computer, net_name, guid, conn_mode, reason, datetime(time_created, " + self.UTC + "), source " \
                    "FROM event_log WHERE (event_id = '10000' AND net_name IS NOT '') OR (event_id = '10001' AND net_name IS NOT '') OR event_id = '8003';"
            cur.execute(query)
            rows = cur.fetchall()
            conn.close()

            count = len(rows)
            self.network_evt_table.setRowCount(count)
            self.network_evt_table.setColumnCount(9)
            column_headers = ["이벤트 아이디", "상세설명", "컴퓨터 이름", "행위 발생 시간", "net_name", "GUID", "conn_mode", "reason", "출처"]
            self.network_evt_table.setHorizontalHeaderLabels(column_headers)

            for i in range(count):
                event_id, detailed, computer, net_name, guid, conn_mode, reason, time_created, source = rows[i]
                self.network_evt_table.setItem(i, 0, QTableWidgetItem(str(event_id)))
                self.network_evt_table.setItem(i, 1, QTableWidgetItem(detailed))
                self.network_evt_table.setItem(i, 2, QTableWidgetItem(computer))
                self.network_evt_table.setItem(i, 3, QTableWidgetItem(time_created))
                self.network_evt_table.setItem(i, 4, QTableWidgetItem(net_name))
                self.network_evt_table.setItem(i, 5, QTableWidgetItem(guid))
                self.network_evt_table.setItem(i, 6, QTableWidgetItem(conn_mode))
                self.network_evt_table.setItem(i, 7, QTableWidgetItem(reason))
                self.network_evt_table.setItem(i, 8, QTableWidgetItem(source))

            self.network_evt_table.setColumnWidth(0, self.width() * 3 / 30)
            self.network_evt_table.setColumnWidth(1, self.width() * 5 / 30)
            self.network_evt_table.setColumnWidth(2, self.width() * 4 / 30)
            self.network_evt_table.setColumnWidth(3, self.width() * 4 / 30)
            self.network_evt_table.setColumnWidth(4, self.width() * 6 / 30)
            self.network_evt_table.setColumnWidth(5, self.width() * 8 / 30)
            self.network_evt_table.setColumnWidth(6, self.width() * 5 / 30)
            self.network_evt_table.setColumnWidth(7, self.width() * 12 / 30)
            self.network_evt_table.setColumnWidth(8, self.width() * 3 / 30)

        except:
            pass

    # item3_1 외부저장장치 - 레지스트리
    def set_storage_reg(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT GUID, label, vendor_name, product_name, version, serial_num, " \
                    "datetime(first_connected, " + self.UTC + "), datetime(last_connected, " + self.UTC + ") FROM Connected_USB"
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

            self.storage_reg_table.setColumnWidth(0, self.width() * 8 / 30)
            self.storage_reg_table.setColumnWidth(1, self.width() * 3 / 30)
            self.storage_reg_table.setColumnWidth(2, self.width() * 3 / 30)
            self.storage_reg_table.setColumnWidth(3, self.width() * 3 / 30)
            self.storage_reg_table.setColumnWidth(4, self.width() * 2 / 30)
            self.storage_reg_table.setColumnWidth(5, self.width() * 4 / 30)
            self.storage_reg_table.setColumnWidth(6, self.width() * 4 / 30)
            self.storage_reg_table.setColumnWidth(7, self.width() * 4 / 30)

        except:
            pass

    # item3_2 외부저장장치 - 이벤트로그
    def set_storage_evt(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT event_id, detailed, computer, bus_type, drive_manufac, drive_serial, drive_model," \
                    "drive_location, datetime(time_created, " + self.UTC + ") FROM event_log WHERE event_id LIKE '1006'"
            cur.execute(query)
            rows = cur.fetchall()
            conn.close()

            count = len(rows)
            self.storage_evt_table.setRowCount(count)
            self.storage_evt_table.setColumnCount(9)
            column_headers = ["이벤트 아이디", "상세설명", "컴퓨터 이름", "행위 발생 시간", "연결 내용", "제조사", "시리얼 번호", "드라이브 모델",
                              "드라이브 위치"]
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

            self.storage_evt_table.setColumnWidth(0, self.width() * 3 / 30)
            self.storage_evt_table.setColumnWidth(1, self.width() * 10 / 30)
            self.storage_evt_table.setColumnWidth(2, self.width() * 4 / 30)
            self.storage_evt_table.setColumnWidth(3, self.width() * 4 / 30)
            self.storage_evt_table.setColumnWidth(4, self.width() * 3 / 30)
            self.storage_evt_table.setColumnWidth(5, self.width() * 3 / 30)
            self.storage_evt_table.setColumnWidth(6, self.width() * 4 / 30)
            self.storage_evt_table.setColumnWidth(7, self.width() * 6 / 30)
            self.storage_evt_table.setColumnWidth(8, self.width() * 3 / 30)
        except:
            pass

    # item4_1 검색 기록
    def set_browser_search(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT keyword, datetime(timestamp, " + self.UTC + ") FROM keyword"
            cur.execute(query)
            rows = cur.fetchall()
            conn.close()

            count = len(rows)
            self.browser_search_table.setRowCount(count)
            self.browser_search_table.setColumnCount(2)
            column_headers = ["키워드", "시간"]
            self.browser_search_table.setHorizontalHeaderLabels(column_headers)

            for i in range(count):
                keyword, timestamp = rows[i]
                self.browser_search_table.setItem(i, 0, QTableWidgetItem(keyword))
                self.browser_search_table.setItem(i, 1, QTableWidgetItem(timestamp))
            self.browser_search_table.resizeColumnsToContents()

            self.browser_search_table.setColumnWidth(0, self.width() * 22/ 30)
            self.browser_search_table.setColumnWidth(1, self.width() * 4 / 30)

        except:
            pass

    # item4_2 다운로드 기록
    def set_browser_download(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT url, status, path, interrupt_reason, danger_type, opened, etag, " \
                    "datetime(timestamp, " + self.UTC + "), datetime(last_modified, " + self.UTC + ") from download;"
            cur.execute(query)
            rows = cur.fetchall()
            conn.close()

            count = len(rows)
            self.browser_dowload_table.setRowCount(count)
            self.browser_dowload_table.setColumnCount(9)
            column_headers = ["URL", "경로", "다운로드 시간", "마지막 수정 시간", "상태", "실패 이유", "위험 파일", "열림 유무", "이태그"]
            self.browser_dowload_table.setHorizontalHeaderLabels(column_headers)

            for i in range(count):
                url, status, path, interrupt_reason, danger_type, opened, etag, \
                timestamp, last_modified = rows[i]
                self.browser_dowload_table.setItem(i, 0, QTableWidgetItem(url))
                self.browser_dowload_table.setItem(i, 1, QTableWidgetItem(path))
                self.browser_dowload_table.setItem(i, 2, QTableWidgetItem(timestamp))
                self.browser_dowload_table.setItem(i, 3, QTableWidgetItem(last_modified))
                self.browser_dowload_table.setItem(i, 4, QTableWidgetItem(status))
                self.browser_dowload_table.setItem(i, 5, QTableWidgetItem(interrupt_reason))
                self.browser_dowload_table.setItem(i, 6, QTableWidgetItem(danger_type))
                self.browser_dowload_table.setItem(i, 7, QTableWidgetItem(opened))
                self.browser_dowload_table.setItem(i, 8, QTableWidgetItem(etag))

            self.browser_dowload_table.setColumnWidth(0, self.width() * 10 / 30)
            self.browser_dowload_table.setColumnWidth(1, self.width() * 10 / 30)
            self.browser_dowload_table.setColumnWidth(2, self.width() * 4 / 30)
            self.browser_dowload_table.setColumnWidth(3, self.width() * 4 / 30)
            self.browser_dowload_table.setColumnWidth(4, self.width() * 4 / 30)
            self.browser_dowload_table.setColumnWidth(5, self.width() * 4 / 30)
            self.browser_dowload_table.setColumnWidth(6, self.width() * 4 / 30)
            self.browser_dowload_table.setColumnWidth(7, self.width() * 2 / 30)
            self.browser_dowload_table.setColumnWidth(8, self.width() * 4 / 30)

        except:
            pass

    # item4_3 URL 히스토리
    def set_browser_url(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT url, title, datetime(timestamp, " + self.UTC + "), source, visit_duration, visit_count, " \
                    "typed_count, url_hidden, transition from url;"
            cur.execute(query)
            rows = cur.fetchall()
            conn.close()

            count = len(rows)
            self.browser_url_table.setRowCount(count)
            self.browser_url_table.setColumnCount(9)
            column_headers = ["url", "제목", "시간", "소스", "머문 시간", "방문 횟수", "검색 횟수", "hidden 값", "접근 방식"]
            self.browser_url_table.setHorizontalHeaderLabels(column_headers)

            for i in range(count):
                url, title, timestamp, source, visit_duration, visit_count, typed_count, url_hidden, transition = rows[i]
                self.browser_url_table.setItem(i, 0, QTableWidgetItem(url))
                self.browser_url_table.setItem(i, 1, QTableWidgetItem(title))
                self.browser_url_table.setItem(i, 2, QTableWidgetItem(timestamp))
                self.browser_url_table.setItem(i, 3, QTableWidgetItem(source))
                self.browser_url_table.setItem(i, 4, QTableWidgetItem(visit_duration))
                self.browser_url_table.setItem(i, 5, QTableWidgetItem(str(visit_count)))
                self.browser_url_table.setItem(i, 6, QTableWidgetItem(str(typed_count)))
                self.browser_url_table.setItem(i, 7, QTableWidgetItem(str(url_hidden)))
                self.browser_url_table.setItem(i, 8, QTableWidgetItem(transition))

            self.browser_url_table.setColumnWidth(0, self.width() * 10 / 30)
            self.browser_url_table.setColumnWidth(1, self.width() * 10 / 30)
            self.browser_url_table.setColumnWidth(2, self.width() * 4 / 30)
            self.browser_url_table.setColumnWidth(3, self.width() * 2 / 30)
            self.browser_url_table.setColumnWidth(4, self.width() * 2 / 30)
            self.browser_url_table.setColumnWidth(5, self.width() * 2 / 30)
            self.browser_url_table.setColumnWidth(6, self.width() * 2 / 30)
            self.browser_url_table.setColumnWidth(7, self.width() * 2 / 30)
            self.browser_url_table.setColumnWidth(8, self.width() * 4 / 30)
        except:
            pass

    # item4_4 로그인 기록
    def set_browser_login(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT url, name, data, password_element, password_value," \
                    "datetime(timestamp, " + self.UTC + ") from login;"
            cur.execute(query)
            rows = cur.fetchall()
            conn.close()

            count = len(rows)
            self.browser_login_table.setRowCount(count)
            self.browser_login_table.setColumnCount(6)
            column_headers = ["로그인 url", "시간", "id임을 나타내는 값", "id 또는 계정", "password임을 나타내는 값", "비밀번호"]
            self.browser_login_table.setHorizontalHeaderLabels(column_headers)

            for i in range(count):
                url, name, data, password_element, password_value, timestamp = rows[i]
                self.browser_login_table.setItem(i, 0, QTableWidgetItem(url))
                self.browser_login_table.setItem(i, 1, QTableWidgetItem(timestamp))
                self.browser_login_table.setItem(i, 2, QTableWidgetItem(name))
                self.browser_login_table.setItem(i, 3, QTableWidgetItem(data))
                self.browser_login_table.setItem(i, 4, QTableWidgetItem(password_element))
                self.browser_login_table.setItem(i, 5, QTableWidgetItem(str(password_value)))

            self.browser_login_table.setColumnWidth(0, self.width() * 8 / 30)
            self.browser_login_table.setColumnWidth(1, self.width() * 4 / 30)
            self.browser_login_table.setColumnWidth(2, self.width() * 4 / 30)
            self.browser_login_table.setColumnWidth(3, self.width() * 5 / 30)
            self.browser_login_table.setColumnWidth(4, self.width() * 5 / 30)
            self.browser_login_table.setColumnWidth(5, self.width() * 4 / 30)
        except:
            pass

    # item4_5 쿠키
    def set_browser_cookies(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT url, title, value, datetime(timestamp, " + self.UTC + ") from cookies;"
            cur.execute(query)
            rows = cur.fetchall()
            conn.close()

            count = len(rows)
            self.browser_cookies_table.setRowCount(count)
            self.browser_cookies_table.setColumnCount(4)
            column_headers = ["url", "시간", "타이틀", "쿠키값"]
            self.browser_cookies_table.setHorizontalHeaderLabels(column_headers)

            for i in range(count):
                url, title, value, timestamp = rows[i]
                self.browser_cookies_table.setItem(i, 0, QTableWidgetItem(url))
                self.browser_cookies_table.setItem(i, 1, QTableWidgetItem(timestamp))
                self.browser_cookies_table.setItem(i, 2, QTableWidgetItem(title))
                self.browser_cookies_table.setItem(i, 3, QTableWidgetItem(value))

            self.browser_cookies_table.setColumnWidth(0, self.width() * 8 / 30)
            self.browser_cookies_table.setColumnWidth(1, self.width() * 4 / 30)
            self.browser_cookies_table.setColumnWidth(2, self.width() * 4 / 30)
            self.browser_cookies_table.setColumnWidth(3, self.width() * 4 / 30)

        except:
            pass

    # item4_6 캐시
    def set_browser_cache(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT url, value, datetime(timestamp, " + self.UTC + "), datetime(last_modified, " + self.UTC + "), " \
                    "status, etag, server_name, data_location, all_http_headers from cache;"
            cur.execute(query)
            rows = cur.fetchall()
            conn.close()

            count = len(rows)
            self.browser_cache_table.setRowCount(count)
            self.browser_cache_table.setColumnCount(9)
            column_headers = ["url", "파일", "생성 시간", "마지막 수정 시간", "상태", "etag",  "서버", "데이터 위치", "http 트래픽"]
            self.browser_cache_table.setHorizontalHeaderLabels(column_headers)

            for i in range(count):
                url, value, timestamp, last_modified, status, etag, server_name, data_location, all_http_headers = rows[
                    i]
                self.browser_cache_table.setItem(i, 0, QTableWidgetItem(url))
                self.browser_cache_table.setItem(i, 1, QTableWidgetItem(value))
                self.browser_cache_table.setItem(i, 2, QTableWidgetItem(timestamp))
                self.browser_cache_table.setItem(i, 3, QTableWidgetItem(last_modified))
                self.browser_cache_table.setItem(i, 4, QTableWidgetItem(status))
                self.browser_cache_table.setItem(i, 5, QTableWidgetItem(etag))
                self.browser_cache_table.setItem(i, 6, QTableWidgetItem(server_name))
                self.browser_cache_table.setItem(i, 7, QTableWidgetItem(data_location))
                self.browser_cache_table.setItem(i, 8, QTableWidgetItem(all_http_headers))

            self.browser_cache_table.setColumnWidth(0, self.width() * 8 / 30)
            self.browser_cache_table.setColumnWidth(1, self.width() * 8 / 30)
            self.browser_cache_table.setColumnWidth(2, self.width() * 4 / 30)
            self.browser_cache_table.setColumnWidth(3, self.width() * 4 / 30)
            self.browser_cache_table.setColumnWidth(4, self.width() * 4 / 30)
            self.browser_cache_table.setColumnWidth(5, self.width() * 4 / 30)
            self.browser_cache_table.setColumnWidth(6, self.width() * 4 / 30)
            self.browser_cache_table.setColumnWidth(7, self.width() * 4 / 30)
            self.browser_cache_table.setColumnWidth(8, self.width() * 9 / 30)
        except:
            pass

    # item4_7 북마크
    def set_browser_bookmark(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT url, title, value, datetime(timestamp, " + self.UTC + ") from bookmark;"
            cur.execute(query)
            rows = cur.fetchall()
            conn.close()

            count = len(rows)
            self.browser_bookmark_table.setRowCount(count)
            self.browser_bookmark_table.setColumnCount(4)
            column_headers = ["타이틀", "url", "시간",  "상위값"]
            self.browser_bookmark_table.setHorizontalHeaderLabels(column_headers)

            for i in range(count):
                url, title, value, timestamp = rows[i]
                self.browser_bookmark_table.setItem(i, 0, QTableWidgetItem(title))
                self.browser_bookmark_table.setItem(i, 1, QTableWidgetItem(url))
                self.browser_bookmark_table.setItem(i, 2, QTableWidgetItem(timestamp))
                self.browser_bookmark_table.setItem(i, 3, QTableWidgetItem(value))

            self.browser_bookmark_table.setColumnWidth(0, self.width() * 8 / 30)
            self.browser_bookmark_table.setColumnWidth(1, self.width() * 10 / 30)
            self.browser_bookmark_table.setColumnWidth(2, self.width() * 4 / 30)
            self.browser_bookmark_table.setColumnWidth(3, self.width() * 4 / 30)

        except:
            pass

    # item4_8 자동완성
    def set_browser_autofill(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT status, value, datetime(timestamp, " + self.UTC + ") from autofill;"
            cur.execute(query)
            rows = cur.fetchall()
            conn.close()

            count = len(rows)
            self.browser_autofill_table.setRowCount(count)
            self.browser_autofill_table.setColumnCount(3)
            column_headers = ["id/email", "자동 완성 값", "시간", ]
            self.browser_autofill_table.setHorizontalHeaderLabels(column_headers)

            for i in range(count):
                status, value, timestamp = rows[i]
                self.browser_autofill_table.setItem(i, 0, QTableWidgetItem(status))
                self.browser_autofill_table.setItem(i, 1, QTableWidgetItem(value))
                self.browser_autofill_table.setItem(i, 2, QTableWidgetItem(timestamp))

            self.browser_autofill_table.setColumnWidth(0, self.width() * 8 / 30)
            self.browser_autofill_table.setColumnWidth(1, self.width() * 10 / 30)
            self.browser_autofill_table.setColumnWidth(2, self.width() * 4 / 30)

        except:
            pass

    # item4_9 환경설정
    def set_browser_preference(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT url, status, data, datetime(timestamp, " + self.UTC + ") FROM preference;"
            cur.execute(query)
            rows = cur.fetchall()
            conn.close()

            count = len(rows)
            self.browser_preference_table.setRowCount(count)
            self.browser_preference_table.setColumnCount(4)
            column_headers = ["url", "시간", "상태", "데이터"]
            self.browser_preference_table.setHorizontalHeaderLabels(column_headers)

            for i in range(count):
                url, status, data, timestamp = rows[i]
                self.browser_preference_table.setItem(i, 0, QTableWidgetItem(url))
                self.browser_preference_table.setItem(i, 1, QTableWidgetItem(timestamp))
                self.browser_preference_table.setItem(i, 2, QTableWidgetItem(status))
                self.browser_preference_table.setItem(i, 3, QTableWidgetItem(data))

            self.browser_preference_table.setColumnWidth(0, self.width() * 10 / 30)
            self.browser_preference_table.setColumnWidth(1, self.width() * 4 / 30)
            self.browser_preference_table.setColumnWidth(2, self.width() * 6 / 30)
            self.browser_preference_table.setColumnWidth(3, self.width() * 6 / 30)


        except:
            pass

    # item4_10 클라우드 접속기록
    def set_browser_cloud(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT url, title, datetime(timestamp, " + self.UTC + ") FROM cloud;"
            cur.execute(query)
            rows = cur.fetchall()
            conn.close()

            count = len(rows)
            self.browser_cloud_table.setRowCount(count)
            self.browser_cloud_table.setColumnCount(3)
            column_headers = ["사이트 제목", "url", "접근 시간",]
            self.browser_cloud_table.setHorizontalHeaderLabels(column_headers)

            for i in range(count):
                url, title, timestamp = rows[i]
                self.browser_cloud_table.setItem(i, 0, QTableWidgetItem(title))
                self.browser_cloud_table.setItem(i, 1, QTableWidgetItem(url))
                self.browser_cloud_table.setItem(i, 2, QTableWidgetItem(timestamp))

            self.browser_cloud_table.setColumnWidth(0, self.width() * 10 / 30)
            self.browser_cloud_table.setColumnWidth(1, self.width() * 10 / 30)
            self.browser_cloud_table.setColumnWidth(2, self.width() * 4 / 30)

        except:
            pass

    # item5_1_1 프로그램 실행 흔적 - 레지스트리 - BAM
    def set_program_bam(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT SID, program_path, datetime(last_executed, " + self.UTC + ") FROM BAM;"
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

            self.program_bam.setColumnWidth(0, self.width() * 9 / 30)
            self.program_bam.setColumnWidth(1, self.width() * 16 / 30)
            self.program_bam.setColumnWidth(2, self.width() * 4 / 30)

        except:
            pass

    # item5_1_2 프로그램 실행 흔적 - 레지스트리 - UserAssist
    def set_program_userassist(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT name, run_count, datetime(last_executed, " + self.UTC + ") FROM UserAssist_CEB;"
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
                self.program_userassist.setItem(i, 1, QTableWidgetItem(str(run_count)))
                self.program_userassist.setItem(i, 2, QTableWidgetItem(last_executed))

            self.program_userassist.setColumnWidth(0, self.width() * 15 / 30)
            self.program_userassist.setColumnWidth(1, self.width() * 3 / 30)
            self.program_userassist.setColumnWidth(2, self.width() * 4 / 30)

        except:
            pass

    # item5_1_3 프로그램 실행 흔적 - 레지스트리 - Uninstall
    def set_program_uninstall(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT name, version, install_location, publisher, type, datetime(install_date, " + self.UTC + ") FROM Uninstall;"
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

            self.program_uninstall.setColumnWidth(0, self.width() * 7 / 30)
            self.program_uninstall.setColumnWidth(1, self.width() * 3 / 30)
            self.program_uninstall.setColumnWidth(2, self.width() * 8 / 30)
            self.program_uninstall.setColumnWidth(3, self.width() * 5 / 30)
            self.program_uninstall.setColumnWidth(4, self.width() * 2 / 30)
            self.program_uninstall.setColumnWidth(5, self.width() * 4 / 30)

        except:
            pass

    # item5_1_4 프로그램 실행 흔적 - 레지스트리 - MuiCache
    def set_program_muicache(self):
        try:
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

            self.program_muicache.setColumnWidth(0, self.width() * 9 / 30)
            self.program_muicache.setColumnWidth(1, self.width() * 20 / 30)
        except:
            pass

    # item5_1_5 프로그램 실행 흔적 - 레지스트리 - FirstFolder
    def set_program_firstfolder(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT program_name, folder, mru, datetime(opened_on, " + self.UTC + ") FROM FirstFolder;"
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
                self.program_firstfolder.setItem(i, 2, QTableWidgetItem(str(mru)))
                self.program_firstfolder.setItem(i, 3, QTableWidgetItem(opened_on))

            self.program_firstfolder.setColumnWidth(0, self.width() * 8 / 30)
            self.program_firstfolder.setColumnWidth(1, self.width() * 15 / 30)
            self.program_firstfolder.setColumnWidth(2, self.width() * 2 / 30)
            self.program_firstfolder.setColumnWidth(3, self.width() * 4 / 30)
        except:
            pass

    # item5_1_6 프로그램 실행 흔적 - 레지스트리 - CIDSizeMRU
    def set_program_cidsizemru(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT program_name, mru, datetime(opened_on, " + self.UTC + ") FROM CIDSizeMRU;"
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
                self.program_cidsizemru.setItem(i, 1, QTableWidgetItem(str(mru)))
                self.program_cidsizemru.setItem(i, 2, QTableWidgetItem(opened_on))

            self.program_cidsizemru.setColumnWidth(0, self.width() * 20 / 30)
            self.program_cidsizemru.setColumnWidth(1, self.width() * 2 / 30)
            self.program_cidsizemru.setColumnWidth(2, self.width() * 4 / 30)

        except:
            pass

    # item5_1_7 프로그램 실행 흔적 - 레지스트리 - Legacy
    def set_etc_dialog(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT program, mru, datetime(opened_on, " + self.UTC + ") FROM Legacy"
            cur.execute(query)
            rows = cur.fetchall()
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

            self.etc_dialog_table.setColumnWidth(0, self.width() * 4 / 30)
            self.etc_dialog_table.setColumnWidth(1, self.width() * 4 / 30)
            self.etc_dialog_table.setColumnWidth(2, self.width() * 4 / 30)

        except:
            pass

    # item5_2 프로그램 실행 흔적 - 프리패치
    def set_program_pre(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT Executable_Name, Run_Count, " \
                    "datetime(Last_Executed1, " + self.UTC + "), datetime(Last_Executed2, " + self.UTC + "), " \
                    "datetime(Last_Executed3, " + self.UTC + "), datetime(Last_Executed4, " + self.UTC + "), " \
                    "datetime(Last_Executed5, " + self.UTC + "), datetime(Last_Executed6, " + self.UTC + "), " \
                    "datetime(Last_Executed7, " + self.UTC + "), datetime(Last_Executed8, " + self.UTC + ") FROM prefetch1"
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

            self.program_pre.setColumnWidth(0, self.width() * 7 / 30)
            self.program_pre.setColumnWidth(1, self.width() * 2 / 30)
            self.program_pre.setColumnWidth(2, self.width() * 4 / 30)
            self.program_pre.setColumnWidth(3, self.width() * 4 / 30)
            self.program_pre.setColumnWidth(4, self.width() * 4 / 30)
            self.program_pre.setColumnWidth(5, self.width() * 4 / 30)
            self.program_pre.setColumnWidth(6, self.width() * 4 / 30)
            self.program_pre.setColumnWidth(7, self.width() * 4 / 30)
            self.program_pre.setColumnWidth(8, self.width() * 4 / 30)
            self.program_pre.setColumnWidth(9, self.width() * 4 / 30)

        except:
            pass

    # item6_1 문서실행 흔적 - 레지스트리
    def set_doc_reg(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT program, lnk, datetime(opened_on, " + self.UTC + ") FROM RecentDocs WHERE (program LIKE '%.pdf' OR program LIKE '%.hwp' " \
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

            self.doc_reg_table.setColumnWidth(0, self.width() * 11 / 30)
            self.doc_reg_table.setColumnWidth(1, self.width() * 11 / 30)
            self.doc_reg_table.setColumnWidth(2, self.width() * 4 / 30)

        except:
            pass

    # item6_2 문서실행 흔적 - 링크 파일
    def set_doc_lnk(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "select file_name, lnk_file_full_path, file_flags, file_size, local_base_path, show_command, " \
                    "datetime(target_accessed_time, " + self.UTC + "), datetime(target_creation_time," + self.UTC + ")," \
                    "datetime(target_modified_time, " + self.UTC + "), drive_serial_number, drive_type, volume_label, " \
                    "icon_location, machine_info FROM lnk_files WHERE (local_base_path LIKE '%.pdf' OR local_base_path LIKE '%.hwp' " \
                    "OR local_base_path LIKE '%.docx' OR local_base_path LIKE '%.doc' OR local_base_path LIKE '%.xlsx' " \
                    "OR local_base_path LIKE '%.csv' OR local_base_path LIKE '%.pptx' OR local_base_path LIKE '%.ppt' " \
                    "OR local_base_path LIKE '%.txt')"
            cur.execute(query)
            rows = cur.fetchall()
            conn.close()

            count = len(rows)
            self.doc_lnk_table.setRowCount(count)
            self.doc_lnk_table.setColumnCount(14)
            column_headers = ["파일", "링크 파일 경로", "플래그", "크기", "원본 파일 경로", "Show_Command",
                              "원본 생성 시간", "원본 수정 시간", "원본 접근 시간", "드라이브 시리얼 번호",
                              "드라이브 타입", "볼륨 라벨", "아이콘 경로", "NetBIOS 이름"]
            self.doc_lnk_table.setHorizontalHeaderLabels(column_headers)

            for i in range(count):
                file_name, lnk_file_full_path, file_flags, file_size, local_base_path, show_command, \
                target_creation_time, target_modified_time, target_accessed_time, \
                drive_serial_number, drive_type, volume_label, icon_location, machine_info = rows[i]
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

            self.doc_lnk_table.setColumnWidth(0, self.width() * 6 / 30)
            self.doc_lnk_table.setColumnWidth(1, self.width() * 10 / 30)
            self.doc_lnk_table.setColumnWidth(2, self.width() * 5 / 30)
            self.doc_lnk_table.setColumnWidth(3, self.width() * 2 / 30)
            self.doc_lnk_table.setColumnWidth(4, self.width() * 8 / 30)
            self.doc_lnk_table.setColumnWidth(5, self.width() * 3 / 30)
            self.doc_lnk_table.setColumnWidth(6, self.width() * 4 / 30)
            self.doc_lnk_table.setColumnWidth(7, self.width() * 4 / 30)
            self.doc_lnk_table.setColumnWidth(8, self.width() * 4 / 30)
            self.doc_lnk_table.setColumnWidth(9, self.width() * 4 / 30)
        except:
            pass

    # item6_3 문서실행 흔적 - 점프 목록
    def set_doc_jmp(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT file_name, jump_file_name, lnk_counter, local_base_path, file_size, file_flags, show_command, icon, description, volume_label, drive_type, " \
                    "datetime(target_creation_time, " + self.UTC + "), datetime(target_modified_time, " + self.UTC + "), datetime(target_accessed_time, " + self.UTC + ")" \
                    " FROM jumplist WHERE (local_base_path LIKE '%.pdf' OR local_base_path LIKE '%.hwp' OR local_base_path LIKE '%.docx' " \
                    "OR local_base_path LIKE '%.doc' OR local_base_path LIKE '%.xlsx' OR local_base_path LIKE '%.csv' OR local_base_path LIKE '%.pptx' " \
                    "OR local_base_path LIKE '%.ppt' OR local_base_path LIKE '%.txt')"
            cur.execute(query)
            rows = cur.fetchall()
            conn.close()

            count = len(rows)
            self.doc_jmp_table.setRowCount(count)
            self.doc_jmp_table.setColumnCount(14)
            column_headers = ["파일 이름", "점프리스트 이름", "링크 넘버", "원본 파일 경로", "사이즈", "플래그",
                              "원본 생성 시간", "원본 수정 시간", "원본 접근 시간", "Show_Command", "아이콘 경로", "행위",
                              "볼륨 라벨", "드라이브 타입"]
            self.doc_jmp_table.setHorizontalHeaderLabels(column_headers)

            for i in range(count):
                file_name, jump_file_name, lnk_counter, local_base_path, file_size, file_flags, show_command, icon, description, volume_label, drive_type, \
                target_creation_time, target_modified_time, target_accessed_time, = rows[i]
                self.doc_jmp_table.setItem(i, 0, QTableWidgetItem(file_name))
                self.doc_jmp_table.setItem(i, 1, QTableWidgetItem(jump_file_name))
                self.doc_jmp_table.setItem(i, 2, QTableWidgetItem(lnk_counter))
                self.doc_jmp_table.setItem(i, 3, QTableWidgetItem(local_base_path))
                self.doc_jmp_table.setItem(i, 4, QTableWidgetItem(file_size))
                self.doc_jmp_table.setItem(i, 5, QTableWidgetItem(file_flags))
                self.doc_jmp_table.setItem(i, 6, QTableWidgetItem(target_creation_time))
                self.doc_jmp_table.setItem(i, 7, QTableWidgetItem(target_modified_time))
                self.doc_jmp_table.setItem(i, 8, QTableWidgetItem(target_accessed_time))
                self.doc_jmp_table.setItem(i, 9, QTableWidgetItem(show_command))
                self.doc_jmp_table.setItem(i, 10, QTableWidgetItem(icon))
                self.doc_jmp_table.setItem(i, 11, QTableWidgetItem(description))
                self.doc_jmp_table.setItem(i, 12, QTableWidgetItem(volume_label))
                self.doc_jmp_table.setItem(i, 13, QTableWidgetItem(drive_type))

            self.doc_jmp_table.setColumnWidth(0, self.width() * 6 / 30)
            self.doc_jmp_table.setColumnWidth(1, self.width() * 6 / 30)
            self.doc_jmp_table.setColumnWidth(2, self.width() * 2 / 30)
            self.doc_jmp_table.setColumnWidth(3, self.width() * 8 / 30)
            self.doc_jmp_table.setColumnWidth(4, self.width() * 2 / 30)
            self.doc_jmp_table.setColumnWidth(5, self.width() * 2 / 30)
            self.doc_jmp_table.setColumnWidth(6, self.width() * 4 / 30)
            self.doc_jmp_table.setColumnWidth(7, self.width() * 4 / 30)
            self.doc_jmp_table.setColumnWidth(8, self.width() * 4 / 30)
            self.doc_jmp_table.setColumnWidth(9, self.width() * 4 / 30)
            self.doc_jmp_table.setColumnWidth(10, self.width() * 3 / 30)
            self.doc_jmp_table.setColumnWidth(11, self.width() * 2 / 30)
            self.doc_jmp_table.setColumnWidth(12, self.width() * 4 / 30)
            self.doc_jmp_table.setColumnWidth(13, self.width() * 4 / 30)

        except:
            pass

    # item6_4 문서실행 흔적 - 프리패치
    def set_doc_pre(self):
        try:
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

            self.doc_pre_table.setColumnWidth(0, self.width() * 11 / 30)
            self.doc_pre_table.setColumnWidth(1, self.width() * 18 / 30)

        except:
            pass

    # item7_1 기타실행 흔적 - 링크 파일
    def set_etc_lnk(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT file_name, lnk_file_full_path, file_flags, file_size, local_base_path, show_command, " \
                    "datetime(target_accessed_time, " + self.UTC + "), datetime(target_creation_time, " + self.UTC + "), datetime(target_modified_time, " + self.UTC + "), " \
                    "drive_serial_number, drive_type, volume_label, icon_location, machine_info " \
                    "FROM lnk_files WHERE(local_base_path LIKE '%.jpg' OR local_base_path LIKE '%.jpeg' OR local_base_path LIKE '%.gif' " \
                    "OR local_base_path LIKE '%.bmp' OR local_base_path LIKE '%.png' OR local_base_path LIKE '%.raw' OR local_base_path LIKE '%.tiff' " \
                    "OR local_base_path LIKE '%.wav' OR local_base_path LIKE '%.wma' OR local_base_path LIKE '%.mp3' OR local_base_path LIKE '%.mp4' " \
                    "OR local_base_path LIKE '%.mkv' OR local_base_path LIKE '%.avi' OR local_base_path LIKE '%.flv' OR local_base_path LIKE '%.mov' " \
                    "OR local_base_path LIKE '%.zip' OR local_base_path LIKE '%.7z' OR local_base_path LIKE '%.alz' OR local_base_path LIKE '%.egg' " \
                    "OR local_base_path LIKE '%.rar')"
            cur.execute(query)
            rows = cur.fetchall()
            conn.close()

            count = len(rows)
            self.etc_lnk_table.setRowCount(count)
            self.etc_lnk_table.setColumnCount(14)
            column_headers = ["파일", "링크 파일 경로", "플래그", "크기", "원본 파일 경로", "Show_Command",
                              "원본 생성 시간", "원본 수정 시간", "원본 접근 시간", "드라이브 시리얼 번호",
                              "드라이브 타입", "볼륨 라벨", "아이콘 경로", "NetBIOS 이름"]
            self.etc_lnk_table.setHorizontalHeaderLabels(column_headers)

            for i in range(count):
                file_name, lnk_file_full_path, file_flags, file_size, local_base_path, show_command, \
                target_creation_time, target_modified_time, target_accessed_time, \
                drive_serial_number, drive_type, volume_label, icon_location, machine_info = rows[i]
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

            self.etc_lnk_table.setColumnWidth(0, self.width() * 6 / 30)
            self.etc_lnk_table.setColumnWidth(1, self.width() * 10 / 30)
            self.etc_lnk_table.setColumnWidth(2, self.width() * 5 / 30)
            self.etc_lnk_table.setColumnWidth(3, self.width() * 2 / 30)
            self.etc_lnk_table.setColumnWidth(4, self.width() * 8 / 30)
            self.etc_lnk_table.setColumnWidth(5, self.width() * 4 / 30)
            self.etc_lnk_table.setColumnWidth(6, self.width() * 4 / 30)
            self.etc_lnk_table.setColumnWidth(7, self.width() * 4 / 30)
            self.etc_lnk_table.setColumnWidth(8, self.width() * 4 / 30)
            self.etc_lnk_table.setColumnWidth(9, self.width() * 4 / 30)
            self.etc_lnk_table.setColumnWidth(10, self.width() * 4 / 30)
            self.etc_lnk_table.setColumnWidth(11, self.width() * 4 / 30)
            self.etc_lnk_table.setColumnWidth(12, self.width() * 4 / 30)
            self.etc_lnk_table.setColumnWidth(13, self.width() * 4 / 30)

        except:
            pass

    # item7_2 기타실행 흔적 - 프리패치
    def set_etc_pre(self):
        try:
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

            self.etc_pre_table.setColumnWidth(0, self.width() * 11 / 30)
            self.etc_pre_table.setColumnWidth(1, self.width() * 18 / 30)
        except:
            pass

    # item8_1 이벤트 로그 삭제
    def set_eventlog_delete(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT event_id, detailed, computer, sbt_usr_name, channel, " \
                    "datetime(time_created, " + self.UTC + "), source FROM event_log WHERE event_id == '104' or event_id == '1102'"

            cur.execute(query)
            rows = cur.fetchall()
            conn.close()

            count = len(rows)
            self.eventlog_delete_table.setRowCount(count)
            self.eventlog_delete_table.setColumnCount(7)
            column_headers = ["이벤트 아이디", "상세 설명", "컴퓨터 이름", "행위 발생 시간", "주체 이름", "채널", "출처"]
            self.eventlog_delete_table.setHorizontalHeaderLabels(column_headers)

            for i in range(count):
                event_id, detailed, computer, sbt_usr_name, channel, time_created, source = rows[i]
                self.eventlog_delete_table.setItem(i, 0, QTableWidgetItem(str(event_id)))
                self.eventlog_delete_table.setItem(i, 1, QTableWidgetItem(detailed))
                self.eventlog_delete_table.setItem(i, 2, QTableWidgetItem(computer))
                self.eventlog_delete_table.setItem(i, 3, QTableWidgetItem(time_created))
                self.eventlog_delete_table.setItem(i, 4, QTableWidgetItem(sbt_usr_name))
                self.eventlog_delete_table.setItem(i, 5, QTableWidgetItem(channel))
                self.eventlog_delete_table.setItem(i, 6, QTableWidgetItem(source))

            self.eventlog_delete_table.setColumnWidth(0, self.width() * 3 / 30)
            self.eventlog_delete_table.setColumnWidth(1, self.width() * 10 / 30)
            self.eventlog_delete_table.setColumnWidth(2, self.width() * 4 / 30)
            self.eventlog_delete_table.setColumnWidth(3, self.width() * 4 / 30)
            self.eventlog_delete_table.setColumnWidth(4, self.width() * 3 / 30)
            self.eventlog_delete_table.setColumnWidth(5, self.width() * 3 / 30)
            self.eventlog_delete_table.setColumnWidth(6, self.width() * 3 / 30)

        except:
            pass

    # item8_2 프로세스 강제 종료
    def set_eventlog_terminate(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT event_id, detailed, computer, app_name, app_version, app_path, " \
                    "datetime(time_created, " + self.UTC + "), source FROM event_log WHERE event_id == '1002' AND app_name IS NOT '';"
            cur.execute(query)
            rows = cur.fetchall()
            count = len(rows)
            self.eventlog_terminate_table.setRowCount(count)
            self.eventlog_terminate_table.setColumnCount(8)
            column_headers = ["이벤트 아이디", "상세설명", "컴퓨터 이름", "행위 발생 시간", "프로세스 이름", "프로그램 버전", "경로", "출처"]
            self.eventlog_terminate_table.setHorizontalHeaderLabels(column_headers)

            for i in range(count):
                event_id, detailed, computer, app_name, app_version, app_path, time_created, source = rows[i]
                self.eventlog_terminate_table.setItem(i, 0, QTableWidgetItem(str(event_id)))
                self.eventlog_terminate_table.setItem(i, 1, QTableWidgetItem(detailed))
                self.eventlog_terminate_table.setItem(i, 2, QTableWidgetItem(computer))
                self.eventlog_terminate_table.setItem(i, 3, QTableWidgetItem(time_created))
                self.eventlog_terminate_table.setItem(i, 4, QTableWidgetItem(app_name))
                self.eventlog_terminate_table.setItem(i, 5, QTableWidgetItem(app_version))
                self.eventlog_terminate_table.setItem(i, 6, QTableWidgetItem(app_path))
                self.eventlog_terminate_table.setItem(i, 7, QTableWidgetItem(source))

            self.eventlog_terminate_table.setColumnWidth(0, self.width() * 3 / 30)
            self.eventlog_terminate_table.setColumnWidth(1, self.width() * 3 / 30)
            self.eventlog_terminate_table.setColumnWidth(2, self.width() * 4 / 30)
            self.eventlog_terminate_table.setColumnWidth(3, self.width() * 4 / 30)
            self.eventlog_terminate_table.setColumnWidth(4, self.width() * 4 / 30)
            self.eventlog_terminate_table.setColumnWidth(5, self.width() * 4 / 30)
            self.eventlog_terminate_table.setColumnWidth(6, self.width() * 10 / 30)
            self.eventlog_terminate_table.setColumnWidth(7, self.width() * 3 / 30)
        except:
            pass

    # item8_3_1 PC 전원 기록 - 운영체제 시작 및 종료
    def set_eventlog_onoff(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT event_id, detailed, computer, " \
                    "datetime(time_created, " + self.UTC + "), source FROM event_log WHERE event_id = '12' OR event_id = '13';"
            cur.execute(query)
            rows = cur.fetchall()
            count = len(rows)
            self.eventlog_onoff_table.setRowCount(count)
            self.eventlog_onoff_table.setColumnCount(5)
            column_headers = ["이벤트 아이디", "상세설명", "컴퓨터 이름", "행위 발생 시간", "출처"]
            self.eventlog_onoff_table.setHorizontalHeaderLabels(column_headers)

            for i in range(count):
                event_id, detailed, computer, time_created, source = rows[i]
                self.eventlog_onoff_table.setItem(i, 0, QTableWidgetItem(str(event_id)))
                self.eventlog_onoff_table.setItem(i, 1, QTableWidgetItem(detailed))
                self.eventlog_onoff_table.setItem(i, 2, QTableWidgetItem(computer))
                self.eventlog_onoff_table.setItem(i, 3, QTableWidgetItem(time_created))
                self.eventlog_onoff_table.setItem(i, 4, QTableWidgetItem(source))

            self.eventlog_onoff_table.setColumnWidth(0, self.width() * 3 / 30)
            self.eventlog_onoff_table.setColumnWidth(1, self.width() * 4 / 30)
            self.eventlog_onoff_table.setColumnWidth(2, self.width() * 4 / 30)
            self.eventlog_onoff_table.setColumnWidth(3, self.width() * 4 / 30)
            self.eventlog_onoff_table.setColumnWidth(4, self.width() * 3 / 30)

        except:
            pass

    # item8_3_2 PC 전원 기록 - 절전모드 전환 및 해제
    def set_eventlog_powersaving(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT event_id, detailed, computer, datetime(time_created, " + self.UTC + "), " \
                    "datetime(sleep_time, " + self.UTC + "), datetime(wake_time, " + self.UTC + "), source " \
                    "FROM event_log WHERE (event_id = '1' AND sleep_time IS NOT '') OR (event_id = '42' AND source IS 'System.evtx')"
            cur.execute(query)
            rows = cur.fetchall()
            conn.close()

            count = len(rows)
            self.eventlog_powersaving_table.setRowCount(count)
            self.eventlog_powersaving_table.setColumnCount(7)
            column_headers = ["이벤트 아이디", "상세설명", "컴퓨터 이름", "행위 발생 시간", "전환시간", "복귀시간", "출처"]
            self.eventlog_powersaving_table.setHorizontalHeaderLabels(column_headers)

            for i in range(count):
                event_id, detailed, computer, time_created, sleep_time, wake_time, source = rows[i]
                self.eventlog_powersaving_table.setItem(i, 0, QTableWidgetItem(str(event_id)))
                self.eventlog_powersaving_table.setItem(i, 1, QTableWidgetItem(detailed))
                self.eventlog_powersaving_table.setItem(i, 2, QTableWidgetItem(computer))
                self.eventlog_powersaving_table.setItem(i, 3, QTableWidgetItem(time_created))
                self.eventlog_powersaving_table.setItem(i, 4, QTableWidgetItem(sleep_time))
                self.eventlog_powersaving_table.setItem(i, 5, QTableWidgetItem(wake_time))
                self.eventlog_powersaving_table.setItem(i, 6, QTableWidgetItem(source))

            self.eventlog_powersaving_table.setColumnWidth(0, self.width() * 3 / 30)
            self.eventlog_powersaving_table.setColumnWidth(1, self.width() * 5 / 30)
            self.eventlog_powersaving_table.setColumnWidth(2, self.width() * 4 / 30)
            self.eventlog_powersaving_table.setColumnWidth(3, self.width() * 4 / 30)
            self.eventlog_powersaving_table.setColumnWidth(4, self.width() * 4 / 30)
            self.eventlog_powersaving_table.setColumnWidth(5, self.width() * 4 / 30)
            self.eventlog_powersaving_table.setColumnWidth(6, self.width() * 3 / 30)
        except:
            pass

    # item8_4_1 원격 - 원격 접속 기록
    def set_eventlog_access1(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT event_id, detailed, computer, remo_conn_user, remo_conn_addr, remo_conn_local, local_manager_sess_id, " \
                    "datetime(time_created, " + self.UTC + "), source FROM event_log WHERE event_id = '261' or event_id = '1149' or event_id = '24' or event_id = '25';"
            cur.execute(query)
            rows = cur.fetchall()
            conn.close()

            count = len(rows)
            self.eventlog_access1_table.setRowCount(count)
            self.eventlog_access1_table.setColumnCount(9)
            column_headers = ["이벤트 아이디", "상세설명", "컴퓨터 이름", "행위 발생 시간", "로그인 계정", "들어온 IP", "내 컴퓨터 이름", "세션 ID", "출처"]
            self.eventlog_access1_table.setHorizontalHeaderLabels(column_headers)

            for i in range(count):
                event_id, detailed, computer, remo_conn_user, remo_conn_addr, remo_conn_local, local_manager_sess_id, time_created, source = \
                rows[i]
                self.eventlog_access1_table.setItem(i, 0, QTableWidgetItem(str(event_id)))
                self.eventlog_access1_table.setItem(i, 1, QTableWidgetItem(detailed))
                self.eventlog_access1_table.setItem(i, 2, QTableWidgetItem(computer))
                self.eventlog_access1_table.setItem(i, 3, QTableWidgetItem(time_created))
                self.eventlog_access1_table.setItem(i, 4, QTableWidgetItem(remo_conn_user))
                self.eventlog_access1_table.setItem(i, 5, QTableWidgetItem(remo_conn_addr))
                self.eventlog_access1_table.setItem(i, 6, QTableWidgetItem(remo_conn_local))
                self.eventlog_access1_table.setItem(i, 7, QTableWidgetItem(local_manager_sess_id))
                self.eventlog_access1_table.setItem(i, 8, QTableWidgetItem(source))

            self.eventlog_access1_table.setColumnWidth(0, self.width() * 3 / 30)
            self.eventlog_access1_table.setColumnWidth(1, self.width() * 8 / 30)
            self.eventlog_access1_table.setColumnWidth(2, self.width() * 4 / 30)
            self.eventlog_access1_table.setColumnWidth(3, self.width() * 4 / 30)
            self.eventlog_access1_table.setColumnWidth(4, self.width() * 3 / 30)
            self.eventlog_access1_table.setColumnWidth(5, self.width() * 3 / 30)
            self.eventlog_access1_table.setColumnWidth(6, self.width() * 4 / 30)
            self.eventlog_access1_table.setColumnWidth(7, self.width() * 4 / 30)
            self.eventlog_access1_table.setColumnWidth(8, self.width() * 6 / 30)
        except:
            pass

    # item8_4_2 원격 - 원격 실행 기록
    def set_eventlog_access2(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT event_id, detailed, computer, rdp_name, rdp_value, rdp_custom_level, rdp_domain, rdp_session, sec_id, " \
                    "datetime(time_created, " + self.UTC + "), source FROM event_log where (event_id = '1024' AND rdp_value IS NOT  '') or (event_id = '1026' AND rdp_value IS NOT '') or event_id = '1025' or event_id = '1027' or event_id = '1028' or event_id = '1102';"
            cur.execute(query)
            rows = cur.fetchall()
            conn.close()

            count = len(rows)
            self.eventlog_access2_table.setRowCount(count)
            self.eventlog_access2_table.setColumnCount(11)
            column_headers = ["이벤트 아이디", "상세설명", "컴퓨터 이름", "행위 발생 시간", "서버 이름", "서버 주소", "커스텀 레벨", "도메인 이름", "세션 ID",
                              "계정 SID", "출처"]
            self.eventlog_access2_table.setHorizontalHeaderLabels(column_headers)

            for i in range(count):
                event_id, detailed, computer, rdp_name, rdp_value, rdp_custom_level, rdp_domain, rdp_session, sec_id, time_created,source = \
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
                self.eventlog_access2_table.setItem(i, 10, QTableWidgetItem(source))

            self.eventlog_access2_table.setColumnWidth(0, self.width() * 3 / 30)
            self.eventlog_access2_table.setColumnWidth(1, self.width() * 6 / 30)
            self.eventlog_access2_table.setColumnWidth(2, self.width() * 4 / 30)
            self.eventlog_access2_table.setColumnWidth(3, self.width() * 4 / 30)
            self.eventlog_access2_table.setColumnWidth(4, self.width() * 4 / 30)
            self.eventlog_access2_table.setColumnWidth(5, self.width() * 3 / 30)
            self.eventlog_access2_table.setColumnWidth(6, self.width() * 3 / 30)
            self.eventlog_access2_table.setColumnWidth(7, self.width() * 3 / 30)
            self.eventlog_access2_table.setColumnWidth(8, self.width() * 3 / 30)
            self.eventlog_access2_table.setColumnWidth(9, self.width() * 8 / 30)
            self.eventlog_access2_table.setColumnWidth(10, self.width() * 4 / 30)
        except:
            pass

    # item8_5 시스템 시간 변경  기록
    def set_eventlog_time(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT event_id, detailed, computer, reason, old_bias, new_bias, sbt_usr_name, datetime(sys_prv_time, " + self.UTC + "),  datetime(sys_new_time, " + self.UTC + "), " \
                    "datetime(time_created, " + self.UTC + "), source FROM event_log where (event_id = '1' AND reason IS NOT '') OR event_id = '22' OR event_id = '4616'"
            cur.execute(query)
            rows = cur.fetchall()
            conn.close()

            count = len(rows)
            self.eventlog_time_table.setRowCount(count)
            self.eventlog_time_table.setColumnCount(11)
            column_headers = ["이벤트 아이디", "상세설명", "컴퓨터 이름", "행위 발생 시간", "이유", "전 표준시간", "후 표준시간", "주체 이름", "전 시간", "후 시간", "출처"]
            self.eventlog_time_table.setHorizontalHeaderLabels(column_headers)

            for i in range(count):
                event_id, detailed, computer, reason, old_bias, new_bias, sbt_usr_name, sys_prv_time, sys_new_time, time_created, source = \
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
                self.eventlog_time_table.setItem(i, 10, QTableWidgetItem(source))

            self.eventlog_time_table.setColumnWidth(0, self.width() * 3 / 30)
            self.eventlog_time_table.setColumnWidth(1, self.width() * 4 / 30)
            self.eventlog_time_table.setColumnWidth(2, self.width() * 4 / 30)
            self.eventlog_time_table.setColumnWidth(3, self.width() * 4 / 30)
            self.eventlog_time_table.setColumnWidth(4, self.width() * 10 / 30)
            self.eventlog_time_table.setColumnWidth(5, self.width() * 3 / 30)
            self.eventlog_time_table.setColumnWidth(6, self.width() * 3 / 30)
            self.eventlog_time_table.setColumnWidth(7, self.width() * 3 / 30)
            self.eventlog_time_table.setColumnWidth(8, self.width() * 4 / 30)
            self.eventlog_time_table.setColumnWidth(9, self.width() * 4 / 30)
            self.eventlog_time_table.setColumnWidth(10, self.width() * 4 / 30)
        except:
            pass

    # item9_1 전체 파일 및 폴더
    def set_file_and_folder(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "select src, drive, file_path, is_dir, is_in_use, file_size, SI_flag, FN_flag, " \
                    "datetime(SI_M_timestamp, " + self.UTC + "), datetime(SI_A_timestamp, " + self.UTC + "), " \
                    "datetime(SI_C_timestamp, " + self.UTC + "), datetime(SI_E_timestamp, " + self.UTC + "), " \
                    "datetime(FN_M_timestamp, " + self.UTC + "), datetime(FN_A_timestamp, " + self.UTC + "), " \
                    "datetime(FN_C_timestamp, " + self.UTC + "), datetime(FN_E_timestamp, " + self.UTC + "), " \
                    "mft_ref_num, LSN, ADS_list FROM parsed_MFT"
            cur.execute(query)
            rows = cur.fetchall()
            conn.close()

            count = len(rows)
            self.file_and_folder_table.setRowCount(count)
            self.file_and_folder_table.setColumnCount(19)
            column_headers = ["출처", "볼륨", "파일경로", "폴더여부", "할당여부", "파일크기", "$SI Flag", "$FN Flag",
                              "$SI 생성 시각", "$SI 접근 시간", "$SI 수정 시간", "$SI mft변경 시간",
                              "$FN 생성 시각", "$FN 접근 시간", "$FN 수정 시간", "$FN mft변경 시간",
                              "MFT 참조", "LSN", "ADS 목록"]
            self.file_and_folder_table.setHorizontalHeaderLabels(column_headers)

            for i in range(count):
                src, drive, file_path, is_dir, is_in_use, file_size, SI_flag, FN_flag, \
                SI_C_timestamp, SI_A_timestamp, SI_M_timestamp, SI_E_timestamp, \
                FN_C_timestamp, FN_A_timestamp, FN_M_timestamp, FN_E_timestamp, \
                mft_ref_num, LSN, ADS_list = rows[i]

                self.file_and_folder_table.setItem(i, 0, QTableWidgetItem(src))
                self.file_and_folder_table.setItem(i, 1, QTableWidgetItem(drive))
                self.file_and_folder_table.setItem(i, 2, QTableWidgetItem(file_path))
                self.file_and_folder_table.setItem(i, 3, QTableWidgetItem(is_dir))
                self.file_and_folder_table.setItem(i, 4, QTableWidgetItem(is_in_use))
                self.file_and_folder_table.setItem(i, 5, QTableWidgetItem(file_size))
                self.file_and_folder_table.setItem(i, 6, QTableWidgetItem(SI_flag))
                self.file_and_folder_table.setItem(i, 7, QTableWidgetItem(FN_flag))
                self.file_and_folder_table.setItem(i, 8, QTableWidgetItem(SI_C_timestamp))
                self.file_and_folder_table.setItem(i, 9, QTableWidgetItem(SI_A_timestamp))
                self.file_and_folder_table.setItem(i, 10, QTableWidgetItem(SI_M_timestamp))
                self.file_and_folder_table.setItem(i, 11, QTableWidgetItem(SI_E_timestamp))
                self.file_and_folder_table.setItem(i, 12, QTableWidgetItem(FN_C_timestamp))
                self.file_and_folder_table.setItem(i, 13, QTableWidgetItem(FN_A_timestamp))
                self.file_and_folder_table.setItem(i, 14, QTableWidgetItem(FN_M_timestamp))
                self.file_and_folder_table.setItem(i, 15, QTableWidgetItem(FN_E_timestamp))
                self.file_and_folder_table.setItem(i, 16, QTableWidgetItem(str(mft_ref_num)))
                self.file_and_folder_table.setItem(i, 17, QTableWidgetItem(str(LSN)))
                self.file_and_folder_table.setItem(i, 18, QTableWidgetItem(ADS_list))

            self.file_and_folder_table.setColumnWidth(0, self.width() * 3 / 30)
            self.file_and_folder_table.setColumnWidth(1, self.width() * 3 / 30)
            self.file_and_folder_table.setColumnWidth(2, self.width() * 10 / 30)
            self.file_and_folder_table.setColumnWidth(3, self.width() * 3 / 30)
            self.file_and_folder_table.setColumnWidth(4, self.width() * 3 / 30)
            self.file_and_folder_table.setColumnWidth(5, self.width() * 3 / 30)
            self.file_and_folder_table.setColumnWidth(6, self.width() * 6 / 30)
            self.file_and_folder_table.setColumnWidth(7, self.width() * 8 / 30)
            self.file_and_folder_table.setColumnWidth(8, self.width() * 5 / 30)
            self.file_and_folder_table.setColumnWidth(9, self.width() * 5 / 30)
            self.file_and_folder_table.setColumnWidth(10, self.width() * 5 / 30)
            self.file_and_folder_table.setColumnWidth(11, self.width() * 5 / 30)
            self.file_and_folder_table.setColumnWidth(12, self.width() * 5 / 30)
            self.file_and_folder_table.setColumnWidth(13, self.width() * 5 / 30)
            self.file_and_folder_table.setColumnWidth(14, self.width() * 5 / 30)
            self.file_and_folder_table.setColumnWidth(15, self.width() * 5 / 30)
            self.file_and_folder_table.setColumnWidth(16, self.width() * 6 / 30)
            self.file_and_folder_table.setColumnWidth(17, self.width() * 3 / 30)
            self.file_and_folder_table.setColumnWidth(18, self.width() * 3 / 30)

        except:
            pass

    # item9_2 삭제된 파일 및 폴더
    def set_del_file_and_folder(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "select drive, file_path, is_dir, is_in_use, file_size, SI_flag, FN_flag, " \
                    "datetime(SI_M_timestamp, " + self.UTC + "), datetime(SI_A_timestamp, " + self.UTC + "), " \
                    "datetime(SI_C_timestamp, " + self.UTC + "), datetime(SI_E_timestamp, " + self.UTC + "), " \
                    "datetime(FN_M_timestamp, " + self.UTC + "), datetime(FN_A_timestamp, " + self.UTC + "), " \
                    "datetime(FN_C_timestamp, " + self.UTC + "), datetime(FN_E_timestamp, " + self.UTC + "), " \
                    "mft_ref_num, LSN, ADS_list FROM parsed_MFT WHERE is_in_use LIKE 'N' and src LIKE 'File record'"
            cur.execute(query)
            rows = cur.fetchall()
            conn.close()

            count = len(rows)
            self.del_file_and_folder_table.setRowCount(count)
            self.del_file_and_folder_table.setColumnCount(18)
            column_headers = ["볼륨", "파일경로", "폴더여부", "할당여부", "파일크기", "$SI Flag", "$FN Flag",
                              "$SI 생성 시각", "$SI 접근 시간", "$SI 수정 시간", "$SI mft변경 시간",
                              "$FN 생성 시각", "$FN 접근 시간", "$FN 수정 시간", "$FN mft변경 시간",
                              "MFT 참조", "LSN", "ADS 목록"]
            self.del_file_and_folder_table.setHorizontalHeaderLabels(column_headers)

            for i in range(count):
                drive, file_path, is_dir, is_in_use, file_size, SI_flag, FN_flag, \
                SI_C_timestamp, SI_A_timestamp, SI_M_timestamp, SI_E_timestamp, \
                FN_C_timestamp, FN_A_timestamp, FN_M_timestamp, FN_E_timestamp, \
                mft_ref_num, LSN, ADS_list = rows[i]
                self.del_file_and_folder_table.setItem(i, 0, QTableWidgetItem(drive))
                self.del_file_and_folder_table.setItem(i, 1, QTableWidgetItem(file_path))
                self.del_file_and_folder_table.setItem(i, 2, QTableWidgetItem(is_dir))
                self.del_file_and_folder_table.setItem(i, 3, QTableWidgetItem(is_in_use))
                self.del_file_and_folder_table.setItem(i, 4, QTableWidgetItem(file_size))
                self.del_file_and_folder_table.setItem(i, 5, QTableWidgetItem(SI_flag))
                self.del_file_and_folder_table.setItem(i, 6, QTableWidgetItem(FN_flag))
                self.del_file_and_folder_table.setItem(i, 7, QTableWidgetItem(SI_C_timestamp))
                self.del_file_and_folder_table.setItem(i, 8, QTableWidgetItem(SI_A_timestamp))
                self.del_file_and_folder_table.setItem(i, 9, QTableWidgetItem(SI_M_timestamp))
                self.del_file_and_folder_table.setItem(i, 10, QTableWidgetItem(SI_E_timestamp))
                self.del_file_and_folder_table.setItem(i, 11, QTableWidgetItem(FN_C_timestamp))
                self.del_file_and_folder_table.setItem(i, 12, QTableWidgetItem(FN_A_timestamp))
                self.del_file_and_folder_table.setItem(i, 13, QTableWidgetItem(FN_M_timestamp))
                self.del_file_and_folder_table.setItem(i, 14, QTableWidgetItem(FN_E_timestamp))
                self.del_file_and_folder_table.setItem(i, 15, QTableWidgetItem(str(mft_ref_num)))
                self.del_file_and_folder_table.setItem(i, 16, QTableWidgetItem(str(LSN)))
                self.del_file_and_folder_table.setItem(i, 17, QTableWidgetItem(ADS_list))

            self.del_file_and_folder_table.setColumnWidth(0, self.width() * 4 / 30)
            self.del_file_and_folder_table.setColumnWidth(1, self.width() * 10 / 30)
            self.del_file_and_folder_table.setColumnWidth(2, self.width() * 3 / 30)
            self.del_file_and_folder_table.setColumnWidth(3, self.width() * 3 / 30)
            self.del_file_and_folder_table.setColumnWidth(4, self.width() * 4 / 30)
            self.del_file_and_folder_table.setColumnWidth(5, self.width() * 4 / 30)
            self.del_file_and_folder_table.setColumnWidth(6, self.width() * 4 / 30)
            self.del_file_and_folder_table.setColumnWidth(7, self.width() * 5 / 30)
            self.del_file_and_folder_table.setColumnWidth(8, self.width() * 5 / 30)
            self.del_file_and_folder_table.setColumnWidth(9, self.width() * 5 / 30)
            self.del_file_and_folder_table.setColumnWidth(10, self.width() * 5 / 30)
            self.del_file_and_folder_table.setColumnWidth(11, self.width() * 5 / 30)
            self.del_file_and_folder_table.setColumnWidth(12, self.width() * 5 / 30)
            self.del_file_and_folder_table.setColumnWidth(13, self.width() * 5 / 30)
            self.del_file_and_folder_table.setColumnWidth(14, self.width() * 5 / 30)
            self.del_file_and_folder_table.setColumnWidth(15, self.width() * 7 / 30)
            self.del_file_and_folder_table.setColumnWidth(16, self.width() * 4 / 30)
            self.del_file_and_folder_table.setColumnWidth(17, self.width() * 4 / 30)

        except:
            pass

    # item9_3 파일 변경 사항
    def set_modified_file(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT USN, src, reason, file_name, file_path, MFT_refer_num, parent_MFT_refer_num, " \
                    "datetime(time_stamp, " + self.UTC + ") FROM parsed_usn"
            cur.execute(query)
            rows = cur.fetchall()
            conn.close()

            count = len(rows)
            self.modified_file_table.setRowCount(count)
            self.modified_file_table.setColumnCount(8)
            column_headers = ["USN", "주체", "변경 이벤트", "파일이름", "파일경로", "MFT 참조주소", "부모 MFT 참조주소", "변경시각"]
            self.modified_file_table.setHorizontalHeaderLabels(column_headers)

            for i in range(count):
                USN, src, reason, file_name, file_path, MFT_refer_num, parent_MFT_refer_num, time_stamp = rows[i]
                self.modified_file_table.setItem(i, 0, QTableWidgetItem(str(USN)))
                self.modified_file_table.setItem(i, 1, QTableWidgetItem(src))
                self.modified_file_table.setItem(i, 2, QTableWidgetItem(reason))
                self.modified_file_table.setItem(i, 3, QTableWidgetItem(file_name))
                self.modified_file_table.setItem(i, 4, QTableWidgetItem(file_path))
                self.modified_file_table.setItem(i, 5, QTableWidgetItem(str(MFT_refer_num)))
                self.modified_file_table.setItem(i, 6, QTableWidgetItem(str(parent_MFT_refer_num)))
                self.modified_file_table.setItem(i, 7, QTableWidgetItem(time_stamp))

            self.modified_file_table.setColumnWidth(0, self.width() * 4 / 30)
            self.modified_file_table.setColumnWidth(1, self.width() * 4 / 30)
            self.modified_file_table.setColumnWidth(2, self.width() * 10 / 30)
            self.modified_file_table.setColumnWidth(3, self.width() * 8 / 30)
            self.modified_file_table.setColumnWidth(4, self.width() * 8 / 30)
            self.modified_file_table.setColumnWidth(5, self.width() * 5 / 30)
            self.modified_file_table.setColumnWidth(6, self.width() * 5 / 30)
            self.modified_file_table.setColumnWidth(7, self.width() * 5 / 30)

        except:
            pass

    # item9_4 폴더 열람 흔적
    def set_recent_folder(self):
        try:
            conn = sqlite3.connect("Believe_Me_Sister.db")
            cur = conn.cursor()
            query = "SELECT file_name, lnk_file_full_path, file_flags, file_size, local_base_path, show_command, " \
                    "drive_serial_number, drive_type, volume_label, icon_location, machine_info, droid_file, droid_vol, known_guid, " \
                    "datetime(target_creation_time, " + self.UTC + "), datetime(target_modified_time, " + self.UTC + "), datetime(target_accessed_time, " + self.UTC + ")" \
                    " FROM lnk_files WHERE file_flags LIKE '%DIRECTORY%'"
            cur.execute(query)
            rows = cur.fetchall()
            conn.close()

            count = len(rows)
            self.recent_folder_table.setRowCount(count)
            self.recent_folder_table.setColumnCount(17)
            column_headers = ["파일", "링크 파일 경로", "플래그", "크기", "원본 파일 경로", "Show_Command", \
                              "원본 생성 시간", "원본 수정 시간", "원본 접근 시간",
                              "드라이브 시리얼 번호",
                              "드라이브 타입", "볼륨 라벨", "아이콘 경로", "NetBIOS 이름", "Droid_File", "Droid_Vol",
                              "Known_GUID"]
            self.recent_folder_table.setHorizontalHeaderLabels(column_headers)

            for i in range(count):
                file_name, lnk_file_full_path, file_flags, file_size, local_base_path, show_command, \
                drive_serial_number, drive_type, volume_label, icon_location, machine_info, droid_file, droid_vol, known_guid, \
                target_creation_time, target_modified_time, target_accessed_time = rows[i]
                self.recent_folder_table.setItem(i, 0, QTableWidgetItem(file_name))
                self.recent_folder_table.setItem(i, 1, QTableWidgetItem(lnk_file_full_path))
                self.recent_folder_table.setItem(i, 2, QTableWidgetItem(file_flags))
                self.recent_folder_table.setItem(i, 3, QTableWidgetItem(file_size))
                self.recent_folder_table.setItem(i, 4, QTableWidgetItem(local_base_path))
                self.recent_folder_table.setItem(i, 5, QTableWidgetItem(show_command))
                self.recent_folder_table.setItem(i, 6, QTableWidgetItem(target_creation_time))
                self.recent_folder_table.setItem(i, 7, QTableWidgetItem(target_modified_time))
                self.recent_folder_table.setItem(i, 8, QTableWidgetItem(target_accessed_time))
                self.recent_folder_table.setItem(i, 9, QTableWidgetItem(drive_serial_number))
                self.recent_folder_table.setItem(i, 10, QTableWidgetItem(drive_type))
                self.recent_folder_table.setItem(i, 11, QTableWidgetItem(volume_label))
                self.recent_folder_table.setItem(i, 12, QTableWidgetItem(icon_location))
                self.recent_folder_table.setItem(i, 13, QTableWidgetItem(machine_info))
                self.recent_folder_table.setItem(i, 14, QTableWidgetItem(droid_file))
                self.recent_folder_table.setItem(i, 15, QTableWidgetItem(droid_vol))
                self.recent_folder_table.setItem(i, 16, QTableWidgetItem(known_guid))

            self.recent_folder_table.setColumnWidth(0, self.width() * 5 / 30)
            self.recent_folder_table.setColumnWidth(1, self.width() * 7 / 30)
            self.recent_folder_table.setColumnWidth(2, self.width() * 3 / 30)
            self.recent_folder_table.setColumnWidth(3, self.width() * 2 / 30)
            self.recent_folder_table.setColumnWidth(4, self.width() * 7 / 30)
            self.recent_folder_table.setColumnWidth(5, self.width() * 4 / 30)
            self.recent_folder_table.setColumnWidth(6, self.width() * 4 / 30)
            self.recent_folder_table.setColumnWidth(7, self.width() * 4 / 30)
            self.recent_folder_table.setColumnWidth(8, self.width() * 4 / 30)
            self.recent_folder_table.setColumnWidth(9, self.width() * 4 / 30)
            self.recent_folder_table.setColumnWidth(10, self.width() * 4 / 30)
            self.recent_folder_table.setColumnWidth(11, self.width() * 4 / 30)
            self.recent_folder_table.setColumnWidth(12, self.width() * 4 / 30)
            self.recent_folder_table.setColumnWidth(13, self.width() * 4 / 30)
            self.recent_folder_table.setColumnWidth(14, self.width() * 4 / 30)
            self.recent_folder_table.setColumnWidth(15, self.width() * 4 / 30)
            self.recent_folder_table.setColumnWidth(16, self.width() * 4 / 30)
        except:
            pass