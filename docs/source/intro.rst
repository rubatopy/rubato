Getting Started
===============

Rubato is designed so that you can get started quickly and focus on what matters.

Installation
------------
Installing Rubato is easy! Just run:

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

Rubato is uses a sprite based system. This means that everything you see on
screen is a :ref:`Sprite <sprite>`. Sprites can have components attached to
them. Components is what gives a sprite functionality. For example, you can
attach an :ref:`Image <image>` or a :ref:`RigidBody <rigidbody>`.

To add a sprite to the screen, you need to create a new :ref:`Scene <scene>`.
Then you need to add the scene to the :ref:`Scene Manager <scenemanager>`.
Finally, you can create a sprite and add it to the scene.

.. code-block:: python

    scene = rb.Scene()
    rb.game.scenes.add(scene)

    image = rb.Sprite({
        "pos": rb.Vector(100, 100),
    }).add(rb.Image())

    scene.add(image)


The code above creates an image at position :code:`(100, 100)`. Since no image path is
given, Rubato will use the default image (a pink and black square).

You might notice that after running this code, nothing happens. Thats because
the game loop hasn't started. To start the game loop run:

.. code-block:: python

    rb.begin()

Now when running this you should see a small pink and black square draw on your
screen!

To learn how to do specific things, look at the :doc:`Tutorials Page <tutorials>`
