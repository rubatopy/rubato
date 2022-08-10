#pragma once
#include <cstring>
#include <../../rubato/static/dlls/windows/SDL2/SDL.h>

SDL_Surface* FAKE = SDL_CreateRGBSurfaceWithFormat(0, 1, 1, 32, SDL_PIXELFORMAT_RGBA32);
//Sets the pixel at x, y to the color specified, must be locked b4 unlocked after
void setPixelRGB(void* _pixels, int width, int x, int y, int _r, int _g, int _b) {
	Uint32* pixels = (Uint32*)_pixels;
	Uint32* pixel = pixels + (y*width) + x;
	Uint8 r = _r, g = _g, b = _b;
	*pixel = SDL_MapRGB(FAKE->format, r, g, b);
}
