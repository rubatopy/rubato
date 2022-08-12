cdef extern from "PixelEditor.cpp":

    void setPixelRGB(size_t _pixels, int width, int x, int y, size_t mapped)
    void setPixelRGBA(size_t _pixels, int width, int x, int y, size_t mapped_a)
    void setPixelRGBSafe(size_t _pixels, int width, int x, int y, size_t mapped)
    void setPixelRGBASafe(size_t _pixels, int width, int x, int y, size_t mapped_a)
    int getPixel(size_t _pixels, int width, int x, int y)