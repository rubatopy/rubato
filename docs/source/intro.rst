Getting Started
===============

Installation
------------
Installing Rubato is simple. Just run:

.. code-block:: console

    (.venv) $ pip install rubato

.. note::
    | A virtual environment is recommended
    | Python >= 3.10 required

Usage
-----
To get started, import rubato and initilize it.

.. code-block:: python

    import rubato as rb

    rb.init()

Rubato is sprite-based. This means that most objects rendered
to the screen are :ref:`Sprites <sprite>`. However, sprites do
very little on their own. Components are what gives a sprite
functionality. For example, you can attach an :ref:`Image <image>`
or a :ref:`RigidBody <rigidbody>` to a sprite to make it draw an image
or interact with the physics engine.

To add a sprite to the screen in our example, you need to first create a
new :ref:`Scene <scene>` and add it to the :ref:`Scene Manager <scenemanager>`.
Finally, you can create your sprite and add it to the scene.

.. code-block:: python

    scene = rb.Scene()
    rb.game.scenes.add(scene, "main")

    ball = rb.Sprite({
        "pos": rb.Vector(100,100)
    }).add(rb.Circle({
        "color": rb.Color.green
    }))

    scene.add(ball)


The above code creates a sprite with a circular hitbox at position :code:`(100, 100)`.
We've also specified that we'd like for the circle to be rendered green.

You might notice that after running this code, nothing happens. Thats because
the game loop hasn't started. To start Rubato's engine, run:

.. code-block:: python

    rb.begin()

Hopefully you see a green circle in a new window on your screen, and if so,
congratulations! You're up and running with your first Rubato project.

More feature-specific tutorials can be found :doc:`here <tutorials>`.
