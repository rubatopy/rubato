#include <cstdint>
#include <cstring>

// Sets the pixel at x, y to the color specified.
inline void setPixel(size_t _pixels, int width, int x, int y, size_t color) {
	((uint32_t*) _pixels)[y*width + x] = (uint32_t) color;
}

// Sets the pixel but clips at the edges of the surface.
inline void setPixelSafe(size_t _pixels, int width, int height, int x, int y, size_t color) {
	if (x < width && y < height && x >= 0 && y >= 0) {
		setPixel(_pixels, width, x, y, color);
	}
}

// Gets the pixel at x, y from the surface and returns it as an int.
inline int getPixel(size_t _pixels, int width, int x, int y) {
	return (int) ((uint32_t*) _pixels)[y*width + x];
}

// Gets the pixel but returns 0 if the pixel is outside the surface.
inline int getPixelSafe(size_t _pixels, int width, int height, int x, int y) {
	if (x < width && y < height && x >= 0 && y >= 0) {
		return getPixel(_pixels, width, x, y);
	}
	return 0;
}


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

inline void drawCircle(size_t _pixels, int width, int height, int xc, int yc, int radius, size_t color) {
    int x = radius;
    int y = 0;
    int E = -x;
    while (x >= y) {
        setPixelSafe(_pixels, width, height, xc + x, yc + y, color);
        setPixelSafe(_pixels, width, height, xc + y, yc + x, color);
        setPixelSafe(_pixels, width, height, xc - y, yc + x, color);
        setPixelSafe(_pixels, width, height, xc - x, yc + y, color);
        setPixelSafe(_pixels, width, height, xc - x, yc - y, color);
        setPixelSafe(_pixels, width, height, xc - y, yc - x, color);
        setPixelSafe(_pixels, width, height, xc + y, yc - x, color);
        setPixelSafe(_pixels, width, height, xc + x, yc - y, color);

        E += 2 * (y++) + 1;
        if (E >= 0) {
            E -= 2 * (x--) + 1;
        }
    }
}

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

// Fill a rectangle with the specified color.
inline void fillRect(size_t _pixels, int width, int height, int x, int y, int w, int h, size_t color) {
	for (int i = y; i < h + y; i++) {
		for (int j = x; j < w + x; j++) {
			setPixelSafe(_pixels, width, height, j, i, color);
		}
	}
}

inline void clearPixels(size_t _pixels, int width, int height) {
	memset((size_t*) _pixels, 0, width * height * 4);
}
