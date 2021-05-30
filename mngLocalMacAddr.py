#!/usr/bin/env python

# TODO: initial script comments

import argparse
import sys
sys.path.insert(0, 'plugins/actions')
from generate import Generate  # type: ignore
from populate import Populate  # type: ignore
from list import ListRecords  # type: ignore
from delete import DeleteRecords  # type: ignore


# commands functions
def generate(args):
    macAddr = Generate(args.hostname, args.vendor, args.database, args.table)
    print(macAddr.get_macAddr())
    if not args.noinsert:
        macAddr.insert(macAddr.get_table())


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
parser_populate = subparsers.add_parser('populate',
                                        help='populate database(s)'
                                        )
parser_populate.add_argument('table', type=str, choices=tablesAll,
                             default='all',
                             help='table(s) to populate'
                             )

# generate MAC address
parser_generate = subparsers.add_parser('generate',
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
parser_delete = subparsers.add_parser('delete',
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
args.func(args)
