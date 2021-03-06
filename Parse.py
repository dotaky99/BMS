from EventLogParse import Save_Event
from LnkParse import Lnk_Parse
from BrowserParse import BrowserParser
from PrefetchParse import Prefetch_Parse
from NTFSParse import MFT_Parser, UsnJrnl_Parser
from JumpListParse import Jump_Parse
import os


def main():
    print("[*] Parsing Event Log")
    Save_Event.Save_Event()

    print("[*] Parsing Lnk")
    Lnk_Parse.main()

    print("[*] Parsing Browser")
    BrowserParser.Browser_parser()

    print("[*] Parsing Prefetch")
    Prefetch_Parse.main()

    print("[*] Parsing JumpList")
    Jump_Parse.main()

    print("[*] Parsing $MFT")
    MFT_Parser.parsing()

    print("[*] Parsing $UsnJrnl")
    UsnJrnl_Parser.usn_parse()

    print("[*] Parsing Registry")
    os.system("REGParse.exe COPY\REGHIVE\SYSTEM COPY\REGHIVE\SOFTWARE COPY\REGHIVE\SAM COPY\REGHIVE\\NTUSER.DAT COPY\REGHIVE\\USRCLASS.DAT")

    print("THE END Parsing")