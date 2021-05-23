#!/usr/bin/env python3

# API to mac address sqlite3 DB
# SELECT, INSERT, DELETE

import sqlite3
from GenMacAddr import GenMacAddr
import re


class MngMacDB(sqlite3.Connection):
    """
    Management of Mac Addresses Database
    Inherit sqlite3.Connection
    """

    def __init__(self, database):
        super().__init__(database)
        self._database = database
        self._cur = self.cursor()
        # % Matches any in SQL WHERE condition
        self._mac = '%'
        self._hostname = '%'
        self._patternModes = {}
        self._patternModes["mac"] = True
        self._patternModes["hostname"] = True
        self._safeQuery = True
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

    def get_patternModes(self):
        return self._patternModes

    def get_safeQuery(self):
        return self._safeQuery

    def get_tables(self):
        return self._tables

    def set_database(self, database):
        " Connect to a new database and set a new cursor "
        self.close()
        super().__init__(database)
        self._database = database
        self._cur = self.cursor()

    def set_mac(self, mac, patternMode=False):
        """
        Set mac from a GenMacAddr instance
        if None:
            set it to '%' (turn pattern mode ON)
        if pattern mode is set:
            doesnt check for integrity and only select is allowed
        """
        self._patternModes["mac"] = patternMode
        if patternMode:
            self._mac = mac
        else:
            if mac is None:
                self._mac = '%'
                self._patternModes["mac"] = True
            elif isinstance(mac, GenMacAddr):
                if not mac.isEmpty():
                    self._mac = mac.toString()
                else:
                    raise ValueError(mac, "mac address is empty.")
            else:
                raise TypeError(mac,
                                " is not an instance of GenMacAddr class."
                                )

    def set_hostname(self, hostname, patternMode=False):
        """
        Set hostname from a valid hostname
        if None:
            set it to '%' (turn pattern mode ON)
        if pattern mode is set:
            doesnt check for integrity and only select is allowed
        """
        self._patternModes["hostname"] = patternMode
        if patternMode:
            self._hostname = hostname
        else:
            if hostname is None:
                self._hostname = '%'
                self._patternModes["hostname"] = True
            else:
                if self.__class__.isValidHostname(hostname):
                    self._hostname = hostname
                else:
                    raise ValueError(hostname + " is not valid.")

    def set_patternModes(self, patternModes):
        """
        Set pattern modes (True or False) for mac and hostname
        modes is a dictionnary with at least 1 property: mac or hostname
        """
        for key in patternModes:
            if key in self._patternModes:
                self._patternModes[key] = patternModes[key]
            else:
                raise ValueError(
                    key,
                    " invalid key.\
                    Only 'mac' or 'hostname' are allowed."
                )

    def set_safeQuery(self, isSafe=True):
        """
        Enable safe mode query (default True):
        Can only do INSERT INTO and UPDATE with non pattern mac and/or hostname
        Without arg, set it to True
        """
        if type(isSafe) is bool:
            self._safeQuery = isSafe
        else:
            raise TypeError(isSafe, "is not a boolean.")

    def set_Tables(self):
        " Set _tables to a list of existing tables in database "
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

    def isQueryingSafe(self):
        if self._safeQuery:
            for key in self._patternModes:
                if self._patternModes[key]:
                    return False
        return True

    # Overrides sqlite3.Connection
    def execute(self, sql, parameter, table):
        if not self.tableExist(table):
            raise ValueError(table, " does not exist in database.")
        self._cur.execute(sql, parameter)
        return self._cur.fetchall()

    # SELECT
    def select(self, table):
        query = 'SELECT * FROM {}'.format(table) + \
         ' WHERE mac LIKE :mac AND hostname LIKE :hostname;'
        return self.execute(query, {
            "mac": self._mac,
            "hostname": self._hostname,
        }, table)

    # INSERT INTO
    def insert(self, table):
        # Prevent insert with pattern (data corruption)
        if not self.isQueryingSafe():
            raise ValueError(
                "Invalid query. mac or hostname is a pattern."
            )

        query = 'INSERT INTO {}'.format(table) + \
            ' (mac, hostname) VALUES (:mac, :hostname);'
        return self.execute(query, {
            "mac": self._mac,
            "hostname": self._hostname
        }, table)

    # Update abstract
    def update(self, table, columns):
        """ Columns is an object:
        {
            updated: {"colname1": value},
            matched: {"colname2": value}
        }
        """
        # Prevent update with pattern (data corruption)
        if self.isQueryingSafe():
            raise ValueError(
                "Invalid query. mac or hostname is a pattern."
            )

        query = 'UPDATE {}'.format(table) + \
            ' SET :updatedCol = :updatedVal' + \
            ' WHERE :matchedCol LIKE :matchedVal;'
        return self.execute(query, {
            "updatedCol": columns.updated.keys()[0],
            "updatedVal": columns.updated.values()[0],
            "matchedCol": columns.matched.keys()[0],
            "matchedVal": columns.matched.values()[0]
        }, table)

    def updateMac(self, table):
        return self.update(table, {
            "updated": {"mac": self._mac},
            "matched": {"hostname": self._hostname}
        })

    def updateHostname(self, table):
        return self.update(table, {
            "updated": {"hostname": self._hostname},
            "matched": {"mac": self._mac}
        })

    def delete(self, table):
        if not self.isQueryingSafe():
            raise ValueError(
                "safe mode ON.",
                "Disable it to use DELETE with a pattern."
            )
        query = 'DELETE FROM {}'.format(table) + \
            ' WHERE mac LIKE :mac AND hostname LIKE :hostname;'
        return self.execute(query, {
            "mac": self._mac,
            "hostname": self._hostname
            }, table)

    @staticmethod
    def isValidHostname(hostname):
        if len(hostname) > 255:
            return False
        if hostname[-1] == ".":
            # strip exactly one dot from the right, if present
            hostname = hostname[:-1]
        allowed = re.compile("(?!-)[A-Z0-9-]{1,63}(?<!-)$", re.IGNORECASE)
        return all(allowed.match(x) for x in hostname.split("."))


if __name__ == '__main__':
    """
    mngMacDB = MngMacDB('mac.db')
    print(mngMacDB.get_tables())
    # ['vbox', 'any']

    print(mngMacDB.tableExist('any'))
    # True

    print(mngMacDB.select('any'))
    # dump table any

    mngMacDB.set_database('mac.db')
    print(mngMacDB.get_database())
    # mac.db

    macAddr = GenMacAddr(None)
    macAddr.set_addr({
        "vendorId": [0x32, 0x5D, 0xB9],
        "serialId": [0x49, 0x1B, 0x5E]
    })
    mngMacDB.set_mac(macAddr)
    print(mngMacDB.select('any'))
    # [('325DB9491B5E', 'host1')]

    mngMacDB.set_mac(None)
    mngMacDB.set_hostname('host-2')
    print(mngMacDB.select('any'))
    # [('2A523B85189F', 'host-2' ), ('86A1EC0CB254', 'host-2')]

    mngMacDB.set_hostname('host%', True)
    print(mngMacDB.select('any'))
    # [('325DB9491B5E', 'host1'), ('2A523B85189F', 'host-2'),
    # ('86A1EC0CB254', 'host-2')]

    try:
        mngMacDB.insert('any')
    except ValueError as e:
        print(e)
    # Invalid query. mac or hostname is pattern.

    print(mngMacDB.select('any'))
    # [('325DB9491B5E', 'host1'), ('2A523B85189F', 'host-2'),
    # ('86A1EC0CB254', 'host-2')]

    mngMacDB.set_hostname('hostToDelete', False)
    macAddr.set_vendorId([0x12, 0x15, 0x5A])
    mngMacDB.set_mac(macAddr, False)
    mngMacDB.insert('any')
    # {'mac': '12155A491B5E', 'hostname': 'hostToDelete'}

    print(mngMacDB.select('any'))
    # [('12155A491B5E', 'hostToDelete')]

    mngMacDB.delete('any')

    print(mngMacDB.select('any'))
    # []
    """
