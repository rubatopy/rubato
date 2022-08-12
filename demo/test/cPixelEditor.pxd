cdef extern from "PixelEditor.cpp":

    void setPixel(size_t _pixels, int width, int x, int y, size_t color)
    int getPixel(size_t _pixels, int width, int x, int y)
    void setPixelSafe(size_t _pixels, int width, int height, int x, int y, size_t color)
    int getPixelSafe(size_t _pixels, int width, int height, int x, int y)

    void drawLine(size_t _pixels, int width, int height, int x1, int y1, int x2, int y2, size_t color)
    void drawCircle(size_t _pixels, int width, int height, int xc, int yc, int radius, size_t color)
    void fillCircle(size_t _pixels, int width, int height, int xc, int yc, int radius, size_t color)
    void drawRect(size_t _pixels, int width, int height, int x, int y, int w, int h, size_t color)
    void fillRect(size_t _pixels, int width, int height, int x, int y, int w, int h, size_t color)

    void clearPixels(size_t _pixels, int width, int height)
