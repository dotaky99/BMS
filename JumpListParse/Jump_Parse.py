# -*- Coding:utf-8 -*-
import os
import re
from io import BytesIO
from olefile.olefile import OleFileIO
from JumpListParse.pylnk import Lnk
import struct
import sqlite3
import Database

def read_custom(jump_filename):
    datalist = []
    link_header = b'\x4C\x00\x00\x00\x01\x14\x02\x00\x00\x00\x00\x00\xC0\x00\x00\x00\x00\x00\x00\x46'
    prefix = b'\x01\x14\x02\x00\x00\x00\x00\x00\xC0\x00\x00\x00\x00\x00\x00\x46'
    fileend = b'\xAB\xFB\xBF\xBA'

    with open(jump_filename, 'rb') as f:
        custom = f.read()
    try:
        header = struct.unpack('<IIIII', custom[:20])
        count = header[4]

        matches = []
        for match in re.finditer(link_header, custom):
            matches.append(match.start())

        lnk_counter = 0

        matches.append(len(custom))
        for i in range(len(matches)-1):
            lnk_data = custom[matches[i]:matches[i+1]]
            if lnk_data.endswith(prefix):
                lnk_data = lnk_data[:-len(prefix)]
            if lnk_data.endswith(fileend):
                lnk_data = lnk_data[:-len(fileend)]

            try:

                link = Lnk(BytesIO(lnk_data))
                flags = []
                file_flags = ''
                seq = 0
                type = ['archive', 'compressed', 'directory', 'encrypted', 'hidden', 'normal', 'not_content_indexed','offline','read_only','reparse_point'
                        ,'reserved1','reserved2','sparse_file','system_file','temporary']
                for i in type:
                    if link.file_flags[i] == True:
                        flags.append(i)

                for i in range(len(flags)):
                    if len(flags) == i + 1:
                        file_flags += flags[seq]
                    else:
                        file_flags += flags[seq] + ', '

                    seq += 1
                file_name = link.link_info.local_base_path.split["\\"][-1]
                data = ["CustDest", jump_filename, file_name, lnk_counter, link.path, link.file_size, file_flags, link.creation_time, link.modification_time, link.access_time, link.show_command, link.icon,
                link.description, link.link_info.local_base_path, link.link_info.volume_label, link.link_info.drive_type]
                lnk_counter += 1

                datalist.append(data)

            except:
                pass

    except:
        pass

    return datalist

def read_auto(jump_filename):
    datalist = []
    ole = OleFileIO(jump_filename)
    lnk_counter = 0
    for ole_stream in ole.listdir():
        ole_stream = ole_stream[0]
        link_io = ole.openstream(ole_stream)
        try:
            link = Lnk(link_io)
            flags = []
            seq = 0
            file_flags = ''
            type = ['archive', 'compressed', 'directory', 'encrypted', 'hidden', 'normal', 'not_content_indexed',
                    'offline', 'read_only', 'reparse_point', 'reserved1', 'reserved2', 'sparse_file', 'system_file', 'temporary']
            for i in type:
                if link.file_flags[i] == True:
                    flags.append(i)

            for i in range(len(flags)):
                if len(flags) == i + 1:
                    file_flags += flags[seq]
                else:
                    file_flags += flags[seq] + ', '

                seq += 1
            file_name = link.link_info.local_base_path.split("\\")[-1]

            data = ["AutoDest", jump_filename, file_name, lnk_counter, link.path, link.file_size, file_flags, link.creation_time, link.modification_time,
                    link.access_time, link.show_command, link.icon,
                    link.description, link.link_info.local_base_path, link.link_info.volume_label, link.link_info.drive_type]
            lnk_counter += 1
            datalist.append(data)

        except:
            pass
    return datalist

def main():

    path = 'COPY\\JUMPLIST'
    lists = os.listdir(path)
    jump_list_auto, jump_list_cust = [], []
    try:
        for i in lists:
            jm_type = i.split(".")[-1]
            if jm_type == 'automaticDestinations-ms':
                jump_list_auto.append("COPY/JUMPLIST/"+i)
            if jm_type == 'customDestinations-ms':
                jump_list_cust.append("COPY/JUMPLIST/"+i)
    except:
        pass

    datalist_auto = []
    datalist_cust = []

    for i in jump_list_auto:
        datalist_auto += read_auto(i)

    for i in jump_list_cust:
        datalist_cust += read_custom(i)

    datalist = datalist_auto + datalist_cust
    Database.JumpList_Databases(datalist)

if __name__ == '__main__':
    main()