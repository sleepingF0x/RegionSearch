import io
import struct

from ..lookup import RegionLookup, RegionLookupFactory


class PhoneLookup(RegionLookup):
    def __init__(self, dat_file):
        with open(dat_file, 'rb') as f:
            self.buf = f.read()

        self.head_fmt = "<4sI"
        self.idx_fmt = "<II"
        self.head_fmt_length = struct.calcsize(self.head_fmt)
        self.idx_fmt_length = struct.calcsize(self.idx_fmt)
        self.version, self.first_phone_idx_offset = struct.unpack(self.head_fmt, self.buf[:self.head_fmt_length])
        self.idx_record_count = (len(self.buf) - self.first_phone_idx_offset) // self.idx_fmt_length

    def get_dat_msg(self):
        print("版本号:{}".format(self.version.decode("utf8")))
        print("总记录条数:{}".format(self.idx_record_count))
        print("内存占用:{:.2f}MB".format(len(self.buf) / 1024 / 1024))

    @staticmethod
    def _format_phone_content(phone_num, record_content):
        province, city, isp = record_content.split('|')
        return {
            "phone": phone_num,
            "province": province,
            "city": city,
            "isp": isp,
        }

    @staticmethod
    def _get_record_content(buf, start_offset):
        end_offset = buf.find(b'\x00', start_offset)
        return buf[start_offset:end_offset].decode()

    def _lookup_phone(self, phone_num):
        phone_num = str(phone_num)
        assert 7 <= len(phone_num) <= 11
        int_phone = int(str(phone_num)[0:7])

        left = 0
        right = self.idx_record_count
        buf_len = len(self.buf)
        while left <= right:
            middle = (left + right) // 2
            current_offset = (self.first_phone_idx_offset + middle * self.idx_fmt_length)
            if current_offset >= buf_len:
                return

            buffer = self.buf[current_offset: current_offset + self.idx_fmt_length]
            cur_phone, record_offset = struct.unpack(self.idx_fmt, buffer)

            if cur_phone > int_phone:
                right = middle - 1
            elif cur_phone < int_phone:
                left = middle + 1
            else:
                record_content = self._get_record_content(self.buf, record_offset)
                return self._format_phone_content(phone_num, record_content)

    def lookup(self, phone_number):
        return self._lookup_phone(phone_number)

    @staticmethod
    def csv2dat(csv_path, columns, csv_version, dat_path="phone.dat"):
        import pandas as pd

        df = pd.read_csv(csv_path, usecols=columns.keys())
        df = df.rename(columns=columns)
        df['phone'] = df['phone'].astype('uint32')

        df['region'] = df.apply(lambda x: '|'.join([x['province'], x['city'], x['isp']]), axis=1)
        df = df[['phone', 'region']].sort_values(by='phone')

        head_buffer = io.BytesIO()
        data_buffer = io.BytesIO()
        index_buffer = io.BytesIO()

        header_length = 8
        data_offset = header_length
        index_offset = header_length

        for row in df.itertuples():
            bin_data = row.region.encode('utf-8') + '\0'.encode('utf-8')
            data_buffer.write(bin_data)

            index_data = struct.pack('II', row.phone, data_offset)
            index_buffer.write(index_data)

            data_offset += len(bin_data)
            index_offset += len(index_data)

        head_data = struct.pack('4sI', csv_version.encode("utf8"), data_offset)
        head_buffer.write(head_data)

        with open(dat_path, 'wb') as combined_file:
            combined_file.write(head_buffer.getvalue())
            combined_file.write(data_buffer.getvalue())
            combined_file.write(index_buffer.getvalue())


class PhoneRegionLookupFactory(RegionLookupFactory):
    def create_region_lookup(self, db_path):
        return PhoneLookup(db_path)
