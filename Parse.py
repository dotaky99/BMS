from EventLogParse import Save_Event
from LnkParse import Lnk_Parse
from BrowserParse import BrowserParser
from PretchParse import Prefetch_Parse
# import NTFSParse
import os

if __name__ == "__main__":
    # print("[*] Parsing Event Log")
    # Save_Event.Save_Event()

    print("[*] Parsing Lnk")
    Lnk_Parse.main()

    # print("[*] Parsing Browser")
    # BrowserParser.Browser_parser()

    # print("[*] Parsing Prefetch")
    # Prefetch_Parse.main()

    # print("[*] Parsing MFT")
    # MFT_Parser.parsing()

    # print("[*] Parsing Registry")
    # os.system('python RegistryParse\REGParse.py REGHIVE\SYSTEM REGHIVE\SOFTWARE REGHIVE\SAM REGHIVE\82102.NTUSER.DAT REGHIVE\82102.USRCLASS.DAT')