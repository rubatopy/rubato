cdef extern from "PixelEditor.h":

    void setPixelRGB(void* _pixels, int width, int x, int y, int _r, int _g, int _b)
