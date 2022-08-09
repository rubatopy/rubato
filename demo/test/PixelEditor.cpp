#include <cstring>
#include <../../rubato/static/dlls/windows/SDL2/SDL.h>

//Sets the pixel at x, y to the color specified
void setPixelRGB(SDL_Surface* surf, int x, int y, Uint8 r, Uint8 g, Uint8 b) {
    SDL_LockSurface(surf);
    Uint32* pixels = (Uint32*)surf->pixels;
    Uint32* pixel = pixels + (y*surf->w) + x;
    *pixel = SDL_MapRGB(surf->format, r, g, b);
    SDL_UnlockSurface(surf);
}

//Sets the pixel at x, y to the color specified using the alpha channel
void setPixelRGBA(SDL_Surface* surf, int x, int y, Uint8 r, Uint8 g, Uint8 b, Uint8 a) {
    SDL_LockSurface(surf);
    Uint32* pixels = (Uint32*)surf->pixels;
    Uint32* pixel = pixels + (y*surf->w) + x;
    *pixel = SDL_MapRGBA(surf->format, r, g, b, a);
    SDL_UnlockSurface(surf);
}
//Sets the pixel at x, y to the color specified, checking for x and y < 0 and x > width and y > height
void setPixelRGBSafe(SDL_Surface* surf, int x, int y, Uint8 r, Uint8 g, Uint8 b) {
    if (y < 0 || y >  surf->h || x < 0 || x > surf->w) {
        return;
    }
    setPixelRGB(surf, x, y, r, g, b);
}

//Sets the pixel at x, y to the color specified, checking for x and y < 0 and x > width and y > height using the alpha channel
void setPixelRGBSafe(SDL_Surface* surf, int x, int y, Uint8 r, Uint8 g, Uint8 b, Uint8 a) {
    if (y < 0 || y >  surf->h || x < 0 || x > surf->w) {
        return;
    }
    setPixelRGBA(surf, x, y, r, g, b, a);
}
//Sets the pixel at x, y to the color specified, uses a Uint32 for the color
void setPixel(SDL_Surface* surf, int x, int y, Uint32 pixel) {
    SDL_LockSurface(surf);
    Uint32 *pixels = (Uint32*)surf->pixels;
    pixels[(y*surf->w) + x] = pixel;
    SDL_UnlockSurface(surf);
}
//Sets the pixel at x, y to the color specified, checks for x and y < 0 and x > width and y > height
void setPixelSafe(SDL_Surface* surf, int x, int y, Uint32 pixel) {
    if (y < 0 || y > surf->h || x < 0 || x > surf->w) {
        return;
    }
    setPixel(surf, x, y, pixel);
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
int main(){
    std::cout << "Hello, World!" << std::endl;
}
