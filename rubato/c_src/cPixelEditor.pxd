from libcpp cimport bool

cdef extern from "PixelEditor.cpp":

    void setPixel(size_t _pixels, int width, int height, int x, int y, size_t color, bool blending)
    int getPixel(size_t _pixels, int width, int height, int x, int y)
    void clearPixels(size_t _pixels, int width, int height)

    void drawLine(size_t _pixels, int width, int height, int x1, int y1, int x2, int y2, size_t color, bool aa, bool blending, int thickness)

    void drawCircle(size_t _pixels, int width, int height, int xc, int yc, int radius, size_t color, bool aa, bool blending, int thickness)
    void fillCircle(size_t _pixels, int width, int height, int xc, int yc, int radius, size_t color, bool blending)

    void drawRect(size_t _pixels, int width, int height, int x, int y, int w, int h, size_t color, bool blending, int thickness)
    void fillRect(size_t _pixels, int width, int height, int x, int y, int w, int h, size_t color, bool blending)

    void drawPoly(size_t _pixels, int width, int height, void* vx, void* vy, int len, size_t color, bool aa, bool blending, int thickness)
    void fillPolyConvex(size_t _pixels, int width, int height, void* vx, void* vy, int len, size_t color, bool blending)

