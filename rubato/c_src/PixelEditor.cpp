#include <cstdint>
#include <cstring>
#include <limits.h>
#include <math.h>
#include <cstdlib>

#include <iostream> // get rid of this

#define elif else if

// Sets the pixel at x, y to the color specified. Clips at the edges.
inline void setPixel(size_t _pixels, int width, int height, int x, int y, size_t color, bool blending = false) {
    if (x < width && y < height && x >= 0 && y >= 0) {
        uint32_t rMask = 0xFF000000;
        uint32_t gMask = 0x00FF0000;
        uint32_t bMask = 0x0000FF00;
        uint32_t aMask = 0x000000FF;
        int off = y * width + x;
        uint32_t added = (uint32_t) color;
        uint32_t* pixels = (uint32_t*) _pixels;

        if (!blending) {
            pixels[off] = added;
        } else {
            uint32_t base = pixels[off];
            double baseA = (pixels[off] & aMask) / 255.0;
            double addedA = (added & aMask) / 255.0;

            uint8_t addedRed = ((added & rMask) >> 24);
            uint8_t addedGreen = ((added & gMask) >> 16);
            uint8_t addedBlue = ((added & bMask) >> 8);

            uint8_t baseRed = ((base & rMask) >> 24);
            uint8_t baseGreen = ((base & gMask) >> 16);
            uint8_t baseBlue = ((base & bMask) >> 8);

            double newA = 1 - (1 - addedA) * (1 - baseA);
            uint8_t newRed = round((addedRed * addedA / newA) + (baseRed * baseA * (1 - addedA) / newA));
            uint8_t newGreen = round((addedGreen * addedA / newA) + (baseGreen * baseA * (1 - addedA) / newA));
            uint8_t newBlue = round((addedBlue * addedA / newA) + (baseBlue * baseA * (1 - addedA) / newA));

            pixels[off] = (newRed << 24) | (newGreen << 16) | (newBlue << 8) | (uint8_t) (newA * 255);
        }
    }
}

// Gets the pixel but returns 0 if the pixel is outside the surface.
inline int getPixel(size_t _pixels, int width, int height, int x, int y) {
    if (x < width && y < height && x >= 0 && y >= 0) {
        return (int) ((uint32_t*) _pixels)[y * width + x];
    }
    return NULL;
}

// Draws a line from (x1, y1) to (x2, y2) with the specified color.
inline void _drawLine(size_t _pixels, int width, int height, int x1, int y1, int x2, int y2, size_t color, bool blending = false) {
    bool x_l = x1 < x2;
    bool y_l = y1 < y2;

    int dx = x_l ? x2 - x1 : x1 - x2;
    int dy = y_l ? y2 - y1 : y1 - y2;
    int sx = x_l ? 1 : -1;
    int sy = y_l ? 1 : -1;

    int err = dx - dy;
    while (true) {
        setPixel(_pixels, width, height, x1, y1, color);
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

/** Draws an antialiased line from (x10, y10) to (x1, y1) with the specified color.
 *
 * @param _pixels The pixels of the surface.
 * @param width The width of the surface.
 * @param height The height of the surface.
 * @param x0 The x-coordinate of the first point.
 * @param y0 The y-coordinate of the first point.
 * @param x1 The x-coordinate of the second point.
 * @param y1 The y-coordinate of the second point.
 * @param color The color of the line.
 * @param top Whether the top part of the aa line should be drawn. (or the left side if vertical)
 * @param bottom Whether the bottom part of the aa line should be drawn. (or the right side if vertical)
*/
inline void _aaDrawLine(size_t _pixels, int width, int height, int x0, int y0, int x1, int y1, size_t color, bool top = true, bool bottom = true) {
    auto fpart = [](float x) { return (float) (x - floor(x)); };
    auto rfpart = [fpart](float x) { return 1 - fpart(x); };

    uint32_t color_u = (uint32_t) color;
    uint32_t colorRGB = color_u & 0xFFFFFF00;
    uint8_t colorA = color_u & 0x000000FF;

    bool steep = abs(y1 - y0) > abs(x1 - x0);
    if (steep) {
        int temp = x0;
        x0 = y0;
        y0 = temp;
        temp = x1;
        x1 = y1;
        y1 = temp;
    }
    if (x0 > x1) {
        int temp = x0;
        x0 = x1;
        x1 = temp;
        temp = y0;
        y0 = y1;
        y1 = temp;
    }

    int dx = x1 - x0;
    int dy = y1 - y0;

    float gradient = 1;
    if (dx != 0) {
        gradient = (float) dy / (float) dx;
    }

    float intery = y0 + gradient;

    if (steep) {
        setPixel(_pixels, width, height, y0, x0, color);
        setPixel(_pixels, width, height, y1, x1, color);

        bool drawLeft = (gradient > 0 && bottom) || (gradient < 0 && top);
        bool drawRight = (gradient > 0 && top) || (gradient < 0 && bottom);

        for (int x = x0 + 1; x < x1; x++) {
            if (drawLeft) setPixel(_pixels, width, height, floor(intery), x, colorRGB | (uint8_t) (rfpart(intery) * colorA)); // left pixel
            if (drawRight) setPixel(_pixels, width, height, floor(intery) + 1, x, colorRGB | (uint8_t) (fpart(intery) * colorA)); // right pixel
            intery += gradient;
        }
    } else {
        setPixel(_pixels, width, height, x0, y0, color);
        setPixel(_pixels, width, height, x1, y1, color);

        bool drawTop = (gradient > 0 && top) || (gradient < 0 && bottom);
        bool drawBottom = (gradient > 0 && bottom) || (gradient < 0 && top);

        for (int x = x0 + 1; x < x1; x++) {
            if (drawTop) setPixel(_pixels, width, height, x, floor(intery), colorRGB | (uint8_t) (rfpart(intery) * colorA)); // top pixel
            if (drawBottom) setPixel(_pixels, width, height, x, floor(intery) + 1, colorRGB | (uint8_t) (fpart(intery) * colorA)); // bottom pixel
            intery += gradient;
        }
    }
}

// Draws a line from (x1, y1) to (x2, y2) with the specified color and thickness.
inline void _drawLine(size_t _pixels, int width, int height, int x1, int y1, int x2, int y2, size_t color, bool blending, int thickness) {
    if (thickness == 1) {
        _drawLine(_pixels, width, height, x1, y1, x2, y2, color);
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
            _drawLine(_pixels, width, height, x1 + x, y1 + y, x2 + x, y2 + y, color);
        }
    }
}

// This is the drawLine accesible from python.
inline void drawLine(size_t _pixels, int width, int height, int x1, int y1, int x2, int y2, size_t color, bool aa = false, bool blending = false, int thickness = -1) {
    if (aa) _aaDrawLine(_pixels, width, height, x1, y1, x2, y2, color); // when included -> , blending, thickness);
    elif(thickness == -1)
        _drawLine(_pixels, width, height, x1, y1, x2, y2, color, blending, thickness);
    else
        _drawLine(_pixels, width, height, x1, y1, x2, y2, color, blending);
}

// Draws a circle with the specified color.
inline void _drawCircle(size_t _pixels, int width, int height, int xc, int yc, int radius, size_t color) {
    int x = radius;
    int y = 0;
    int E = -x;
    while (x >= y) {
        setPixel(_pixels, width, height, xc + x, yc + y, color);
        setPixel(_pixels, width, height, xc - x, yc - y, color);
        setPixel(_pixels, width, height, xc + y, yc + x, color);
        setPixel(_pixels, width, height, xc - y, yc + x, color);
        setPixel(_pixels, width, height, xc + x, yc - y, color);
        setPixel(_pixels, width, height, xc - x, yc + y, color);
        setPixel(_pixels, width, height, xc + y, yc - x, color);
        setPixel(_pixels, width, height, xc - y, yc - x, color);

        E += 2 * (y++) + 1;
        if (E >= 0) {
            E -= 2 * (x--) + 1;
        }
    }
}

inline void _drawCircle(size_t _pixels, int width, int height, int xc, int yc, int radius, size_t color, int thickness) {
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
        drawLine(_pixels, width, height, xc + xi, yc + y, xc + xo, yc + y, color);
        drawLine(_pixels, width, height, xc + y, yc + xi, xc + y, yc + xo, color);
        drawLine(_pixels, width, height, xc - xo, yc + y, xc - xi, yc + y, color);
        drawLine(_pixels, width, height, xc - y, yc + xi, xc - y, yc + xo, color);
        drawLine(_pixels, width, height, xc - xo, yc - y, xc - xi, yc - y, color);
        drawLine(_pixels, width, height, xc - y, yc - xo, xc - y, yc - xi, color);
        drawLine(_pixels, width, height, xc + xi, yc - y, xc + xo, yc - y, color);
        drawLine(_pixels, width, height, xc + y, yc - xo, xc + y, yc - xi, color);

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

inline void _drawCircleAA(int pixels, int width, int _height, int xc, int yc, int outer_radius, size_t color) {

    uint32_t aMask = 0x000000FF;
    auto _draw_point = [pixels, width, _height, xc, yc, color, aMask](int x, int y, int alpha) {
        setPixel(pixels, width, _height, xc + x, yc + y, color & ~aMask | alpha);
        setPixel(pixels, width, _height, xc + x, yc - y, color & ~aMask | alpha);
        setPixel(pixels, width, _height, xc - x, yc + y, color & ~aMask | alpha);
        setPixel(pixels, width, _height, xc - x, yc - y, color & ~aMask | alpha);
        setPixel(pixels, width, _height, xc - y, yc - x, color & ~aMask | alpha);
        setPixel(pixels, width, _height, xc - y, yc + x, color & ~aMask | alpha);
        setPixel(pixels, width, _height, xc + y, yc - x, color & ~aMask | alpha);
        setPixel(pixels, width, _height, xc + y, yc + x, color & ~aMask | alpha);
    };
    auto max = [](int a, int b) {
        return a > b ? a : b;
    };
    int i = 0;
    int j = outer_radius;
    int last_fade_amount = 0;
    int fade_amount = 0;

    int MAX_OPAQUE = color & aMask;
    int height;

    while (i < j) {
        height = sqrt(max(outer_radius * outer_radius - i * i, 0));
        fade_amount = MAX_OPAQUE * (ceil(height) - height);

        if (fade_amount < last_fade_amount) {
            // Opaqueness reset so drop down a row.
            j -= 1;
        }
        last_fade_amount = fade_amount;

        // The API needs integers, so convert here now we've checked if
        // it dropped.
        int fade_amount_i = fade_amount;

        // We're fading out the current j row, and fading in the next one down.
        _draw_point(i, j, MAX_OPAQUE - fade_amount_i);
        _draw_point(i, j - 1, fade_amount_i);

        i += 1;
    }
}

// Circle functction accesiible from python.
inline void drawCircle(size_t _pixels, int width, int height, int xc, int yc, int radius, size_t color, bool aa = false, bool blending = false, int thickness = -1) {
    std::cout << "called";
    if (aa) {
        _drawCircleAA(_pixels, width, height, xc, yc, radius, color);
    } else {
        if (thickness == -1) {
            _drawCircle(_pixels, width, height, xc, yc, radius, color);
        } else {
            _drawCircle(_pixels, width, height, xc, yc, radius, color, thickness);
        }
    }
}

// Fills a circle with the specified color.
inline void fillCircle(size_t _pixels, int width, int height, int xc, int yc, int radius, size_t color) {
    int x = radius;
    int y = 0;
    int E = -x;
    while (x >= y) {
        drawLine(_pixels, width, height, xc + x, yc + y, xc - x, yc + y, color);
        drawLine(_pixels, width, height, xc - y, yc + x, xc + y, yc + x, color);
        drawLine(_pixels, width, height, xc - x, yc - y, xc + x, yc - y, color);
        drawLine(_pixels, width, height, xc - y, yc - x, xc + y, yc - x, color);

        E += 2 * (y++) + 1;
        if (E >= 0) {
            E -= 2 * (x--) + 1;
        }
    }
}


// Fill a polygon with the specified color.
inline void drawPoly(size_t _pixels, int width, int height, void* vx, void* vy, int len, size_t color, int thickness = 1) {
    int* v_x = (int*) vx;
    int* v_y = (int*) vy;
    for (int i = 0; i < len; i++) {
        drawLine(_pixels, width, height, v_x[i], v_y[i], v_x[(i + 1) % len], v_y[(i + 1) % len], color, thickness);
    }
}

// Fill an antialiased polygon with the specified color.
inline void aaDrawPoly(size_t _pixels, int width, int height, void* vx, void* vy, int len, size_t color) {
    int* v_x = (int*) vx;
    int* v_y = (int*) vy;

    int cy = 0;
    int cx = 0;
    for (int i = 0; i < len; i++) {
        cx += v_x[i];
        cy += v_y[i];
    }
    cx /= len;
    cy /= len;

    for (int i = 0; i < len; i++) {
        bool top, bottom;
        double dx = v_x[(i + 1) % len] - v_x[i];
        double slope;
        if (dx == 0) {
            if (v_x[i] < cx) {
                top = true;
                bottom = false;
            } else {
                top = false;
                bottom = true;
            }
        } else {
            slope = (double) (v_y[(i + 1) % len] - v_y[i]) / (double) (v_x[(i + 1) % len] - v_x[i]);
            if (slope == 0) {
                if (v_y[i] < cy) {
                    top = true;
                    bottom = false;
                } else {
                    top = false;
                    bottom = true;
                }
            } else if (v_x[i] < cx) {
                top = (slope > 0);
                bottom = (slope < 0);
            } else {
                top = (slope < 0);
                bottom = (slope > 0);
            }
        }

        _aaDrawLine(_pixels, width, height, v_x[i], v_y[i], v_x[(i + 1) % len], v_y[(i + 1) % len], color, top, bottom);
    }
}

// Fill a polygon with the specified color.
inline void fillPolyConvex(size_t _pixels, int width, int height, void* vx, void* vy, int len, size_t color) {
    int* v_x = (int*) vx;
    int* v_y = (int*) vy;
    int* v_x_min = (int*) malloc(sizeof(int) * height); // max height
    int* v_x_max = (int*) malloc(sizeof(int) * height); // max height

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
            if (x1 < v_x_min[y1]) {
                v_x_min[y1] = x1;
            }
            if (x1 > v_x_max[y1]) {
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
        drawLine(_pixels, width, height, v_x_min[i], i, v_x_max[i], i, color);
    }
    free(v_x_min);
    free(v_x_max);
}

// Draw a rectangle with the specified color.
inline void drawRect(size_t _pixels, int width, int height, int x, int y, int w, int h, size_t color) {
    for (int i = x; i < w + x; i++) {
        setPixel(_pixels, width, height, i, y, color);
        setPixel(_pixels, width, height, i, y + h - 1, color);
    }
    for (int i = y; i < h + y; i++) {
        setPixel(_pixels, width, height, x, i, color);
        setPixel(_pixels, width, height, x + w - 1, i, color);
    }
}

// Draws a rectangle with the specified color and thickness.
inline void drawRect(size_t _pixels, int width, int height, int x, int y, int w, int h, size_t color, int thickness) {
    if (thickness == 1) {
        drawRect(_pixels, width, height, x, y, w, h, color);
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
            drawRect(_pixels, width, height, x + i, y + i, w - (2 * i), h - (2 * i), color);
        }
    }
}

// Fill a rectangle with the specified color.
inline void fillRect(size_t _pixels, int width, int height, int x, int y, int w, int h, size_t color) {
    for (int i = y; i < h + y; i++) {
        for (int j = x; j < w + x; j++) {
            setPixel(_pixels, width, height, j, i, color);
        }
    }
}

inline void clearPixels(size_t _pixels, int width, int height) {
    memset((size_t*) _pixels, 0, width * height * 4);
}
