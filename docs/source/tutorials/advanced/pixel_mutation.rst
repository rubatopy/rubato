##############
Pixel Mutation
##############

Assumes you finished getting started.

Pixel mutation is not currently implemented to surfaces in rubato as of ``2.1.0``.
This will hopefully come in future.

First make sure you have the numpy installed.

.. code-block:: console

    $ pip install numpy

Then, import ``numpy`` and ``rubato``:

.. code-block:: python

    import numpy, rubato as rb


This demo will show how to change specific image pixels.

.. code-block:: python

    def draw_on(surf):
        pixels: numpy.ndarray = rb.sdl2.ext.pixelaccess.pixels2d(surf)
        for x in range(pixels.shape[0]):
            for y in range(pixels.shape[1]):
                random.shuffle((new := list(rb.Color.color_defaults.values())))
                pixels[x][y] = rb.Color(*(new[0])).rgba32
        return surf

    image.image = draw_on(image.image)

The ``pixels2d()`` function takes in an ``SDL_Surface`` and will return a numpy array
which will change the surfaces pixels by reference.

.. note::

    If you just need to draw to the screen use :func:`Draw.point <rubato.utils.draw.Draw.point>`

The source code is available
`here <https://github.com/rubatopy/rubato/tree/main/demo/pixel_mutation.py>`__.
