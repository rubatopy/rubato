cdef extern from "PixelEditor.cpp":

    void setPixel(size_t _pixels, int width, int x, int y, size_t mapped)
    void setPixelSafe(size_t _pixels, int width, int height, int x, int y, size_t mapped)
    int getPixel(size_t _pixels, int width, int x, int y)