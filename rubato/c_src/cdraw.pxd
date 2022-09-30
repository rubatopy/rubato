from libcpp cimport bool

cdef extern from "cdraw.cpp":

    size_t createPixelBuffer(int width, int height)
    void freePixelBuffer(size_t buffer)
    void colorkeyCopy(size_t source, size_t destination, int width, int height, size_t color_key)
    size_t clonePixelBuffer(size_t _source, int width, int height)

    void setPixel(size_t _pixels, int width, int height, int x, int y, size_t color, bool blending)
    int getPixel(size_t _pixels, int width, int height, int x, int y)
    void clearPixels(size_t _pixels, int width, int height)
    void blit(size_t _source, size_t _destination, int sw, int sh, int dw, int dh, int srx, int sry, int srw, int srh, int drx, int dry, int drw, int drh)
    void switchColors(size_t _pixels, int width, int height, size_t color1, size_t color2)

    void drawLine(size_t _pixels, int width, int height, int x1, int y1, int x2, int y2, size_t color, bool aa, bool blending, int thickness)
    void drawCircle(size_t _pixels, int width, int height, int xc, int yc, int radius, size_t borderColor, size_t fillColor, bool aa, bool blending, int thickness)
    void drawPoly(size_t _pixels, int width, int height, void* vx, void* vy, int len, size_t borderColor, size_t fillColor, bool aa, bool blending, int thickness)
    void drawRect(size_t _pixels, int width, int height, int x, int y, int w, int h, size_t borderColor, size_t fillColor, bool blending, int thickness)
