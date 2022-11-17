###############################
Step 3 - Adding Player Behavior
###############################

In this step, we will be adding player behavior to our character.

We want our dinosaur to be able to move left, right and jump.
We also want to apply physics laws to him, such as gravity and collisions with future obstacles.

First, let's add physics to our player. To do this, we will add a :func:`RigidBody <rubato.structure.gameobject.physics.rigidbody.RigidBody>` component to our
player. Add the following code after the animation code, but before the ``main.add`` call.

In :code:`shared.py`:

.. code-block:: python

    # define the player rigidbody
    player_body = rb.RigidBody(
        gravity=rb.Vector(y=rb.Display.res.y * -0.5),  # gravity is 1/2 the screen height per second/second.
        pos_correction=1,
        friction=0.8,
    )
    player.add(player_body)

This enables physics for our player. Running the file, you should see the dinosaur slowly falling down the screen. 2 things to note here:
    * We base the gravity off of our Display resolution so that scaling our screen does not affect the gravity.
    * ``pos_correction`` is the amount we correct the position of the player every frame if it is colliding with something. Setting it to 1 means that all overlaps are fully corrected in one frame.

Let's also add a hitbox to our player. For simplicity, we will use a rectangular hitbox. Add the following code right after the previous block.

In :code:`shared.py`:

.. code-block:: python

    # add a hitbox to the player with the collider
    player.add(rb.Rectangle(
        width=64,
        height=64,
        tag="player",
    ))

This rectangle won't actually draw unless the following line is added.
Feel free to remove the following line once you've confirmed that the rectangle was added properly.

.. code-block:: python

    rb.Game.debug = True

.. image:: /_static/tutorials_static/platformer/step3/1.png
    :width: 75%
    :align: center

Running the script at this point should show a falling dinosaur.

Clean code recap will be in step 3b.
