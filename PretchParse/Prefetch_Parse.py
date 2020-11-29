# -*- coding : utf-8 -*-
from argparse import ArgumentParser
import binascii
import ctypes
from datetime import datetime, timedelta
import os
import struct
import sys
import tempfile
import Database

second_data_list1 = []
second_data_list2 = []

path_dir = 'COPY/PREFETCH/'
file_list = os.listdir(path_dir)

class Prefetch(object):

    def __init__(self, infile):
        self.pFileName = infile

        with open(infile, "rb") as f:
            if f.read(3).decode() == "MAM":
                f.close()

                d = DecompressWin10()
                decompressed = d.decompress(infile)

                t = tempfile.mkstemp()

                with open(t[1], "wb+")as f:
                    f.write(decompressed)
                    f.seek(0)

                    self.parseHeader(f)
                    self.fileInformation(f)
                    self.metricsArray(f)
                    self.traceChainsArray(f)
                    self.volumeInformation(f)
                    self.getTimeStamps(self.lastRunTime)
                    self.directoryStrings(f)
                    self.getFilenameStrings(f)
                    self.filepath(f)
                    self.output()
                    return

    def parseHeader(self, infile):
        # Prefetcher Version(0x0000001E)
        self.version = struct.unpack_from("I", infile.read(4))[0]
        # Signature('SCCA')
        self.signature = struct.unpack_from("I", infile.read(4))[0]
        # Prefetcher Management Service Version
        unknown0 = struct.unpack_from("I", infile.read(4))[0]
        # File Size
        self.fileSize = struct.unpack_from("I", infile.read(4))[0]
        executableName = struct.unpack_from("60s", infile.read(60))[0]
        executableName = executableName.decode('UTF-16')
        executableName = executableName.split("\x00\x00")[0]
        self.executableName = executableName.replace("\x00", "")
        # File Path Hash Value
        self.rawhash = struct.unpack_from("I", infile.read(4))[0]

    def fileInformation(self, infile):

        # UnKnown0
        unknown0 = infile.read(4)
        # SectionInfoOffset
        self.metricsOffset = struct.unpack_from("I", infile.read(4))[0]
        # NumSections
        self.metricsCount = struct.unpack_from("I", infile.read(4))[0]
        # PageInfoOffset
        self.traceChainOffset = struct.unpack_from("I", infile.read(4))[0]
        # NumPages
        self.traceChainCount = struct.unpack_from("I", infile.read(4))[0]
        # FileNameInfoOffset
        self.filenameStringsOffset = struct.unpack_from("I", infile.read(4))[0]
        # FileNameInfoSize
        self.filenameStringsSize = struct.unpack_from("I", infile.read(4))[0]
        # MetadataInfoOffset
        self.volumesInformationOffset = struct.unpack_from("I", infile.read(4))[0]
        # NumMetadataRecords
        self.volumesCount = struct.unpack_from("I", infile.read(4))[0]
        # MetadataInfoSize
        self.volumesInformationSize = struct.unpack_from("I", infile.read(4))[0]
        # UnKnown1(8byte)
        unknown1 = infile.read(8)
        # LastLaunchTime1~8
        self.lastRunTime = infile.read(64)
        # UnKnown2 (8byte)
        unknown2 = infile.read(8)
        # NumLaunches
        self.NumLaunches = struct.unpack_from("I", infile.read(4))[0]


    def metricsArray(self, infile):
        # File Metrics Array
        # 32 bytes per array, not parsed in this script
        infile.seek(self.metricsOffset)
        unknown0 = infile.read(4)
        unknown1 = infile.read(4)
        unknown2 = infile.read(4)
        self.filenameOffset = struct.unpack_from("I", infile.read(4))[0]
        self.filenameLength = struct.unpack_from("I", infile.read(4))[0]
        self.flag = struct.unpack_from("I", infile.read(4))[0]
        self.mftRecordNumber = self.convertFileReference(infile.read(6))
        self.mftSeqNumber = struct.unpack_from("H", infile.read(2))[0]

    def traceChainsArray(self, infile):
        # Trace Chains Array
        # Read though, not being parsed for information
        # 8 bytes
        infile.read(8)

    def volumeInformation(self, infile):
        # Volumes Information
        # 96 bytes

        infile.seek(self.volumesInformationOffset)
        self.volumesInformationArray = []
        self.directoryStringsArray = []

        count = 0
        while count < self.volumesCount:
            self.volPathOffset = struct.unpack_from("I", infile.read(4))[0]
            self.volPathLength = struct.unpack_from("I", infile.read(4))[0]
            self.volCreationTime = struct.unpack_from("Q", infile.read(8))[0]
            self.volSerialNumber = hex(struct.unpack_from("I", infile.read(4))[0])
            self.volSerialNumber = self.volSerialNumber.rstrip("L").lstrip("0x")
            self.fileRefOffset = struct.unpack_from("I", infile.read(4))[0]
            self.fileRefCount = struct.unpack_from("I", infile.read(4))[0]
            self.dirStringsOffset = struct.unpack_from("I", infile.read(4))[0]
            self.dirStringsCount = struct.unpack_from("I", infile.read(4))[0]
            unknown0 = infile.read(60)

            self.directoryStringsArray.append(self.directoryStrings(infile))

            infile.seek(self.volumesInformationOffset + self.volPathOffset)
            volume = {}
            volume["Volume Name"] = infile.read(self.volPathLength * 2).decode().replace("\x00", "")
            volume["Creation Date"] = self.convertTimestamp(self.volCreationTime)
            volume["Serial Number"] = self.volSerialNumber
            self.volumesInformationArray.append(volume)

            count += 1
            infile.seek(self.volumesInformationOffset + (96 * count))

    def getFilenameStrings(self, infile):
        # Parses filename strings from the PF file
        self.resources = []
        infile.seek(self.filenameStringsOffset)
        self.filenames = infile.read(self.filenameStringsSize)

        for i in self.filenames.decode('UTF-16').split("\x00"):
            self.resources.append(i)


    def convertTimestamp(self, timestamp):
        # Timestamp is a Win32 FILETIME value
        # This function returns that value in a human-readable format
        #return str(datetime(1601, 1, 1) + timedelta(microseconds=timestamp / 10.)).split(".")[0]
        return str(datetime(1601, 1, 1) + timedelta(microseconds=timestamp / 10.)).split(".")[0]


    def getTimeStamps(self, lastRunTime):
        self.timestamps = ['' for i in range(8)]
        self.timestamps1 = []

        start = 0
        end = 8
        while end <= len(lastRunTime):
            timestamp = struct.unpack_from("Q", lastRunTime[start:end])[0]
            if timestamp:
                self.timestamps1.append(self.convertTimestamp(timestamp))
                start += 8
                end += 8
            else:
                break

        for i in range(8):
            try:
                self.timestamps[i] = self.timestamps1[i]
            except:
                pass


    def directoryStrings(self, infile):
        infile.seek(self.volumesInformationOffset)
        infile.seek(self.dirStringsOffset, 1)

        directoryStrings = []

        count = 0
        while count < self.dirStringsCount:
            stringLength = struct.unpack_from("<H", infile.read(2))[0] * 2
            directoryString = infile.read(stringLength).decode('utf-16').replace("\x00", "")
            infile.read(2)  # Read through the end-of-string null byte
            directoryStrings.append(directoryString)
            count += 1

        return directoryStrings

    def convertFileReference(self, buf):
        # byteArray = list(map(lambda x: '%02x' % ord(x), buf))
        byteArray = list(map(lambda x: '%02x' % x, buf))
        # byteArray1 = buf
        byteString = ""
        for i in byteArray[::-1]:
            byteString += i

        return int(byteString, 16)


    def filepath(self, infile):
        infile.seek(self.filenameStringsOffset+self.filenameStringsSize)
        size = self.volumesInformationOffset-self.filenameStringsOffset-self.filenameStringsSize
        try:
            self.path = infile.read(size).decode('utf-16').split("\x00")[0]
        except:
            pass


    def output(self):
        data_list1_1 = [self.executableName, self.path, self.NumLaunches]
        data_list1_2 = []

        for i in range(0, 8):
            try:
                data_list1_2.append(self.timestamps[i])
            except:
                pass

        second_data_list1.append(data_list1_1+data_list1_2)

        for i in self.resources:
            data_list2 = [i.split("\\")[-1], i]
            second_data_list2.append(data_list2)

class DecompressWin10(object):
    def __init__(self):
        pass

    def tohex(self, val, nbits):
        """Utility to convert (signed) integer to hex."""
        return hex((val + (1 << nbits)) % (1 << nbits))

    def decompress(self, infile):
        """Utility core."""

        NULL = ctypes.POINTER(ctypes.c_uint)()
        SIZE_T = ctypes.c_uint
        DWORD = ctypes.c_uint32
        USHORT = ctypes.c_uint16
        UCHAR = ctypes.c_ubyte
        ULONG = ctypes.c_uint32

        # You must have at least Windows 8, or it should fail.
        try:
            RtlDecompressBufferEx = ctypes.windll.ntdll.RtlDecompressBufferEx
        except AttributeError as e:
            sys.exit("[ - ] {}".format(e) + \
                     "\n[ - ] Windows 8+ required for this script to decompress Win10 Prefetch files")

        RtlGetCompressionWorkSpaceSize = \
            ctypes.windll.ntdll.RtlGetCompressionWorkSpaceSize

        with open(infile, 'rb') as fin:
            header = fin.read(8)
            compressed = fin.read()

            signature, decompressed_size = struct.unpack('<LL', header)
            calgo = (signature & 0x0F000000) >> 24
            crcck = (signature & 0xF0000000) >> 28
            magic = signature & 0x00FFFFFF
            if magic != 0x004d414d:
                sys.exit('Wrong signature... wrong file?')

            if crcck:
                # I could have used RtlComputeCrc32.
                file_crc = struct.unpack('<L', compressed[:4])[0]
                crc = binascii.crc32(header)
                crc = binascii.crc32(struct.pack('<L', 0), crc)
                compressed = compressed[4:]
                crc = binascii.crc32(compressed, crc)
                if crc != file_crc:
                    sys.exit('{} Wrong file CRC {0:x} - {1:x}!'.format(infile, crc, file_crc))

            compressed_size = len(compressed)

            ntCompressBufferWorkSpaceSize = ULONG()
            ntCompressFragmentWorkSpaceSize = ULONG()

            ntstatus = RtlGetCompressionWorkSpaceSize(USHORT(calgo),
                                                      ctypes.byref(ntCompressBufferWorkSpaceSize),
                                                      ctypes.byref(ntCompressFragmentWorkSpaceSize))

            if ntstatus:
                sys.exit('Cannot get workspace size, err: {}'.format(
                    self.tohex(ntstatus, 32)))

            ntCompressed = (UCHAR * compressed_size).from_buffer_copy(compressed)
            ntDecompressed = (UCHAR * decompressed_size)()
            ntFinalUncompressedSize = ULONG()
            ntWorkspace = (UCHAR * ntCompressFragmentWorkSpaceSize.value)()

            ntstatus = RtlDecompressBufferEx(
                USHORT(calgo),
                ctypes.byref(ntDecompressed),
                ULONG(decompressed_size),
                ctypes.byref(ntCompressed),
                ULONG(compressed_size),
                ctypes.byref(ntFinalUncompressedSize),
                ctypes.byref(ntWorkspace))

            if ntstatus:
                sys.exit('Decompression failed, err: {}'.format((ntstatus, 32)))

            if ntFinalUncompressedSize.value != decompressed_size:
                sys.exit('Decompressed with a different size than original!')

        return bytearray(ntDecompressed)

#Execute
def main():
    for i in file_list:
        if i.endswith(".pf"):
            Prefetch(path_dir + i)
        else:
            pass

    Database.Prefetch_Database(second_data_list1, second_data_list2)

if __name__ == '__main__':
    main()
