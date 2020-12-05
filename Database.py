import sqlite3


def Event_Log_Database(data_list):
    conn = sqlite3.connect('Believe_Me_Sister.db')
    cur = conn.cursor()
    conn.execute('DROP TABLE IF EXISTS event_log')
    conn.execute('CREATE TABLE event_log('
                 'event_id INTEGER,            detailed TEXT,              time_created DATETIME,  source TEXT,'
                 'computer TEXT,               new_bias TEXT,              old_bias TEXT, '
                 'sleep_time DATETIME,         wake_time DATETIME,         svc_name TEXT, '
                 'img_path TEXT,               svc_type TEXT,              start_type TEXT, '
                 'acc_name TEXT,               net_name TEXT,              guid TEXT, '
                 'conn_mode TEXT,              reason TEXT,                sys_bit_volume TEXT, '
                 'trg_usr_name TEXT,           sbt_usr_name TEXT,          display_name TEXT, '
                 'mem_sid TEXT,                ip_addr TEXT,               exe_path TEXT, '
                 'rdp_name TEXT,               rdp_value TEXT,             rdp_custom_level TEXT, '
                 'sec_id TEXT,                 rdp_domain TEXT,            rdp_session TEXT, '
                 'local_manager_sess_id TEXT,  bus_type TEXT,'
                 'local_manager_reason TEXT,   local_manager_sess TEXT,    remo_conn_user TEXT,       capacity TEXT,'
                 'remo_conn_addr TEXT,         remo_conn_local TEXT,       drive_location TEXT, '
                 'dev_num TEXT,                drive_manufac TEXT,         drive_serial TEXT, '
                 'drive_model TEXT,            package TEXT,               sys_prv_time DATETIME,'
                 'sys_new_time DATETIME,       sys_dev_id TEXT,            sys_framework_ver TEXT,'
                 'sys_svc_name TEXT,           sys_drv_file_name TEXT,     sys_dvc_inst_id TEXT,'
                 'sys_old_time TEXT,           app_name TEXT,              app_path TEXT,'
                 'app_version TEXT,            channel TEXT)')

    cur.executemany('INSERT INTO event_log VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?,'
                    '?, ?, ?, ?, ?, ?, ?, ?, ?, ?,'
                    '?, ?, ?, ?, ?, ?, ?, ?, ?, ?,'
                    '?, ?, ?, ?, ?, ?, ?, ?, ?, ?,'
                    '?, ?, ?, ?, ?, ?, ?, ?, ?, ?,'
                    '?, ?, ?, ?, ?, ?, ?)',
                    data_list)
    conn.commit()
    conn.close()


def Prefetch_Database(data_list1, data_list2):
    conn = sqlite3.connect('Believe_Me_Sister.db')
    cur1 = conn.cursor()
    cur2 = conn.cursor()

    conn.execute('DROP TABLE IF EXISTS prefetch1')
    conn.execute('CREATE TABLE prefetch1(Executable_Name TEXT, Full_Path TEXT, '
                 'Run_Count INTEGER, Last_Executed1 DATETIME, Last_Executed2 DATETIME, Last_Executed3 DATETIME,'
                 ' Last_Executed4 DATETIME, Last_Executed5 DATETIME, Last_Executed6 DATETIME, Last_Executed7 DATETIME,'
                 'Last_Executed8 DATETIME)')
    conn.execute('DROP TABLE IF EXISTS prefetch2')
    conn.execute('CREATE TABLE prefetch2(FILENAME TEXT, PATH TEXT)')

    cur1.executemany('INSERT INTO prefetch1 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', data_list1)
    cur2.executemany('INSERT INTO prefetch2 VALUES(?, ?)', data_list2)

    conn.commit()


def browser_db_insert(data_list1, data_list2, data_list3, data_list4, data_list5, data_list6, data_list7, data_list8, data_list9):
    dest = sqlite3.connect("Believe_Me_Sister.db")
    d_cur = dest.cursor()
    d_cur.execute('DROP TABLE IF EXISTS url')
    d_cur.execute(
        'CREATE TABLE url(type TEXT, timestamp DATETIME, url TEXT, title TEXT, '
        'source TEXT, visit_duration TEXT, visit_count INTEGER, '
        'typed_count INTEGER, url_hidden INTEGER, transition TEXT)')
    d_cur.execute('DROP TABLE IF EXISTS download')
    d_cur.execute(
        'CREATE TABLE download(type TEXT, filename TEXT, timestamp DATETIME, URL TEXT, '
        'Status TEXT, Path TEXT, Interrupt_Reason TEXT, '
        'Danger_Type TEXT, Opened TEXT, ETag TEXT, Last_Modified DATETIME)')
    d_cur.execute('DROP TABLE IF EXISTS autofill')
    d_cur.execute(
        'CREATE TABLE autofill(type TEXT, timestamp DATETIME, '
        'Status TEXT, Value TEXT)')
    d_cur.execute('DROP TABLE IF EXISTS bookmark')
    d_cur.execute(
        'CREATE TABLE bookmark(type TEXT, timestamp DATETIME, '
        'URL TEXT, Title TEXT, Value TEXT)')
    d_cur.execute('DROP TABLE IF EXISTS cookies')
    d_cur.execute(
        'CREATE TABLE cookies(type TEXT, timestamp DATETIME, URL TEXT, '
        'Title TEXT, Value TEXT)')
    d_cur.execute('DROP TABLE IF EXISTS login')
    d_cur.execute(
        'CREATE TABLE login(type TEXT, timestamp DATETIME, URL TEXT, Name TEXT, '
        'Data TEXT, Password_element, Password_value)')
    d_cur.execute('DROP TABLE IF EXISTS preference')
    d_cur.execute(
        'CREATE TABLE preference(type TEXT, timestamp DATETIME, URL TEXT, '
        'Status TEXT, Data TEXT)')
    d_cur.execute('DROP TABLE IF EXISTS keyword')
    d_cur.execute(
        'CREATE TABLE keyword(type TEXT, timestamp DATETIME, keyword TEXT)')
    d_cur.execute('DROP TABLE IF EXISTS cache')
    d_cur.execute(
        'CREATE TABLE cache(type TEXT, timestamp DATETIME, URL TEXT, '
        'Status TEXT, Value TEXT, '
        'ETag TEXT, Last_Modified DATETIME, Server_Name TEXT, Data_Location TEXT, All_HTTP_Headers TEXT)')
    d_cur.execute('DROP TABLE IF EXISTS cloud')
    d_cur.execute(
        'CREATE TABLE cloud(timestamp DATETIME, URL TEXT, Title TEXT)')

    sql1 = "INSERT INTO url(type, timestamp, url, title, source, visit_duration, visit_count, typed_count, url_hidden, transition) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    sql2 = "INSERT INTO autofill (type, timestamp, Status, Value) VALUES (?, ?, ?, ?)"
    sql3 = "INSERT INTO bookmark (type, timestamp, url, title, value) VALUES (?, ?, ?, ?, ?)"
    sql4 = "INSERT INTO cookies (type, timestamp, url, title, value) VALUES (?, ?, ?, ?, ?)"
    sql5 = "INSERT INTO login (type, timestamp, URL, Name, Data, Password_element, Password_value) VALUES (?, ?, ?, ?, ?, ?, ?)"
    sql6 = "INSERT INTO preference (type, timestamp, url, status, data) VALUES (?, ?, ?, ?, ?)"
    sql7 = "INSERT INTO keyword (type, timestamp, keyword) VALUES (?, ?, ?)"
    sql8 = "INSERT INTO download (type, filename, timestamp, url, Status, Path, Interrupt_Reason, Danger_Type, Opened, Etag, Last_Modified) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    sql9 = "INSERT INTO cloud(timestamp, url, title) VALUES(?, ?, ?)"

    d_cur.executemany(sql1, data_list1)
    d_cur.executemany(sql2, data_list2)
    d_cur.executemany(sql3, data_list3)
    d_cur.executemany(sql4, data_list4)
    d_cur.executemany(sql5, data_list5)
    d_cur.executemany(sql6, data_list6)
    d_cur.executemany(sql7, data_list7)
    d_cur.executemany(sql8, data_list8)
    d_cur.executemany(sql9, data_list9)

    dest.commit()
    dest.close()


def cache_db_insert(data_list):
    dest = sqlite3.connect("Believe_Me_Sister.db")
    d_cur = dest.cursor()

    sql="INSERT INTO cache (type, timestamp, url, status, value, etag, last_modified, server_name, data_location, all_http_headers) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

    d_cur.executemany(sql, data_list)

    dest.commit()
    dest.close()


def Lnk_Databases(data_list):
    conn = sqlite3.connect("Believe_Me_Sister.db")
    cur = conn.cursor()
    conn.execute('DROP TABLE IF EXISTS lnk_files')
    conn.execute(
        "CREATE TABLE lnk_files("
        "lnk_file_full_path TEXT,       file_name TEXT,                file_flags TEXT, "
        "file_size TEXT,                show_command TEXT,             target_creation_time DATETIME, "
        "target_modified_time DATETIME, target_accessed_time DATETIME, local_base_path TEXT,"
        "drive_serial_number TEXT,      drive_type TEXT,               volume_label TEXT, "
        "icon_location TEXT,            machine_info TEXT,             droid_vol TEXT, "
        "droid_file TEXT,               icon_path TEXT,                known_guid TEXT)")
    cur.executemany("INSERT INTO lnk_files VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data_list)

    conn.commit()
    conn.close()


def JumpList_Databases(data_list):

    conn = sqlite3.connect("Believe_Me_Sister.db")
    cur = conn.cursor()
    conn.execute('DROP TABLE IF EXISTS jumplist')
    conn.execute(
        "CREATE TABLE jumplist(Type TEXT, jump_file_name TEXT, file_name TEXT, lnk_counter TEXT, Used_path TEXT, file_size TEXT, "
        "file_flags TEXT, target_creation_time DATETIME, target_modified_time DATETIME, target_accessed_time DATETIME, "
        "show_command TEXT, icon TEXT, description TEXT, local_base_path TEXT, volume_label TEXT, "
        "drive_type TEXT)")
    cur.executemany("INSERT INTO jumplist VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data_list)

    conn.commit()
    conn.close()


def MFT_Databases(data_list):
    conn = sqlite3.connect('Believe_Me_Sister.db')
    cur = conn.cursor()
    conn.execute('DROP TABLE IF EXISTS parsed_MFT')
    cur.execute(
        "CREATE TABLE parsed_MFT(drive, src, mft_ref_num, is_in_use, is_dir, LSN, file_path, SI_flag, FN_flag, SI_M_timestamp, SI_A_timestamp, SI_C_timestamp, SI_E_timestamp, SI_USN, FN_M_timestamp, FN_A_timestamp, FN_C_timestamp, FN_E_timestamp, OBJID_timestamp, File_size, ADS_list, WSL_M_timestamp, WSL_A_timestamp, WSL_CH_timestamp);")
    cur.executemany('INSERT INTO parsed_MFT VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', data_list)
    conn.commit()
    conn.close()


def Usn_Databases(data_list):
    conn = sqlite3.connect('Believe_Me_Sister.db')
    cur = conn.cursor()
    conn.execute('DROP TABLE IF EXISTS parsed_usn')
    cur.execute(
        "CREATE TABLE parsed_usn(USN, src, reason, MFT_refer_num, parent_MFT_refer_num, time_stamp, file_name, file_path);")
    cur.executemany('INSERT INTO parsed_usn VALUES (?, ?, ?, ?, ?, ?, ?, ?);', data_list)
    conn.commit()
    conn.close()

##############################
# REGParse.py가 호출하는 함수들 #
##############################
def Reg_OSInformation(data_list):
    if data_list is not None:
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        try:
            conn.execute('DROP TABLE IF EXISTS OSInformation')
            query = "CREATE TABLE OSInformation" \
                "(product_name TEXT, product_ID TEXT, system_root TEXT, owner TEXT, install_date TEXT, organization TEXT, build_lab, " \
                "timezone_name TEXT, active_time_bias TEXT, UTC INTEGER, " \
                "computer_name TEXT, default_user_name TEXT, last_used_user_name TEXT, shutdown_time TEXT)"
            conn.execute(query)
            cur.execute("INSERT INTO OSInformation VALUES(?, ?, ?, ?, "
                    "?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data_list)
            conn.commit()
        except:
            print("Error while making OSInformation table")
        conn.close()


def Reg_Uninstall(data_list):
    if data_list is not None:
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        try:
            conn.execute('DROP TABLE IF EXISTS Uninstall')
            query = "CREATE TABLE Uninstall(id TEXT, name TEXT, version TEXT, install_location TEXT, publisher TEXT, install_date TEXT, type TEXT)"
            conn.execute(query)
            cur.executemany("INSERT INTO Uninstall VALUES(?, ?, ?, ?, ?, ?, ?)", data_list)
            conn.commit()
        except:
            print("Error while making Uninstall table")
        conn.close()


def Reg_BAM(data_list):
    if data_list is not None:
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        try:
            conn.execute('DROP TABLE IF EXISTS BAM')
            query = "CREATE TABLE BAM(SID TEXT, program_path TEXT, last_executed TEXT)"
            conn.execute(query)
            cur.executemany("INSERT INTO BAM VALUES(?, ?, ?)", data_list)
            conn.commit()
        except:
            print("Error while making BAM table")
        conn.close()


def Reg_UserAccounts(data_list):
    if data_list is not None:
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        try:
            conn.execute('DROP TABLE IF EXISTS UserAccounts')
            query = "CREATE TABLE UserAccounts(RID TEXT, RID_int INTEGER, last_login_time TEXT, last_password_change_time TEXT," \
                "expires_on TEXT, last_incorrect_password_time TEXT, logon_failure_count INTEGER, logon_success_count INTEGER," \
                "account_name TEXT, complete_account_name TEXT, comment TEXT, homedir TEXT, created_on TEXT)"
            conn.execute(query)
            cur.executemany("INSERT INTO UserAccounts VALUES(?, ?, ?, "
                         "?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data_list)
            conn.commit()
        except:
            print("Error while making UserAccounts table")
        conn.close()


def Reg_MuiCache(data_list):
    if data_list is not None:
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        try:
            conn.execute('DROP TABLE IF EXISTS MuiCache')
            query = "CREATE TABLE MuiCache(name TEXT, path TEXT)"
            conn.execute(query)
            cur.executemany("INSERT INTO MuiCache VALUES(?, ?)", data_list)
            conn.commit()
        except:
            print("Error while making MuiCache table")
        conn.close()


def Reg_UseraAsist_CEB(data_list):
    if data_list is not None:
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        try:
            conn.execute('DROP TABLE IF EXISTS UserAssist_CEB')
            query = "CREATE TABLE UserAssist_CEB(name TEXT, run_count INTEGER, last_executed TEXT)"
            conn.execute(query)
            cur.executemany("INSERT INTO UserAssist_CEB VALUES(?, ?, ?)", data_list)
            conn.commit()
        except:
            print("Error while making UserAssist_CEB table")
        conn.close()


def Reg_UserAssist_F4E(data_list):
    if data_list is not None:
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        try:
            conn.execute('DROP TABLE IF EXISTS UserAssist_F4E')
            query = "CREATE TABLE UserAssist_F4E(name TEXT, run_count INTEGER, last_executed TEXT)"
            conn.execute(query)
            cur.executemany("INSERT INTO UserAssist_F4E VALUES(?, ?, ?)", data_list)
            conn.commit()
        except:
            print("Error while making UserAssist_F4E table")
        conn.close()


def Reg_UserAssist_CIDSizeMRU(data_list):
    if data_list is not None:
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        try:
            conn.execute('DROP TABLE IF EXISTS CIDSizeMRU')
            query = "CREATE TABLE CIDSizeMRU(program_name TEXT, mru INTEGER, opened_on TEXT)"
            conn.execute(query)
            cur.executemany("INSERT INTO CIDSizeMRU VALUES(?, ?, ?)", data_list)
            conn.commit()
        except:
            print("Error while making CIDSizeMRU table")
        conn.close()


def Reg_FirstFolder(data_list):
    if data_list is not None:
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        try:
            conn.execute('DROP TABLE IF EXISTS FirstFolder')
            query = "CREATE TABLE FirstFolder(program_name TEXT, folder TEXT, mru INTEGER, opened_on TEXT)"
            conn.execute(query)
            cur.executemany("INSERT INTO FirstFolder VALUES(?, ?, ?, ?)", data_list)
            conn.commit()
        except:
            print("Error while making FirstFolder table")
        conn.close()


def Reg_Connected_USB(data_list):
    if data_list is not None:
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        try:
            conn.execute('DROP TABLE IF EXISTS Connected_USB')
            query = "CREATE TABLE Connected_USB(DCID TEXT, UIID TEXT, GUID TEXT, label TEXT, " \
                    "first_connected TEXT, last_connected TEXT, vendor_name TEXT, product_name TEXT, version TEXT, serial_num TEXT, random_yn INTEGER)"
            conn.execute(query)
            cur.executemany("INSERT INTO Connected_USB VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data_list)
            conn.commit()
        except:
            print("Error while making Connected_USB table")
        conn.close()


def Reg_RecentDocs(data_list):
    if data_list is not None:
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        try:
            conn.execute('DROP TABLE IF EXISTS RecentDocs')
            query = "CREATE TABLE RecentDocs(extension TEXT, mru INTEGER, program TEXT, lnk TEXT, opened_on TEXT)"
            conn.execute(query)
            cur.executemany("INSERT INTO RecentDocs VALUES(?, ?, ?, ?, ?)", data_list)
            conn.commit()
        except:
            print("Error while making RecentDocs table")
        conn.close()


def Reg_LastVisitedPidl(data_list):
    if data_list is not None:
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        try:
            conn.execute('DROP TABLE IF EXISTS LastVisitedPidl')
            query = "CREATE TABLE LastVisitedPidl(program TEXT, mru INTEGER, opened_on TEXT)"
            conn.execute(query)
            cur.executemany("INSERT INTO LastVisitedPidl VALUES(?, ?, ?)", data_list)
            conn.commit()
        except:
            print("Error while making LastVisitedPidl table")
        conn.close()


def Reg_Legacy(data_list):
    if data_list is not None:
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        try:
            conn.execute('DROP TABLE IF EXISTS Legacy')
            query = "CREATE TABLE Legacy(program TEXT, mru INTEGER, opened_on TEXT)"
            conn.execute(query)
            cur.executemany("INSERT INTO Legacy VALUES(?, ?, ?)", data_list)
            conn.commit()
        except:
            print("Error while making Legacy table")
        conn.close()


def Reg_OpenSavePidl(data_list):
    if data_list is not None:
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        try:
            conn.execute('DROP TABLE IF EXISTS OpenSavePidl')
            query = "CREATE TABLE OpenSavePidl(extension TEXT, program TEXT, mru INTEGER, opened_on TEXT)"
            conn.execute(query)
            cur.executemany("INSERT INTO OpenSavePidl VALUES(?, ?, ?, ?)", data_list)
            conn.commit()
        except:
            print("Error while making OpenSavePidl table")
        conn.close()


def Reg_Run(data_list):
    if data_list is not None:
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        try:
            conn.execute('DROP TABLE IF EXISTS Run')
            query = "CREATE TABLE Run(program TEXT, path TEXT, type TEXT)"
            conn.execute(query)
            cur.executemany("INSERT INTO Run VALUES(?, ?, ?)", data_list)
            conn.commit()
        except:
            print("Error while making Run table")
        conn.close()


def Reg_Network(data_list):
    if data_list is not None:
        conn = sqlite3.connect("Believe_Me_Sister.db")
        cur = conn.cursor()
        try:
            conn.execute('DROP TABLE IF EXISTS Network')
            query = "CREATE TABLE Network(ip TEXT)"
            conn.execute(query)
            cur.executemany("INSERT INTO Network VALUES(?)", data_list)
            conn.commit()
        except:
            print("Error while making Network table")
        conn.close()