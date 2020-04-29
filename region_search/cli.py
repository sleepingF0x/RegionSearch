import argparse
import configparser

from region_search.ip.lookup import IPLookup
from region_search.phone.lookup import PhoneLookup


def dat_maker():
    parser = argparse.ArgumentParser(description='dat maker')

    parser.add_argument('--type', required=True, dest='type', choices=['ip', 'phone'], help='输出类型，可选的值为 "ip" 或 "phone"')
    parser.add_argument('--cfg', required=True, dest='cfg_path', action='store', help='配置文件ini路径')

    args = parser.parse_args()
    cfg_path = args.cfg_path

    config = configparser.ConfigParser()
    config.read(cfg_path)

    # 获取 CSV 文件路径
    csv_path = config.get('csv', 'path')
    # 获取输出 DAT 文件路径
    dat_path = config.get('output', 'dat_path')
    # 获取数据版本
    data_version = config.get('metadata', 'data_version')

    if args.type == 'ip':
        mapped_fields = {
            "ip_start_num": config.get('mapping', 'ip_start_num'),
            "country": config.get('mapping', 'country'),
            "province": config.get('mapping', 'province'),
            "city": config.get('mapping', 'city'),
            "district": config.get('mapping', 'district'),
            "isp": config.get('mapping', 'isp'),
        }
        IPLookup.csv2dat(csv_path, mapped_fields, data_version, dat_path)
    elif args.type == 'phone':
        mapped_fields = {
            "phone": config.get('mapping', 'phone'),
            "province": config.get('mapping', 'province'),
            "city": config.get('mapping', 'city'),
            "isp": config.get('mapping', 'isp'),
        }
        PhoneLookup.csv2dat(csv_path, mapped_fields, data_version, dat_path)
    else:
        print("unknown type")
