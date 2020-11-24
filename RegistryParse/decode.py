import codecs
from datetime import datetime,timedelta


# convert little endian 8 bytes to time
def convert_time(bytes_time):
    if bytes_time == b"\x00\x00\x00\x00\x00\x00\x00\x00":
        return None
    elif bytes_time == b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x7F":
        return None
    else:
        tmp = int.from_bytes(bytes_time, "big", signed=False)
        tmp = int.to_bytes(tmp, 8, "little")
        dt = tmp.hex()

        us = int(dt, 16) / 10.
        a = str(datetime(1601, 1, 1) + timedelta(microseconds=us))
        return a.split('.')[0]


def ROT13(string):
    return codecs.getencoder("rot-13")(string)[0]


def GUID_to_display_name(display_name):
    # https://docs.microsoft.com/en-us/windows/win32/shell/knownfolderid
    GUID = [
        ["{008ca0b1-55b4-4c56-b8a8-4de4b299d3be}", "Account Pictures"],
        ["{de61d971-5ebc-4f02-a3a9-6c82895e5c04}", "Get Programs"],
        ["{724EF170-A42D-4FEF-9F26-B60E846FBA4F}", "Administrative Tools"],
        ["{B2C5E279-7ADD-439F-B28C-C41FE1BBF672}", "AppDataDesktop"],
        ["{7BE16610-1F7F-44AC-BFF0-83E15F2FFCA1}", "AppDataDocuments"],
        ["{7CFBEFBC-DE1F-45AA-B843-A542AC536CC9}", "AppDataFavorites"],
        ["{559D40A3-A036-40FA-AF61-84CB430A4D34}", "AppDataProgramData"],
        ["{A3918781-E5F2-4890-B3D9-A7E54332328C}", "Application Shortcuts"],
        ["{1e87508d-89c2-42f0-8a7e-645a0f50ca58}", "Application"],
        ["{a305ce99-f527-492b-8b1a-7e76fa98d6e4}", "Installed Updates"],
        ["{AB5FB87B-7CE2-4F83-915D-550846C9537B}", "Camera Roll"],
        ["{9E52AB10-F80D-49DF-ACB8-4330F5687855}", "Temporary Burn Folder"],
        ["{df7266ac-9274-4867-8d55-3bd661de872d}", "Programs and Features"],
        ["{D0384E7D-BAC3-4797-8F14-CBA229B392B5}", "Administrative Tools"],
        ["{C1BAE2D0-10DF-4334-BEDD-7AA20B227A9D}", "OEM Links"],
        ["{0139D44E-6AFE-49F2-8690-3DAFCAE6FFB8}", "Programs"],
        ["{A4115719-D62E-491D-AA7C-E74B8BE3B067}", "Start Menu"],
        ["{82A5EA35-D9CD-47C5-9629-E15D2F714E6E}", "Startup"],
        ["{B94237E7-57AC-4347-9151-B08C6C32D1F7}", "Templates"],
        ["{0AC0837C-BBF8-452A-850D-79D08E667CA7}", "Computer"],
        ["{4bfefb45-347d-4006-a5be-ac0cb0567192}", "Conflicts"],
        ["{6F0CD92B-2E97-45D1-88FF-B0D186B8DEDD}", "Network Connections"],
        ["{56784854-C6CB-462b-8169-88E350ACB882}", "Contacts"],
        ["{82A74AEB-AEB4-465C-A014-D097EE346D63}", "Control Panel"],
        ["{2B0F765D-C0E9-4171-908E-08A611B84FF6}", "Cookies"],
        ["{B4BFCC3A-DB2C-424C-B029-7FE99A87C641}", "Desktop"],
        ["{5CE4A5E9-E4EB-479D-B89F-130C02886155}", "DeviceMetadataStore"],
        ["{FDD39AD0-238F-46AF-ADB4-6C85480369C7}", "Documents"],
        ["{7B0DB17D-9CD2-4A93-9733-46CC89022E7C}", "Documents"],
        ["{374DE290-123F-4565-9164-39C4925E467B}", "Downloads"],
        ["{1777F761-68AD-4D8A-87BD-30B759FA33DD}", "Favorites"],
        ["{FD228CB7-AE11-4AE3-864C-16F3910AB8FE}", "Fonts"],
        ["{CAC52C1A-B53D-4edc-92D7-6B2E8AC19434}", "Games"],
        ["{054FAE61-4DD8-4787-80B6-090220C4B700}", "GameExplorer"],
        ["{D9DC8A3B-B784-432E-A781-5A1130A75963}", "History"],
        ["{52528A6B-B9E3-4ADD-B60D-588C2DBA842D}", "Homegroup"],
        ["{9B74B6A3-0DFD-4f11-9E78-5F7800F2E772}", "%USERNAME%"],
        ["{BCB5256F-79F6-4CEE-B725-DC34E402FD46}", "ImplicitAppShortcuts"],
        ["{352481E8-33BE-4251-BA85-6007CAEDCF9D}", "Temporary Internet Files"],
        ["{4D9F7874-4E0C-4904-967B-40B0D20C3E4B}", "The Internet"],
        ["{1B3EA5DC-B587-4786-B4EF-BD1DC332AEAE}", "Libraries"],
        ["{bfb9d5e0-c6a9-404c-b2b2-ae6db6af4968}", "Links"],
        ["{F1B32785-6FBA-4FCF-9D55-7B8E7F157091}", "Local"],
        ["{A520A1A4-1780-4FF6-BD18-167343C5AF16}", "LocalLow"],
        ["{2A00375E-224C-49DE-B8D1-440DF7EF3DDC}", "None"],
        ["{4BD8D571-6D19-48D3-BE97-422220080E43}", "Music"],
        ["{2112AB0A-C86A-4FFE-A368-0DE96E47012E}", "Music"],
        ["{C5ABBF53-E17F-4121-8900-86626FC2C973}", "Network Shortcuts"],
        ["{D20BEEC4-5CA8-4905-AE3B-BF251EA09B53}", "Network"],
        ["{31C0DD25-9439-4F12-BF41-7FF4EDA38722}", "3D Objects"],
        ["{2C36C0AA-5812-4b87-BFD0-4CD0DFB19B39}", "Original Images"],
        ["{69D2CF90-FC33-4FB7-9A0C-EBB0F0FCB43C}", "Slide Shows"],
        ["{A990AE9F-A03B-4E80-94BC-9912D7504104}", "Pictures"],
        ["{33E28130-4E1E-4676-835A-98395C3BC3BB}", "Piuctures"],
        ["{DE92C1C7-837F-4F69-A3BB-86E631204A23}", "Playlists"],
        ["{76FC4E2D-D6AD-4519-A663-37BD56068185}", "Printers"],
        ["{9274BD8D-CFD1-41C3-B35E-B13F55A758F4}", "Printer Shortcuts"],
        ["{5E6C858F-0E22-4760-9AFE-EA3317B67173}", "%USERNAME%"],
        ["{62AB5D82-FDC1-4DC3-A9DD-070D1D495D97}", "ProgramData"],
        ["{905e63b6-c1bf-494e-b29c-65b732d3d21a}", "Program Files"],
        ["{6D809377-6AF0-444b-8957-A3773F02200E}", "Program Files"],
        ["{7C5A40EF-A0FB-4BFC-874A-C0F2E0B9FA8E}", "Program Files"],
        ["{F7F1ED05-9F6D-47A2-AAAE-29D317C6F066}", "Common Files"],
        ["{6365D5A7-0F0D-45E5-87F6-0DA56B6A4F7D}", "Common Files"],
        ["{DE974D24-D9C6-4D3E-BF91-F4455120B917}", "Common Files"],
        ["{A77F5D77-2E2B-44C3-A6A2-ABA601054A51}", "Programs"],
        ["{DFDF76A2-C82A-4D63-906A-5644AC457385}", "Public"],
        ["{C4AA340D-F20F-4863-AFEF-F87EF2E6BA25}", "Public Desktop"],
        ["{ED4824AF-DCE4-45A8-81E2-FC7965083634}", "Public Documents"],
        ["{3D644C9B-1FB8-4f30-9B45-F670235F79C0}", "Public Downloads"],
        ["{DEBF2536-E1A8-4c59-B6A2-414586476AEA}", "GameExplorer"],
        ["{48DAF80B-E6CF-4F4E-B800-0E69D84EE384}", "Libraries"],
        ["{3214FAB5-9757-4298-BB61-92A9DEAA44FF}", "Public Music"],
        ["{B6EBFB86-6907-413C-9AF7-4FC2ABF07CC5}", "Public Pictures"],
        ["{E555AB60-153B-4D17-9F04-A5FE99FC15EC}", "Ringtones"],
        ["{0482af6c-08f1-4c34-8c90-e17ec98b1e17}", "Public Account Pictures"],
        ["{2400183A-6185-49FB-A2D8-4A392A602BA3}", "Public Videos"],
        ["{52a4f021-7b75-48a9-9f6b-4b87a210bc8f}", "Quick Launch"],
        ["{AE50C081-EBD2-438A-8655-8A092E34987A}", "Recent Items"],
        ["{1A6FDBA2-F42D-4358-A798-B74D745926C5}", "Recorded TV"],
        ["{B7534046-3ECB-4C18-BE4E-64CD4CB7D6AC}", "Recycle Bin"],
        ["{8AD10C31-2ADB-4296-A8F7-E4701232C972}", "Resources"],
        ["{C870044B-F49E-4126-A9C3-B52A1FF411E8}", "Ringtones"],
        ["{3EB685DB-65F9-4CF6-A03A-E3EF65729F3D}", "Roaming"],
        ["{AAA8D5A5-F1D6-4259-BAA8-78E7EF60835E}", "RoamedTileImages"],
        ["{00BCFC5A-ED94-4e48-96A1-3F6217F21990}", "RoamingTiles"],
        ["{B250C668-F57D-4EE1-A63C-290EE7D1AA1F}", "Sample Music"],
        ["{C4900540-2379-4C75-844B-64E6FAF8716B}", "Sample Pictures"],
        ["{15CA69B3-30EE-49C1-ACE1-6B5EC372AFB5}", "Sample Playlists"],
        ["{859EAD94-2E85-48AD-A71A-0969CB56A6CD}", "Sample Videos"],
        ["{4C5C32FF-BB9D-43b0-B5B4-2D72E54EAAA4}", "Saved Games"],
        ["{3B193882-D3AD-4eab-965A-69829D1FB59F}", "Saved Pictures"],
        ["{E25B5812-BE88-4bd9-94B0-29233477B6C3}", "Saved Pictures Library"],
        ["{7d1d3a04-debb-4115-95cf-2f29da2920da}", "Searches"],
        ["{b7bede81-df94-4682-a7d8-57a52620b86f}", "Screenshots"],
        ["{ee32e446-31ca-4aba-814f-a5ebd2fd6d5e}", "Offline Files"],
        ["{0D4C3DB6-03A3-462F-A0E6-08924C41B5D4}", "History"],
        ["{190337d1-b8ca-4121-a639-6d472d16972a}", "Search Results"],
        ["{98ec0e18-2098-4d44-8644-66979315a281}", "Microsoft Office Outlook"],
        ["{7E636BFE-DFA9-4D5E-B456-D7B39851D8A9}", "Templates"],
        ["{8983036C-27C0-404B-8F08-102D10DCFD74}", "SendTo"],
        ["{7B396E54-9EC5-4300-BE0A-2482EBAE1A26}", "Gadgets"],
        ["{A75D362E-50FC-4fb7-AC2C-A8BEAA314493}", "Gadgets"],
        ["{A52BBA46-E9E1-435f-B3D9-28DAA648C0F6}", "OneDrive"],
        ["{767E6811-49CB-4273-87C2-20F355E1085B}", "Camera Roll"],
        ["{24D89E24-2F19-4534-9DDE-6A6671FBB8FE}", "Documents"],
        ["{339719B5-8C47-4894-94C2-D8F77ADD44A6}", "Pictures"],
        ["{625B53C3-AB48-4EC1-BA1F-A1EF4146FC19}", "Start Menu"],
        ["{B97D20BB-F46A-4C97-BA10-5E3608430854}", "Startup"],
        ["{43668BF8-C14E-49B2-97C9-747784D784B7}", "Sync Center"],
        ["{289a9a43-be44-4057-a41b-587a76d7e7f9}", "Sync Results"],
        ["{0F214138-B1D3-4a90-BBA9-27CBC0C5389A}", "Sync Setup"],
        ["{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}", "System32"],
        ["{D65231B0-B2F1-4857-A4CE-A8E7C6EA7D27}", "System32"],
        ["{A63293E8-664E-48DB-A079-DF759E0509F7}", "Templates"],
        ["{9E3995AB-1F9C-4F13-B827-48B24B6C7174}", "User Pinned"],
        ["{0762D272-C50A-4BB0-A382-697DCD729B80}", "Users"],
        ["{5CD7AEE2-2219-4A67-B85D-6C9CE15660CB}", "Programs"],
        ["{BCBD3057-CA5C-4622-B42D-BC56DB0AE516}", "Programs"],
        ["{f3ce0f7c-4901-4acc-8648-d5d44b04ef8f}", "User's full name"],
        ["{A302545D-DEFF-464b-ABE8-61C8648D939B}", "Libraries"],
        ["{18989B1D-99B5-455B-841C-AB7C74E4DDFC}", "Videos"],
        ["{491E922F-5643-4AF4-A7EB-4E7A138D8174}", "Videos"],
        ["{F38BF404-1D43-42F2-9305-67DE0B28FC23}", "Windows"]
    ]
    for g in GUID:
        display_name = display_name.replace(g[0], g[1])

    return display_name