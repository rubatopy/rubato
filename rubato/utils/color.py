from rubato.utils import PMath


class HSV:
    def __init__(self, h, s, v):
        self.h: float = h
        self.s: float = s
        self.v: float = v

    def set(self, value):
        self.h = value
        self.s = value
        self.v = value

    def __eq__(self, other):
        if type(other) == type(self):
            return \
                abs(self.h - other.h) < 0.0001 and \
                abs(self.s - other.s) < 0.0001 and \
                abs(self.v - other.v) < 0.0001
        return False

    @property
    def values(self):
        return [self.h, self.s, self.v]

    def check_values(self):
        self.h = PMath.clamp(self.h, 0, 255)
        self.s = PMath.clamp(self.s, 0, 255)
        self.v = PMath.clamp(self.v, 0, 255)


class RGB:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
        self.check_values()

    def set(self, value):
        self.r = value
        self.g = value
        self.b = value
        self.check_values()

    def __eq__(self, other):
        if type(other) == type(self):
            return \
                abs(self.r - other.r) < 0.0001 and \
                abs(self.g - other.g) < 0.0001 and \
                abs(self.b - other.b) < 0.0001
        return False

    @property
    def values(self):
        return [self.r, self.g, self.b]

    def check_values(self):
        self.r = PMath.clamp(self.r, 0, 255)
        self.g = PMath.clamp(self.b, 0, 255)
        self.b = PMath.clamp(self.g, 0, 255)


class Color:
    # colors from https://www.rapidtables.com/web/color/RGB_Color.html
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    lime = (0, 255, 0)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)
    cyan = aqua = (0, 255, 255)
    magenta = fuchsia = (255, 0, 255)
    silver = (192, 192, 192)
    gray = (128, 128, 128)
    maroon = (128, 0, 0)
    olive = (128, 128, 0)
    green = (0, 128, 0)
    purple = (128, 0, 128)
    teal = (0, 128, 128)
    navy = (0, 0, 128)

    # @staticmethod
    # def lerp(a: Color.RGB, b: Color.RGB, t):
    #     t = PMath.clamp(t, 0, 1)
    #     return RGB(
    #     a.r + (b.r - a.r) * t,
    #     a.g + (b.g - a.g) * t,
    #     a.b + (b.b - a.b) * t,
    #     a.a + (b.a - a.a) * t
    #     )

    class HSV(HSV):
        def __init__(self, h, s, v):
            super().__init__(h,s,v)

    class RGB(RGB):
        def __init__(self, r, g, b):
            super().__init__(r, g, b)

    @staticmethod
    def rgb_to_hsv(color_in: RGB):
        out = Color.HSV()

        cmax = max(color_in.r, color_in.g, color_in.b)  # maximum of r, g, b
        cmin = min(color_in.r, color_in.g, color_in.b)  # minimum of r, g, b
        diff = cmax - cmin  # diff of cmax and cmin.

        out.v = cmax
        delta = cmax - cmin
        if delta == 0:
            return out
        if cmax > 0.0:
            out.s = (delta / cmax)
        else:
            return out

        if color_in.r == cmax:
            out.h = (color_in.g - color_in.b) / delta  # between yellow & magenta
        elif color_in.g == cmax:
            out.h = 2.0 + (color_in.b - color_in.r) / delta  # between cyan & yellow
        else:
            out.h = 4.0 + (color_in.r - color_in.g) / delta  # between magenta & cyan

        out.h *= 60.0  # degrees

        if out.h < 0.0:
            out.h += 360.0

        return out

    @staticmethod
    def hsv_to_rgb(color_in: HSV):
        out = Color.RGB()
        if color_in.s == 0:
            out.set(color_in.v)
        hh = color_in.h
        if hh >= 360.0:
            hh = 0.0
        hh /= 60.0
        i = int(hh)
        ff = hh - i
        p = color_in.v * (1.0 - color_in.s)
        q = color_in.v * (1.0 - (color_in.s * ff))
        t = color_in.v * (1.0 - (color_in.s * (1.0 - ff)))
        if i == 0:
            out.r = color_in.v
            out.g = t
            out.b = p
        elif i == 1:
            out.r = q
            out.g = color_in.v
            out.b = p
        elif i == 2:
            out.r = p
            out.g = color_in.v
            out.b = t
        elif i == 3:
            out.r = p
            out.g = q
            out.b = color_in.v
        elif i == 4:
            out.r = t
            out.g = p
            out.b = color_in.v
        elif i == 5:
            out.r = color_in.v
            out.g = p
            out.b = q
        else:
            out.r = color_in.v
            out.g = p
            out.b = q

        return out
