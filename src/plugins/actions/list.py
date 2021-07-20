from src.lib.MngMacDB import MngMacDB


class ListInDB(MngMacDB):
    """
    list known mac addresses
    """

    def __init__(self, database, table, **options):
        super().__init__(database)
        if "macAddr" in options:
            self.set_macAddr(options['macAddr'], True)
        if "hostname" in options:
            self.set_hostname(options['hostname'], True)
        self.table = table

    def selection(self):
        if self.table == 'all':
            res = {}
            for table in self.get_tables():
                res[table] = self.select(table)
            return res
        else:
            return {self.table: self.select(self.table)}
