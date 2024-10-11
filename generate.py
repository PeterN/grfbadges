# pip install git+https://github.com/citymania-org/grf-py.git@ae4aeab54638cc206d3c969caae0e473a8636651#egg=grf

import io
from pathlib import Path
from cairosvg import svg2png
from PIL import Image
from filters import SpriteFilter, QuantizeSprite
import math

import lib
import grf

BADGE_PATH = Path("badges")
BADGE_ZOOM = grf.ZOOM_2X
BADGE_BPP = [grf.BPP_32, grf.BPP_8]

# Base sizes at 1x zoom.
BADGE_HEIGHT = int(12)
FLAG_HEIGHT = int(10)
FLAG_WIDTH = int(FLAG_HEIGHT * 3 / 2) # Force flags to have a 3:2 aspect ratio to fit the overlays.

BADGE = lib.register_badge_feature()

class BadgeOverlays:
    def __init__(self, name):
        self.name = name
        self.overlays = {}

    def get_overlay(self, zoom, w, h):
        key = (zoom, w, h)
        if key not in self.overlays:
            if zoom == grf.ZOOM_NORMAL:
                self.overlays[key] = grf.Image.open(BADGE_PATH / f"{self.name}-{w}x{h}.png")
            else:
                scale = lib.get_scale_for_zoom(zoom)
                self.overlays[key] = self.get_overlay(grf.ZOOM_NORMAL, w, h).resize(size=(w * scale, h * scale), resample=Image.Resampling.NEAREST)

        return self.overlays[key]

# Overlay for flags to provide shading and texture. This also subdues the flag colours slightly which makes the flags
# less accurate, but actually makes them fit in better.
flag_overlays = BadgeOverlays("flag-overlay")

class Badge(grf.SpriteGenerator):
    def __init__(self, id, label, image, string, flags=None, crop=True, filters=None, overlay=False):
        if string is not None and not isinstance(string, grf.StringRef):
            raise ValueError("string must be None or a StringRef")
        if filters is not None:
            for filter in filters:
                if not isinstance(filter, SpriteFilter):
                    raise ValueError("filters must be None or a SpriteFilter")

        self.id = id
        self.label = label
        self.image = image
        self.string = string
        self.flags = flags
        self.crop = crop
        self.filters = filters
        self.overlay = overlay

    def get_sprites(self, g):
        # In the interests of code reuse, and laziness, this produces a 'batch' of just one badge.
        badges = Badges()
        badges.badges.append(self)
        return badges.get_sprites(g)

class Badges(grf.SpriteGenerator):
    def __init__(self, s = None):
        self.badges = []
        self.next_id = 0
        if s is None:
            self.s = grf.StringManager()
            self.s.import_lang_dir(str(BADGE_PATH / "lang"))
        else:
            self.s = s

    def add(self, label, image, string, flags=None, filters=None, overlay=False):
        self.badges.append(Badge(self.next_id, label, image, None if string is None else self.s[string], flags, filters=filters, overlay=overlay))
        self.next_id += 1

    def get_sprites(self, g):
        return [
            # Define properties
            lib.PropertyBatcher(BADGE, "label", ((b.id, b.label) for b in self.badges if b.label is not None)),
            lib.PropertyBatcher(BADGE, "flags", ((b.id, b.flags) for b in self.badges if b.flags is not None)),
            # Define names
            lib.StringBatcher(BADGE, ((b.id, b.string) for b in self.badges)),
            # Define sprites
            BadgeSpriteBatch([b for b in self.badges if b.image is not None]),
        ]

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
        if self.image is None:
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
        return im, grf.BPP_32

class BlendOverlaySprite(grf.SpriteWrapper):
    def __init__(self, sprite):
        super().__init__((sprite, ))
        self.sprite = sprite
        self.w = None
        self.h = None

    def get_image(self):
        scale = lib.get_scale_for_zoom(self.sprite.zoom)
        img, bpp = self.sprite.get_image()
        img = Image.blend(img, flag_overlays.get_overlay(self.sprite.zoom, math.ceil(img.size[0] / scale), math.ceil(img.size[1] / scale)), 0.25)
        return img, bpp

    def get_fingerprint(self):
        return {
            'class': self.__class__.__name__,
            'sprite': self.sprite.get_fingerprint(),
        }

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
    def __init__(self, file):
        self.file = grf.ResourceFile(str(file))
        self.image = None

    def load(self):
        return grf.Image.open(self.file.path).convert(mode="RGBA")

    def get_image(self):
        if self.image is None:
            self.image = self.load()
        return self.image

    def get_resource_files(self):
        return super().get_resource_files() + (self.file,)

    def get_fingerprint(self):
        return {
            'class': self.__class__.__name__,
            'filename': self.file.path,
        }

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

class CropSprite(grf.SpriteWrapper):
    def __init__(self, sprite, zoom):
        super().__init__((sprite, ))
        self.sprite = sprite
        self.zoom = zoom
        self.w = None
        self.h = None

    def get_image(self):
        scale = lib.get_scale_for_zoom(self.zoom)
        img, bpp = self.sprite.get_image()
        left, top, right, bottom = img.getbbox()
        left = int(scale * math.floor(left / scale))
        top = int(scale * math.floor(top / scale))
        right = int(scale * math.ceil(right / scale))
        bottom = int(scale * math.ceil(bottom / scale))
        img = img.crop((left, top, right, bottom))
        return img, bpp

class BadgeSprites(grf.SpriteGenerator):
    def __init__(self, badge):
        self.badge = badge
        self.filename = str(BADGE_PATH / badge.label[0] / badge.image)

    def make_badge_bpps(self, sprite, zoom):
        sprites = []
        if self.badge.crop:
            sprite = CropSprite(sprite, zoom)
        if self.badge.overlay:
            sprite = BlendOverlaySprite(sprite)
        if self.badge.filters is not None:
            for filter in self.badge.filters:
                sprite = filter.apply_filter(sprite)
        if grf.BPP_32 in BADGE_BPP: sprites.append(sprite)
        if grf.BPP_8 in BADGE_BPP: sprites.append(QuantizeSprite(sprite))
        return sprites

    def make_badge_from_svg(self, zoom, is_flag):
        sprite = BlendOverlaySprite(SvgFlagSprite(self.badge, zoom)) if is_flag else SvgBadgeSprite(self.badge, zoom)
        return self.make_badge_bpps(sprite, zoom)

    def make_badge_from_image(self, im, zoom):
        sprite = ImageBadgeSprite(im, zoom)
        return self.make_badge_bpps(sprite, zoom)

    def get_sprites(self, g):
        sprites = []
        if self.badge.image.endswith(".svg"):
            # Badges in the flag class have the flag overlay applied
            is_flag = self.badge.label[0] == "f"
            sprites.extend(self.make_badge_from_svg(grf.ZOOM_NORMAL, is_flag))
            if BADGE_ZOOM == grf.ZOOM_2X or BADGE_ZOOM == grf.ZOOM_4X: sprites.extend(self.make_badge_from_svg(grf.ZOOM_2X, is_flag))
            if BADGE_ZOOM == grf.ZOOM_4X: sprites.extend(self.make_badge_from_svg(grf.ZOOM_4X, is_flag))
        else:
            im = ReusableImage(self.filename)
            sprites.extend(self.make_badge_from_image(im, grf.ZOOM_NORMAL))
            if BADGE_ZOOM == grf.ZOOM_2X or BADGE_ZOOM == grf.ZOOM_4X: sprites.extend(self.make_badge_from_image(im, grf.ZOOM_2X))
            if BADGE_ZOOM == grf.ZOOM_4X: sprites.extend(self.make_badge_from_image(im, grf.ZOOM_4X))

        return [
            grf.AlternativeSprites(*sprites)
        ]

class BadgeSpriteBatch(grf.SpriteGenerator):
    def __init__(self, badges):
        self.badges = badges

    def get_sprites(self, g):
        res = []
        res.append(grf.Action1(feature=BADGE, set_count=len(self.badges), sprite_count=1))

        for b in self.badges:
            b.sprites = BadgeSprites(b)
            res.append(b.sprites)

        act1id = 0
        for b in self.badges:
            res.append(grf.Action3(feature=BADGE, ids=[b.id], maps={}, default=grf.GenericSpriteLayout(feature=BADGE, ent1=[act1id], ent2=[])))
            act1id += 1

        return res
