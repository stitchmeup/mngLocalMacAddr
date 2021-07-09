from src.bin.MngMacDB import MngMacDB


class DeleteInDB(MngMacDB):
    """
    delete record(s) in database
    """

    def __init__(self, database, table, **options):
        super().__init__(database)
        if "macAddr" in options:
            self.set_macAddr(options['macAddr'], True)
        if "hostname" in options:
            self.set_hostname(options['hostname'], True)
        self.table = table
        self.set_safeQuery(False)

    def deletion(self):
        if self.table == 'all':
            res = {}
            for table in self.get_tables():
                print("looking for match into table", table, "...")
        else:
            print("looking for match into table", table, "...")
        self.commit()
        print("delete operation from database finished.")
