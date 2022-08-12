#include <cstdint>
#include <iostream>
typedef uint32_t Uint32;

// Sets the pixel at x, y to the color specified, must be locked b4 unlocked after
inline void setPixel(size_t _pixels, int width, int x, int y, size_t mapped) {
	*((uint32_t*)(_pixels) + y*width + x) = (uint32_t) mapped;
}

// Sets the pixel but clips at the edges of the surface.
inline void setPixelSafe(size_t _pixels, int width, int height, int x, int y, size_t mapped) {
	if (x < width && y < height && x >= 0 && y >= 0) {
		setPixel(_pixels, width, x, y, mapped);
	}
}

// Gets the pixel at x, y from the surface and returns it as a uint32_t
inline int getPixel(size_t _pixels, int width, int x, int y) {
	return (int) *((uint32_t*)(_pixels) + y*width + x);
}

// Gets the pixel but returns 0 if the pixel is outside the surface.
inline int getPixelSafe(size_t _pixels, int width, int height, int x, int y) {
	if (x < width && y < height && x >= 0 && y >= 0) {
		return getPixel(_pixels, width, x, y);
	}
	return 0;
}


inline void Bresenham(size_t _pixels, int width, int x1, int y1, int x2, int y2, size_t mapped) {
	int dx = abs(x2 - x1);
	int dy = abs(y2 - y1);
	int sx = x1 < x2 ? 1 : -1;
	int sy = y1 < y2 ? 1 : -1;
	int err = dx - dy;
	while (true) {
		setPixel(_pixels, width, x1, y1, mapped);
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

inline void MidpointCircle(size_t _pixels, int width, int height, int xc, int yc, int radius, size_t mapped) {
    int x = radius;
    int y = 0;
    int E = -x;
    while (x >= y) {
        setPixelSafe(_pixels, width, height, xc + x, yc + y, mapped);
        setPixelSafe(_pixels, width, height, xc + y, yc + x, mapped);
        setPixelSafe(_pixels, width, height, xc - y, yc + x, mapped);
        setPixelSafe(_pixels, width, height, xc - x, yc + y, mapped);
        setPixelSafe(_pixels, width, height, xc - x, yc - y, mapped);
        setPixelSafe(_pixels, width, height, xc - y, yc - x, mapped);
        setPixelSafe(_pixels, width, height, xc + y, yc - x, mapped);
        setPixelSafe(_pixels, width, height, xc + x, yc - y, mapped);

        E += 2 * y + 1;
        y++;
        if (E >= 0) {
            E -= 2 * x + 1;
            x--;
        }
    }
}