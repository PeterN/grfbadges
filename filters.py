# pip install git+https://github.com/citymania-org/grf-py.git@ae4aeab54638cc206d3c969caae0e473a8636651#egg=grf

from PIL import Image
import numpy as np
import colorsys
import grf

rgb_to_hsv = np.vectorize(colorsys.rgb_to_hsv)
hsv_to_rgb = np.vectorize(colorsys.hsv_to_rgb)

CC_VALUE_TO_BRIGHTNESS = np.array([0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 32, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 55, 55, 57, 58, 59, 59, 61, 61, 63, 64, 64, 65, 67, 68, 69, 69, 70, 72, 72, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 96, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 125, 125, 126, 127, 128, 128, 130, 131, 132, 133, 134, 134, 136, 136, 136, 138, 138, 141, 117, 117, 119, 119, 119, 119, 122, 122, 123, 123, 124, 125, 125, 127, 127, 128, 128, 129, 130, 131, 131, 132, 133, 134, 134, 134, 136, 136, 137, 138, 138, 140, 117, 118, 118, 119, 119, 120, 121, 121, 122, 122, 123, 123, 124, 125, 125, 126, 127, 127, 128, 128, 129, 130, 130, 131, 131, 132, 132, 134, 134, 134, 135, 136, 136, 136, 137, 119, 119, 120, 120, 121, 122, 122, 123, 123, 124, 124, 125, 126, 126, 126, 127, 127, 128, 128, 129, 130, 130, 130, 131, 132, 132, 132, 133, 134, 134, 134, 136, 136, 136, 136, 137, 138, 121, 121, 121, 122, 122, 123, 123, 123, 123, 125, 125, 125, 125, 126, 126, 127, 127, 127, 128, 128, 128, 129, 130, 130, 131, 131, 131, 132, 132, 133, 133, 133, 134, 135, 135, 135, 135, 136, 136, 137, 138, 120, 120, 120, 121, 122, 122, 123, 123, 123, 123, 124, 124, 125, 125, 125, 126, 126, 127, 127, 127, 127, 128, 128, 128, 129, 129, 130, 130, 131, 131, 132, 132, 132, 133, 134, 134, 134, 134, 135, 135, 136, 136, 137, 138, 138, 138, 138, 139, 139, 121, 121, 121, 122, 122, 122, 122, 123, 123, 124, 124, 124, 124, 125, 125, 125, 126, 126, 126, 127, 127, 127, 127, 128, 128, 129, 129, 129, 130, 130, 131, 131, 131, 132, 132, 133, 133, 134, 134, 134, 135, 135, 135, 136, 137, 137, 137, 137, 137, 139, 139, 122, 123, 123, 123, 123, 124, 124, 124, 125, 125, 125, 126, 126, 126, 126, 127, 127, 127, 127, 128, 128, 129, 129, 130, 130, 130, 130, 131, 131, 132, 132, 132, 132, 133, 133, 133, 133, 134, 134, 135, 135, 135, 135, 136, 136, 137, 137, 137, 137, 138, 138, 139, 139, 139, 139, 140, 140, 141, 141, 141, 141, 142, 142, 142, 142, 143, 143, 144, 144, 144, 144, 145, 145, 146, 146, 147, 147, 148, 148, 149, 149, 149, 149, 151, 151, 151, 151, 152, 152, 153, 153, 153, 153, 153, 153, 155, 155, 155, 155, 156, 156, 157, 157, 158, 158, 159, 159, 159, 159, 160, 160, 160, 160, 162, 162, 163, 163, 163, 163, 164, 164, 166, 166, 166, 166, 166])
CC_VALUE_TO_INDEX = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7])

CC_ONE = (0, 0xC6, CC_VALUE_TO_BRIGHTNESS, CC_VALUE_TO_INDEX) # First company colour range
CC_TWO = (0, 0x50, CC_VALUE_TO_BRIGHTNESS, CC_VALUE_TO_INDEX) # Second company colour range

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

class MakeCCSprite(grf.SpriteWrapper):
    def __init__(self, sprite, maskercc1, maskercc2):
        super().__init__((sprite, ))
        self.sprite = sprite
        self.maskercc1 = maskercc1
        self.maskercc2 = maskercc2
        self.w = None
        self.h = None

    def apply_cc(self, npimg, mask, cc, cc_mask):
        _fingerprint, first, vtb, vti = cc

        value = npimg[cc_mask][:, 0].astype(np.uint16) + npimg[cc_mask][:, 1]
        npimg[cc_mask, 0] = vtb[value]
        npimg[cc_mask, 1] = vtb[value]
        npimg[cc_mask, 2] = vtb[value]
        mask[cc_mask] = vti[value] + first

    def get_image(self):
        return self.sprite.get_image()

    def get_data_layers(self, context):
        w, h, img, bpp = self._do_get_image(context)

        timer = context.start_timer()

        self.bpp = bpp
        npimg = np.asarray(img).copy()
        mask = np.zeros((h, w), dtype=np.uint8)

        if self.maskercc1 is not None: maskcc1 = self.maskercc1.make_mask(npimg)
        if self.maskercc2 is not None: maskcc2 = self.maskercc2.make_mask(npimg)
        if self.maskercc1 is not None: self.apply_cc(npimg, mask, CC_ONE, maskcc1)
        if self.maskercc2 is not None: self.apply_cc(npimg, mask, CC_TWO, maskcc2)

        if bpp == grf.BPP_32:
            rgb, alpha = npimg[:, :, :3], npimg[:, :, 3]
        else:
            rgb, alpha = npimg, None

        timer.count_custom('Mask-to-CC processing')

        return w, h, rgb, alpha, mask

    def get_fingerprint(self):
        return {
            'class': self.__class__.__name__,
            'sprite': self.sprite.get_fingerprint(),
            'masker1': None if self.maskercc1 is None else self.maskercc1.get_fingerprint(),
            'masker2': None if self.maskercc2 is None else self.maskercc2.get_fingerprint(),
        }

class MakeCCFilter(SpriteFilter):
    def __init__(self, maskercc1 = None, maskercc2 = None):
        self.maskercc1 = maskercc1
        self.maskercc2 = maskercc2

    def apply_filter(self, sprite):
        return MakeCCSprite(sprite, self.maskercc1, self.maskercc2)
