Getting Started
===============

Installation
------------
Installing Rubato is simple. Just run:

.. code-block:: console

    $ pip install rubato

You also need to install the SDL dlls. (These are just the c-library files needed to make Rubato work):

.. tab-set::

    .. tab-item:: Windows
        :sync: win

        .. code-block:: console

            $ pip install pysdl-dll


    .. tab-item:: Linux
        :sync: linux

        .. code-block:: console

            $ pip install pysdl-dll

    .. tab-item:: Mac OS X (Intel)
        :sync: macintel

        .. code-block:: console

            $ pip install pysdl-dll

    .. tab-item:: Mac OS X (Silicon)
        :sync: macsil

        .. code-block:: console

            $ brew install sdl2 sdl2_mixer sdl2_ttf sdl2_gfx sdl2_image

.. note::
    | A virtual environment is recommended
    | Python >= 3.10 required
    | Issues have been found when using the python from Microsoft store (use python.org)

Usage
-----
To get started, import rubato and initilize it.

.. code-block:: python

    import rubato as rb

    init()

Rubato is "game object"-based. This means that most objects rendered
to the screen are :ref:`Game Objects <gameobj>`. However, game objects do
very little on their own. Components are what gives a game object
functionality. For example, you can attach a :func:`Circle <rubato.classes.components.hitbox.Circle>`
or any other :ref:`components <components>` to a game object to make it draw an image
or interact with the physics engine.

To add a game object to the screen in our example, you need to first create a
new :ref:`Scene <scene>` and add it to the :ref:`Scene Manager <scenemanager>`.
Finally, you can create your game object and add it to the scene.

.. code-block:: python

    scene = Scene()
    Game.scenes.add(scene, "main")

    ball = GameObject({
        "pos": Vector(100,100)
    }).add(Circle({
        "color": Color.green
    }))

    scene.add(ball)


The above code creates a game object with a circular hitbox at position :code:`(100, 100)`.
We've also specified that we'd like for the circle to be rendered green.

This is how we do class parameters in rubato. Game Object and Component classes
take in a dictionary of parameters. You can find all the
:ref:`default options<defaults>` in our docs.

You might notice that after running this code, nothing happens. That's because
the game loop hasn't started. To start Rubato's engine, run:

.. code-block:: python

    begin()

Hopefully you see a green circle in a new window on your screen, and if so,
congratulations! You're up and running with your first Rubato project.

The next step is to learn to use the rest of the library.

You can follow the step-by-step tutorial where you will be making a platformer :doc:`here <tutorials>`.

Or you can jump straight into the :doc:`full api documentation  <api>`.
