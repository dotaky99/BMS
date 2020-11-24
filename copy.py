# https://github.com/jschicht/RawCopy
# https://github.com/jschicht/ExtractUsnJrnl
# http://forensic-proof.com/archives/3757

import os
import string
from ctypes  import windll
import getpass


def get_drives():
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask>>=1
    return drives

def file_copy():
    # path
    cur_path = os.getcwd()
    prefetch_path = "C:/Windows/Prefetch"
    eventlog_path = "C:\windows\sysnative\winevt\logs" #https://nroses-taek.tistory.com/337
    eventlog_path2 = "C:\Windows\System32\winevt\Logs"

    reg_path = "C:\Windows\System32\config"
    reg = ['SAM', 'SECURITY', 'SOFTWARE', 'SYSTEM']
    cur_user_dir = r"C:\Users"+"\\"+getpass.getuser()

    nt_dir = "./NTFS"
    reg_dir = "./REGHIVE"
    evtx_dir = "./EVENTLOG"


    # prefetch ./PREFETCH
    os.system('robocopy {} ./PREFETCH'.format(prefetch_path)) # 관리자 권한 필요.


    # registry ./REGHIVE
    if not os.path.isdir(reg_dir):
        os.mkdir(reg_dir)
    for r in reg:
        os.system(r'RawCopy.exe /FileNamePath:{}\{} /OutputPath:{}\REGHIVE'.format(reg_path,r,cur_path))
    os.system(r'RawCopy.exe /FileNamePath:{}\NTUSER.DAT /OutputPath:{}\REGHIVE'.format(cur_user_dir, cur_path))
    os.system(r'RawCopy.exe /FileNamePath:{}\AppData\Local\Microsoft\Windows\UsrClass.dat /OutputPath:{}\REGHIVE'.format(cur_user_dir, cur_path))


    # mft ./NTFS
    drive_list = get_drives()

    if not os.path.isdir(nt_dir):
        os.mkdir(nt_dir)
    for drive in drive_list:
        os.system(r'RawCopy.exe /FileNamePath:{}:\$mft /OutputPath:{}\NTFS /OutputName:{}_mft'.format(drive,cur_path,drive))
    os.system(r'ExtractUsnJrnl.exe /DevicePath:C: /OutputPath:{}\NTFS /OutputName:$UsnJrnl'.format(cur_path))


    # 이벤트로그 ./EVENTLOG
    '''
    evtx_list = os.listdir(eventlog_path)
    if not os.path.isdir(evtx_dir):
        os.mkdir(evtx_dir)
    for e in evtx_list:
        os.system(r'RawCopy.exe /FileNamePath:{}\{} /OutputPath:{}\EVENTLOG'.format(eventlog_path2, e, cur_path))
    '''
    os.system(r'forecopy_handy.exe -e {}'.format(cur_path)) # ./eventlogs/Logs


    # 브라우저 ./BROWSER
    os.system(r'robocopy "{}\AppData\Local\Google\Chrome\User Data\Default" ./BROWSER History Bookmarks Cookies Preferences "Web Data" "Login Data"'.format(cur_user_dir))
    os.system(r'robocopy "{}\AppData\Local\Google\Chrome\User Data\Default\Cache" ./BROWSER/Cache'.format(cur_user_dir))
    os.system(r'robocopy "{}\AppData\Local\Google\Chrome\User Data\Default\GPUCache" ./BROWSER/GPUCache'.format(cur_user_dir))


    # 바로가기 ./LNK
    lnk_list = ['C:\\Users\\Default','%UserProfile%']
    for l in lnk_list:
        os.system(r'robocopy "{}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs" ./LNK *.lnk /e'.format(l))
        os.system(r'robocopy "{}\AppData\Local\Microsoft\Windows\WinX" ./LNK *.lnk /e'.format(l))
        os.system(r'robocopy "{}\AppData\Local\Microsoft\Internet Explorer\Quick Launch" ./LNK *.lnk /e'.format(l))
        os.system(r'robocopy "{}\AppData\Roaming\Microsoft\Windows\SendTo" ./LNK *.lnk /e'.format(l))

    os.system(r'robocopy "C:\ProgramData\Microsoft\Windows\Start Menu" ./LNK *.lnk /e')
    os.system(r'robocopy "%UserProfile%\AppData\Local\Microsoft\Windows\Application Shoutcuts" ./LNK *.lnk /e')
    os.system(r'robocopy "%UserProfile%\AppData\Roaming\Microsoft\Windows\Recent" ./LNK/Recent *.lnk /e')
    os.system(r'robocopy "%UserProfile%\Links" ./LNK *.lnk /e')

    os.system(r'robocopy "%UserProfile%\AppData\Roaming\Microsoft\Windows\Recent\AutomaticDestinations" ./LNK/jmplst')
    os.system(r'robocopy "%UserProfile%\AppData\Roaming\Microsoft\Windows\Recent\CustomDestinations" ./LNK/jmplst')

file_copy()