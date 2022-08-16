#include <cstdint>
#include <cstring>
#include <limits.h>
#include <math.h>
#include <cstdlib>

// Sets the pixel at x, y to the color specified.
inline void setPixel(size_t _pixels, int width, int x, int y, size_t color) {
    uint32_t a_mask = 0x000000FF;

    int off = y * width + x;
    uint32_t src = (uint32_t)color;
    uint32_t* pixels = (uint32_t*)_pixels;
    uint8_t src_a = src & a_mask;

    if (src_a == 0xFF) {
        pixels[off] = src;
    } else {
        uint32_t r_mask = 0xFF000000;
        uint32_t g_mask = 0x00FF0000;
        uint32_t b_mask = 0x0000FF00;

        uint32_t dest = pixels[off];
        uint8_t dest_a = pixels[off] & a_mask;
        uint8_t one_minus = 0xFF - src_a;

        uint8_t red = ((((src & r_mask) >> 24) * src_a) >> 8) | ((((dest & r_mask) >> 24) * one_minus) >> 8);
        uint8_t green = ((((src & g_mask) >> 16) * src_a) >> 8) | ((((dest & g_mask) >> 16) * one_minus) >> 8);
        uint8_t blue = ((((src & b_mask) >> 8) * src_a) >> 8) | ((((dest & b_mask) >> 8) * one_minus) >> 8);

        uint8_t alpha = src_a | ((dest_a * one_minus) >> 8);

        pixels[off] = (red << 24) | (green << 16) | (blue << 8) | alpha;
    }
}

// Sets the pixel but clips at the edges of the surface.
inline void setPixelSafe(size_t _pixels, int width, int height, int x, int y, size_t color) {
    if (x < width && y < height && x >= 0 && y >= 0) {
        setPixel(_pixels, width, x, y, color);
    }
}

// Gets the pixel at x, y from the surface and returns it as an int.
inline int getPixel(size_t _pixels, int width, int x, int y) {
    return (int)((uint32_t*)_pixels)[y * width + x];
}

// Gets the pixel but returns 0 if the pixel is outside the surface.
inline int getPixelSafe(size_t _pixels, int width, int height, int x, int y) {
    if (x < width && y < height && x >= 0 && y >= 0) {
        return getPixel(_pixels, width, x, y);
    }
    return 0;
}

// Draws a line from (x1, y1) to (x2, y2) with the specified color.
inline void drawLine(size_t _pixels, int width, int height, int x1, int y1, int x2, int y2, size_t color) {
    bool x_l = x1 < x2;
    bool y_l = y1 < y2;

    int dx = x_l ? x2 - x1 : x1 - x2;
    int dy = y_l ? y2 - y1 : y1 - y2;
    int sx = x_l ? 1 : -1;
    int sy = y_l ? 1 : -1;

    int err = dx - dy;
    while (true) {
        setPixelSafe(_pixels, width, height, x1, y1, color);
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
inline void drawLine(size_t _pixels, int width, int height, int x1, int y1, int x2, int y2, size_t color, int thickness) {
    if (thickness == 1) {
        drawLine(_pixels, width, height, x1, y1, x2, y2, color);
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
            drawLine(_pixels, width, height, x1 + x, y1 + y, x2 + x, y2 + y, color);
        }
    }
}

// Draws a circle with the specified color.
inline void drawCircle(size_t _pixels, int width, int height, int xc, int yc, int radius, size_t color) {
    int x = radius;
    int y = 0;
    int E = -x;
    while (x >= y) {
        setPixelSafe(_pixels, width, height, xc + x, yc + y, color);
        setPixelSafe(_pixels, width, height, xc - x, yc - y, color);
        setPixelSafe(_pixels, width, height, xc + y, yc + x, color);
        setPixelSafe(_pixels, width, height, xc - y, yc + x, color);
        setPixelSafe(_pixels, width, height, xc + x, yc - y, color);
        setPixelSafe(_pixels, width, height, xc - x, yc + y, color);
        setPixelSafe(_pixels, width, height, xc + y, yc - x, color);
        setPixelSafe(_pixels, width, height, xc - y, yc - x, color);

        E += 2 * (y++) + 1;
        if (E >= 0) {
            E -= 2 * (x--) + 1;
        }
    }
}

inline void drawCircle(size_t _pixels, int width, int height, int xc, int yc, int radius, size_t color, int thickness) {
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
    int* v_x = (int*)vx;
    int* v_y = (int*)vy;
    for (int i = 0; i < len; i++) {
        drawLine(_pixels, width, height, v_x[i], v_y[i], v_x[(i + 1) % len], v_y[(i + 1) % len], color, thickness);
    }
}

// Fill a polygon with the specified color.
inline void fillPolyConvex(size_t _pixels, int width, int height, void* vx, void* vy, int len, size_t color) {
    int* v_x = (int*)vx;
    int* v_y = (int*)vy;
    int* v_x_min = (int*)malloc(sizeof(int) * height); // max height
    int* v_x_max = (int*)malloc(sizeof(int) * height); // max height

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
        setPixelSafe(_pixels, width, height, i, y, color);
        setPixelSafe(_pixels, width, height, i, y + h - 1, color);
    }
    for (int i = y; i < h + y; i++) {
        setPixelSafe(_pixels, width, height, x, i, color);
        setPixelSafe(_pixels, width, height, x + w - 1, i, color);
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
            setPixelSafe(_pixels, width, height, j, i, color);
        }
    }
}

inline void clearPixels(size_t _pixels, int width, int height) {
    memset((size_t*)_pixels, 0, width * height * 4);
}
