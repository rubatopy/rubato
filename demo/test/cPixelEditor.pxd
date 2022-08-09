cdef extern from "../../rubato/static/dlls/windows/SDL2/SDL.h":
    pass

cdef extern from "PixelEditor.h":

    void setPixelRGB(SDL_Surface* surf, int x, int y, Uint8 r, Uint8 g, Uint8 b)
    void setPixelRGBA(SDL_Surface* surf, int x, int y, Uint8 r, Uint8 g, Uint8 b, Uint8 a)
    void setPixelRGBSafe(SDL_Surface* surf, int x, int y, Uint8 r, Uint8 g, Uint8 b)
    void setPixelRGBSafe(SDL_Surface* surf, int x, int y, Uint8 r, Uint8 g, Uint8 b, Uint8 a)
    void setPixel(SDL_Surface* surf, int x, int y, Uint32 pixel)
    void setPixelSafe(SDL_Surface* surf, int x, int y, Uint32 pixel)
    int* getPixel(SDL_Surface* surf, int x, int y)
