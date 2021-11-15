# API to mac address sqlite3 DB
# SELECT, INSERT, DELETE

import sqlite3
import os
import re
from src.lib.GenMacAddr import GenMacAddr  # type: ignore


class MngMacDB(sqlite3.Connection):
    """
    Management of Mac Addresses Database
    Inherit sqlite3.Connection
    """

    def __init__(self, database):
        super().__init__(os.path.abspath(database))
        self._database = os.path.abspath(database)
        self._cur = self.cursor()
        # % Matches any in SQL WHERE condition
        self._macAddr = '%'
        self._hostname = '%'
        self._patternModes = {}
        self._patternModes["mac"] = True
        self._patternModes["hostname"] = True
        self._safeQuery = True
        self._tables = []
        self.set_Tables()

    def get_database(self):
        return self._database

    def get_macAddr(self):
        return self._macAddr

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
        super().__init__(os.path.abspath(database))
        self._database = os.path.abspath(database)
        self._cur = self.cursor()
        self.set_tables()

    def set_macAddr(self, mac=None, patternMode=False):
        """
        Set mac from a GenMacAddr instance
        if None:
            set it to '%' (turn pattern mode ON)
        if pattern mode is set:
            doesnt check for integrity and only select is allowed
        """
        self._patternModes["mac"] = patternMode
        if patternMode:
            self._macAddr = mac
        else:
            if mac is None:
                self._macAddr = '%'
                self._patternModes["mac"] = True
            elif isinstance(mac, GenMacAddr):
                if not mac.isEmpty():
                    self._macAddr = mac.toString()
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
        Can only do INSERT INTO, UPDATE and DELETE with non pattern mac and/or hostname
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
            "mac": self._macAddr,
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
            "mac": self._macAddr,
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
            "updated": {"mac": self._macAddr},
            "matched": {"hostname": self._hostname}
        })

    def updateHostname(self, table):
        return self.update(table, {
            "updated": {"hostname": self._hostname},
            "matched": {"mac": self._macAddr}
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
            "mac": self._macAddr,
            "hostname": self._hostname
        }, table)

    def isMacUniq(self):
        """
        Determine if mac Addr is already known in specified tables
        tables must be a list of string.
        """
        for table in self.get_tables():
            if self.select(table):
                return False
        return True

    @staticmethod
    def isValidHostname(hostname):
        if len(hostname) > 255:
            return False
        if hostname[-1] == ".":
            # strip exactly one dot from the right, if present
            hostname = hostname[:-1]
        allowed = re.compile("(?!-)[A-Z0-9-]{1,63}(?<!-)$", re.IGNORECASE)
        return all(allowed.match(x) for x in hostname.split("."))
