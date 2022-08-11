cdef extern from "PixelEditor.cpp":

    void setPixelRGB(int _pixels, int width, int x, int y, int _r, int _g, int _b)
