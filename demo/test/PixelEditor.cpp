#include <cstdint>
#include <iostream>
typedef uint32_t Uint32;

//Sets the pixel at x, y to the color specified, must be locked b4 unlocked after
inline void setPixelRGB(size_t _pixels, int width, int x, int y, size_t mapped) {
	Uint32* pixels = (Uint32*)(_pixels);
	Uint32* pixel = pixels + (y*width) + x;
	*pixel = (Uint32) mapped;
}

//Sets the pixel at x, y to the color specified using the alpha channel
inline void setPixelRGBA(size_t _pixels, int width, int x, int y, size_t mapped_a) {
	Uint32* pixels = (Uint32*)(_pixels);
	Uint32* pixel = pixels + (y*width) + x;
	*pixel = (Uint32) mapped_a;
}

//Sets the pixel at x, y to the color specified, checking for x and y < 0 and x > width and y > height
inline void setPixelRGBSafe(size_t _pixels, int width, int x, int y, size_t mapped) {
	if (x < 0 || y < 0 || x >= width || y >= width) {
		return;
	}
	setPixelRGB(_pixels, width, x, y, mapped);
}

//Sets the pixel at x, y to the color specified, checking for x and y < 0 and x > width and y > height using the alpha channel
inline void setPixelRGBASafe(size_t _pixels, int width, int x, int y, size_t mapped_a) {
	if (x < 0 || y < 0 || x >= width || y >= width) {
		return;
	}
	setPixelRGBA(_pixels, width, x, y, mapped_a);
}

// Gets the pixel at x, y from the surface and returns it as a Uint32
inline int getPixel(size_t _pixels, int width, int x, int y) {
	Uint32* pixels = (Uint32*)(_pixels);
	Uint32* pixel_p = pixels + (y*width) + x;
	Uint32 pixel = *pixel_p;
	std::cout << "Pixel at " << x << ", " << y << " is " << pixel << std::endl;
	return (int) pixel;
}