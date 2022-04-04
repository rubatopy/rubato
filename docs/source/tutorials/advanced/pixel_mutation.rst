Using Pixel Mutation
====================

Assumes you finished getting started.

Pixel mutation is not currently implemented to surfaces in rubato as of `2.0.0`.
This will hopefully come in future
.. code-block:: console
    $ pip install numpy

In your code we need to import `numpy` and `sdl2.ext.pixelaccess`

.. code-block:: python
    import numpy, sdl2.ext.pixelaccess as pixel_access


This demo will show how to change specific image pixels.


.. code-block:: python

    def draw_on(surf: sdl2.SDL_Surface):
        pixels: numpy.ndarray = pixel_access.pixels2d(surf)
        for x in range(pixels.shape[0]):
            for y in range(pixels.shape[1]):
                random.shuffle((new := list(Defaults.color_defaults.values())))
                pixels[x][y] = Color(*(new[0])).rgba32
        return surf

    image.image = draw_on(image.image)

The `pixels2d()` function takes in an `SDL_Surface` and will return a numpy array
which will change the surfaces pixels by reference.

The source code is available
`here <https://github.com/rubatopy/rubato/tree/main/demo/draw_point.py>`__.