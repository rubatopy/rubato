###############################
Step 5 - Finishing Touches
###############################

This is the final step! We'll be making quality-of-life changes to the game to make it play more like a real platformer.

.. important::

    This step covers general game development concepts that are not unique to rubato (grounding detection, camera scrolling, etc). We will not be going
    over how these work, rather we will be focusing on how to implement them in our game. A quick Google search on any of these topics is a great place
    to start learning.

*********
Main Menu
*********

Every good game needs a menu screen. For our platformer, we'll make a new scene for the main menu. Create a new file
named :code:`main_menu.py`. Here's the code needed for implementing the basic menu.

.. literalinclude:: ../../../../demo/platformer_stripped/main_menu.py
    :caption: main_menu.py
    :linenos:
    :emphasize-lines: 1-

Also be sure to import and load it in :code:`main.py`.

.. literalinclude:: ../../../../demo/platformer_stripped/main.py
    :caption: main.py
    :lines: 10-16
    :lineno-start: 10
    :emphasize-lines: 1,4

In the menu, we use 4 new classes:
:func:`Font <rubato.utils.rendering.font.Font>`,
:func:`Text <rubato.structure.gameobject.ui.text.Text>`,
:func:`Button <rubato.structure.gameobject.ui.button.Button>`, and
:func:`Raster <rubato.structure.gameobject.sprites.raster.Raster>`.
The behaviors of Font, Text, and Button are fairly trivial.
Raster is a special component in rubato that you can draw custom art to.
In this case, we're using it to draw a background for our button.

**********
Jump Limit
**********

Right now, when you move around, you'll find that you quickly run out of jumps. This is because we implemented a 2 jump limit. However,
once you run out of jumps, you can't do anything to reset your jump counter. We want this counter to be reset whenever you land on the ground. To do
that, we will add a ground detection hitbox to the player, making sure to set the ``trigger`` parameter to true.

Making a hitbox a ``trigger`` prevents the hitbox from resolving collisions in the rubato physics engine. It will still detect overlap
and call the relevant callbacks. We will define a player_collide callback that will be called when the player's ground detector collides.
When this happens, we use the provided collision :func:`Manifold <rubato.structure.gameobject.physics.engine.Manifold>` to
make sure the other collider is a ground hitbox, that we are not already grounded, and that we are indeed falling towards the ground.
That code looks like this:

In :code:`shared.py`, add the following code:

.. literalinclude:: ../../../../demo/platformer_stripped/shared.py
    :caption: shared.py
    :lines: 17-51
    :lineno-start: 16
    :emphasize-lines: 16-

In :code:`player_controller.py` we get our ground detector and set its on_collide and on_exit callbacks:

.. literalinclude:: ../../../../demo/platformer_stripped/player_controller.py
    :caption: player_controller.py
    :lines: 7-36
    :lineno-start: 7
    :emphasize-lines: 9-12,16,17,21-

*************
Camera Scroll
*************

In your testing, you may have also noticed that you are able to walk past the right side of your screen. This is because there is actually more level
space there! Remember that we set our level to be 120% the width of the screen. Lets use rubato's built-in lerp function to make our camera follow the player.

.. literalinclude:: ../../../../demo/platformer_stripped/player_controller.py
    :caption: player_controller.py
    :lines: 38-46,73-87
    :lineno-start: 38
    :emphasize-lines: 11-

``lerp`` and ``clamp`` are both built-in methods to the :func:`Math <rubato.utils.computation.rb_math.Math>` class.
Note that we've used :func:`Time.fixed_delta <rubato.utils.rb_time.Time.fixed_delta>`, which represents the
time elapsed since the last update to the physics engine, in seconds. This is to make our camera follow the player more smoothly,
in line with the fps.

*******************************
Final Player Controller Touches
*******************************

We currently only change the animation when the player jumps. Lets add some more animations when the player is moving left and right.

.. literalinclude:: ../../../../demo/platformer_stripped/player_controller.py
    :caption: player_controller.py
    :lines: 38-46,53-65
    :lineno-start: 38
    :emphasize-lines: 11-

Let's also add a reset function. If the player falls off the level or presses the reset key ("r" in this case),
we want to place them back at the start of the level.

.. literalinclude:: ../../../../demo/platformer_stripped/player_controller.py
    :caption: player_controller.py
    :lines: 54-72
    :lineno-start: 54
    :emphasize-lines: 14-

Finally, let's add a little bit of polish to the player movement in the form of friction.
This will make the player feel a little more grounded.

.. literalinclude:: ../../../../demo/platformer_stripped/player_controller.py
    :caption: player_controller.py
    :lines: 38-52
    :lineno-start: 38
    :emphasize-lines: 10-

***********
To Conclude
***********

**That's it! You've finished your first platformer in rubato!**

This was just the tip of the iceberg of what rubato can do.

.. dropdown:: If you got lost, here's the full code, just for kicks:

    .. literalinclude:: ../../../../demo/platformer_stripped/main.py
        :caption: main.py
        :linenos:
        :emphasize-lines: 10, 13

    .. literalinclude:: ../../../../demo/platformer_stripped/shared.py
        :caption: shared.py
        :lines: 2-
        :lineno-start: 1
        :emphasize-lines: 31-50

    .. literalinclude:: ../../../../demo/platformer_stripped/player_controller.py
        :caption: player_controller.py
        :linenos:
        :emphasize-lines: 2,15-18,22-23,27-36,47-87

    .. literalinclude:: ../../../../demo/platformer_stripped/level1.py
        :caption: level1.py
        :linenos:

    .. literalinclude:: ../../../../demo/platformer_stripped/main_menu.py
        :caption: main_menu.py
        :linenos:
        :emphasize-lines: 1-

We're also including a version with some more in-depth features that weren't covered in this tutorial, including
win detection, advanced animation switching, and a respawn system. Also new scenes, with multiple levels. Noice.

Sneak Peak:

.. image:: /_static/tutorials_static/platformer/step5/1.png
    :align: center
    :width: 75%

|

.. dropdown:: Here is what that code looks like:

    This code has new
    `files <https://raw.githubusercontent.com/rubatopy/rubato/main/demo/platformer/files.zip>`_.


    .. literalinclude:: ../../../../demo/platformer/main.py
        :language: python
        :caption: main.py

    .. literalinclude:: ../../../../demo/platformer/level1.py
        :language: python
        :caption: level1.py

    .. literalinclude:: ../../../../demo/platformer/level2.py
        :language: python
        :caption: level2.py

    .. literalinclude:: ../../../../demo/platformer/main_menu.py
        :language: python
        :caption: main_menu.py

    .. literalinclude:: ../../../../demo/platformer/end_menu.py
        :language: python
        :caption: end_menu.py

    .. literalinclude:: ../../../../demo/platformer/shared.py
        :language: python
        :caption: shared.py

    .. literalinclude:: ../../../../demo/platformer/player_controller.py
        :language: python
        :caption: player_controller.py

    .. literalinclude:: ../../../../demo/platformer/moving_platform.py
        :language: python
        :caption: moving_platform.py

We hope this tutorial gave enough detail as to the basics of rubato to let you make your own games and simulations!
If you have questions or feedback, please feel free to contact us on our `Discord server <https://discord.gg/rdce5GXRrC>`_ or by `sending us an email <mailto:info@rubato.app>`_!
