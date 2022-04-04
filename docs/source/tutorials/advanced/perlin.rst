Using Perlin Noise
==================

Perlin Noise is not a built in feature to rubato, however we do recommend using the
`opensimplex` library.

Install in your terminal

.. code-block:: bash

    pip install opensimplex

Import to your python file

.. code-block:: python

    import opensimplex

As a developer we need to know how to use the :code:`opensimplex.noise2()` function
which generates 2D OpenSimplex noise from X,Y coordinates.

Simplex noise has values from -1 to 1 and moves smoothly between values.

For the resolution of the noise we use a scale value by which we divide.
(The higher the value the more zoomed)

To get a different noise region (different randomness) we use an offset variable.

.. code-block:: python

    scale = 20
    offset = rb.Vector(100, 100)

    for x in range(rb.Display.res.x):
        for y in range(rb.Display.res.y):
            noise = opensimplex.noise2((x + offset.x) / scale, (y + offset.y) / scale)

That is how we get noise, in order to use it with rubato visually we need to
draw points to the renderer.

The source code is available
`here <https://github.com/rubatopy/rubato/tree/main/demo/test_noise.py>`__.