#!/usr/bin/env python

# TODO: initial script comments

import argparse
import os
from src.plugins.actions.generate import Generate
from src.plugins.actions.list import ListInDB
# from src.plugins.actions.populate import Populate
# from src.plugins.actions.list import ListRecords
# from src.plugins.actions.delete import DeleteRecords


# argparse
tablesList = ['generic']
tablesAll = tablesList.copy()
tablesAll.append('all')
macAddrVendor = ['laa', 'vbox']
# TODO: check for redundancy with MngMacDB class about os.path.abspath
database = os.path.abspath("./mac.db")


# commands functions
def generate(args):
    options = {}
    if args.vendor:
        options = {**{'vendor': args.vendor}}
    if args.table:
        options = {**options, **{'table': args.table}}
    macAddr = Generate(database, args.hostname, **options)
    print(macAddr.get_macAddr())
    if not args.noinsert:
        macAddr.insertion()
    macAddr.close()


def list(args):
    options = {}
    if args.mac:
        options = {**{'macAddr': args.mac}}
    if args.hostname:
        options = {**options, **{'hostname': args.hostname}}
    listInDB = ListInDB(database, args.table, **options)
    found = listInDB.selection()
    for table in found:
        # TODO formating output
        print(table, found[table])
    listInDB.close()


# TODO: description
parser = argparse.ArgumentParser(description="TBD")

parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1')
subparsers = parser.add_subparsers(help='sub-command --help')

# populate database(s)
parser_populate = subparsers.add_parser('populate', aliases=['pop'],
                                        help='populate database(s)'
                                        )
parser_populate.add_argument('table', type=str, choices=tablesAll,
                             default='all',
                             help='table(s) to populate'
                             )

# generate MAC address
parser_generate = subparsers.add_parser('generate', aliases=['gen'],
                                        help='generate a new MAC address'
                                        )
parser_generate.add_argument('--vendor', type=str, choices=macAddrVendor,
                             default='laa',
                             help='type of MAC addr: LAA or VBox (default: laa)'
                             )
parser_generate.add_argument('hostname', type=str,
                             help='hostname associated to MAC address'
                             )
parser_generate.add_argument('-T', '--table', type=str, choices=tablesList,
                             default='generic',
                             help='save it in the specified table (default: generic)'
                             )
parser_generate.add_argument('-n', '--noinsert', action="store_true",
                             help='Does not insert newly generated mac address into database.\
                             Overrides --table <table>'
                             )
parser_generate.set_defaults(func=generate)

# list
parser_list = subparsers.add_parser('list',
                                    help='list known MAC addresses'
                                    )
parser_list.add_argument('-m', '--mac', type=str,
                         help='mac address to look for (SQL pattern matching enabled)'
                         )
parser_list.add_argument('-T', '--table', type=str, choices=tablesAll,
                         default='all',
                         help='table to look into (default: all)'
                         )
parser_list.add_argument('-H', '--hostname', type=str,
                         help='hostname to look for (SQL pattern matching enabled)'
                         )
parser_list.set_defaults(func=list)

# delete
parser_delete = subparsers.add_parser('delete', aliases=['del'],
                                      help='delete record(s)'
                                      )
parser_delete.add_argument('-m', '--mac', type=str,
                           help='mac address to delete'
                           )
parser_delete.add_argument('-T', '--table', type=str, choices=tablesAll,
                           default='all',
                           help='table to look into (default: all)'
                           )
parser_delete.add_argument('-H', '--hostname', type=str,
                           help='hostname to delete'
                           )


# parse args
args = parser.parse_args()
print(args)
args.func(args)
