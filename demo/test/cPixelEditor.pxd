cdef extern from "PixelEditor.cpp":

    void setPixelRGB(size_t _pixels, int width, int x, int y, int mapped)
