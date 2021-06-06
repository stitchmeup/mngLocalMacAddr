import sys
sys.path.insert(0, '../../bin/')
from MngMacDB import MngMacDB  # type: ignore
from GenMacAddr import GenMacAddr  # type: ignore


class Generate(MngMacDB):
    """
    generate a random MAC for CLI tool use
    """

    def __init__(self,
                 hostname,
                 vendor="laa",
                 database="../../mac.db",
                 table="generic"
                 ):
        super().__init__(database)
        self.set_macAddr(GenMacAddr(vendor))
        while not self.isMacUniq():
            self.set_macAddr(GenMacAddr(vendor))
        self.vendor = vendor
        self.set_hostname(hostname)
        self.table = table

        def get_vendor(self):
            return self.vendor

        def get_table(self):
            return self.table

        def set_vendor(self, vendor):
            self.vendor = vendor

        def set_table(self, table):
            self.table = table
