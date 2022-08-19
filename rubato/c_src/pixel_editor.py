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


def set_pixel(pixels: int, width: int, height: int, x: int, y: int, color: int, blending: bool = False):
    PE.setPixel(pixels, width, height, x, y, color, blending)


def get_pixel(pixels: int, width: int, height: int, x: int, y: int):
    return PE.getPixel(pixels, width, height, x, y)


def clear_pixels(pixels: int, width: int, height: int):
    PE.clearPixels(pixels, width, height)


def draw_line(
    pixels: int,
    width: int,
    height: int,
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    color: int,
    aa: bool = False,
    blending: bool = False,
    thickness: int = 1,
):
    PE.drawLine(pixels, width, height, x1, y1, x2, y2, color, aa, blending, thickness)


def draw_circle(
    pixels: int,
    width: int,
    height: int,
    xc: int,
    yc: int,
    radius: int,
    color: int,
    aa: bool = False,
    blending: bool = False,
    thickness: int = 1
):
    PE.drawCircle(pixels, width, height, xc, yc, radius, color, aa, blending, thickness)


def fill_circle(
    pixels: int,
    width: int,
    height: int,
    xc: int,
    yc: int,
    radius: int,
    color: int,
    blending: bool = False,
):
    PE.fillCircle(pixels, width, height, xc, yc, radius, color, blending)


def draw_rect(
    pixels: int,
    width: int,
    height: int,
    x: int,
    y: int,
    w: int,
    h: int,
    color: int,
    blending: bool = False,
    thickness: int = 1,
):
    PE.drawRect(pixels, width, height, x, y, w, h, color, blending, thickness)


def fill_rect(
    pixels: int,
    width: int,
    height: int,
    x: int,
    y: int,
    w: int,
    h: int,
    color: int,
    blending: bool = False,
):
    PE.fillRect(pixels, width, height, x, y, w, h, color, blending)


def draw_poly(
    pixels: int,
    width: int,
    height: int,
    points: list[Vector],
    color: int,
    aa: bool = False,
    blending: bool = False,
    thickness: int = 1,
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
    PE.drawPoly(
        pixels, width, height, vx.data.as_voidptr, vy.data.as_voidptr, len(points), color, aa, blending, thickness
    )


def fill_poly(pixels: int, width: int, height: int, points: list[Vector], color: int, blending: bool = False):
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
    PE.fillPolyConvex(pixels, width, height, vx.data.as_voidptr, vy.data.as_voidptr, len(points), color, blending)
