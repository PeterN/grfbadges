#!/usr/bin/env python3
# pip install git+https://github.com/citymania-org/grf-py.git@ae4aeab54638cc206d3c969caae0e473a8636651#egg=grf

import struct
import grf
import lib

THIS_FILE = grf.PythonFile(__file__)

g = grf.NewGRF(
    grfid=b'PNS\xFE',
    name='Default Vehicle Badges',
    description='Applies some badges to the default vehicles',
)

grf.actions.ACTION0_PROP_DICT[grf.TRAIN]['badges'] = (0x33, lib.WordListProperty())
grf.actions.ACTION0_PROP_DICT[grf.GLOBAL_VAR]['badge_table'] = (0x18, lib.StringProperty())

class BadgeTranslationTable(grf.SpriteGenerator):
    def __init__(self):
        self.labels = []

    def add(self, label):
        self.labels.append(label)
        return len(self.labels) - 1

    def get_sprites(self, g):
        return [
            grf.DefineMultiple(
                feature=grf.GLOBAL_VAR,
                first_id=0,
                count=len(self.labels),
                props={
                    'badge_table': [grf.to_bytes(l) for l in self.labels]
                }
            )
        ]

    def map_labels(self, labels):
        if self.labels is None:
            raise RuntimeError(f'`{self.__class__.__name__}.map_labels` requires labels to be added')
        return [self.labels.index(l) for l in labels]

btt = BadgeTranslationTable()

POWER_STEAM = btt.add('power/steam')
POWER_DIESEL = btt.add('power/diesel')
POWER_TURBINE = btt.add('power/turbine')
POWER_ELECTRIC = btt.add('power/electric')
POWER_MONORAIL = btt.add('power/monorail')
POWER_MAGLEV = btt.add('power/maglev')

FLAG_DE = btt.add('flag/DE')
FLAG_EU = btt.add('flag/europe')
FLAG_FR = btt.add('flag/FR')
FLAG_GB = btt.add('flag/GB')
FLAG_US = btt.add('flag/US')
FLAG_ZA = btt.add('flag/ZA')

train = {}
train[0] = [POWER_STEAM, FLAG_GB]
train[1] = [POWER_DIESEL, FLAG_US]
train[2] = [POWER_STEAM]
train[3] = [POWER_STEAM]
train[4] = [POWER_STEAM]
train[5] = [POWER_DIESEL]
train[6] = [POWER_DIESEL]
train[7] = [POWER_STEAM, FLAG_US]
train[8] = [POWER_STEAM, FLAG_GB]
train[9] = [POWER_STEAM, FLAG_GB]
train[10] = [POWER_STEAM, FLAG_GB]
train[11] = [POWER_DIESEL, FLAG_GB]
train[12] = [POWER_DIESEL, FLAG_GB]
train[13] = [POWER_DIESEL, FLAG_GB]
train[14] = [POWER_DIESEL, FLAG_GB]
train[15] = [POWER_DIESEL, FLAG_GB]
train[16] = [POWER_DIESEL, FLAG_DE]
train[17] = [POWER_DIESEL, FLAG_US]
train[18] = [POWER_DIESEL, FLAG_US]
train[19] = [POWER_DIESEL, FLAG_US]
train[20] = [POWER_TURBINE, FLAG_US]
train[21] = [POWER_DIESEL, FLAG_ZA]
train[22] = [POWER_DIESEL, FLAG_GB]
train[23] = [POWER_ELECTRIC, FLAG_GB]
train[24] = [POWER_ELECTRIC, FLAG_GB]
train[25] = [POWER_ELECTRIC, FLAG_FR]
train[26] = [POWER_ELECTRIC, FLAG_EU]
train[54] = [POWER_MONORAIL, POWER_ELECTRIC]
train[55] = [POWER_MONORAIL, POWER_ELECTRIC]
train[56] = [POWER_MONORAIL, POWER_ELECTRIC]
train[84] = [POWER_MAGLEV, POWER_ELECTRIC]
train[85] = [POWER_MAGLEV, POWER_ELECTRIC]
train[86] = [POWER_MAGLEV, POWER_ELECTRIC]
train[87] = [POWER_MAGLEV, POWER_ELECTRIC]
train[88] = [POWER_MAGLEV, POWER_ELECTRIC]

g.add(btt)

for (first, values) in grf.combine_ranges((b, train[b]) for b in train):
    g.add(definition := grf.DefineMultiple(feature=grf.TRAIN, first_id=first, props={'badges': values}, count=len(values)))

grf.main(g, 'default-badges.grf')
