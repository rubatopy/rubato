Basic Structure
===============

Welcome to the first part of making a platformer in rubato. In this first step, we will
be setting up our project and laying down the foundation for the next steps.

First, lets make sure you have rubato installed. Make sure you have python 3.10.x
installed and run

.. code-block:: console

    $ pip install rubato

It should then successfully install. Now we are ready to start programming. Note that
if you run into any issues. The source code for this step is available
`here <https://github.com/rubatopy/rubato/tree/main/tutorials/platformer/step1>`__.
Let's get started.

In a folder of your choice, create a file and name it :code:`main.py`. At the top
of this file, import rubato:

.. code-block:: python

    from rubato import *

This will allow to access the entire rubato library by just typing the name

Next we need to initialize rubato:

.. code-block:: python

    # initialize a new game
    init()

    # begin the game
    begin()

At this point, if you run the code, you should see a white window appear.

.. image:: /_static/tutorial_ss/step1/1.png
    :width: 245
    :align: center

:code:`rb.init()` is the initializer function for the library.
It will make sure that the computer hardware can communicate with Python and it will
set up a window for you. :code:`rb.begin()` actually runs the game loop. The loop will
handle all of the rendering, player logic, etc. Without calling it, nothing happens.

To customize your game window, you can pass in a few parameters. For now, lets:
    * Give our window a name
    * Increase its size a little
    * Change its resolution
    * Set a more interesting background color

Replace the previous :code:`rb.init()` call with this:

.. code-block:: python

    # initialize a new game
    init(
        {
            "name": "Platformer Demo",  # Set a name
            "window_size": Vector(960, 540),  # Set the window size
            "background_color": Color.cyan.lighter(),  # Set the background color
            "res": Vector(1920, 1080),  # Increase the window resolution
        }
    )


Here we're introducing 2 new classes: :func:`rb.Vector <rubato.utils.vector.Vector>`
and :func:`rb.Color <rubato.utils.color.Color>`.

A vector is a class that contains an x variable and a y variable.
It can represent a point, dimensions, a vector, or anything else that has an x and y
parameter. The :func:`Vector <rubato.utils.vector.Vector>` class comes loaded with
many useful linear algebra functions and can have nearly every builtin python math function
applied to them.

The :func:`Color <rubato.utils.color.Color>` class helps you manage colors. Colors
are stored in the RGBA format and can be loaded from HSV and tuples. It comes
preloaded with a lot of :func:`default colors <rubato.utils.color.Color.random>` and
has a few functions to manipulate color. In the code above, we use :func:`lighter() <rubato.utils.color.Color.lighter>`
to increase the shade of the color.

At this point, running the game should look like this:

.. image:: /_static/tutorial_ss/step1/2.png
    :width: 540
    :align: center

Here is what you main.py should look like:

.. code-block:: python

    from rubato import *

    # initialize a new game
    init(
        {
            "name": "Platformer Demo",  # Set a name
            "window_size": Vector(960, 540),  # Set the window size
            "background_color": Color.cyan.lighter(),  # Set the background color
            "res": Vector(1920, 1080),  # Increase the window resolution
        }
    )

    # begin the game
    begin()


There we go! Now your game is set up. In the next step, we will create a player
and add him to the game.

The source code for this step is available
`here <https://github.com/rubatopy/rubato/tree/main/tutorials/platformer/step1>`__.
