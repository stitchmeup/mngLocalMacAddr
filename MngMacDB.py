#!/usr/bin/env python3

# API to mac address sqlite3 DB
# SELECT, INSERT, DELETE

import sqlite3
from GenMacAddr import GenMacAddr


class MngMacDB(sqlite3.Connection):
    """
    Management of Mac Addresses Database
    Inherit sqlite3.Connection
    """

    def __init__(self, database, mac, hostname, tables):
        sqlite3.Connection.__init__(self, database)
        self.cur = self.cursor()

        # Tables
        # define available tables in database
        self.cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table';")
        res = self.cur.fetchall()
        self.tables = [
            table[0] for table in res
            if table[0] != "sqlite_sequence"
            ]
        for table in tables:
            if table in self.tables:
                self.tables.append(table)
        if not self.tables:
            raise ValueError(tables + "not found.")

        # MAC address
        if isinstance(mac, GenMacAddr):
            if mac.isEmpty():
                self.mac = '%'
            elif GenMacAddr.isValidMacStr(mac.toString()):
                self.mac = GenMacAddr.toString()



        # hostname
        if hostname is None:
            self.hostname = '%'
        else:
            self.hostname = hostname

        # SELECT
        def select(self):
            self.cur.excute(
                "SELECT * from :table WHERE mac LIKE \
                 :mac AND hostname LIKE :hostname",
                {
                    "table": ','.join(self.tables),
                    "mac": self.mac,
                    "hostname": self.hostname
                })
            return self.cur.fetchall()

if __name__ == '__main__':
