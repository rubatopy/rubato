
cdef extern from "SDL2/include/SDL.h":
    struct SDL_Surface:
      pass
    struct SDL_PixelFormat:
      pass
    int SDL_MapRGB(SDL_PixelFormat * format, int r, int g, int b)
    SDL_Surface* SDL_CreateRGBSurfaceWithFormat(int flags, int width, int height, int depth, int format)


cdef extern from "PixelEditor.cpp":

    void setPixelRGB(int _pixels, int width, int x, int y, int _r, int _g, int _b)
