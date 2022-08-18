from libcpp cimport bool

cdef extern from "PixelEditor.cpp":

    void setPixel(size_t _pixels, int width, int height, int x, int y, size_t color, bool blending)
    int getPixel(size_t _pixels, int width, int height, int x, int y)

    void drawLine(size_t _pixels, int width, int height, int x1, int y1, int x2, int y2, size_t color, bool aa, bool blending, int thickness)
    void drawCircle(size_t _pixels, int width, int height, int xc, int yc, int radius, size_t color)
    void drawCircle(size_t _pixels, int width, int height, int xc, int yc, int radius, size_t color, int thickness)
    void fillCircle(size_t _pixels, int width, int height, int xc, int yc, int radius, size_t color)
    void drawRect(size_t _pixels, int width, int height, int x, int y, int w, int h, size_t color)
    void drawRect(size_t _pixels, int width, int height, int x, int y, int w, int h, size_t color, int thickness)
    void fillRect(size_t _pixels, int width, int height, int x, int y, int w, int h, size_t color)
    void aaDrawPoly(size_t _pixels, int width, int height, void* vx, void* vy, int len, size_t color)
    void fillPolyConvex(size_t _pixels, int width, int height, void* vx, void* vy, int len, size_t color)
    void drawPoly(size_t _pixels, int width, int height, void* vx, void* vy, int len, size_t color, int thickness)

    void clearPixels(size_t _pixels, int width, int height)
    void drawCircleAA(int pixels, int width, int _height, int base_aa, int xc, int yc, int outer_radius, int color)
