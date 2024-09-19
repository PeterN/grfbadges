#!/usr/bin/env python3
# pip install git+https://github.com/citymania-org/grf-py.git@ae4aeab54638cc206d3c969caae0e473a8636651#egg=grf

import io
from pathlib import Path
from cairosvg import svg2png
from PIL import Image

import lib
import grf

THIS_FILE = grf.PythonFile(__file__)

ZOOM = grf.ZOOM_2X
BPP = grf.BPP_32

BADGE_PATH = Path("badges")

# Base sizes at 1x zoom.
BADGE_HEIGHT = int(12)
FLAG_HEIGHT = int(10)
FLAG_WIDTH = int(FLAG_HEIGHT * 3 / 2) # Force flags to have a 3:2 aspect ratio to fit the overlays.

BADGE = lib.register_badge_feature()

g = grf.NewGRF(
    format_version=8,
    grfid=b"PNS\xFF",
    name="Default Badge Set",
    description="A set of badges for common country flags, power types and operator logos",
    id_map_file="id_map.json",
)

s = grf.StringManager()
s.import_lang_dir(str(BADGE_PATH / "lang"))

class Badge:
    def __init__(self, id, label, image, string, flags=None):
        if len(grf.to_bytes(bytes(label, "utf-8").decode("unicode_escape"))) != 4:
            raise ValueError("label must be 4 bytes")

        self.id = g.resolve_id(BADGE, label) if id == None else id
        self.label = label
        self.image = image
        self.string = string
        self.flags = flags

class Badges:
    def __init__(self):
        self.badges = []
        self.next_id = 0

    def add(self, label, image, string, flags=None):
        self.badges.append(Badge(self.next_id, label, image, None if string == None else s[string], flags))
        self.next_id += 1

badges = Badges()

from badges import define_badges

define_badges(badges)

# Overlay for flags to provide shading and texture. This also subdues the flag colours slightly which makes the flags
# less accurate, but actually makes them fit in better.
flag_overlay = {}
flag_overlay[grf.ZOOM_NORMAL] = grf.Image.open(BADGE_PATH / f"flag-overlay-{FLAG_WIDTH}x{FLAG_HEIGHT}.png")
flag_overlay[grf.ZOOM_2X] = flag_overlay[grf.ZOOM_NORMAL].resize(size=(FLAG_WIDTH * 2, FLAG_HEIGHT * 2), resample=Image.Resampling.NEAREST)
flag_overlay[grf.ZOOM_4X] = flag_overlay[grf.ZOOM_NORMAL].resize(size=(FLAG_WIDTH * 4, FLAG_HEIGHT * 4), resample=Image.Resampling.NEAREST)

class BadgeSprite(grf.SpriteGenerator):
    def __init__(self, badge):
        self.badge = badge
        self.filename = str(BADGE_PATH / badge.label[0] / badge.image)

    def make_badge_bpps(self, im, zoom):
        sprites = []
        sprites.append(grf.QuantizeSprite(grf.ImageSprite(im, zoom=zoom, crop=False)))
        if BPP == grf.BPP_32:
            sprites.append(grf.ImageSprite(im, zoom=zoom, crop=False))
        return sprites

    def make_flag(self, zoom, scale):
        flag = svg2png(url=self.filename, output_height=scale * FLAG_HEIGHT * scale)
        f = io.BytesIO(flag)
        im = grf.Image.open(f).convert(mode="RGBA").resize((FLAG_WIDTH * scale, FLAG_HEIGHT * scale))
        return Image.blend(im, flag_overlay[zoom], 0.25)

    def make_badge(self, scale):
        flag = svg2png(url=self.filename, output_width=BADGE_HEIGHT * scale * 4 / 3, output_height=BADGE_HEIGHT * scale)
        f = io.BytesIO(flag)
        return grf.Image.open(f)

    def make_badge_from_svg(self, zoom, scale, isFlag):
        im = self.make_flag(zoom, scale) if isFlag else self.make_badge(scale)
        return self.make_badge_bpps(im, zoom)

    def make_badge_from_image(self, im, zoom, scale):
        im = im.resize((int(BADGE_HEIGHT * scale * im.size[0] / im.size[1]), int(BADGE_HEIGHT * scale)))
        return self.make_badge_bpps(im, zoom)

    def get_sprites(self, g):
        sprites = []
        if self.badge.image.endswith(".svg"):
            # Badges in the flag class have the flag overlay applied
            isFlag = self.badge.label.startswith("f")
            sprites.extend(self.make_badge_from_svg(grf.ZOOM_NORMAL, 1, isFlag))
            if ZOOM == grf.ZOOM_2X or ZOOM == grf.ZOOM_4X: sprites.extend(self.make_badge_from_svg(grf.ZOOM_2X, 2, isFlag))
            if ZOOM == grf.ZOOM_4X: sprites.extend(self.make_badge_from_svg(grf.ZOOM_4X, 4, isFlag))
        else:
            im = grf.Image.open(self.filename).convert(mode="RGBA")
            sprites.extend(self.make_badge_from_image(im, grf.ZOOM_NORMAL, 1))
            if ZOOM == grf.ZOOM_2X or ZOOM == grf.ZOOM_4X: sprites.extend(self.make_badge_from_image(im, grf.ZOOM_2X, 2))
            if ZOOM == grf.ZOOM_4X: sprites.extend(self.make_badge_from_image(im, grf.ZOOM_4X, 4))

        return [
            grf.AlternativeSprites(*sprites)
        ]

class BadgeSpriteBatch(grf.SpriteGenerator):
    def __init__(self, first_id, badges):
        self.first_id = first_id
        self.badges = badges

    def get_sprites(self, g):
        res = []
        res.append(grf.Action1(feature=BADGE, set_count=len(self.badges), sprite_count=1))

        for b in self.badges:
            res.append(BadgeSprite(b))

        act1id = 0
        for b in self.badges:
            res.append(grf.Action3(feature=BADGE, ids=[b.id], maps={}, default=grf.GenericSpriteLayout(feature=BADGE, ent1=[act1id], ent2=[])))
            act1id += 1

        return res

# Define properties
g.add(lib.PropertyBatcher(BADGE, "label", ((b.id, grf.to_bytes(bytes(b.label, "utf-8").decode("unicode_escape"))) for b in badges.badges if b.label != None)))
g.add(lib.PropertyBatcher(BADGE, "flags", ((b.id, b.flags) for b in badges.badges if b.flags != None)))

# Define names
g.add(lib.StringBatcher(BADGE, ((b.id, b.string) for b in badges.badges)))

# Define sprites
for first, values in grf.combine_ranges((b.id, b) for b in badges.badges if b.image != None):
    g.add(BadgeSpriteBatch(first, values))

grf.main(g, "badges.grf")
