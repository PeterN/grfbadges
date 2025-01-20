import struct
import grf

class WordListProperty(grf.actions.Property):
    def validate(cls, value):
        if not isinstance(value, (list, tuple)):
            raise ValueError(f'list or tuple object expected')
        if not all(isinstance(x, int) and 0 <= x <= 65535 for x in value):
            raise ValueError(f'expected integer values in range 0..65535')

    def encode(cls, value):
        values = [struct.pack('<H', w) for w in value]
        length = len(value)
        return struct.pack('H', length) + b''.join(values)

class StringProperty(grf.actions.Property):
    def validate(cls, value):
        if not isinstance(value, (list, tuple)):
            raise ValueError(f'list or tuple object expected')
        if not all(isinstance(x, int) and 1 <= x <= 255 for x in value):
            raise ValueError(f'expected integer values in range 0..255')

    def encode(cls, value):
        return grf.to_bytes(value) + b'\x00'

def register_badge_feature():
    ACTION0_BADGE_PROPS = {
        0x08: ("label", StringProperty()),
        0x09: ("flags", "D"),
    }
    BADGE = grf.dev.add_feature(0x15, "badge", "Badge", properties=ACTION0_BADGE_PROPS)

    from grf import VEHICLE_FEATURES
    VEHICLE_FEATURES.add(BADGE)

    return BADGE

class BadgeFlags:
    COPY = 0x01
    NAME_LIST_STOP = 0x02
    NAME_LIST_FIRST_ONLY = 0x04
    USE_COMPANY_PALETTE = 0x08

def get_scale_for_zoom(zoom):
    if zoom == grf.ZOOM_NORMAL: return 1
    if zoom == grf.ZOOM_2X: return 2
    if zoom == grf.ZOOM_4X: return 4
    raise ValueError("zoom out of range")

class PropertyBatcher(grf.SpriteGenerator):
    def __init__(self, feature, property, values):
        self.feature = feature
        self.property = property
        self.values = values

    def get_sprites(self, g):
        return [
            grf.DefineMultiple(feature=self.feature, first_id=first, props={self.property: values}, count=len(values)) for first, values in grf.combine_ranges(self.values)
        ]

class StringBatcher(grf.SpriteGenerator):
    def __init__(self, feature, strings):
        self.feature = feature
        self.strings = strings

    def get_sprites(self, g):
        lang_strings = {}
        for id, string in self.strings:
            if string is not None:
                for lang_id, text in string.get_pairs():
                    if not lang_id in lang_strings:
                        lang_strings[lang_id] = []
                    lang_strings[lang_id].append((id, text))

        res = []
        for lang_id in lang_strings:
            for first, values in grf.combine_ranges(lang_strings[lang_id]):
                res.append(grf.DefineStrings(feature=self.feature, offset=first, strings=values, is_generic_offset=False, lang=lang_id))

        return res

