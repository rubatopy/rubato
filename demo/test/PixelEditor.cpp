#include <cstdint>
#include <iostream>
typedef uint32_t Uint32;

//Sets the pixel at x, y to the color specified, must be locked b4 unlocked after
inline void setPixel(size_t _pixels, int width, int x, int y, size_t mapped) {
	*((uint32_t*)(_pixels) + y*width + x) = (uint32_t) mapped;
}

// Gets the pixel at x, y from the surface and returns it as a uint32_t
inline int getPixel(size_t _pixels, int width, int x, int y) {
	uint32_t* pixels = (uint32_t*)(_pixels);
	uint32_t* pixel_p = pixels + (y*width) + x;
	uint32_t pixel = *pixel_p;
	return (int) pixel;
}


inline void Bresenham(size_t _pixels, int width, int x1, int y1, int x2, int y2, size_t mapped) {
	int dx = abs(x2 - x1);
	int dy = abs(y2 - y1);
	int sx = x1 < x2 ? 1 : -1;
	int sy = y1 < y2 ? 1 : -1;
	int err = dx - dy;
	while (true) {
		setPixelRGB(_pixels, width, x1, y1, mapped);
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

inline void MidpointCircle(size_t _pixels, int width, int xc, int yc, int radius, size_t mapped) {

}