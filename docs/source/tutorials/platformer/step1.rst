##########################
Step 1 - Basic Structure
##########################

Welcome to the first part of making a platformer in rubato. In this first step, we will
be setting up our project and laying the foundation for the next steps.

First, let's make sure you have rubato installed. Make sure you have python 3.10.x
installed and run

.. code-block:: console

    $ pip install rubato

It should install successfully. Now we are ready to start programming.

Make sure you have downloaded and extracted these
`files <https://raw.githubusercontent.com/rubatopy/rubato/main/demo/platformer_files/platformer_files.zip>`_ and create
a ``main.py`` file next to the ``platformer_files`` directory. Add this to the top of your file:

.. code-block:: python

    import rubato as rb

This will allow us to access all of rubato using :code:`rb`.

Next, we need to initialize rubato:

.. code-block:: python

    # initialize a new game
    rb.init()

    # begin the game
    rb.begin()

At this point, if you run the code, you should see a white window appear.

.. image:: /_static/tutorials_static/platformer/step1/1.png
    :width: 25%
    :align: center

:code:`rb.init()` is the initializer function for the library.
It will ensure that the computer hardware can communicate with Python and
set up a window for you. :code:`rb.begin()` actually runs the game loop. The loop will
handle all of the rendering, player logic, etc. Without calling it, nothing happens.

To customize your game window, you can pass in a few parameters. For now, let's:
    * Give our window a name
    * Increase its size a little
    * Change its resolution
    * Set a more exciting background-color

Replace the previous :code:`rb.init()` call with this:

.. code-block:: python

    # initialize a new game
    rb.init(
        name="Platformer Demo",  # Set a name
        res=rb.Vector(1920, 1080),  # Increase the window resolution
    )


Here we're introducing a new classe: :func:`rb.Vector <rubato.utils.vector.Vector>`.

:func:`Vector <rubato.utils.vector.Vector>` is a class that contains an x variable and a y variable.
It can represent a point, dimensions, a vector, or anything else that has an x and y
parameter. The :func:`Vector <rubato.utils.vector.Vector>` class comes loaded with
many useful linear algebra functions and can have nearly every built-in Python math function
applied to them.

At this point, running the game should look like this:

.. image:: /_static/tutorials_static/platformer/step1/2.png
    :width: 75%
    :align: center

Here is what your main.py should look like:

.. code-block:: python

    import rubato as rb

    # initialize a new game
    rb.init(
        name="Platformer Demo",  # Set a name
        res=rb.Vector(1920, 1080),  # Increase the window resolution
    )

    # begin the game
    rb.begin()


There we go! Now your game is set up. In the next step, we will create a player
and add him to the game.
