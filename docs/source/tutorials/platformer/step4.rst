###############################
Step 4 - Creating a Level
###############################

In this step, we will be creating a small level for our player to run in.

We will build our level out of basic rectangle hitboxes. To get them to draw, we'll specify a fill color in their constructor.

First let's set a variable for the level size. This will be the width of the level; 120% the resolution of the screen in this case.
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


The :func:`darker() <rubato.utils.color.Color.darker>` function allows us to darken a color by an amount.
It simply subtracts that amount from each of the red, green, and blue color channels.

Next, we'll create a new file :code:`level1.py` to house the elements unique to our level.

:code:`level1.py` holds a scene with our level in it. All the scene work we did up until now should have really been put in :code:`level1.py`.
So lets make a scene in level1.py and move our scene code there (deleting it from :code:`main.py`):

.. code-block:: python
    :caption: level1.py
    :linenos:

    import shared
    import rubato as rb

    scene = rb.Scene("level1", background_color=shared.background_color)

    # Add the player to the scene
    scene.add(shared.player)


Since we just added a new file, we'll need to import it.
Since :code:`main.py` doesn't need :code:`shared.py` anymore, simply replace the :code:`import shared` line in :code:`main.py` with :code:`import level1`


Now onto the floor. We create the ground by initializing a GameObject and adding a Rectangle hitbox to it.

.. literalinclude:: step4_level1.py
    :caption: level1.py
    :lines: 4-14
    :lineno-start: 4
    :emphasize-lines: 3-

Notice how we used the :func:`Rectangle.bottom_left <rubato.structure.gameobject.physics.hitbox.Rectangle.bottom_left>`
property to place the floor correctly. We also give a tag to our floor, to help us identify it later when the player collides with it.

Also update the :code:`scene.add` line to add the floor to the scene.

.. code-block:: python
    :caption: level1.py

    scene.add(shared.player, ground)


You can also change the player gravity to :code:`rb.Vector(y=rb.Display.res.y * -1.5)`, which will make the game more realistic. It should look like this
now:

.. image:: /_static/tutorials_static/platformer/step4/1.png
    :align: center
    :width: 75%

The process for adding the remaining platforms is the same as what we've just done. Easy!
This is a great place to unleash your creativity and make a better level than we did.

Below is a very basic example for the rest of the tutorial.

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

        :func:`wrap() <rubato.misc.wrap>` is a rubato helper function that lets us make GameObjects and automatically add components to them in fewer lines of code.

    .. code-block:: python
        :lineno-start: 59
        :emphasize-lines: 1-

        scene.add(shared.player, ground, wrap(platforms), *pillars)

Now that you have a level built, you may notice that you are currently able to walk or jump out of the frame of the window.
Let's fix this by adding an invisible hitbox on either side of the play area.

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

You'll now notice that the player is unable to fall off the world. This is because the hitbox is blocking its path.

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
    :emphasize-lines: 1-
