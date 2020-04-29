import io
import socket
import struct

from ..lookup import RegionLookup, RegionLookupFactory


class IPLookup(RegionLookup):
    def __init__(self, dat_file):
        with open(dat_file, 'rb') as f:
            self.buf = f.read()

        self.head_fmt = "<4sI"
        self.idx_fmt = "<II"
        self.head_fmt_length = struct.calcsize(self.head_fmt)
        self.idx_fmt_length = struct.calcsize(self.idx_fmt)
        self.version, self.first_ip_idx_offset = struct.unpack(self.head_fmt, self.buf[:self.head_fmt_length])
        self.idx_record_count = (len(self.buf) - self.first_ip_idx_offset) // self.idx_fmt_length

    def get_dat_msg(self):
        print("版本号:{}".format(self.version.decode("utf8")))
        print("总记录条数:{}".format(self.idx_record_count))
        print("内存占用:{:.2f}MB".format(len(self.buf) / 1024 / 1024))

    @staticmethod
    def _format_ip_content(ip_address, record_content):
        country, province, city, district, isp = record_content.split('|')
        return {
            "ip": ip_address,
            "country": country,
            "province": province,
            "city": city,
            "district": district,
            "isp": isp,
        }

    @staticmethod
    def _get_record_content(buf, start_offset):
        end_offset = buf.find(b'\x00', start_offset)
        return buf[start_offset:end_offset].decode()

    @staticmethod
    def _ip_to_long(ip):
        _ip = socket.inet_aton(ip)
        return struct.unpack("!L", _ip)[0]

    def _lookup_ip(self, ip_address):
        long_ip = self._ip_to_long(ip_address)

        left = 0
        right = self.idx_record_count

        buf_len = len(self.buf)
        while left <= right:
            middle = (left + right) // 2

            current_offset = (self.first_ip_idx_offset + middle * self.idx_fmt_length)
            if self.first_ip_idx_offset <= current_offset < buf_len:
                buffer = self.buf[current_offset: current_offset + self.idx_fmt_length]
                ip_start, record_offset = struct.unpack(self.idx_fmt, buffer)
                if ip_start > long_ip:
                    right = middle - 1
                elif ip_start < long_ip:
                    left = middle + 1
                else:
                    right = middle - 1
            else:
                break

        index = left - 1
        current_offset = (self.first_ip_idx_offset + index * self.idx_fmt_length)
        if self.first_ip_idx_offset <= current_offset < buf_len:
            buffer = self.buf[current_offset: current_offset + self.idx_fmt_length]
            ip_start, record_offset = struct.unpack(self.idx_fmt, buffer)
            record_content = self._get_record_content(self.buf, record_offset)
            return self._format_ip_content(ip_address, record_content)

    def lookup(self, phone_number):
        return self._lookup_ip(phone_number)

    @staticmethod
    def csv2dat(csv_path, columns, csv_version, dat_path="ip.dat"):
        import pandas as pd

        df = pd.read_csv(csv_path, usecols=columns.keys())
        df = df.rename(columns=columns)
        df['ip_start_num'] = df['ip_start_num'].astype('uint32')
        df[['country', 'province', 'city', 'district', 'isp']] = df[['country', 'province', 'city', 'district', 'isp']].fillna('')
        df['region'] = df.apply(lambda x: '|'.join([x['country'], x['province'], x['city'], x['district'], x['isp']]), axis=1)
        df = df[['ip_start_num', 'region']].sort_values(by='ip_start_num')

        head_buffer = io.BytesIO()
        data_buffer = io.BytesIO()
        index_buffer = io.BytesIO()

        header_length = 8
        data_offset = header_length
        index_offset = header_length

        for row in df.itertuples():
            bin_data = row.region.encode('utf-8') + '\0'.encode('utf-8')
            data_buffer.write(bin_data)

            index_data = struct.pack('II', row.ip_start_num, data_offset)
            index_buffer.write(index_data)

            data_offset += len(bin_data)
            index_offset += len(index_data)

        head_data = struct.pack('4sI', csv_version.encode("utf8"), data_offset)
        head_buffer.write(head_data)

        with open(dat_path, 'wb') as combined_file:
            combined_file.write(head_buffer.getvalue())
            combined_file.write(data_buffer.getvalue())
            combined_file.write(index_buffer.getvalue())


class IPRegionLookupFactory(RegionLookupFactory):
    def create_region_lookup(self, db_path):
        return IPLookup(db_path)
