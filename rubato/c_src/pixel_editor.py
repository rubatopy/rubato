# distutils: language = c++
"""Loader for PixelEditor.cpp"""
from cython.cimports.rubato.c_src import cPixelEditor as PE  # pyright: ignore
from cython.cimports.cpython import array  # pyright: ignore
import array  # pylint: disable=reimported


class PixelEditor:
    """The PixelEditor Wrapper"""

    @staticmethod
    def set_pixel(pixels, width, x, y, color):
        """
        C Header:
        ```c
        void setPixel(size_t _pixels, int width, int x, int y, size_t color)
        ```
        """
        PE.setPixel(pixels, width, x, y, color)

    @staticmethod
    def set_pixel_safe(pixels, width, height, x, y, color):
        """
        C Header:
        ```c
        void setPixelSafe(size_t _pixels, int width, int height, int x, int y, size_t color)
        ```
        """
        PE.setPixelSafe(pixels, width, height, x, y, color)

    @staticmethod
    def get_pixel(pixels, width, x, y):
        """
        C Header:
        ```c
        size_t getPixel(size_t _pixels, int width, int x, int y)
        ```
        """
        return PE.getPixel(pixels, width, x, y)

    @staticmethod
    def get_pixel_safe(pixels, width, height, x, y):
        """
        C Header:
        ```c
        int getPixelSafe(size_t _pixels, int width, int height, int x, int y)
        ```
        """
        return PE.getPixelSafe(pixels, width, height, x, y)

    @staticmethod
    def draw_line(pixels, width, height, x1, y1, x2, y2, color):
        """
        C Header:
        ```c
        void drawLine(size_t _pixels, int width, int height, int x1, int y1, int x2, int y2, size_t color)
        ```
        """
        PE.drawLine(pixels, width, height, x1, y1, x2, y2, color)

    @staticmethod
    def draw_circle(pixels, width, height, xc, yc, radius, color):
        """
        C Header:
        ```c
        void drawCircle(size_t _pixels, int width, int height, int xc, int yc, int radius, size_t color)
        ```
        """
        PE.drawCircle(pixels, width, height, xc, yc, radius, color)

    @staticmethod
    def fill_circle(pixels, width, height, xc, yc, radius, color):
        """
        C Header:
        ```c
        void fillCircle(size_t _pixels, int width, int height, int xc, int yc, int radius, size_t color)
        ```
        """
        PE.fillCircle(pixels, width, height, xc, yc, radius, color)

    @staticmethod
    def draw_rect(pixels, width, height, x, y, w, h, color):
        """
        C Header:
        ```c
        void drawRect(size_t _pixels, int width, int height, int x, int y, int w, int h, size_t color)
        ```
        """
        PE.drawRect(pixels, width, height, x, y, w, h, color)

    @staticmethod
    def fill_rect(pixels, width, height, x, y, w, h, color):
        """
        C Header:
        ```c
        void fillRect(size_t _pixels, int width, int height, int x, int y, int w, int h, size_t color)
        ```
        """
        PE.fillRect(pixels, width, height, x, y, w, h, color)

    @staticmethod
    def draw_poly(pixels, width, height, points, color):
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
        for (x, y) in points:
            vxt.append(x)
            vyt.append(y)
        vx: array.array = array.array('i', (*vxt,))
        vy: array.array = array.array('i', (*vyt,))
        PE.drawPoly(pixels, width, height, vx.data.as_voidptr, vy.data.as_voidptr, len(points), color)

    @staticmethod
    def clear_pixels(pixels, width, height):
        """
        C Header:
        ```c
        void clearPixels(size_t _pixels, int width, int height)
        ```
        """
        PE.clearPixels(pixels, width, height)
