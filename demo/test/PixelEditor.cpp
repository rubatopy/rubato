#pragma once
#include <SDL2/SDL.h>


SDL_Surface* FAKE = SDL_CreateRGBSurfaceWithFormat(0, 1, 1, 32, SDL_PIXELFORMAT_RGBA32);
//Sets the pixel at x, y to the color specified, must be locked b4 unlocked after
void setPixelRGB(int _pixels, int width, int x, int y, int _r, int _g, int _b) {
	Uint32* pixels = (Uint32*)((size_t)_pixels);
	Uint32* pixel = pixels + (y*width) + x;
	Uint8 r = _r, g = _g, b = _b;
	*pixel = SDL_MapRGB(FAKE->format, r, g, b);
}

//Sets the pixel at x, y to the color specified using the alpha channel
void setPixelRGB(int _pixels, int width, int x, int y, int _r, int _g, int _b, int _a) {
	Uint32* pixels = (Uint32*)((size_t)_pixels);
	Uint32* pixel = pixels + (y*width) + x;
	Uint8 r = _r, g = _g, b = _b, a = _a;
	*pixel = SDL_MapRGBA(FAKE->format, r, g, b, a);
}

//Sets the pixel at x, y to the color specified, checking for x and y < 0 and x > width and y > height
void setPixelRGBSafe(int _pixels, int width, int height, int x, int y, int _r, int _g, int _b) {
	if (x < 0 || y < 0 || x > width || y > height) {
		return;
	}
	setPixelRGB(_pixels, width, x, y, _r, _g, _b);
}

//Sets the pixel at x, y to the color specified, checking for x and y < 0 and x > width and y > height using the alpha channel
void setPixelRGBASafe(int _pixels, int width, int height, int x, int y, int _r, int _g, int _b, int _a) {
	if (x < 0 || y < 0 || x > width || y > height) {
		return;
	}
	setPixelRGB(_pixels, width, x, y, _r, _g, _b, _a);
}
//Sets the pixel at x, y to the color specified, uses a Uint32 for the color
void setPixel(int _pixels, int width, int x, int y, int _pixel) {
	Uint32 pixel = _pixel;
	Uint32* pixels = (Uint32*)((size_t)_pixels);
	pixels[(y*width) + x] = pixel;
}
//Sets the pixel at x, y to the color specified, checks for x and y < 0 and x > width and y > height
void setPixelSafe(int _pixels, int width, int height, int x, int y, int pixel) {
	if (y < 0 || y > height || x < 0 || x > width) {
		return;
	}
	setPixel(_pixels, width, x, y, pixel);
}

// Gets the pixel at x, y from the surface and returns it as a Uint32
int* getPixel(SDL_Surface* surf, int x, int y) {
	SDL_LockSurface(surf);
	Uint32 *pixels = (Uint32 *)surf->pixels;
	SDL_UnlockSurface(surf);
	Uint32 pixel = pixels[(y * surf->w) + x];
	// pixel is RGBA, we want to parse out each color
	Uint8 r, g, b, a;
	SDL_GetRGBA(pixel, surf->format, &r, &g, &b, &a);
	int* colors = new int[4];
	colors[0] = r;
	colors[1] = g;
	colors[2] = b;
	colors[3] = a;
	return colors;
}