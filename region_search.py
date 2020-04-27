import re
import socket
import struct

import redis

from config import *
from db_pool import DBPool

regex_phone = re.compile(r"1[3-9]\d{9}")
regex_ipv4_address = re.compile(
    '^(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$')


class PhoneRegion(object):
    """search region from mysql"""
    _instance = None
    db = DBPool(**DATABASE_CONFIG["public"])

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def lookup(cls, phone):
        if regex_phone.match(phone):
            with cls.db.db_session() as session:
                session.execute("SELECT province, city, isp FROM phone WHERE phone=LEFT( %(phone)s, 7)",
                                {"phone": phone})
                return session.fetchone()


class IPRegion(object):
    """search region from mysql"""
    _instance = None
    db = DBPool(**DATABASE_CONFIG["public"])

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def lookup(cls, ip):
        if regex_ipv4_address.match(ip):
            with cls.db.db_session() as session:
                session.execute("SELECT country, province, city, district, isp FROM ip "
                                "WHERE INET_ATON( %(ip)s ) BETWEEN ip_start_num AND ip_end_num LIMIT 1", {"ip": ip})
                return session.fetchone()


class PhoneRegionRedis(object):
    """search region from redis"""
    _instance = None
    pool = redis.ConnectionPool(**REDIS_CONFIG, decode_responses=True)
    rds_cli = redis.Redis(connection_pool=pool)

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def import_db(cls, db_config):
        db = DBPool(**db_config)
        with cls.rds_cli.pipeline(transaction=False) as pipe:
            with db.db_session() as session:
                session.execute("SELECT phone, CONCAT_WS('|', province, city, isp) `value` FROM `phone`")
                while True:
                    ret = session.fetchone()
                    if ret:
                        pipe.hset("phone", ret["phone"], ret["value"])
                    else:
                        break
            pipe.execute()

    @classmethod
    def lookup(cls, phone):
        if regex_phone.match(phone):
            r = cls.rds_cli.hget("phone", phone[:7])
            if r:
                r = r.split("|")
                if r:
                    return {"province": r[0], "city": r[1], "isp": r[2]}


class IPRegionRedis(object):
    """search region from redis"""
    _instance = None
    pool = redis.ConnectionPool(**REDIS_CONFIG, decode_responses=True)
    rds_cli = redis.Redis(connection_pool=pool)

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def import_db(cls, db_config):
        db = DBPool(**db_config)
        with cls.rds_cli.pipeline(transaction=False) as pipe:
            with db.db_session() as session:
                session.execute(
                    "SELECT ip_start_num, CONCAT_WS('|',ip_start_num, country, province, city, district, isp) `key` "
                    "FROM ip ORDER BY ip_start_num")
                while True:
                    ret = session.fetchone()
                    if ret:
                        pipe.zadd("ip", {ret["key"]: ret["ip_start_num"]})
                    else:
                        break
            pipe.execute()

    @staticmethod
    def ip_to_long(ip):
        _ip = socket.inet_aton(ip)
        return struct.unpack("!L", _ip)[0]

    @classmethod
    def lookup(cls, ip):
        if regex_ipv4_address.match(ip):
            ip_num = cls.ip_to_long(ip)
            r = cls.rds_cli.zrevrangebyscore("ip", ip_num, "-inf", 0, 1)
            if r:
                r = r[0].split("|")
                if r:
                    return {"country": r[1], "province": r[2], "city": r[3], "district": r[4], "isp": r[5]}


class PhoneRegionMem(object):
    """search region from RAM, 450155 records will cost about 372 MB"""
    _instance = None
    db = DBPool(**DATABASE_CONFIG["public"])

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.phone_regions = {}
        self._load_db()

    def _load_db(self):
        with self.db.db_session() as session:
            session.execute("SELECT phone, province, city, isp FROM `phone`")
            results = session.fetchall()
            for res in results:
                self.phone_regions.update(
                    {res["phone"]: {"province": res["province"], "city": res["city"], "isp": res["isp"]}})

    def lookup(self, phone):
        if regex_phone.match(phone):
            return self.phone_regions.get(phone[-11:-4], None)


class IPRegionMem(object):
    """search region from ram, 648831 records will cost about 458 MB"""
    _instance = None
    db = DBPool(**DATABASE_CONFIG["public"])

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.ip_regions = {}
        self.max_idx = 0
        self._load_db()

    def _load_db(self):
        with self.db.db_session() as session:
            session.execute("SELECT ip_start_num, country, province, city, district, isp FROM ip ORDER BY ip_start_num")
            self.ip_regions = session.fetchall()
            self.max_idx = len(self.ip_regions) - 1

    @staticmethod
    def ip_to_long(ip):
        _ip = socket.inet_aton(ip)
        return struct.unpack("!L", _ip)[0]

    def lookup(self, ip):
        if regex_ipv4_address.match(ip):
            ip_num = self.ip_to_long(ip)
            left = 0
            right = self.max_idx
            while left <= right:
                mid = left + (right - left) // 2
                if self.ip_regions[mid]["ip_start_num"] == ip_num:
                    break
                elif self.ip_regions[mid]["ip_start_num"] < ip_num:
                    left = mid + 1
                elif self.ip_regions[mid]["ip_start_num"] > ip_num:
                    right = mid - 1
            r = self.ip_regions[min(left, right)].copy()
            r.pop("ip_start_num")
            return r
