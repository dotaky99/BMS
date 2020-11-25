from NTFSParse.ntfs import MFT, USN, Format
import Database

def usn_parse():
    usn_path = "../COPY/NTFS/$UsnJrnl"
    mft_path = "../COPY/NTFS/C_mft"

    input_file = open(usn_path, 'rb')
    input_mft = open(mft_path,' rb')

    usn_journal = USN.ChangeJournalParser(input_file)
    mft_file = MFT.MasterFileTableParser(input_mft)

    data_list = []

    for usn_record in usn_journal.usn_records():
        r_usn = usn_record.get_usn()
        r_source = USN.ResolveSourceCodes(usn_record.get_source_info())
        r_reason = USN.ResolveReasonCodes(usn_record.get_reason())
        fr_reference_number = usn_record.get_file_reference_number()
        parent_fr_reference_number = usn_record.get_parent_file_reference_number()

        if type(usn_record) is USN.USN_RECORD_V2_OR_V3:
            r_timestamp = Format.format_timestamp(usn_record.get_timestamp())
            fr_file_name = usn_record.get_file_name()
        else:
            r_timestamp = ''
            fr_file_name = ''

        fr_number, fr_sequence = MFT.DecodeFileRecordSegmentReference(fr_reference_number)

        try:
            file_record = mft_file.get_file_record_by_number(fr_number, fr_sequence)
            file_paths = mft_file.build_full_paths(file_record)
        except MFT.MasterFileTableException:
            fr_file_path = ''
        else:
            if len(file_paths) > 0:
                fr_file_path = file_paths[0]
            else:
                fr_file_path = ''

        t = (r_usn, r_source, r_reason, fr_reference_number, parent_fr_reference_number, r_timestamp, fr_file_name, fr_file_path)
        data_list.append(t)

    Database.Usn_Databases(data_list)


