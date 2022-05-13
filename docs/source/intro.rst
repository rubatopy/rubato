###############
Getting Started
###############

************
Installation
************
Installing rubato is simple. Just run the following in a terminal:

.. code-block:: console

    $ pip install rubato

.. note::
    | Python 3.10.x required
    | We recommend installing python direct from python.org if you do not already have it.

On Windows and Mac, the dll files that SDL needs come pre-bundled with rubato, so you should be ready to go.
On Linux **only**, you'll need to install them yourself:

.. code-block:: console

    $ pip install pysdl2-dll

************
Setting Up
************
Once you've installed rubato, setting up a new project is easy.
To create a new blank project, simply create a new python file and type the following:

.. code-block:: python

    import rubato as rb

    rb.init()

:func:`rb.init() <rubato.init>` initializes rubato.
An optional dictionary argument passed into :func:`rb.init() <rubato.init>` can specify such things as window size, resolution, background color, and more.

.. note::

    Throughout our documentation, we assume that rubato is imported as ``rb``.

rubato documentation describes exactly what custom parameters you can specify when creating rubato objects or calling specific functions such as ``init()``.
You can see these parameters and their default values on the :doc:`defaults page <defaults>`.

.. warning::
    You should `only` interact with rubato (adding scenes, game objects, etc.) **AFTER** calling ``init()``.

Now that rubato is ready, add the following line of code to the end of the file:

.. code-block:: python

    rb.begin()

:func:`rb.begin() <rubato.begin>` is the function that starts the rubato engine.
Without it, rubato won't know to begin the engine cycle, and your game won't run.
It is recommended to call :func:`rb.begin() <rubato.begin>` at the bottom of your project file as in this example.

Now run your code in a terminal using ``python3 YOUR_FILENAME.py``. If you see a white square window, congrats!
You're officially up and running with rubato.

.. note::
    Code not working? It's possible something went wrong during the dependency installation process.
    Check your terminal log for errors and reinstall rubato and the SDL dlls if necessary.

you can jump straight into the :doc:`full api documentation  <api>`.
