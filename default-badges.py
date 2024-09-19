#!/usr/bin/env python3
# pip install git+https://github.com/citymania-org/grf-py.git@ae4aeab54638cc206d3c969caae0e473a8636651#egg=grf

import struct
import grf

THIS_FILE = grf.PythonFile(__file__)

g = grf.NewGRF(
    grfid=b'PNS\xFE',
    name='Default Vehicle Badges',
    description='Applies some badges to the default vehicles',
)


from grf.actions import Property

class DwordListProperty(Property):
    def validate(cls, value):
        if not isinstance(value, (list, tuple)):
            raise ValueError(f'list or tuple object expected')
        if not all(isinstance(x, int) and 0 <= x < 256 for x in value):
            raise ValueError(f'expected integer values in range 0..255')
        if len(value) % 4 != 0:
            raise ValueError(f'expected 4-byte values')

    def read(cls, data, ofs):
        n = data[ofs]
        res = tuple(map(int, data[ofs + 1: ofs + 1 + n]))
        return res, ofs + 1 + n

    def encode(cls, value):
        return struct.pack('<B', int(len(value) / 4)) + bytes(value)

class BadgeListProperty(DwordListProperty):
    pass

from grf.actions import ACTION0_PROP_DICT
ACTION0_PROP_DICT[grf.TRAIN]['badges'] = (0x32, BadgeListProperty())

train = {}
train[0] = ['pSTE', 'fGB ']
train[1] = ['pDIE', 'fUS ']
train[2] = ['pSTE']
train[3] = ['pSTE']
train[4] = ['pSTE']
train[5] = ['pDIE']
train[6] = ['pDIE']
train[7] = ['pSTE', 'fUS ']
train[8] = ['pSTE', 'fGB ']
train[9] = ['pSTE', 'fGB ']
train[10] = ['pSTE', 'fGB ']
train[11] = ['pDIE', 'fGB ']
train[12] = ['pDIE', 'fGB ']
train[13] = ['pDIE', 'fGB ']
train[14] = ['pDIE', 'fGB ']
train[15] = ['pDIE', 'fGB ']
train[16] = ['pDIE', 'fDE ']
train[17] = ['pDIE', 'fUS ']
train[18] = ['pDIE', 'fUS ']
train[19] = ['pDIE', 'fUS ']
train[20] = ['pTUR', 'fUS ']
train[21] = ['pDIE', 'fZA ']
train[22] = ['pDIE', 'fGB ']
train[23] = ['pELE', 'fGB ']
train[24] = ['pELE', 'fGB ']
train[25] = ['pELE', 'fFR ']
train[26] = ['pELE', 'fEU ']
train[54] = ['pMON', 'pELE']
train[55] = ['pMON', 'pELE']
train[56] = ['pMON', 'pELE']
train[84] = ['pMAG', 'pELE']
train[85] = ['pMAG', 'pELE']
train[86] = ['pMAG', 'pELE']
train[87] = ['pMAG', 'pELE']
train[88] = ['pMAG', 'pELE']

for (first, values) in grf.combine_ranges((b, train[b]) for b in train):
    badges = [[byte for byte in grf.to_bytes(''.join(map(str, label)))] for label in values]
    g.add(definition := grf.DefineMultiple(feature=grf.TRAIN, first_id=first, props={'badges': badges}, count=len(values)))

grf.main(g, 'default-badges.grf')
