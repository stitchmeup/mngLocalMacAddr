#!/usr/bin/env python

# Generate a unique MAC address (locally), LAA or VirtualBox MAC address
# Save it in a SQLite3 database
# Can populate database from existing MAC Address
# Can modify a VagrantFile accordingly

from MngMacDB import MngMacDB
import argparse


# argparse
existingTables = ['generic']
tablesPop = existingTables.copy()
tablesPop.append('all')
macAddrType = ['laa', 'vbox']

parser = argparse.ArgumentParser(description="Generate a unique MAC address (locally), LAA or VirtualBox MAC address.\
Keep track of all generated Mac in a SQLite3 DB.\
Can interface with openwrt dnsmasq DHCP API (TBD)\
And can populate the database from VirtualBox VM network interface.\
Can modify a VagrantFile accordingly")

parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1')
subparsers = parser.add_subparsers(help='sub-command --help')

# populate database(s)
parser_populateDb = subparsers.add_parser('populate',
                                          help='populate database(s)'
                                          )
parser_populateDb.add_argument('table', type=str, choices=tablesPop,
                               default='all',
                               help='table(s) to populate'
                               )

# generate MAC address
parser_generateMac = subparsers.add_parser('generate',
                                           help='generate a new MAC address'
                                           )
parser_generateMac.add_argument('type', type=str, choices=macAddrType,
                                default='laa',
                                help='type of MAC addr: LAA or VBox'
                                )
parser_generateMac.add_argument('hostname', type=str, required=True,
                                help='hostname associated to MAC address'
                                )
parser_generateMac.add_argument('--table', type=str, choices=existingTables,
                                default='generic',
                                help='save it in the specified table'
                                )
parser_generateMac.add_argument('--vagrant', type=int,
                                help='Modify VagrantFile in working directory if present, setting MAC address for the selected adapter (must be already defined in VagrantFile)'
                                )

# parse args
args = parser.parse_args()
