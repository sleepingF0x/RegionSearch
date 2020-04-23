from db_pool import DBPool

from config import *

public_res_db = DBPool(**DATABASE_CONFIG["public"])


class PhoneRegion(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @staticmethod
    def lookup(phone):
        with public_res_db.db_session() as session:
            session.execute("SELECT province, city, isp FROM phone WHERE phone=LEFT( %(phone)s, 7)", {"phone": phone})
            return session.fetchone()


class IPRegion(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @staticmethod
    def lookup(ip):
        with public_res_db.db_session() as session:
            session.execute("SELECT country, province, city, district, isp FROM ip "
                            "WHERE INET_ATON( %(ip)s ) BETWEEN ip_start_num AND ip_end_num LIMIT 1", {"ip": ip})
            return session.fetchone()


PhoneRegionChecker = PhoneRegion()
IPRegionChecker = IPRegion()
