# -*- coding: utf-8 -*-
import os
import datetime
import re
import struct
import shutil
import pytz
import Database

cache_data_list=[]
cache_data_list_2=[]

def change_last_modified_time(str):
    before_change = str.split(' ', maxsplit=6)
    month = {
        'Jan': '01',
        'Feb': '02',
        'Mar': '03',
        'Apr': '04',
        'May': '05',
        'Jun': '06',
        'Jul': '07',
        'Aug': '08',
        'Sep': '09',
        'Oct': '10',
        'Nov': '11',
        'Dec': '12'
    }

    if before_change[2] in list(month.keys()):
        time_friendly = month[before_change[2]]
    elif before_change[2] is None:
        time_friendly = None
    else:
        time_friendly = '[Error - Unknown Danger Code]'

    after_change = before_change[3] + "-" + time_friendly + "-" + before_change[1] + " " + before_change[4]

    return after_change

def to_datetime(timestamp, timezone=None):
    """Convert a variety of timestamp formats to a datetime object."""

    try:
        if isinstance(timestamp, datetime.datetime):
            return timestamp
        try:
            timestamp = float(timestamp)
        except:
            timestamp = 0

        if 13700000000000000 > timestamp > 12000000000000000:  # 2035 > ts > 1981
            # Webkit
            new_timestamp = datetime.datetime.utcfromtimestamp((float(timestamp) / 1000000) - 11644473600)
        elif 1900000000000 > timestamp > 2000000000:  # 2030 > ts > 1970
            # Epoch milliseconds
            new_timestamp = datetime.datetime.utcfromtimestamp(float(timestamp) / 1000)
        elif 1900000000 > timestamp >= 0:  # 2030 > ts > 1970
            # Epoch
            new_timestamp = datetime.datetime.utcfromtimestamp(float(timestamp))
        else:
            new_timestamp = datetime.datetime.utcfromtimestamp(0)

        if timezone is not None:
            try:
                return new_timestamp.replace(tzinfo=pytz.utc).astimezone(timezone)
            except NameError:
                return new_timestamp
        else:
            return new_timestamp
    except Exception as e:
        print(e)

class CacheAddressError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class CacheAddress():
    """
    Object representing a Chrome Cache Address
    """
    SEPARATE_FILE = 0
    RANKING_BLOCK = 1
    BLOCK_256 = 2
    BLOCK_1024 = 3
    BLOCK_4096 = 4

    typeArray = [("Separate file", 0),
                 ("Ranking block file", 36),
                 ("256 bytes block file", 256),
                 ("1k bytes block file", 1024),
                 ("4k bytes block file", 4096)]

    def __init__(self, uint_32, path):
        """
        Parse the 32 bits of the uint_32
        """
        if uint_32 == 0:
            raise CacheAddressError("Null Address")

        #XXX Is self.binary useful ??
        self.addr = uint_32
        self.path = path

        # Checking that the MSB is set
        self.binary = bin(uint_32)
        if len(self.binary) != 34:
            raise CacheAddressError("Uninitialized Address")

        self.blockType = int(self.binary[3:6], 2)

        # If it is an address of a separate file
        if self.blockType == CacheAddress.SEPARATE_FILE:
            self.fileSelector = "f_%06x" % int(self.binary[6:], 2)
        elif self.blockType == CacheAddress.RANKING_BLOCK:
            self.fileSelector = "data_" + str(int(self.binary[10:18], 2))
        else:
            self.entrySize = CacheAddress.typeArray[self.blockType][1]
            self.contiguousBlock = int(self.binary[8:10], 2)
            self.fileSelector = "data_" + str(int(self.binary[10:18], 2))
            self.blockNumber = int(self.binary[18:], 2)

    def __str__(self):
        string = hex(self.addr) + " ("
        if self.blockType >= CacheAddress.BLOCK_256:
            string += str(self.contiguousBlock) + \
                      " contiguous blocks in "
        string += CacheAddress.typeArray[self.blockType][0] + \
                  " : " + self.fileSelector + ")"
        return string


class CacheData:
    """
    Retrieve data at the given address
    Can save it to a separate file for export
    """

    HTTP_HEADER = 0
    UNKNOWN = 1

    def __init__(self, address, size, isHTTPHeader=False):
        """
        It is a lazy evaluation object : the file is open only if it is
        needed. It can parse the HTTP header if asked to do so.
        See net/http/http_util.cc LocateStartOfStatusLine and
        LocateEndOfHeaders for details.
        """
        self.size = size
        self.address = address
        self.type = CacheData.UNKNOWN

        if isHTTPHeader and self.address.blockType != CacheAddress.SEPARATE_FILE:
            # Getting raw data
            block_bytes = b''
            block = open(os.path.join(self.address.path, self.address.fileSelector), 'rb')

            # Offset in file
            self.offset = 8192 + self.address.blockNumber*self.address.entrySize
            block.seek(self.offset)
            for _ in range(self.size):
                block_bytes += struct.unpack('c', block.read(1))[0]
            block.close()

            # Finding the beginning of the request
            start = re.search(b'HTTP', block_bytes)
            if start is None:
                return
            else:
                block_bytes = block_bytes[start.start():]

            # Finding the end (some null characters : verified by experience)
            end = re.search(b'\x00\x00', block_bytes)
            if end is None:
                return
            else:
                block_bytes = block_bytes[:end.end()-2]

            # Creating the dictionary of headers
            self.headers = {}
            for line in block_bytes.split(b'\0'):
                stripped = line.split(b':')
                self.headers[stripped[0].lower()] = \
                    b':'.join(stripped[1:]).strip()
            self.type = CacheData.HTTP_HEADER

    def save(self, filename=None):
        """Save the data to the specified filename"""
        if self.address.blockType == CacheAddress.SEPARATE_FILE:
            shutil.copy(self.address.path + self.address.fileSelector,
                        filename)
        else:
            output = open(filename, 'wB')
            block = open(self.address.path + self.address.fileSelector, 'rb')
            block.seek(8192 + self.address.blockNumber*self.address.entrySize)
            output.write(block.read(self.size))
            block.close()
            output.close()

    def data(self):
        """Returns a string representing the data"""
        try:
            block = open(os.path.join(self.address.path, self.address.fileSelector), 'rb')
            block.seek(8192 + self.address.blockNumber*self.address.entrySize)
            data = block.read(self.size).decode('utf-8', errors="replace")
            block.close()
        except:
            data = "<error>"
        return data

    def __str__(self):
        """
        Display the type of cacheData
        """
        if self.type == CacheData.HTTP_HEADER:
            if 'content-type' in self.headers:
                return "HTTP Header %s" % self.headers['content-type']
            else:
                return "HTTP Header"
        else:
            return "Data"

class CacheBlock:
    """
    Object representing a block of the cache. It can be the index file or any
    other block type : 256B, 1024B, 4096B, Ranking Block.
    See /net/disk_cache/disk_format.h for details.
    """

    INDEX_MAGIC = 0xC103CAC3
    BLOCK_MAGIC = 0xC104CAC3
    INDEX = 0
    BLOCK = 1

    def __init__(self, filename):
        """
        Parse the header of a cache file
        """
        header = open(filename, 'rb')

        # Read Magic Number
        magic = struct.unpack('I', header.read(4))[0]
        if magic == CacheBlock.BLOCK_MAGIC:
            self.type = CacheBlock.BLOCK
            header.seek(2, 1)
            self.version = struct.unpack('h', header.read(2))[0]
            self.header = struct.unpack('h', header.read(2))[0]
            self.nextFile = struct.unpack('h', header.read(2))[0]
            self.blockSize = struct.unpack('I', header.read(4))[0]
            self.entryCount = struct.unpack('I', header.read(4))[0]
            self.entryMax = struct.unpack('I', header.read(4))[0]
            self.empty = []
            for _ in range(4):
                self.empty.append(struct.unpack('I', header.read(4))[0])
            self.position = []
            for _ in range(4):
                self.position.append(struct.unpack('I', header.read(4))[0])
        elif magic == CacheBlock.INDEX_MAGIC:
            self.type = CacheBlock.INDEX
            header.seek(2, 1)
            self.version = struct.unpack('h', header.read(2))[0]
            self.entryCount = struct.unpack('I', header.read(4))[0]
            self.byteCount = struct.unpack('I', header.read(4))[0]
            self.lastFileCreated = "f_%06x" % struct.unpack('I', header.read(4))[0]
            header.seek(4*2, 1)
            self.tableSize = struct.unpack('I', header.read(4))[0]
        else:
            header.close()
            raise Exception("Invalid Chrome Cache File")
        header.close()

class CacheEntry():
    """
    See /net/disk_cache/disk_format.h for details.
    """

    STATE = ["Normal (data cached)",
             "Evicted (data deleted)",
             "Doomed (data to be deleted)"]

    def __init__(self, address, row_type, timezone):
        """
        Parse a Chrome Cache Entry at the given address
        """
        self.httpHeader = None
        self.http_headers_dict = None
        self.timezone = timezone
        block = open(os.path.join(address.path, address.fileSelector), 'rb')

        # Going to the right entry
        block.seek(8192 + address.blockNumber*address.entrySize)

        # Parsing basic fields
        self.hash = struct.unpack('I', block.read(4))[0]
        self.next = struct.unpack('I', block.read(4))[0]
        self.rankingNode = struct.unpack('I', block.read(4))[0]
        self.usageCounter = struct.unpack('I', block.read(4))[0]
        self.reuseCounter = struct.unpack('I', block.read(4))[0]
        self.state = struct.unpack('I', block.read(4))[0]
        self.creationTime = to_datetime(struct.unpack('Q', block.read(8))[0], self.timezone)
        self.keyLength = struct.unpack('I', block.read(4))[0]
        self.keyAddress = struct.unpack('I', block.read(4))[0]

        dataSize = []
        for _ in range(4):
            dataSize.append(struct.unpack('I', block.read(4))[0])

        self.data = []
        for index in range(4):
            addr = struct.unpack('I', block.read(4))[0]
            try:
                addr = CacheAddress(addr, address.path)
                self.data.append(CacheData(addr, dataSize[index], True))
            except CacheAddressError:
                pass

        # Find the HTTP header if there is one
        for data in self.data:
            if data.type == CacheData.HTTP_HEADER:
                self.httpHeader = data
                header_dict = {}
                for header in data.__dict__['headers']:
                    try:
                        header_dict[header.decode('utf-8')] = data.__dict__['headers'][header].decode('utf-8')
                    except:
                        pass
                self.http_headers_dict = header_dict

        self.flags = struct.unpack('I', block.read(4))[0]

        # Skipping pad
        block.seek(5*4, 1)

        # Reading local key
        if self.keyAddress == 0:
            self.key = block.read(self.keyLength).decode('ascii')
        # Key stored elsewhere
        else:
            addr = CacheAddress(self.keyAddress, address.path)

            # It is probably an HTTP header
            self.key = CacheData(addr, self.keyLength, True)

        block.close()

        # Hindsight HistoryItem fields
        self.timestamp = self.creationTime
        self.name = CacheEntry.STATE[self.state]
        self.url = self.keyToStr()
        self.value = ""
        self.etag = ""
        self.server_name = ""
        self.last_modified = ""
        self.file_size = 0
        self.location = ""
        for _ in self.data:
            if _.type != 0:
                self.file_size += _.size
                # Check if we already have an address here; if so, add a text separator
                if len(self.location) > 0:
                    self.location += "; "
                if _.address.blockType == 0:
                    self.location += "{}".format(_.address.fileSelector)
                else:
                    self.location += "{} [{}]".format(_.address.fileSelector, _.offset)

        self.http_headers_str = ""
        if self.http_headers_dict is not None:
            if self.state == 0:
                self.value = "{} ({} bytes)".format(self.http_headers_dict.get('content-type'), self.file_size)
            self.server_name = self.http_headers_dict.get('server')
            self.etag = self.http_headers_dict.get('etag')
            self.last_modified = self.http_headers_dict.get('last-modified')

            for key, value in self.http_headers_dict.items():
                if key and value:
                    self.http_headers_str += "{}: {}\n".format(key, value)
                elif key:
                    self.http_headers_str += "{}\n".format(key)
            self.http_headers_str = self.http_headers_str.rstrip()

            def change_form(timestamp):
                new_form=timestamp.split(".", 2)
                return new_form[0]

            if self.last_modified is None:
                cache_data_list=[row_type, change_form(str(self.timestamp)), self.url, self.name, self.value, self.etag,
                     self.last_modified, self.server_name, self.location,
                     self.http_headers_str]
                cache_data_list_2.append(cache_data_list)
            else:
                cache_data_list=[row_type, change_form(str(self.timestamp)), self.url, self.name, self.value, self.etag,
                     change_last_modified_time(self.last_modified), self.server_name, self.location,
                     self.http_headers_str]
                cache_data_list_2.append(cache_data_list)


    def keyToStr(self):
        """
        Since the key can be a string or a CacheData object, this function is an
        utility to display the content of the key whatever type is it.
        """
        if self.keyAddress == 0:
            return self.key
        else:
            return self.key.data()

    def __str__(self):

        string = "Hash: 0x%08x" % self.hash + '\n'
        if self.__next__ != 0:
            string += "Next: 0x%08x" % self.next + '\n'
        string += "Usage Counter: %d" % self.usageCounter + '\n' \
                                                            "Reuse Counter: %d" % self.reuseCounter + '\n' \
                                                                                                      "Creation Time: %s" % self.creationTime + '\n'
        if self.keyAddress != 0:
            string += "Key Address: 0x%08x" % self.keyAddress + '\n'
        string += "Key: %s" % self.key + '\n'
        if self.flags != 0:
            string += "Flags: 0x%08x" % self.flags + '\n'
        string += "State: %s" % CacheEntry.STATE[self.state]
        for data in self.data:
            string += "\nData (%d bytes) at 0x%08x : %s" % (data.size,
                                                            data.address.addr,
                                                            data)
        return string


def get_cache(self, dir_name, row_type=None):
    """
    read the index file to walk whole cache // from cacheParse.py

    Reads the whole cache and store the collected data in a table
    or find out if the given list of urls is in the cache. If yes it
    return a list of the corresponding entries.
    """

    # Set up empty return array
    results = []

    if dir_name == 'Cache':
        path = os.path.join('COPY\\BROWSER\\Cache', dir_name)
    elif dir_name =='GPUCache':
        path = os.path.join('COPY\\BROWSER\\GPUCache', dir_name)

    cacheBlock = CacheBlock(os.path.join(path, 'index'))

    index = open(os.path.join(path, 'index'), 'rb')

    # Skipping Header
    index.seek(92 * 4)

    for key in range(cacheBlock.tableSize):
        raw = struct.unpack('I', index.read(4))[0]
        if raw != 0:
            entry = CacheEntry(CacheAddress(raw, path=path), 'Cache', pytz.timezone('UTC'))
            # Add the new row to the results array
            results.append(entry)

            # Checking if there is a next item in the bucket because
            # such entries are not stored in the Index File so they will
            # be ignored during iterative lookup in the hash table
            while entry.next != 0:
                entry = CacheEntry(CacheAddress(entry.next, path=path),
                                   'Cache', pytz.timezone('UTC'))


    Database.cache_db_insert(cache_data_list_2)

    index.close()