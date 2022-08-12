cdef extern from "PixelEditor.cpp":

    void setPixel(size_t _pixels, int width, int x, int y, size_t mapped)
    int getPixel(size_t _pixels, int width, int x, int y)
    void setPixelSafe(size_t _pixels, int width, int height, int x, int y, size_t mapped)
    int getPixelSafe(size_t _pixels, int width, int height, int x, int y)

    void Bresenham(size_t _pixels, int width, int x1, int y1, int x2, int y2, size_t mapped)
    void MidpointCircle(size_t _pixels, int width, int height, int xc, int yc, int radius, size_t mapped)
