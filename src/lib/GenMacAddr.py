"""Class to handle MAC address and random generation."""

#  class to handle mac address and mac address random generation

import random
import re


class GenMacAddr:
    """Mac Address class."""

    _specialVendorId = {
        "vbox": [0x08, 0x00, 0x27]
    }

    def __init__(self, vendor="laa"):
        """
        Constructor of MAC addr:
        1 property: _addr
        _addr properties:
            - vendorId: 3 bytes of the manufacturer ID.
            - serialId: 3 least significant (left) bytes of the MAC addr.
        Use vendor to specify a special known vendor for vendorID.
        If vendor is None, doesn't generate a MAC address (vendor="None").
        By default generate a new Locally Administered Address (venor="laa").
        """
        self.vendor = vendor
        self._addr = {
            "vendorId": [],
            "serialId": []
        }
        if vendor is not None:
            self._generate()

    def get_vendorId(self):
        """ Get vendor Id """
        return self._addr['vendorId']

    def get_serialId(self):
        """ Get vendor Id """
        return self._addr['serialId']

    @classmethod
    def get_specialVendorId(cls):
        """ Get dict of special known vendors ID """
        return cls._specialVendorId

    def set_addr(self, addr):
        """
        Set the _addr object from addr object that has two properties:
        - vendorId: list of Integers;
        - serialId: list of Integers.
        """
        self.set_vendorId(addr['vendorId'][:3])
        self.set_serialId(addr['serialId'][:3])

    def set_vendorId(self, id):
        """
        Set the vendor Id of the MAC addr
        from the 3 first elements of list of Integers.
        """
        if type(id) is list:
            for i in range(3):
                if type(id[i]) is not int:
                    raise TypeError(id[i] + " is not Integer.")
        else:
            raise TypeError(id + " is not a List.")
        self._addr['vendorId'] = id[:3]

    def set_serialId(self, id):
        """
        Set the serial Id of the MAC addr
        from the 3 first elements of list of Integers.
        """
        if type(id) is list:
            for i in range(3):
                if type(id[i]) is not int:
                    raise TypeError(id[i] + " is not Integer.")
        else:
            raise TypeError(id + " is not a List.")
        self._addr['serialId'] = id[:3]

    def isEmpty(self):
        """ Return true if vendor Id and serial Id are empty """
        return not (bool(self.get_vendorId()) and bool(self.get_serialId()))

    def toString(self, separator=''):
        """
        Returns MAC address as a string.
        Use separator to insert a string between each bytes.
        """
        return separator.join(
            map(
                lambda byte: "%0.2X" % byte,
                bytearray(self._addr['vendorId'] + self._addr['serialId'])
            ))

    # Generate a list of 6 bytes
    # If no special vendor (i.e VirtualBox) is not provided or unknown,
    # individual locally administered address will be generated randomly,
    # meaning the two least significant bit of first octet are '10':
    # X2XXXXXXXXXX, X6XXXXXXXXXX, XAXXXXXXXXXX, XEXXXXXXXXXX
    # https://www.ibm.com/support/knowledgecenter/en/SSLTBW_2.1.0/com.ibm.zos.v2r1.ioaz100/canon.htm
    def _generate(self):
        """
        Generate a random MAC Address.
        Use vendor to select vendors (see get_specialVendorId() class method).
        By default, generates a Locally Administered Address (vendor="laa").
        """
        addr = {
            "vendorId": [],
            "serialId": []
        }

        # Set vendor ID
        if self.vendor == "laa":
            # Setting the two first bits (LSB) of the most significant byte to '10'
            addr['vendorId'].append(random.randrange(0x01, 0x7F, 2) << 1)
            while (len(addr['vendorId']) < 3):
                addr['vendorId'].append(random.randrange(0x00, 0xFF))
        elif self.vendor in GenMacAddr._specialVendorId:
            addr['vendorId'] = GenMacAddr._specialVendorId[self.vendor]
        else:
            raise ValueError(self.vendor, "not found.")

        # Set serial ID
        while (len(addr['serialId']) < 3):
            addr['serialId'].append(random.randrange(0x00, 0xFF))

        self.set_addr(addr)

    @classmethod
    def toMacAddr(cls, macAsStr, separator=None):
        """
        Return a MacAddr objct from a MAC address as a string.
        Use separator to specify theseparator of the bytes in the given string.
        """
        # Check integrity
        if not cls.isValidMacStr(macAsStr):
            raise ValueError(macAsStr + " not valid.")

        # if not separator: pretty much the same in this context?
        if separator is None or separator == "":
            n = 2
            bytesList = [int(macAsStr[i:i + n], 16)
                         for i in range(0, len(macAsStr), n)
                         ]
        else:
            bytesList = [int(i, 16) for i in macAsStr.split('separator')]

        addr = GenMacAddr()
        addr.set_vendorId(bytesList[:3])
        addr.set_serialId(bytesList[3:])
        return addr

    @staticmethod
    def isValidMacStr(macAsStr):
        """
        Check validity mac address as a string
        Must be of form:
        XXXXXXXXXXXXX
        so without separator
        Comments under are irrelevant but kept as it could be useful:
        Must be of form:
        XXXXXXXXXXXXX, XXyXXyXXyXXyXXyXX, XXyXXXXXXyXXXX, XXXXXXXXXXyXXXX,...
        with X an hexadecimal number and y a character
        regex used: ^[0-9A-F]{2}(.?[0-9A-F]{2}){5}$
        """
        p = re.compile("^[0-9A-F]{12}$", re.IGNORECASE)
        return p.match(macAsStr)
