from EventLogParse.Evtx import Evtx as evtx
from bs4 import BeautifulSoup

'''
------------------------------------------
Collection of PC -> evtx file -> event id -> detailed
------------------------------------------ 
'''
def PC_Processing(file_et):
    two_d_data = []
    '''
    ---------------------------------------------------
    |              structure of file_et               |
    |-------------------------------------------------|
    |          KEY           |          VALUE         |
    |-------------------------------------------------|
    |       evtx_file        |  {eventid : detailed}  |
    ---------------------------------------------------
    '''
    for each_et in file_et:
        print('     [*] {0}'.format(each_et))
        # 로그 추출
        with evtx.Evtx(each_et) as log:
            #변수 초기화 작업 있으면 좋을 듯
            for record in log.records():
                soup = BeautifulSoup(record.xml(), "lxml")
                eventid = soup.eventid.string
                computer = soup.computer.string
                time_created = soup.timecreated['systemtime'].split('.')[0]
                source = each_et.split('/')[-1]

                if eventid not in file_et[each_et]:
                    continue

                # For system evtx list
                detailed = new_bias = old_bias = sleep_time = wake_time = \
                svc_name = img_path = svc_type = start_type = acc_name = channel = \
                net_name = guid = conn_mode = reason = \
                sys_bit_volume = sys_dev_id = sys_framework_ver = \
                sys_svc_name = sys_drv_file_name = sys_dvc_inst_id = sys_old_time = ''

                # For Setup evtx list
                package = ''

                # For Security evtx list
                trg_usr_name = sbt_usr_name = display_name = mem_sid = ip_addr = sys_prv_time = sys_new_time = ''

                # For Compatibility evtx list
                exe_path = ''

                # For RDP Client evtx list
                rdp_name = rdp_value = rdp_custom_level = sec_id = rdp_domain = rdp_session = ''

                # For LocalSessionManager evtx list
                local_manager_sess_id =  local_manager_reason = local_manager_sess = ''

                # For Remote Connection evtx list
                remo_conn_user = remo_conn_addr = remo_conn_local = ''

                # For Partition evtx list
                bus_type = drive_location = dev_num = drive_manufac = drive_serial = drive_model = capacity = ''
                bus = {
                    '0':'Unknown', '1':'SCSI', '2':'ATAPI', '3':'ATA', '4':'IEEE 1394', '5':'SSA', '6':'Fibre Channel',
                    '7':'USB', '8':'RAID', '9':'iSCSI', '10':'SAS', '11':'SATA', '12':'SD', '13':'MMC', '14':'MAX', '15':'File Backed Virtual',
                    '16':'Storage Spaces', '17':'NVMe'
                }

                # Applicaiton evtx list
                app_name = app_path = app_version = ''

                # 시스템 이벤트 파일에서 선별된 이벤트만을 파싱
                if 'System' in each_et and eventid in file_et[each_et]:
                    if eventid == '104':
                        detailed = file_et[each_et][eventid]
                        for data in soup.findAll('userdata'):
                            sbt_usr_name = data.subjectusername.string
                            channel = data.channel.string

                    if eventid == '12' and soup.task.string == '1':
                        detailed = file_et[each_et][eventid]
                    if eventid == '13' and soup.task.string == '2':
                        detailed = file_et[each_et][eventid]

                    if eventid == '42':
                        num = 0
                        for data in soup.findAll('data'):
                            if 'Flags' == data['name'] or 'TransitionsToOn' == data['name']:
                                break
                            if str(soup.data.string) == '6':
                                break
                            num += int(data.string)
                        if num == 8:
                            detailed = '버튼 및 노트북덮개에 의해 절전모드로 전환중입니다.'
                        if num == 10:
                            detailed = '버튼 및 노트북덮개에 의해 최대 절전모드로 전환중입니다.'
                        if num == 12:
                            detailed = '절전모드로 전환하는 중입니다.'
                        if num == 14:
                            detailed = '최대 절전모드로 전환하는 중입니다.'
                        if num == 15:
                            detailed = '시스템 사용이 없어 절전모드로 전환중입니다.'

                    if eventid == '1':
                        try:
                            if soup.version.string == '2':
                                detailed = 'Changed System Time'
                                for data in soup.findAll('data'):
                                    if 'NewTime' == data['name']:
                                        sys_new_time = data.string
                                    if 'OldTime' == data['name']:
                                        sys_old_time = data.string
                                    if 'Reason' == data['name']:
                                        if data.string == '1':
                                            reason = 'An application or system component changed the time.'
                                        elif data.string == '2':
                                            reason = 'System time synchronized with the hardware clock.'
                                        elif data.string == '3':
                                            reason = 'System time adjusted to the new time zone.'
                        except:
                            pass
                        try:
                            if soup.version.string == '3':
                                detailed = file_et[each_et][eventid]
                                for data in soup.findAll('data'):
                                    if 'SleepTime' == data['name']:
                                        sleep_time = data.string
                                    if 'WakeTime' == data['name']:
                                        wake_time = data.string
                        except:
                            pass

                    if eventid == '22' and soup.task.string == '8':
                        detailed = file_et[each_et][eventid]
                        for data in soup.findAll('data'):
                            if 'NewBias' == data['name']:
                                new_bias = data.string
                            if 'OldBias' == data['name']:
                                old_bias = data.string

                    if eventid == '7040':
                        if 'Windows Time' != str(soup.data.string) and '표준 시간대' not in str(soup.data.string):
                            continue
                        sec_id = soup.security['userid']
                        for data in soup.findAll('data'):
                            if 'param1' == data['name']:
                                detailed = data.string + ' 서비스 시작 유형을 '
                            if 'param2' == data['name']:
                                detailed += data.string + '에서 '
                            if 'param3' == data['name']:
                                detailed += data.string + '(으)로 변경했습니다.'

                    if eventid == '7045':
                        detailed = file_et[each_et][eventid]
                        for data in soup.findAll('data'):
                            if 'ServiceName' == data['name']:
                                svc_name = data.string
                            if 'ImagePath' == data['name']:
                                img_path = data.string
                            if 'ServiceType' == data['name']:
                                svc_type = data.string
                            if 'StartType' == data['name']:
                                start_type = data.string
                            if 'AccountName' == data['name']:
                                acc_name = data.string

                    if eventid == '24580' or eventid == '24660':
                        detailed = file_et[each_et][eventid]
                        for data in soup.findAll('data'):
                            if 'Volume' == data['name']:
                                sys_bit_volume = data.string

                    if eventid == '10000' or eventid == '10002' or eventid == '10100' or eventid == '20003' or eventid == '24576' or eventid == '24577' or eventid == '24579':
                        detailed = file_et[each_et][eventid]
                        if eventid == '10000':
                            sys_dev_id = soup.deviceid.string
                            sys_framework_ver = soup.frameworkversion.string

                        if eventid == '20003':
                            sys_svc_name = soup.servicename.string
                            sys_drv_file_name = soup.driverfilename.string
                            sys_dvc_inst_id = soup.deviceinstanceid.string

                # 네트워크 이벤트 파일에서 션별된 이벤트만을 파싱
                if ('Network' in each_et or 'WLAN' in each_et) and eventid in file_et[each_et]:
                    if eventid == '10000' or eventid == '10001':
                        detailed = file_et[each_et][eventid]
                        for data in soup.findAll('data'):
                            if 'Name' == data['name']:
                                net_name = data.string
                            if 'Guid' == data['name']:
                                guid = data.string

                    if eventid == '8003':
                        detailed = file_et[each_et][eventid]
                        for data in soup.findAll('data'):
                            if 'InterfaceGuid' == data['name']:
                                guid = data.string
                            if 'ConnectionMode' == data['name']:
                                conn_mode = data.string
                            if 'ProfileName' == data['name']:
                                net_name = data.string
                            if 'Reason' == data['name']:
                                reason = data.string

                # 애플리케이션 이벤트 파일에서 선별된 이벤트만을 파싱
                if 'Application' in each_et and eventid in file_et[each_et]:
                    if eventid == '1002':
                        try:
                            detailed = file_et[each_et][eventid]
                            temp = ((soup.data.string).replace('<string>', '').replace('</string>','')).split('\n')
                            app_name = temp[0]
                            app_version = temp[1]
                            app_path = temp[5]
                        except:
                            pass

                # 보안 이벤트 파일
                if 'Security' in each_et and eventid in file_et[each_et]:
                    if eventid == '4624' or eventid == '4625' or eventid == '4634':
                        detailed = file_et[each_et][eventid]
                        for data in soup.findAll('data'):
                            if 'TargetUserName' == data['name']:
                                trg_usr_name = data.string
                    if eventid == '4720' or eventid == '4726' or eventid == '4724' or eventid == '4738':
                        detailed = file_et[each_et][eventid]
                        for data in soup.findAll('data'):
                            if 'TargetUserName' == data['name']:
                                trg_usr_name = data.string
                            if 'SubjectUserName' == data['name']:
                                sbt_usr_name = data.string
                            if eventid == '4738' and 'DisplayName' == data['name']:
                                display_name = data.string
                    if eventid == '4732' or eventid == '4733':
                        detailed = file_et[each_et][eventid]
                        for data in soup.findAll('data'):
                            if 'TargetUserName' == data['name']:
                                trg_usr_name = data.string
                            if 'SubjectUserName' == data['name']:
                                sbt_usr_name = data.string
                            if 'MemberSid' == data['name']:
                                mem_sid = data.string

                    if eventid == '1102':
                        detailed = file_et[each_et][eventid]
                        for data in soup.findAll('userdata'):
                            sbt_usr_name = data.subjectusername.string

                    if eventid == '4648':
                        detailed = file_et[each_et][eventid]
                        for data in soup.findAll('data'):
                            if 'SubjectUserName' == data['name']:
                                sbt_usr_name = data.string
                            if 'TargetUserName' == data['name']:
                                trg_usr_name = data.string
                            if 'IpAddress' == data['name']:
                                ip_addr = data.string

                    if eventid == '4616':
                        detailed = file_et[each_et][eventid]
                        for data in soup.findAll('data'):
                            if 'SubjectUserName' == data['name']:
                                sbt_usr_name = data.string
                            if 'PreviousTime' == data['name']:
                                sys_prv_time = (data.string).split('.')[0]
                            if 'NewTime' == data['name']:
                                sys_new_time = (data.string).split('.')[0]

                # Windows Update 관련
                if 'Setup' in each_et and eventid in file_et[each_et]:
                    if eventid == '2':
                        package = soup.packageidentifier.string
                        detailed = package + " " + file_et[each_et][eventid]

                # 실행한 파일 및 설치 프로그램 이름
                if 'Compatibility' in each_et and eventid in file_et[each_et]:
                    if eventid == '17':
                        detailed = file_et[each_et][eventid]
                        for data in soup.findAll('exepath'):
                            exe_path = data.string

                # RDPClient 이벤트 파일 관련 추출
                if 'RDPClient' in each_et and eventid in file_et[each_et]:
                    try:
                        detailed = file_et[each_et][eventid]
                        sec_id = soup.security['userid']
                    except:
                        pass
                    if eventid == '1024' or eventid == '1026' or eventid == '1102':
                        for data in soup.findAll('data'):
                            if 'Name' == data['name']:
                                rdp_name = data.string
                            if 'Value' == data['name']:
                                rdp_value = data.string
                            if 'CustomLevel' == data['name']:
                                rdp_custom_level = data.string
                    if eventid == '1027' or eventid == '1018':
                        for data in soup.findAll('data'):
                            if 'DomainName' == data['name']:
                                rdp_domain = data.string
                            if 'SessionId' == data['name']:
                                rdp_session = data.string


                # Remote Conntection 이벤트 파일 관련 추출
                if 'RemoteConnection' in each_et and eventid in file_et[each_et]:
                    if eventid == '261':
                        detailed = file_et[each_et][eventid] + ' : {}'.format(soup.listenername.string)
                    if eventid == '1149':
                        detailed = file_et[each_et][eventid]
                        remo_conn_user = soup.param1.string
                        remo_conn_local = soup.param2.string
                        remo_conn_addr = soup.param3.string


                # Local Session Manager 이벤트 파일 관련 추출
                if 'LocalSessionManager' in each_et and eventid in file_et[each_et]:
                    detailed = file_et[each_et][eventid]
                    if eventid == '24' or eventid == '25' or eventid == '41' or eventid == '42':
                        remo_conn_local = (soup.user.string).split('\\')[0]
                        remo_conn_user = (soup.user.string).split('\\')[1]
                        local_manager_sess_id = soup.sessionid.string
                        if eventid == '24' or eventid == '25':
                            remo_conn_addr = soup.address.string
                    # if eventid == '40':
                    #     local_manager_sess = soup.session.string
                    #     local_manager_reason = soup.reason.string

                # Partition 이벤트 파일 관련 추출
                if 'Partition' in each_et and eventid in file_et[each_et]:
                    if eventid == '1006':
                        for data in soup.findAll('data'):
                            if 'BusType' == data['name']:
                                if data.string in bus:
                                    bus_type = bus[data.string]
                            if 'DiskNumber' == data['name']:
                                dev_num = data.string
                            if 'Capacity' == data['name']:
                                capacity = data.string
                            if 'Manufacturer' == data['name']:
                                drive_manufac = data.string
                            if 'Model' == data['name']:
                                drive_model = data.string
                            if 'SerialNumber' == data['name']:
                                drive_serial = data.string
                            if 'PartitionTableBytes' == data['name']:
                                if data.string == '0':
                                    detailed = 'The storage device has been successfully connected.'
                                else:
                                    detailed = 'The storage device has been successfully released.'
                            # CHECK VHD/X
                            if 'Location' == data['name']:
                                if 'vhd' in data.string:
                                    drive_location = data.string

                if 'Biometrics' in each_et and eventid in file_et[each_et]:
                    if eventid == '1004' or eventid == '1005':
                        detailed = file_et[each_et][eventid]
                        for data in soup.findAll('data'):
                            if 'Username' == data['name']:
                                sbt_usr_name = data.string

                if detailed == '':
                    continue

                data_list = [eventid,            detailed,            time_created,          source,            computer,
                             new_bias,           old_bias,            sleep_time,            wake_time,
                             svc_name,           img_path,            svc_type,              start_type,
                             acc_name,           net_name,            guid,                  conn_mode,
                             reason,             sys_bit_volume,      trg_usr_name,          sbt_usr_name,
                             display_name,       mem_sid,             ip_addr,               exe_path,
                             rdp_name,           rdp_value,           rdp_custom_level,      sec_id,
                             rdp_domain,         rdp_session,         local_manager_sess_id, bus_type,
                             local_manager_reason,local_manager_sess, remo_conn_user,        capacity,
                             remo_conn_addr,     remo_conn_local,    drive_location,      dev_num,
                             drive_manufac,      drive_serial,       drive_model,        package,
                             sys_prv_time,       sys_new_time,       sys_dev_id,         sys_framework_ver,
                             sys_svc_name,       sys_drv_file_name,  sys_dvc_inst_id,    sys_old_time,
                             app_name,           app_path,           app_version,        channel]
                two_d_data.append(data_list)
    return two_d_data