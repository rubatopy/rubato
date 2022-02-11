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
screen is a :ref:`Sprite <sprite>`. Sprites come in many different types. For
example, you could have an :ref:`Image <image>` sprite or a :ref:`Rigidbody <rigidbody>`
sprite.

To add a sprite to the screen, you need to create a new :ref:`Scene <scene>`
and a new :ref:`Group <group>`. Then you need to add the group to the scene and
the scene to the :ref:`Scene Manager <scenemanager>`. Finally, you can create a
sprite and add it to the group.

.. code-block:: python

    scene = rb.Scene()
    rb.game.scenes.add(scene)

    image_group = rb.Group()
    scene.add(image_group)

    image = rb.Image({
        "pos": rb.Vector(100, 100)
    })

    image_group.add(image)


The code above creates an image at position :code:`(100, 100)`. Since no image path is
given, Rubato will use the default image (a pink and black square).

You might notice that after running this code, nothing happens. Thats because
the game loop hasn't started. To start the game loop run:

.. code-block:: python

    rb.begin()

Now when running this you should see a small pink and black square draw on your
screen!

To learn how to do specific things, look at the :doc:`Tutorials Page <tutorials>`
