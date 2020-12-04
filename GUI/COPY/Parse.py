import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from EventLogParse import Save_Event
from LnkParse import Lnk_Parse
from BrowserParse import BrowserParser
from PretchParse import Prefetch_Parse
from NTFSParse import MFT_Parser, UsnJrnl_Parser
from JumpListParse import Jump_Parse


if __name__ == "__main__":
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
    os.system('python RegistryParse\REGParse.py GUI\COPY\REGHIVE\SYSTEM GUI\COPY\REGHIVE\SOFTWARE GUI\COPY\REGHIVE\SAM GUI\COPY\REGHIVE\\NTUSER.DAT GUI\COPY\REGHIVE\\USRCLASS.DAT')
