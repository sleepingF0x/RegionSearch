# coding:utf-8

import logging
import threading
from contextlib import contextmanager

import pymysql
from DBUtils.PooledDB import PooledDB


class DBPool(object):
    _instance_lock = threading.Lock()
    _instance = {}

    def __new__(cls, *args, **kwargs):
        with DBPool._instance_lock:
            host = kwargs.get("host", "127.0.0.1").replace("localhost", "127.0.0.1")
            port = kwargs.get("port", 3306)
            db_name = kwargs.get("database")
            instance_key = host + str(port) + db_name
            if instance_key not in cls._instance:
                cls._instance[instance_key] = super().__new__(cls)
            return cls._instance[instance_key]

    def __init__(self, max_conn=10, **db_conf):
        self.pool = PooledDB(pymysql, failures=pymysql.MySQLError, **db_conf, maxconnections=max_conn, blocking=True,
                             cursorclass=pymysql.cursors.SSDictCursor)

    @contextmanager
    def db_session(self):
        conn = cur = None
        try:
            conn = self.pool.connection()
            cur = conn.cursor()
            yield cur
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            logging.warning("db error %s", e)
            raise e
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
