import grf

def register_badge_feature():
    ACTION0_BADGE_PROPS = {
        0x08: ("label", "L"), # Unique badge label. The first byte of the label is the label class.
        0x09: ("flags", "D"),
    }
    BADGE = grf.dev.add_feature(0x15, "badge", "Badge", properties=ACTION0_BADGE_PROPS)

    from grf import VEHICLE_FEATURES
    VEHICLE_FEATURES.add(BADGE)

    return BADGE

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
                res.append(grf.DefineStrings(feature=self.feature, offset=first, strings=values, is_generic_offset=True, lang=lang_id))

        return res

