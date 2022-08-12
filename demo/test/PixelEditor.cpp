#include <cstdint>
typedef uint32_t Uint32;

inline void setPixelRGB(size_t _pixels, int width, int x, int y, int mapped)
{
    Uint32 *pixels = (Uint32 *)(_pixels);
    Uint32 *pixel = pixels + (y * width) + x;
    *pixel = (Uint32)mapped;
}