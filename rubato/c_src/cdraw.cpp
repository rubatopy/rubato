#include <cstdint>
#include <cstring>
#include <limits.h>
#include <math.h>
#include <cstdlib>
#include <iostream>
#include <algorithm>

/***********************************************************************************************************************

BUFFER FUNCTIONS

***********************************************************************************************************************/

inline size_t createPixelBuffer(int width, int height) {
    return (size_t) calloc(width * height, sizeof(uint32_t));
}

inline void freePixelBuffer(size_t buffer) {
    free((void*) buffer);
}

inline size_t clonePixelBuffer(size_t _source, int width, int height) {
    uint32_t* source = (uint32_t*) _source;
    uint32_t* newBuffer = new uint32_t[width * height];
    std::copy(source, source + width * height, newBuffer);
    return (size_t) newBuffer;
}

/***********************************************************************************************************************

PIXEL FUNCTIONS

***********************************************************************************************************************/

// Sets the pixel at x, y to the color specified. Clips at the edges.
inline void setPixel(size_t _pixels, int width, int height, int x, int y, size_t color, bool blending = false) {
    if (x < width && y < height && x >= 0 && y >= 0) {
        int off = y * width + x;
        uint32_t added = (uint32_t) color;
        uint32_t* pixels = (uint32_t*) _pixels;

        if (!blending) {
            pixels[off] = added;
        } else {
            uint32_t rMask = 0xFF000000;
            uint32_t gMask = 0x00FF0000;
            uint32_t bMask = 0x0000FF00;
            uint32_t aMask = 0x000000FF;

            uint32_t base = pixels[off];

            uint8_t baseA = base & aMask;
            uint8_t addedA = added & aMask;
            uint8_t invAddedA = 0xFF - addedA;

            uint8_t addedRed = (added & rMask) >> 24;
            uint8_t addedGreen = (added & gMask) >> 16;
            uint8_t addedBlue = (added & bMask) >> 8;

            uint8_t baseRed = (base & rMask) >> 24;
            uint8_t baseGreen = (base & gMask) >> 16;
            uint8_t baseBlue = (base & bMask) >> 8;

            uint8_t newA = 0xFF - ((invAddedA * (0xFF - baseA)) >> 8);

            uint8_t newRed = (addedRed * addedA / newA) + (baseRed * ((baseA * invAddedA) >> 8) / newA);
            uint8_t newGreen = (addedGreen * addedA / newA) + (baseGreen * ((baseA * invAddedA) >> 8) / newA);
            uint8_t newBlue = (addedBlue * addedA / newA) + (baseBlue * ((baseA * invAddedA) >> 8) / newA);


            pixels[off] = (newRed << 24) | (newGreen << 16) | (newBlue << 8) | newA;
        }
    }
}

// Gets the pixel but returns 0 if the pixel is outside the surface.
inline int getPixel(size_t _pixels, int width, int height, int x, int y) {
    if (x < width && y < height && x >= 0 && y >= 0) {
        return (int) ((uint32_t*) _pixels)[y * width + x];
    }
    return 0;
}

inline void clearPixels(size_t _pixels, int width, int height) {
    memset((size_t*) _pixels, 0, width * height * 4);
}

inline void blit(size_t _source, size_t _destination, int sw, int sh, int dw, int dh, int srx, int sry, int srw, int srh, int drx, int dry, int drw, int drh) {
    for (int y = 0; y < srh; y++) {
        for (int x = 0; x < srw; x++) {
            if (x < drw && y < drh) {
                setPixel(_destination, dw, dh, drx + x, dry + y, getPixel(_source, sw, sh, srx + x, sry + y), true);
            }
        }
    }
}


/***********************************************************************************************************************

LINE FUNCTIONS

***********************************************************************************************************************/

// Draws a line from (x1, y1) to (x2, y2) with the specified color.
inline void _drawLine(size_t _pixels, int width, int height, int x1, int y1, int x2, int y2, size_t color, bool blending) {
    bool x_l = x1 < x2;
    bool y_l = y1 < y2;

    int dx = x_l ? x2 - x1 : x1 - x2;
    int dy = y_l ? y2 - y1 : y1 - y2;
    int sx = x_l ? 1 : -1;
    int sy = y_l ? 1 : -1;

    int err = dx - dy;
    while (true) {
        setPixel(_pixels, width, height, x1, y1, color, blending);
        if (x1 == x2 && y1 == y2) {
            break;
        }
        int e2 = 2 * err;
        if (e2 > -dy) {
            err -= dy;
            x1 += sx;
        }
        if (e2 < dx) {
            err += dx;
            y1 += sy;
        }
    }
}

// Draws a line from (x1, y1) to (x2, y2) with the specified color and thickness.
inline void _drawLine(size_t _pixels, int width, int height, int x1, int y1, int x2, int y2, size_t color, bool blending, int thickness) {
    if (thickness == 1) {
        _drawLine(_pixels, width, height, x1, y1, x2, y2, color, blending);
        return;
    }
    int s, f;
    if (thickness % 2 == 0) {
        s = -thickness / 2;
        f = thickness / 2;
    } else {
        s = -(thickness - 1) / 2;
        f = ((thickness - 1) / 2) + 1;
    }
    for (int x = s; x < f; x++) {
        for (int y = s; y < f; y++) {
            _drawLine(_pixels, width, height, x1 + x, y1 + y, x2 + x, y2 + y, color, blending);
        }
    }
}

// Draws an antialiased line from (x1, y1) to (x2, y2) with the specified color.
inline void _aaDrawLine(size_t _pixels, int width, int height, int x1, int y1, int x2, int y2, size_t color, bool blending) {
    auto fpart = [](double x) { return (double) (x - floor(x)); };
    auto rfpart = [fpart](double x) { return 1 - fpart(x); };

    uint32_t color_u = (uint32_t) color;
    uint32_t colorRGB = color_u & 0xFFFFFF00;
    uint8_t colorA = color_u & 0x000000FF;

    bool steep = abs(y2 - y1) > abs(x2 - x1);
    if (steep) {
        int temp = x1;
        x1 = y1;
        y1 = temp;
        temp = x2;
        x2 = y2;
        y2 = temp;
    }
    if (x1 > x2) {
        int temp = x1;
        x1 = x2;
        x2 = temp;
        temp = y1;
        y1 = y2;
        y2 = temp;
    }

    int dx = x2 - x1;
    int dy = y2 - y1;

    double gradient = 1;
    if (dx != 0) {
        gradient = (double) dy / (double) dx;
    }

    double intery = y1 + gradient;

    if (steep) {
        setPixel(_pixels, width, height, y1, x1, color, blending);
        setPixel(_pixels, width, height, y2, x2, color, blending);

        for (int x = x1 + 1; x < x2; x++) {
            setPixel(_pixels, width, height, (int) floor(intery), x, colorRGB | (uint8_t) (rfpart(intery) * colorA), blending);
            setPixel(_pixels, width, height, (int) floor(intery) + 1, x, colorRGB | (uint8_t) (fpart(intery) * colorA), blending);
            intery += gradient;
        }
    } else {
        setPixel(_pixels, width, height, x1, y1, color, blending);
        setPixel(_pixels, width, height, x2, y2, color, blending);

        for (int x = x1 + 1; x < x2; x++) {
            setPixel(_pixels, width, height, x, (int) floor(intery), colorRGB | (uint8_t) (rfpart(intery) * colorA), blending);
            setPixel(_pixels, width, height, x, (int) floor(intery) + 1, colorRGB | (uint8_t) (fpart(intery) * colorA), blending);
            intery += gradient;
        }
    }
}

inline void _aaDrawLine(size_t _pixels, int width, int height, int x1, int y1, int x2, int y2, size_t color, bool blending, int thickness) {
    if (thickness == 1) {
        _aaDrawLine(_pixels, width, height, x1, y1, x2, y2, color, blending);
        return;
    }
    int s, f;
    if (thickness % 2 == 0) {
        s = -thickness / 2;
        f = thickness / 2;
    } else {
        s = -(thickness - 1) / 2;
        f = ((thickness - 1) / 2) + 1;
    }
    for (int x = s; x < f; x++) {
        for (int y = s; y < f; y++) {
            if (x == s || y == s || x == f - 1 || y == f - 1) {
                _aaDrawLine(_pixels, width, height, x1 + x, y1 + y, x2 + x, y2 + y, color, blending);
            } else {
                _drawLine(_pixels, width, height, x1 + x, y1 + y, x2 + x, y2 + y, color, blending);
            }
        }
    }
}

// This is the drawLine accessible from python.
inline void drawLine(size_t _pixels, int width, int height, int x1, int y1, int x2, int y2, size_t color, bool aa, bool blending, int thickness) {
    if (aa) _aaDrawLine(_pixels, width, height, x1, y1, x2, y2, color, blending, thickness);
    else _drawLine(_pixels, width, height, x1, y1, x2, y2, color, blending, thickness);
}

/***********************************************************************************************************************

CIRCLE FUNCTIONS

***********************************************************************************************************************/

// Draws a circle with the specified color.
inline void _drawCircle(size_t _pixels, int width, int height, int xc, int yc, int radius, size_t color, bool blending) {
    int x = radius;
    int y = 0;
    int E = -x;
    while (x >= y) {
        setPixel(_pixels, width, height, xc + x, yc + y, color, blending);
        setPixel(_pixels, width, height, xc - x, yc - y, color, blending);
        setPixel(_pixels, width, height, xc + y, yc + x, color, blending);
        setPixel(_pixels, width, height, xc - y, yc + x, color, blending);
        setPixel(_pixels, width, height, xc + x, yc - y, color, blending);
        setPixel(_pixels, width, height, xc - x, yc + y, color, blending);
        setPixel(_pixels, width, height, xc + y, yc - x, color, blending);
        setPixel(_pixels, width, height, xc - y, yc - x, color, blending);

        E += 2 * (y++) + 1;
        if (E >= 0) {
            E -= 2 * (x--) + 1;
        }
    }
}

// Draws an circle with the specified color and thickness.
inline void _drawCircle(size_t _pixels, int width, int height, int xc, int yc, int radius, size_t color, bool blending, int thickness) {
    if (thickness == 1) {
        _drawCircle(_pixels, width, height, xc, yc, radius, color, blending);
        return;
    }
    int inner, outer;
    if (thickness % 2 == 0) {
        outer = radius + (thickness / 2) - 1;
        inner = radius - (thickness / 2);
    } else {
        outer = radius + (thickness / 2);
        inner = radius - (thickness / 2);
    }
    int xo = outer;
    int xi = inner;
    int y = 0;
    int erro = 1 - xo;
    int erri = 1 - xi;

    while (xo >= y) {
        _drawLine(_pixels, width, height, xc + xi, yc + y, xc + xo, yc + y, color, blending);
        _drawLine(_pixels, width, height, xc + y, yc + xi, xc + y, yc + xo, color, blending);
        _drawLine(_pixels, width, height, xc - xo, yc + y, xc - xi, yc + y, color, blending);
        _drawLine(_pixels, width, height, xc - y, yc + xi, xc - y, yc + xo, color, blending);
        _drawLine(_pixels, width, height, xc - xo, yc - y, xc - xi, yc - y, color, blending);
        _drawLine(_pixels, width, height, xc - y, yc - xo, xc - y, yc - xi, color, blending);
        _drawLine(_pixels, width, height, xc + xi, yc - y, xc + xo, yc - y, color, blending);
        _drawLine(_pixels, width, height, xc + y, yc - xo, xc + y, yc - xi, color, blending);

        y++;

        if (erro < 0) {
            erro += 2 * y + 1;
        } else {
            xo--;
            erro += 2 * (y - xo + 1);
        }

        if (y > inner) {
            xi = y;
        } else {
            if (erri < 0) {
                erri += 2 * y + 1;
            } else {
                xi--;
                erri += 2 * (y - xi + 1);
            }
        }
    }
}

// Draws an anti-aliased circle with the specified color.
inline void _aaDrawCircle(size_t pixels, int width, int _height, int xc, int yc, int outer_radius, size_t color, bool blending) {

    uint32_t rgbMask = 0xFFFFFF00;
    auto _draw_point = [pixels, width, _height, xc, yc, color, rgbMask, blending](int x, int y, uint8_t alpha) {
        setPixel(pixels, width, _height, xc + x, yc + y, (size_t) ((color & rgbMask) | alpha), blending);
        setPixel(pixels, width, _height, xc + x, yc - y, (size_t) ((color & rgbMask) | alpha), blending);
        setPixel(pixels, width, _height, xc - x, yc + y, (size_t) ((color & rgbMask) | alpha), blending);
        setPixel(pixels, width, _height, xc - x, yc - y, (size_t) ((color & rgbMask) | alpha), blending);
        setPixel(pixels, width, _height, xc - y, yc - x, (size_t) ((color & rgbMask) | alpha), blending);
        setPixel(pixels, width, _height, xc - y, yc + x, (size_t) ((color & rgbMask) | alpha), blending);
        setPixel(pixels, width, _height, xc + y, yc - x, (size_t) ((color & rgbMask) | alpha), blending);
        setPixel(pixels, width, _height, xc + y, yc + x, (size_t) ((color & rgbMask) | alpha), blending);
    };
    auto max = [](int a, int b) {
        return a > b ? a : b;
    };

    int i = 0;
    int j = outer_radius;
    double height;

    int sq_r = outer_radius * outer_radius;

    uint8_t last_fade_amount = 0;
    uint8_t fade_amount = 0;

    uint8_t MAX_OPAQUE = ((uint8_t) color) & 0x000000FF;

    while (i < j) {
        height = sqrt(max(sq_r - i * i, 0));
        fade_amount = (uint8_t) (MAX_OPAQUE * (ceil(height) - height));

        if (fade_amount < last_fade_amount) {
            // Opaqueness reset so drop down a row.
            j -= 1;
        }
        last_fade_amount = fade_amount;

        // We're fading out the current j row, and fading in the next one down.
        _draw_point(i, j, MAX_OPAQUE - fade_amount);
        _draw_point(i, j - 1, fade_amount);

        i += 1;
    }
}

inline void _aaDrawCircle(size_t _pixels, int width, int height, int xc, int yc, int outer_radius, size_t color, bool blending, int thickness) {
    if (thickness == 1) {
        _aaDrawCircle(_pixels, width, height, xc, yc, outer_radius, color, blending);
        return;
    }
    int inner, outer;
    if (thickness % 2 == 0) {
        outer = outer_radius + (thickness / 2) - 1;
        inner = outer_radius - (thickness / 2);
    } else {
        outer = outer_radius + (thickness / 2);
        inner = outer_radius - (thickness / 2);
    }
    _drawCircle(_pixels, width, height, xc, yc, outer_radius, color, blending, thickness);
    _aaDrawCircle(_pixels, width, height, xc, yc, inner, color, blending);
    _aaDrawCircle(_pixels, width, height, xc, yc, outer, color, blending);
}

// Fills a circle with the specified color.
inline void _fillCircle(size_t _pixels, int width, int height, int xc, int yc, int radius, size_t color, bool blending) {
    int x = radius;
    int y = 0;
    int E = -x;
    while (x >= y) {
        _drawLine(_pixels, width, height, xc + x, yc + y, xc - x, yc + y, color, blending);
        _drawLine(_pixels, width, height, xc - y, yc + x, xc + y, yc + x, color, blending);
        _drawLine(_pixels, width, height, xc - x, yc - y, xc + x, yc - y, color, blending);
        _drawLine(_pixels, width, height, xc - y, yc - x, xc + y, yc - x, color, blending);

        E += 2 * (y++) + 1;
        if (E >= 0) {
            E -= 2 * (x--) + 1;
        }
    }
}

// Circle function accessible from python.
inline void drawCircle(size_t _pixels, int width, int height, int xc, int yc, int radius, size_t borderColor, size_t fillColor, bool aa, bool blending, int thickness) {
    if (fillColor != 0) {
        _fillCircle(_pixels, width, height, xc, yc, radius, fillColor, blending);
    }
    if (borderColor != 0) {
        if (aa) {
            _aaDrawCircle(_pixels, width, height, xc, yc, radius, borderColor, blending, thickness);
        } else {
            _drawCircle(_pixels, width, height, xc, yc, radius, borderColor, blending, thickness);
        }
    } else if (aa) {
        _aaDrawCircle(_pixels, width, height, xc, yc, radius, fillColor, blending);
    }
}



/***********************************************************************************************************************

POLYGON FUNCTIONS

***********************************************************************************************************************/

// Fill a polygon with the specified color.
inline void _drawPoly(size_t _pixels, int width, int height, void* vx, void* vy, int len, size_t color, bool blending, int thickness) {
    int* v_x = (int*) vx;
    int* v_y = (int*) vy;
    for (int i = 0; i < len; i++) {
        _drawLine(_pixels, width, height, v_x[i], v_y[i], v_x[(i + 1) % len], v_y[(i + 1) % len], color, blending, thickness);
    }
}

// Fill an antialiased polygon with the specified color.
inline void _aaDrawPoly(size_t _pixels, int width, int height, void* vx, void* vy, int len, size_t color, bool blending, int thickness) {
    int* v_x = (int*) vx;
    int* v_y = (int*) vy;

    for (int i = 0; i < len; i++) {
        _aaDrawLine(_pixels, width, height, v_x[i], v_y[i], v_x[(i + 1) % len], v_y[(i + 1) % len], color, blending, thickness);
    }
}

// Fill a polygon with the specified color.
inline void _fillPolyConvex(size_t _pixels, int width, int height, void* vx, void* vy, int len, size_t color, bool blending) {
    int* v_x = (int*) vx;
    int* v_y = (int*) vy;
    int* v_x_min = new int[height];
    int* v_x_max = new int[height];

    for (int i = 0; i < height; i++) {
        v_x_min[i] = width + 1;
        v_x_max[i] = -1;
    }


    // line algo
    for (int i = 0; i < len; i++) {
        int x1 = v_x[i], y1 = v_y[i], x2 = v_x[(i + 1) % len], y2 = v_y[(i + 1) % len];
        bool x_l = x1 < x2;
        bool y_l = y1 < y2;

        int dx = x_l ? x2 - x1 : x1 - x2;
        int dy = y_l ? y2 - y1 : y1 - y2;
        int sx = x_l ? 1 : -1;
        int sy = y_l ? 1 : -1;

        int err = dx - dy;
        while (true) {

            // logic for min and max
            if (0 <= y1 && y1 < height && x1 < v_x_min[y1]) {
                v_x_min[y1] = x1;
            }
            if (0 <= y1 && y1 < height && x1 > v_x_max[y1]) {
                v_x_max[y1] = x1;
            }
            // end


            if (x1 == x2 && y1 == y2) {
                break;
            }
            int e2 = 2 * err;
            if (e2 > -dy) {
                err -= dy;
                x1 += sx;
            }
            if (e2 < dx) {
                err += dx;
                y1 += sy;
            }
        }
    }

    // draw lines across to fill
    for (int i = 0; i < height; i++) {
        if (v_x_max[i] == -1) {
            continue;
        }
        _drawLine(_pixels, width, height, v_x_min[i], i, v_x_max[i], i, color, blending);
    }
    delete[] v_x_min;
    delete[] v_x_max;
}


// Polygon function accessible from python.
inline void drawPoly(size_t _pixels, int width, int height, void* vx, void* vy, int len, size_t borderColor, size_t fillColor, bool aa, bool blending, int thickness) {
    if (fillColor != 0) {
        _fillPolyConvex(_pixels, width, height, vx, vy, len, fillColor, blending);
    }
    if (borderColor != 0) {
        if (aa) {
            _aaDrawPoly(_pixels, width, height, vx, vy, len, borderColor, blending, thickness);
        } else {
            _drawPoly(_pixels, width, height, vx, vy, len, borderColor, blending, thickness);
        }
    } else if (aa) {
        _aaDrawPoly(_pixels, width, height, vx, vy, len, fillColor, blending, 1);
    }
}

/***********************************************************************************************************************

RECTANGLE FUNCTIONS

***********************************************************************************************************************/

// Draw a rectangle with the specified color.
inline void _drawRect(size_t _pixels, int width, int height, int x, int y, int w, int h, size_t color, bool blending) {
    for (int i = x; i < w + x; i++) {
        setPixel(_pixels, width, height, i, y, color, blending);
        setPixel(_pixels, width, height, i, y + h - 1, color, blending);
    }
    for (int i = y; i < h + y; i++) {
        setPixel(_pixels, width, height, x, i, color, blending);
        setPixel(_pixels, width, height, x + w - 1, i, color, blending);
    }
}

// Draws a rectangle with the specified color and thickness.
inline void _drawRect(size_t _pixels, int width, int height, int x, int y, int w, int h, size_t color, bool blending, int thickness) {
    if (thickness == 1) {
        _drawRect(_pixels, width, height, x, y, w, h, color, blending);
        return;
    } else {
        int s, f;
        if (thickness % 2 == 0) {
            s = -thickness / 2;
            f = thickness / 2;
        } else {
            s = -(thickness - 1) / 2;
            f = ((thickness - 1) / 2) + 1;
        }
        for (int i = s; i < f; i++) {
            _drawRect(_pixels, width, height, x + i, y + i, w - (2 * i), h - (2 * i), color, blending);
        }
    }
}

// Fill a rectangle with the specified color.
inline void _fillRect(size_t _pixels, int width, int height, int x, int y, int w, int h, size_t color, bool blending) {
    for (int i = y; i < h + y; i++) {
        for (int j = x; j < w + x; j++) {
            setPixel(_pixels, width, height, j, i, color, blending);
        }
    }
}

// Rectangle function called from python.
inline void drawRect(size_t _pixels, int width, int height, int x, int y, int w, int h, size_t borderColor, size_t fillColor, bool blending, int thickness) {
    if (fillColor != 0) {
        _fillRect(_pixels, width, height, x, y, w, h, fillColor, blending);
    }
    if (borderColor != 0) {
        _drawRect(_pixels, width, height, x, y, w, h, borderColor, blending, thickness);
    }
}
