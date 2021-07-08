from src.bin.MngMacDB import MngMacDB
from src.bin.GenMacAddr import GenMacAddr


class Generate(MngMacDB):
    """
    generate a random MAC for CLI tool use
    """

    def __init__(self, database, hostname, **options):
        defaultOptions = {'vendor': "laa", 'table': "generic"}
        options = {**defaultOptions, **options}
        super().__init__(database)
        self.vendor = options['vendor']
        self.set_macAddr()
        self.set_hostname(hostname)
        self.table = options['table']

    def set_macAddr(self):
        """
        Set mac from a GenMacAddr instance
        Randomly generated and unique in Database
        """
        self._patternModes["mac"] = False
        self._macAddr = GenMacAddr(self.vendor).toString()
        while not self.isMacUniq():
            self._macAddr = GenMacAddr(self.vendor).toString()

    def insertion(self):
        self.insert(self.table)
        self.commit()
        print("inserted into database.")
