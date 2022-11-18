###############################
Step 4 - Creating a Level
###############################

In this step, we will be creating a small level for our player to run in.

We will build our level out of basic rectangle hitboxes. We can also pass in a Color to these hitboxes in order for them to draw.

First let's set a variable for the level size. This will be the width of the level. Let's set it to be 120% the resolution of the screen.
Note that it needs to be an integer, because it represents the width of the level in pixels.

.. literalinclude:: step4_shared.py
    :caption: shared.py
    :lines: 1-6
    :linenos:
    :emphasize-lines: 4-


Along with that lets add some nice colors to our :code:`shared.py` file.

.. literalinclude:: step4_shared.py
    :caption: shared.py
    :lines: 1-12
    :linenos:
    :emphasize-lines: 8-


The :func:`darker() <rubato.utils.color.Color.darker>` function allows us to darken a color by an amount. Subtracting this from all values.

.. important::
    Next we will create a new file :code:`level1.py` in it we will define all the elements unique to our level.

:code:`level1.py` holds a scene with our level in it. All the scene work we did up until now should have really been put in :code:`level1.py`.
So lets make a scene in level1.py and move our scene code there (deleting it from :code:`main.py`).

.. code-block:: python
    :caption: level1.py
    :linenos:

    import shared
    import rubato as rb

    scene = rb.Scene("level1", background_color=shared.background_color)

    # Add the player to the scene
    scene.add(shared.player)


.. important::
    Finally import :code:`level1.py` from :code:`main.py` instead of :code:`shared.py` and check that it works.


We will create our floor. We do this by creating a GameObject and adding a Rectangle hitbox to it.
In the following code we also use the :func:`Rectangle.bottom_left <rubato.structure.gameobject.physics.hitbox.Rectangle.bottom_left>`
property to place the floor correctly. We also give a "ground" tag to our floor. This will be
used later to determine if the player is on the ground.

.. literalinclude:: step4_level1.py
    :caption: level1.py
    :lines: 4-14
    :lineno-start: 4
    :emphasize-lines: 3-

Also update the :code:`scene.add` line to add the floor to the scene.

.. code-block:: python
    :caption: level1.py

    scene.add(shared.player, ground)


You can also change the player gravity to :code:`rb.Vector(y=rb.Display.res.y * -1.5)`, which will make the game more realistic. It should look like this
now:

.. image:: /_static/tutorials_static/platformer/step4/1.png
    :align: center
    :width: 75%

The process for adding all of the remaining platforms is the same as what we've done to add the floor. To have cleaner code, we actually create some
lists to store all of our Game Objects. At this point, you should have fun with it! Create a level of your choice!
You can even add images to the gameobjects instead of giving the hitboxes color, to give the game a much more polished feel.

Below is a very basic example that we will be using for the rest of the tutorial.

.. image:: /_static/tutorials_static/platformer/step4/2.png
    :align: center
    :width: 75%

|
|

.. dropdown:: Code that made the above level

    .. literalinclude:: step4_level1.py
        :caption: level1.py
        :lines: 14-58
        :lineno-start: 14
        :emphasize-lines: 3-

    And remember to add everything to the scene.

    .. tip::

        :func:`wrap() <rubato.misc.wrap>` is a rubato function that allows us to get a GameObject with Components added to it.

    .. code-block:: python
        :lineno-start: 59
        :emphasize-lines: 1-

        scene.add(shared.player, ground, wrap(platforms), *pillars)

Now that you have a level built, you may notice that you are currently able to fall off the world. This is because nothing
is stopping you from doing so. Let's fix this by adding a clear hitbox on either side of the play area.

.. literalinclude:: step4_shared.py
    :caption: shared.py
    :lines: 46-
    :lineno-start: 46
    :emphasize-lines: 3-


.. literalinclude:: step4_level1.py
    :caption: level1.py
    :lines: 54-
    :lineno-start: 54
    :emphasize-lines: 7,8,15,16

.. admonition:: Remember!
    :class: tip

    To not have the hitbox render, don't pass a color to the hitbox! All other functionality will remain untouched.

You'll now notice that the player is unable to fall off the world. This is because the hitbox is blocking it's path.

There's one big issue, however. Jumps don't come back, even once you hit the ground. Not to worry. We will implement this in :doc:`step5`.

Your code should currently look like this (with your own level of course!):

.. literalinclude:: step4_main.py
    :caption: main.py
    :linenos:

.. literalinclude:: step4_shared.py
    :caption: shared.py
    :linenos:
    :emphasize-lines: 4-14,34,48-

.. literalinclude:: step4_player_controller.py
    :caption: player_controller.py
    :linenos:

.. literalinclude:: step4_level1.py
    :caption: level1.py
    :linenos:
