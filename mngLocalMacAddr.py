#!/usr/bin/env python

# TODO: initial script comments

import argparse

# argparse
tablesList = ['generic']
tablesAll = tablesList.copy()
tablesAll.append('all')
macAddrType = ['laa', 'vbox']

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
parser_generate.add_argument('-t', '--type', type=str, choices=macAddrType,
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
parser_generate.add_argument('-V', '--vagrant', metavar='ADAPTER', type=int,
                             help='Modify VagrantFile in working directory if present, setting MAC address for the selected adapter (must be already defined in VagrantFile)'
                             )

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
