# distutils: language = c++
"""Loader for PixelEditor.cpp"""
import cython
from .. import Vector
if cython.compiled:
    from cython.cimports.rubato.c_src import cPixelEditor as PE  # pyright: ignore
    from cython.cimports.cpython import array  # pyright: ignore
else:
    PE = None
    import array


def set_pixel(pixels: int, width: int, x: int, y: int, color: int):
    """
    C Header:
    ```c
    void setPixel(size_t _pixels, int width, int x, int y, size_t color)
    ```
    """
    PE.setPixel(pixels, width, x, y, color)


def set_pixel_safe(pixels: int, width: int, height: int, x: int, y: int, color: int):
    """
    C Header:
    ```c
    void setPixelSafe(size_t _pixels, int width, int height, int x, int y, size_t color)
    ```
    """
    PE.setPixelSafe(pixels, width, height, x, y, color)


def get_pixel(pixels: int, width: int, x: int, y: int):
    """
    C Header:
    ```c
    size_t getPixel(size_t _pixels, int width, int x, int y)
    ```
    """
    return PE.getPixel(pixels, width, x, y)


def get_pixel_safe(pixels: int, width: int, height: int, x: int, y: int):
    """
    C Header:
    ```c
    int getPixelSafe(size_t _pixels, int width, int height, int x, int y)
    ```
    """
    return PE.getPixelSafe(pixels, width, height, x, y)


def draw_line(
    pixels: int,
    width: int,
    height: int,
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    color: int,
    thickness: int = 1,
    aa: bool = False
):
    """
    C Header:
    ```c
    void drawLine(size_t _pixels, int width, int height, int x1, int y1, int x2, int y2, size_t color)
    ```
    """
    if aa:
        PE.aaDrawLine(pixels, width, height, x1, y1, x2, y2, color)
    elif thickness == 1:
        PE.drawLine(pixels, width, height, x1, y1, x2, y2, color)
    else:
        PE.drawLine(pixels, width, height, x1, y1, x2, y2, color, thickness)


def draw_circle(pixels: int, width: int, height: int, xc: int, yc: int, radius: int, color: int, thickness: int = 1):
    """
    C Header:
    ```c
    void drawCircle(size_t _pixels, int width, int height, int xc, int yc, int radius, size_t color)
    ```
    """
    if thickness == 1:
        PE.drawCircle(pixels, width, height, xc, yc, radius, color)
    else:
        PE.drawCircle(pixels, width, height, xc, yc, radius, color, thickness)


def fill_circle(pixels: int, width: int, height: int, xc: int, yc: int, radius: int, color: int):
    """
    C Header:
    ```c
    void fillCircle(size_t _pixels, int width, int height, int xc, int yc, int radius, size_t color)
    ```
    """
    PE.fillCircle(pixels, width, height, xc, yc, radius, color)


def draw_rect(pixels: int, width: int, height: int, x: int, y: int, w: int, h: int, color: int, thickness: int = 1):
    """
    C Header:
    ```c
    void drawRect(size_t _pixels, int width, int height, int x, int y, int w, int h, size_t color)
    ```
    """
    if thickness == 1:
        PE.drawRect(pixels, width, height, x, y, w, h, color)
    else:
        PE.drawRect(pixels, width, height, x, y, w, h, color, thickness)


def fill_rect(pixels: int, width: int, height: int, x: int, y: int, w: int, h: int, color: int):
    """
    C Header:
    ```c
    void fillRect(size_t _pixels, int width, int height, int x, int y, int w, int h, size_t color)
    ```
    """
    PE.fillRect(pixels, width, height, x, y, w, h, color)


def draw_poly(
    pixels: int, width: int, height: int, points: list[Vector], color: int, thickness: int = 1, aa: bool = False
):
    """
    Points can be a list of tuples or a list of Vectors. The conversion to void pointers is handled
    by this function.

    C Header:
    ```c
    void drawPoly(size_t _pixels, int width, int height, void* vx, void* vy, int len, size_t color)
    ```
    """
    vxt = []
    vyt = []
    for v in points:
        x, y = v.tuple_int()
        vxt.append(x)
        vyt.append(y)
    vx: array.array = array.array('i', vxt)
    vy: array.array = array.array('i', vyt)
    if aa:
        PE.aaDrawPoly(pixels, width, height, vx.data.as_voidptr, vy.data.as_voidptr, len(points), color)
    else:
        PE.drawPoly(pixels, width, height, vx.data.as_voidptr, vy.data.as_voidptr, len(points), color, thickness)


def fill_poly(pixels: int, width: int, height: int, points: list[Vector], color: int):
    """
    Points can be a list of tuples or a list of Vectors. The conversion to void pointers is handled
    by this function.

    C Header:
    ```c
    void fillPoly(size_t _pixels, int width, int height, void* vx, void* vy, int len, size_t color)
    ```
    Warning:
        This only works for convex polygons. (for now)
    """
    vxt = []
    vyt = []
    for v in points:
        x, y = v.tuple_int()
        vxt.append(x)
        vyt.append(y)
    vx: array.array = array.array('i', vxt)
    vy: array.array = array.array('i', vyt)
    PE.fillPolyConvex(pixels, width, height, vx.data.as_voidptr, vy.data.as_voidptr, len(points), color)


def clear_pixels(pixels: int, width: int, height: int):
    """
    C Header:
    ```c
    void clearPixels(size_t _pixels, int width, int height)
    ```
    """
    PE.clearPixels(pixels, width, height)


import math


def draw_antialiased_circle(
    pixels: int, width: int, base_aa: int, xc: int, yc: int, outer_radius: int, color: int, thickness: int = 1
):
    # TODO move to c
    def _draw_point(x: int, y: int, alpha: int):
        set_pixel(pixels, width, xc + x, yc + y, color & 0xFFFFFF00 | alpha)
        set_pixel(pixels, width, xc + x, yc - y, color & 0xFFFFFF00 | alpha)
        set_pixel(pixels, width, xc - x, yc + y, color & 0xFFFFFF00 | alpha)
        set_pixel(pixels, width, xc - x, yc - y, color & 0xFFFFFF00 | alpha)
        set_pixel(pixels, width, xc - y, yc - x, color & 0xFFFFFF00 | alpha)
        set_pixel(pixels, width, xc - y, yc + x, color & 0xFFFFFF00 | alpha)
        set_pixel(pixels, width, xc + y, yc - x, color & 0xFFFFFF00 | alpha)
        set_pixel(pixels, width, xc + y, yc + x, color & 0xFFFFFF00 | alpha)

    i = 0
    j = outer_radius
    last_fade_amount = 0
    fade_amount = 0

    MAX_OPAQUE = base_aa

    while i < j:
        height = math.sqrt(max(outer_radius * outer_radius - i * i, 0))
        fade_amount = MAX_OPAQUE * (math.ceil(height) - height)

        if fade_amount < last_fade_amount:
            # Opaqueness reset so drop down a row.
            j -= 1
        last_fade_amount = fade_amount

        # The API needs integers, so convert here now we've checked if
        # it dropped.
        fade_amount_i = int(fade_amount)

        # We're fading out the current j row, and fading in the next one down.
        _draw_point(i, j, int(MAX_OPAQUE) - fade_amount_i)
        _draw_point(i, j - 1, fade_amount_i)

        i += 1