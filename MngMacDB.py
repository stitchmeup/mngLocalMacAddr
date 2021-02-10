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

    def __init__(self, database):
        sqlite3.Connection.__init__(self, database)
        self._database = database
        self._cur = self.cursor()
        # % Matches any in SQL WHERE condition
        self._mac = '%'
        self._hostname = '%'
        self._tables = []
        self.set_Tables()

    def get_database(self):
        return self._database

    def get_cur(self):
        return self._cur

    def get_mac(self):
        return self._mac

    def get_hostname(self):
        return self._hostname

    def get_tables(self):
        return self._tables

    def set_database(self, database):
        " Connect to a new database and set a new cursor "
        self.close()
        sqlite3.Connection.__init__(self, database)
        self._database = database
        self._cur = self.cursor()

    def set_mac(self, mac):
        " Set mac from a GenMacAddr instance or if None provide set it to '%' "
        if mac is None:
            self._mac = '%'
        elif isinstance(mac, GenMacAddr):
            if not mac.isEmpty():
                self._mac = mac.toString()
            else:
                raise ValueError(mac, "mac address is empty")
        else:
            raise TypeError(mac, "mac address is not an instance of GenMacAddr")

    def set_hostname(self, hostname):
        " Set hostname, if provided hostname is None, set it to '%' "
        if hostname is None:
            self._hostname = '%'
        else:
            self._hostname = hostname

    def set_Tables(self):
        " Set _tables to a list of existing tables of in database "
        self._cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table';")
        # Not sure condition in the filtering under is needed
        self._tables = [
            table[0] for table in self._cur.fetchall()
            if table[0] != "sqlite_sequence"
            ]

    def tableExist(self, table):
        " Return True if table is in database "
        return True if table in self._tables else False

    # SELECT
    def select(self, table):
        if self.tableExist(table):
            query = 'SELECT * FROM {}'.format(table) + ' WHERE mac LIKE :mac AND hostname LIKE :hostname;'
            self._cur.execute(query, { "mac": self._mac, "hostname": self._hostname })
            return self._cur.fetchall()
        else:
            raise ValueError(table, " does not exist in databse.")

if __name__ == '__main__':
    mngMacDB = MngMacDB('mac.db')
    # ['vbox', 'any']
    print(mngMacDB.get_tables())
    # false
    print(mngMacDB.tableExist('ay'))
    # dump table any
    print(mngMacDB.select('any'))
    macAddr = GenMacAddr(None)
    macAddr.set_addr({"vendorId": [0x32, 0x5D, 0xB9], "serialId": [0x49, 0x1B, 0x5E]})
    mngMacDB.set_mac(macAddr)
    # [('325DB9491B5E', 'host1')]
    print(mngMacDB.select('any'))
    mngMacDB.set_mac(None)
    mngMacDB.set_hostname('host 2')
    # [('2A523B85189F', 'host 2'), ('86A1EC0CB254', 'host 2')]
    print(mngMacDB.select('any'))
