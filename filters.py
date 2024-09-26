# pip install git+https://github.com/citymania-org/grf-py.git@ae4aeab54638cc206d3c969caae0e473a8636651#egg=grf

from PIL import Image
import numpy as np
import colorsys
import grf

rgb_to_hsv = np.vectorize(colorsys.rgb_to_hsv)
hsv_to_rgb = np.vectorize(colorsys.hsv_to_rgb)

class SpriteMasker:
    def make_mask(self, rgb):
        raise NotImplementedError

    def get_fingerprint(self):
        raise NotImplementedError

class HueMasker(SpriteMasker):
    def __init__(self, hue):
        self.hue = hue / 360.

    def make_mask(self, rgb):
        r, g, b, a = np.rollaxis(rgb, axis=-1)
        h, s, v = rgb_to_hsv(r, g, b)
        m = (v > 31) & (s >= .1) & (h == self.hue)
        return m

    def get_fingerprint(self):
        return {
            'class': self.__class__.__name__,
            'hue': self.hue,
        }

class SaturationMasker(SpriteMasker):
    def __init__(self, sat):
        self.sat = sat

    def make_mask(self, rgb):
        r, g, b, a = np.rollaxis(rgb, axis=-1)
        h, s, v = rgb_to_hsv(r, g, b)
        m = s >= self.sat
        return m

    def get_fingerprint(self):
        return {
            'class': self.__class__.__name__,
            'sat': self.sat,
        }

class SpriteFilter:
    def apply_filter(self, sprite):
        raise NotImplementedError

class AdjustHsvSprite(grf.SpriteWrapper):
    def __init__(self, sprite, hue, sat, val, masker):
        super().__init__((sprite, ))
        self.sprite = sprite
        self.hue = hue / 360.
        self.sat = sat
        self.val = val
        self.masker = masker
        self.w = None
        self.h = None

    def adjust_hsv(self, arr):
        r, g, b, a = np.rollaxis(arr, axis=-1)
        h, s, v = rgb_to_hsv(r, g, b)
        h = (h + self.hue) % 1.
        s = np.clip(s * self.sat, 0, 1)
        v = np.clip(v * self.val, 0, 255)
        r, g, b = hsv_to_rgb(h, s, v)
        arr = np.dstack((r, g, b, a))
        return arr

    def get_image(self):
        img, bpp = self.sprite.get_image()
        arr = np.array(np.asarray(img).astype(float))

        if self.masker is None:
            arr = self.adjust_hsv(arr)
        else:
            mask = self.masker.make_mask(arr)
            adjust = self.adjust_hsv(arr[mask])
            arr[mask] = adjust

        img = Image.fromarray(arr.astype('uint8'), 'RGBA')
        return img, bpp

    def get_fingerprint(self):
        return {
            'class': self.__class__.__name__,
            'sprite': self.sprite.get_fingerprint(),
            'hue': self.hue,
            'sat': self.sat,
            'val': self.val,
            'masker': None if self.masker is None else self.masker.get_fingerprint()
        }

class AdjustHsvFilter(SpriteFilter):
    def __init__(self, *, hue=0., sat=1., val=1, masker=None):
        self.hue = hue
        self.sat = sat
        self.val = val
        self.masker = masker

    def apply_filter(self, sprite):
        return AdjustHsvSprite(sprite, self.hue, self.sat, self.val, self.masker)
