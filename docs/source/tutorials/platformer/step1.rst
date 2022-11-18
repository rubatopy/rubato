##########################
Step 1 - Basic Structure
##########################

Before we can design our game, we need to do a few things to set rubato up.

First, follow the :doc:`setup guide <../../intro>`, naming your file ``main.py``.

Then, download and extract these
`files <https://raw.githubusercontent.com/rubatopy/rubato/main/demo/platformer_stripped/files.zip>`_
into the same directory as your ``main.py`` file (so you have ``main.py`` and the ``files`` folder in the same directory.)

At this point, your ``main.py`` file should look like this:

.. code-block:: python
    :caption: main.py
    :linenos:

    import rubato as rb

    # initialize a new game
    rb.init()

    # begin the game
    rb.begin()

Running ``main.py`` using ``python main.py`` should result in a window similar to this appearing:

.. image:: /_static/tutorials_static/platformer/step1/1.png
    :width: 25%
    :align: center

:func:`rb.init() <rubato.init>` is the initializer function for the library.
It will ensure that rubato can communicate with the computer hardware and
set up a window for you.

:func:`rb.begin() <rubato.begin>` actually runs the game loop. The loop will
handle all of the rendering, player logic, etc. Without calling it, nothing happens.

To customize your game window, you can pass in a few parameters. For now, let's:
    * Give our window a name
    * Change its resolution
    * Make it fullscreen

Replace the previous :func:`rb.init() <rubato.init>` call with this:

.. literalinclude:: step1_main.py
    :caption: main.py
    :lineno-start: 3
    :lines: 3-8
    :emphasize-lines: 3-5

At this point, running the game should look like this (full screen and white). To quit the game either quit like any
other program or press ``Ctrl+C`` in the terminal.

.. image:: /_static/tutorials_static/platformer/step1/2.png
    :width: 75%
    :align: center

Here is what your main.py should look like:

.. literalinclude:: step1_main.py
    :caption: main.py
    :linenos:
    :emphasize-lines: 1-

If you made it here, great! We're ready to build the platformer.
Next, we'll create a player and add him to the game.
