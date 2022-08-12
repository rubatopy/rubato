#include <cstdint>
#include <iostream>

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