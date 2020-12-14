import os
import win32com.client
import getpass
import threading, pythoncom

class Drive(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        pythoncom.CoInitialize()
        self.drives = []

        strComputer = "."
        objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator")
        objSWbemServices = objWMIService.ConnectServer(strComputer, "root\cimv2")
        colItems = objSWbemServices.ExecQuery("Select * from Win32_LogicalDisk")

        for obj in colItems:
            if obj.FileSystem == "NTFS":
                letter = obj.Name.split(':')[0]
                print(obj.Name.split(':')[0])
                self.drives.append(letter)

        pythoncom.CoUninitialize()

    def returnDrive(self):
        return self.drives

def file_copy():
    # path
    cur_path = os.getcwd()
    prefetch_path = "C:/Windows/Prefetch"

    reg_path = "C:\Windows\System32\config"
    reg = ['SAM', 'SECURITY', 'SOFTWARE', 'SYSTEM']
    cur_user_dir = r"C:\Users"+"\\"+getpass.getuser()

    nt_dir = "COPY/NTFS"
    reg_dir = "COPY/REGHIVE"

    #prefetch BMS/COPY/PREFETCH
    os.system('robocopy {} COPY/PREFETCH'.format(prefetch_path))

    #registry BMS/COPY/REGHIVE
    if not os.path.isdir(reg_dir):
        os.mkdir(reg_dir)
    for r in reg:
        os.system(r'COPY\RawCopy.exe /FileNamePath:{}\{} /OutputPath:{}\COPY\REGHIVE'.format(reg_path,r,cur_path))
    os.system(r'COPY\RawCopy.exe /FileNamePath:{}\NTUSER.DAT /OutputPath:{}\COPY\REGHIVE'.format(cur_user_dir, cur_path))
    os.system(r'COPY\RawCopy.exe /FileNamePath:{}\AppData\Local\Microsoft\Windows\UsrClass.dat /OutputPath:{}\COPY\REGHIVE'.format(cur_user_dir, cur_path))

    #mft BMS/COPY/NTFS
    getDrives = Drive()
    getDrives.start()
    getDrives.join()
    drive_list = getDrives.returnDrive()

    if not os.path.isdir(nt_dir):
        os.mkdir(nt_dir)
    for drive in drive_list:
        os.system(r'COPY\RawCopy.exe /FileNamePath:{}:\$mft /OutputPath:{}\COPY\NTFS /OutputName:{}_mft'.format(drive,cur_path,drive))
    data = os.popen(r'COPY\usncopy\fls.exe \\.\c: 11 | find "$UsnJrnl:$J"').read().strip().split(' ')[1].split(':')[0]
    os.system(r'COPY\usncopy\icat.exe -f ntfs \\.\c: {} > {}\COPY\NTFS\$UsnJrnl'.format(data, cur_path))

    # Event Log BMS/COPY/eventlogs/Logs
    os.system(r'COPY\forecopy_handy.exe -e COPY')

    #Browser BMS/COPY/BROWSER
    os.system(r'robocopy "{}\AppData\Local\Google\Chrome\User Data\Default" COPY/BROWSER History Bookmarks Cookies Preferences "Web Data" "Login Data"'.format(cur_user_dir))
    os.system(r'robocopy "{}\AppData\Local\Google\Chrome\User Data\Default\Cache" COPY/BROWSER/Cache'.format(cur_user_dir))
    os.system(r'robocopy "{}\AppData\Local\Google\Chrome\User Data\Default\GPUCache" COPY/BROWSER/GPUCache'.format(cur_user_dir))

    #LNK BMS/COPY/LNK
    lnk_list = ['C:\\Users\\Default','%UserProfile%']
    for l in lnk_list:
        os.system(r'robocopy "{}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs" COPY/LNK *.lnk /e'.format(l))
        os.system(r'robocopy "{}\AppData\Local\Microsoft\Windows\WinX" COPY/LNK *.lnk /e'.format(l))
        os.system(r'robocopy "{}\AppData\Local\Microsoft\Internet Explorer\Quick Launch" COPY/LNK *.lnk /e'.format(l))
        os.system(r'robocopy "{}\AppData\Roaming\Microsoft\Windows\SendTo" COPY/LNK *.lnk /e'.format(l))

    os.system(r'robocopy "C:\ProgramData\Microsoft\Windows\Start Menu" COPY/LNK *.lnk /e')
    os.system(r'robocopy "%UserProfile%\AppData\Local\Microsoft\Windows\Application Shoutcuts" COPY/LNK *.lnk /e')
    os.system(r'robocopy "%UserProfile%\AppData\Roaming\Microsoft\Windows\Recent" COPY/LNK/Recent *.lnk /e')
    os.system(r'robocopy "%UserProfile%\Links" COPY/LNK *.lnk /e')

    # JMPLIST BMS/COPY/JUMPLIST
    os.system(r'robocopy "%UserProfile%\AppData\Roaming\Microsoft\Windows\Recent\AutomaticDestinations" COPY/JUMPLIST')
    os.system(r'robocopy "%UserProfile%\AppData\Roaming\Microsoft\Windows\Recent\CustomDestinations" COPY/JUMPLIST')