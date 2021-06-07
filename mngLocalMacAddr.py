#!/usr/bin/env python

# TODO: initial script comments

import argparse
import os
from src.plugins.actions.generate import Generate
# from src.plugins.actions.populate import Populate
# from src.plugins.actions.list import ListRecords
# from src.plugins.actions.delete import DeleteRecords


# commands functions
def generate(args):
    database = "./mac.db"
    os.path.abspath(database)
    macAddr = Generate(args.hostname, database, args.vendor, args.table)
    print(macAddr.get_macAddr())
    if not args.noinsert:
        macAddr.insert(macAddr.get_table())
        macAddr.get_cur().close()
        macAddr.commit()
    else:
        macAddr.get_cur().close()
    macAddr.close()


# argparse
tablesList = ['generic']
tablesAll = tablesList.copy()
tablesAll.append('all')
macAddrVendor = ['laa', 'vbox']

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
                         help='mac address to look for'
                         )
parser_list.add_argument('-T', '--table', type=str, choices=tablesAll,
                         default='all',
                         help='table to look into (default: all)'
                         )
parser_list.add_argument('-H', '--hostname', type=str,
                         help='hostname to look for'
                         )

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
