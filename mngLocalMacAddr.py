#!/usr/bin/env python

# Generate a unique MAC address (locally)
# LAA or VirtualBox MAC address
# Save it in a SQLite3 Database
# Can modify a VagrantFile accordingly

from MngMacDB import MngMacDB
import argparse

parser = argparse.ArgumentParser(description="\
Generate a unique MAC address (locally),\
LAA or VirtualBox MAC address.\
Keep track of all generated Mac in a SQLite3 DB.\
Can interface with openwrt dnsmasq DHCP API (TBD)\
And can populate the database from VirtualBox VM network interface.\
Can modify a VagrantFile accordingly")
existingDb = ['generic', 'openwrt-dnsmasq', 'vbox']
dbPop = existingDb
dbPop.append('all')
macAddrType = ['laa', 'vbox']
subparsers = parser.add_subparsers(help='sub-command --help')
parser_populateDb = subparsers.add_parser('populate',
                                          help='populate database(s)'
                                          )
parser_populateDb.add_argument('db', type=str, choices=dbPop,
                               help='database(s) to populate:\
                               vbox from VirtualBox VM\
                               or\
                               any from OpenWRT dnsmsq API (openwrt-dnsmasq)\
                               or\
                               both (all)'
                               )
parser_generateMac = subparsers.add_parser('generate',
                                           help='generate a new MAC address'
                                           )
parser_generateMac.add_argument('type', type=str, choices=macAddrType,
                                default='laa',
                                help='type of MAC addr: LAA or VBox'
                                )
parser_generateMac.add_argument('hostname', type=str,
                                help='hostname associated to MAC address'
                                )
parser_generateMac.add_argument('--db', type=str, choices=existingDb,
                                default='generic',
                                help='database to which to add the record'
                                )
parser_generateMac.add_argument('--vagrant', type=int,
                                help='Modify VagrantFile in working directory\
                                if present,\
                                setting MAC address for the selected adapter\
                                (must be already defined in VagrantFile)'
                                )
args = parser.parse_args()
