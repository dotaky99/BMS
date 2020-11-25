# -*- Coding:utf-8 -*-
import LnkParse
import os
import binascii
import Database

 # 파일 리스트 중 lnk 파일을 가져오는 함수
def lnk_parse(files):
   lnk_list = []
   lnk_list_temp = [i for i in files if (i[-4:] == ".lnk")]
   for i in lnk_list_temp:
       with open(i,'rb') as f:
           string = f.read(4)
       if (binascii.b2a_hex(string) == b'4c000000'):
           lnk_list.append(i)

   return lnk_list

# lnk 파일의 전체경로 중 파일명만 따로 추출하는 함수
def name_split(lnk_files):

   file_names = []

   for i in lnk_files:
      file_split = i.split("\\")
      file_name = file_split[-1]
      file_names.append(file_name)

   return file_names

# shell link header
def shell_link_header_parse(x):

    shell_link_header = [x.format_fileFlags(), x.lnk_header['file_size'], x.lnk_header['windowstyle'], x.ms_time_to_unix_time(x.lnk_header['creation_time']),
                             x.ms_time_to_unix_time(x.lnk_header['modified_time']),
                             x.ms_time_to_unix_time(x.lnk_header['accessed_time'])]

    return shell_link_header

# string data
def string_data_parse(x):
    string_keys = list(x.data.keys())

    if 'icon_location' in string_keys:
        icon_location = x.data['icon_location']
    elif 'icon_location' not in string_keys:
        icon_location = ''

    string_data = [icon_location]

    return string_data

# extra data
def extra_data_parse(x):
    extra_keys = list(x.extraBlocks.keys())

    if 'DISTRIBUTED_LINK_TRACKER_BLOCK' in extra_keys:
        extra_dis_values = list(x.extraBlocks['DISTRIBUTED_LINK_TRACKER_BLOCK'].values())
        machine_info = extra_dis_values[3]
        droid_file = extra_dis_values[5]
        droid_vol = extra_dis_values[4]
    elif 'DISTRIBUTED_LINK_TRACKER_BLOCK' not in extra_keys:
        machine_info = ''
        droid_file = ''
        droid_vol = ''
    if 'ICON_LOCATION_BLOCK' in extra_keys:
        extra_icon_values = list(x.extraBlocks['ICON_LOCATION_BLOCK'].values())
        icon_path = extra_icon_values[1]
    elif 'ICON_LOCATION_BLOCK' not in extra_keys:
        icon_path = ''
    if 'KNOWN_FOLDER_LOCATION_BLOCK' in extra_keys:
        extra_known_values = list(x.extraBlocks['KNOWN_FOLDER_LOCATION_BLOCK'].values())
        known_folder_guid = extra_known_values[1]
    elif 'KNOWN_FOLDER_LOCATION_BLOCK' not in extra_keys:
        known_folder_guid = ''

    extra_data = [machine_info, droid_vol, droid_file, icon_path, known_folder_guid]

    return extra_data

def link_info_parse(x):
    drive_serial_number = drive_type = volume_label = ''
    link_info = list(x.loc_information.values())
    link_info_keys = list(x.loc_information.keys())

    if 'local_base_path' in link_info_keys:
        local_base_path = link_info[7]
    elif 'local_base_path' not in link_info_keys:
        local_base_path = ''
    if 'location_info' in link_info_keys:
        try:
            location_info = link_info[10]
        except:
            num = 0
            for i in link_info:
                if isinstance(link_info[num], dict):
                    location_info = link_info[num]
                num += 1
        location_info_keys = list(location_info.keys())
        location_info_values = list(location_info.values())
        if 'drive_serial_number' in location_info_keys:
            drive_serial_number = location_info_values[2]
        if 'drive_type' in location_info_keys:
            drive_type = location_info_values[4]
        if 'volume_label' in location_info_keys:
            volume_label = location_info_values[5]

    link_info_data = [local_base_path, drive_serial_number, drive_type, volume_label]

    return link_info_data

def allfile(path):
   res = []

   for root, dirs, files in os.walk(path):

      roots = root.split("COPY/LNK/")
      root = roots[1]
      rootpath = os.path.join(os.path.abspath(path), root)
      # rootpath = os.path.abspath(path)
      for file in files:
         filepath = os.path.join(rootpath, file)

         res.append(filepath)

   return res

def files_parse():
    path_dir = 'COPY/LNK/'
    file_lists = allfile(path_dir)
    lnk_lists = lnk_parse(file_lists)
    return lnk_lists

def main():

    lnk_lists = files_parse()
    file_name = name_split(lnk_lists)
    seq = 0
    data_list = []

    for a in lnk_lists:

        indata = open(a, 'rb')
        x = LnkParse.lnk_file(indata)
        #shell_link_header
        shell_link_header = shell_link_header_parse(x)
        #link_info
        link_info = link_info_parse(x)
        #string_data
        string_data = string_data_parse(x)
        #extra_data
        extra_data = extra_data_parse(x)

        total = shell_link_header + link_info + string_data + extra_data
        total.insert(0, a)
        total.insert(1, file_name[seq])
        data_list.append(total)
        seq += 1

    Database.Lnk_Databases(data_list)

if __name__ == '__main__':
    main()