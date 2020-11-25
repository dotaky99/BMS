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

    # prefetch BMS/COPY/PREFETCH
    os.system('robocopy {} ./PREFETCH'.format(prefetch_path)) # 관리자 권한 필요.

    # registry BMS/COPY/REGHIVE
    if not os.path.isdir(reg_dir):
        os.mkdir(reg_dir)
    for r in reg:
        os.system(r'COPY\RawCopy.exe /FileNamePath:{}\{} /OutputPath:{}\COPY\REGHIVE'.format(reg_path,r,cur_path))
    os.system(r'COPY\RawCopy.exe /FileNamePath:{}\NTUSER.DAT /OutputPath:{}\COPY\REGHIVE'.format(cur_user_dir, cur_path))
    os.system(r'COPY\RawCopy.exe /FileNamePath:{}\AppData\Local\Microsoft\Windows\UsrClass.dat /OutputPath:{}\COPY\REGHIVE'.format(cur_user_dir, cur_path))

    # mft BMS/COPY/NTFS
    drive_list = get_drives()

    if not os.path.isdir(nt_dir):
        os.mkdir(nt_dir)
    for drive in drive_list:
        os.system(r'COPY\RawCopy.exe /FileNamePath:{}:\$mft /OutputPath:{}\COPY\NTFS /OutputName:{}_mft'.format(drive,cur_path,drive))
    os.system(r'COPY\ExtractUsnJrnl.exe /DevicePath:C: /OutputPath:{}\COPY\NTFS /OutputName:$UsnJrnl'.format(cur_path))

    # Event Log
    os.system(r'COPY\forecopy_handy.exe -e {}'.format(cur_path)) # ./eventlogs/Logs

    # 브라우저 BMS/COPY/BROWSER
    os.system(r'robocopy "{}\AppData\Local\Google\Chrome\User Data\Default" ./COPY/BROWSER History Bookmarks Cookies Preferences "Web Data" "Login Data"'.format(cur_user_dir))
    os.system(r'robocopy "{}\AppData\Local\Google\Chrome\User Data\Default\Cache" ./COPY/BROWSER/Cache'.format(cur_user_dir))
    os.system(r'robocopy "{}\AppData\Local\Google\Chrome\User Data\Default\GPUCache" ./COPY/BROWSER/GPUCache'.format(cur_user_dir))

    # 링크파일 BMS/COPY/LNK
    lnk_list = ['C:\\Users\\Default','%UserProfile%']
    for l in lnk_list:
        os.system(r'robocopy "{}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs" ./COPY/LNK *.lnk /e'.format(l))
        os.system(r'robocopy "{}\AppData\Local\Microsoft\Windows\WinX" ./COPY/LNK *.lnk /e'.format(l))
        os.system(r'robocopy "{}\AppData\Local\Microsoft\Internet Explorer\Quick Launch" ./COPY/LNK *.lnk /e'.format(l))
        os.system(r'robocopy "{}\AppData\Roaming\Microsoft\Windows\SendTo" ./COPY/LNK *.lnk /e'.format(l))

    os.system(r'robocopy "C:\ProgramData\Microsoft\Windows\Start Menu" ./COPY/LNK *.lnk /e')
    os.system(r'robocopy "%UserProfile%\AppData\Local\Microsoft\Windows\Application Shoutcuts" ./COPY/LNK *.lnk /e')
    os.system(r'robocopy "%UserProfile%\AppData\Roaming\Microsoft\Windows\Recent" ./COPY/LNK/Recent *.lnk /e')
    os.system(r'robocopy "%UserProfile%\Links" ./COPY/LNK *.lnk /e')

    # 점프리스트 BMS/COPY/JUMPLIST
    os.system(r'robocopy "%UserProfile%\AppData\Roaming\Microsoft\Windows\Recent\AutomaticDestinations" ./COPY/JUMPLIST')
    os.system(r'robocopy "%UserProfile%\AppData\Roaming\Microsoft\Windows\Recent\CustomDestinations" ./COPY/JUMPLIST')

file_copy()