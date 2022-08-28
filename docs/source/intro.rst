###############
Getting Started
###############

************
Installation
************
Installing rubato is simple. Make sure you have Python 3.10 or later installed, then run the following in a terminal:

.. code-block:: console

    $ pip install rubato

.. note::
    | We recommend installing python directly from `python.org <https://www.python.org/downloads/>`_ if you do not already have it.

On Windows and Mac, the dll files that SDL needs come pre-bundled with rubato, so you should be ready to go.

.. dropdown:: On Linux **only**, you'll need to install them yourself:

    .. code-block:: console

        $ pip install pysdl2-dll

**********
Setting Up
**********
Once you've installed rubato, setting up a new project is easy.
To create a new blank project, simply create a new python file (such as ``main.py``) and type the following:

.. code-block:: python

    import rubato as rb

    rb.init()

:func:`rb.init() <rubato.init>` initializes rubato.
An optional dictionary argument passed into :func:`rb.init() <rubato.init>` can specify such things as window name and size, resolution, and more.

.. note::

    Throughout our documentation, we assume that rubato is imported as ``rb``.
    If you used ``from rubato import *``, just delete the ``rb.`` prefix where needed.

Now that rubato is ready, add the following line of code to the end of the file:

.. code-block:: python

    rb.begin()

:func:`rb.begin() <rubato.begin>` is the function that starts the rubato engine.
Without it, rubato won't know to begin the engine cycle, and your game won't run.
It is recommended to call :func:`rb.begin() <rubato.begin>` at the bottom of your project file as in this example.

Now run your code in a terminal using ``python YOUR_FILENAME.py``. If you see a black square window, congrats!
You're officially up and running with rubato.

.. warning::
    When you are working with rubato, make sure to only call rubato functions after calling ``init()`` and before ``begin()``.
    Note that any code placed after ``begin()`` wont run, because the function blocks the main thread.

.. note::
    Code not working? It's possible something went wrong during the dependency installation process.
    Check your terminal log for errors and reinstall rubato and the SDL dlls if necessary.
    You can also file a bug report `here <https://github.com/rubatopy/rubato/issues>`_ if something went wrong on our end.
