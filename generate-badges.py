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
for zoom in [grf.ZOOM_2X, grf.ZOOM_4X]:
    scale = lib.get_scale_for_zoom(zoom)
    flag_overlay[zoom] = flag_overlay[grf.ZOOM_NORMAL].resize(size=(FLAG_WIDTH * scale, FLAG_HEIGHT * scale), resample=Image.Resampling.NEAREST)

class BadgeSprite(grf.Sprite):
    def __init__(self, badge, zoom):
        self.badge = badge
        self.zoom = zoom
        self.bpp = grf.BPP_32
        self.crop = False
        self.xofs = 0
        self.yofs = 0
        self.file = grf.ResourceFile(str(BADGE_PATH / self.badge.label[0] / self.badge.image))
        self.image = None

    def get_image(self):
        if self.image == None:
            self.image = self.load()
        return self.image

    def get_resource_files(self):
        return super().get_resource_files() + (self.file,)

    def get_fingerprint(self):
        return {
            'class': self.__class__.__name__,
            'filename': self.file.path,
            'zoom': self.zoom,
        }

class SvgFlagSprite(BadgeSprite):
    def __init__(self, badge, zoom):
        super().__init__(badge, zoom)
        scale = lib.get_scale_for_zoom(self.zoom)
        self.w = int(FLAG_WIDTH * scale)
        self.h = int(FLAG_HEIGHT * scale)

    def load(self):
        flag = svg2png(url=self.file.path, output_height=self.h)
        f = io.BytesIO(flag)
        im = grf.Image.open(f).convert(mode="RGBA").resize((self.w, self.h))
        im = Image.blend(im, flag_overlay[self.zoom], 0.25)
        return im, grf.BPP_32

class SvgBadgeSprite(BadgeSprite):
    def __init__(self, badge, zoom):
        super().__init__(badge, zoom)
        scale = lib.get_scale_for_zoom(self.zoom)
        self.w = int(BADGE_HEIGHT * scale * 4 / 3)
        self.h = int(BADGE_HEIGHT * scale)
        self.image = None

    def load(self):
        flag = svg2png(url=self.file.path, output_width=self.w, output_height=self.h)
        f = io.BytesIO(flag)
        im = grf.Image.open(f).convert(mode="RGBA")
        return im, grf.BPP_32

class ReusableImage:
    def __init__(self, filename):
        self.filename = filename
        self.image = None

    def load(self):
        return grf.Image.open(self.filename).convert(mode="RGBA")

    def get_image(self):
        if self.image == None:
            self.image = self.load()
        return self.image

class ImageBadgeSprite(grf.Sprite):
    def __init__(self, image, zoom):
        self.image = image
        self.zoom = zoom
        scale = lib.get_scale_for_zoom(self.zoom)

        im = self.image.get_image()
        self.w = int(BADGE_HEIGHT * scale * im.size[0] / im.size[1])
        self.h = int(BADGE_HEIGHT * scale)
        self.xofs = 0
        self.yofs = 0
        self.bpp = grf.BPP_32 # ReusableImage converts to RGBA
        self.crop = False

    def get_image(self):
        im = self.image.get_image()
        im = im.resize((self.w, self.h))
        return im, self.bpp

    def get_fingerprint(self):
        raise grf.Uncacheable

class BadgeSprites(grf.SpriteGenerator):
    def __init__(self, badge):
        self.badge = badge
        self.filename = str(BADGE_PATH / badge.label[0] / badge.image)

    def make_badge_bpps(self, sprite):
        sprites = []
        if BPP == grf.BPP_32:
            sprites.append(sprite)
        sprites.append(grf.QuantizeSprite(sprite))
        return sprites

    def make_badge_from_svg(self, zoom, isFlag):
        sprite = SvgFlagSprite(self.badge, zoom) if isFlag else SvgBadgeSprite(self.badge, zoom)
        return self.make_badge_bpps(sprite)

    def make_badge_from_image(self, im, zoom):
        sprite = ImageBadgeSprite(im, zoom)
        return self.make_badge_bpps(sprite)

    def get_sprites(self, g):
        sprites = []
        if self.badge.image.endswith(".svg"):
            # Badges in the flag class have the flag overlay applied
            isFlag = self.badge.label.startswith("f")
            sprites.extend(self.make_badge_from_svg(grf.ZOOM_NORMAL, isFlag))
            if ZOOM == grf.ZOOM_2X or ZOOM == grf.ZOOM_4X: sprites.extend(self.make_badge_from_svg(grf.ZOOM_2X, isFlag))
            if ZOOM == grf.ZOOM_4X: sprites.extend(self.make_badge_from_svg(grf.ZOOM_4X, isFlag))
        else:
            im = ReusableImage(self.filename)
            sprites.extend(self.make_badge_from_image(im, grf.ZOOM_NORMAL))
            if ZOOM == grf.ZOOM_2X or ZOOM == grf.ZOOM_4X: sprites.extend(self.make_badge_from_image(im, grf.ZOOM_2X))
            if ZOOM == grf.ZOOM_4X: sprites.extend(self.make_badge_from_image(im, grf.ZOOM_4X))

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
            res.append(BadgeSprites(b))

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
