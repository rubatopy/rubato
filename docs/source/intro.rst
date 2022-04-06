Getting Started
===============

Installation
------------
Installing Rubato is simple. Just run the following in a terminal:

.. code-block:: console

    $ pip install rubato

.. note::
    | Python 3.10.x required
    | We recommend installing python direct from python.org if you do not already have it.

You'll also need to install the SDL dlls (they're the C-lib files that Rubato needs).
Here's how you can do that on your platform:

.. tab-set::

    .. tab-item:: Windows
        :sync: win

        .. code-block:: console

            $ pip install pysdl-dll


    .. tab-item:: Linux
        :sync: linux

        .. code-block:: console

            $ pip install pysdl-dll


    .. tab-item:: Mac
        :sync: mac

        .. code-block:: console

            $ brew install sdl2 sdl2_mixer sdl2_ttf sdl2_gfx sdl2_image

        Go `here <https://brew.sh/>`__ to install Homebrew if you don't have it already.

Setting Up
----------
Once you've installed Rubato, setting up a new project is easy.
To create a new blank project, simply create a new python file and type the following:

.. code-block:: python

    import rubato as rb

    rb.init()

:func:`rb.init() <rubato.init>` initializes Rubato.
An optional dictionary argument passed into :func:`rb.init() <rubato.init>` can specify such things as window size, resolution, background color, and more.

.. note::

    Throughout our documentation, we assume that Rubato is imported as ``rb``.

Rubato documentation describes exactly what custom parameters you can specify when creating Rubato objects or calling specific functions such as ``init()``.
You can see these parameters and their default values on the :doc:`defaults page <defaults>`.

.. warning::
    You should `only` interact with Rubato (adding scenes, game objects, etc.) **AFTER** calling ``init()``.

Now that Rubato is ready, add the following line of code to the end of the file:

.. code-block:: python

    rb.begin()

:func:`rb.begin() <rubato.begin>` is the function that starts the Rubato engine.
Without it, Rubato won't know to begin the engine cycle, and your game won't run.
It is recommended to call :func:`rb.begin() <rubato.begin>` at the bottom of your project file as in this example.

Now run your code in a terminal using ``python3 YOUR_FILENAME.py``. If you see a white square window, congrats!
You're officially up and running with Rubato.

.. note::
    Code not working? It's possible something went wrong during the dependency installation process.
    Check your terminal log for errors and reinstall Rubato and the SDL dlls if necessary.

you can jump straight into the :doc:`full api documentation  <api>`.
