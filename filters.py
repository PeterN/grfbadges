# pip install git+https://github.com/citymania-org/grf-py.git@ae4aeab54638cc206d3c969caae0e473a8636651#egg=grf

from PIL import Image
import numpy as np
import colorsys
import grf

rgb_to_hsv = np.vectorize(colorsys.rgb_to_hsv)
hsv_to_rgb = np.vectorize(colorsys.hsv_to_rgb)

class SpriteFilter:
    def apply_filter(self, sprite):
        raise NotImplementedError

class AdjustHsvSprite(grf.SpriteWrapper):
    def __init__(self, sprite, hue, sat, val):
        super().__init__((sprite, ))
        self.sprite = sprite
        self.hue = hue / 360.
        self.sat = sat
        self.val = val
        self.w = None
        self.h = None

    def adjust_hsv(self, arr):
        r, g, b, a = np.rollaxis(arr, axis=-1)
        h, s, v = rgb_to_hsv(r, g, b)
        h = (h + self.hue) % 1.
        s = s * self.sat
        v = v * self.val
        r, g, b = hsv_to_rgb(h, s, v)
        arr = np.dstack((r, g, b, a))
        return arr

    def get_image(self):
        img, bpp = self.sprite.get_image()
        arr = np.array(np.asarray(img).astype(float))
        img = Image.fromarray(self.adjust_hsv(arr).astype('uint8'), 'RGBA')
        return img, bpp

    def get_fingerprint(self):
        return {
            'class': self.__class__.__name__,
            'sprite': self.sprite.get_fingerprint(),
            'hue': self.hue,
            'sat': self.sat,
            'val': self.val,
        }

class AdjustHsvFilter(SpriteFilter):
    def __init__(self, *, hue = 0., sat = 1., val = 1.):
        self.hue = hue
        self.sat = sat
        self.val = val

    def apply_filter(self, sprite):
        return AdjustHsvSprite(sprite, self.hue, self.sat, self.val)
