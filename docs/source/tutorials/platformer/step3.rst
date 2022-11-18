###############################
Step 3 - Adding Player Behavior
###############################

In this step, we will be adding player behavior to our character.

We want our dinosaur to be able to move left, right and jump.
We also want to apply physics laws to him, such as gravity and collisions with future obstacles.

First, let's add physics to our player. To do this, we will add a :func:`RigidBody <rubato.structure.gameobject.physics.rigidbody.RigidBody>` component to our
player. Add the following code after the animation code, but before the ``main.add`` call.

.. literalinclude:: step3_shared.py
    :caption: shared.py
    :lines: 18-26
    :linenos:
    :lineno-start: 18
    :emphasize-lines: 3-

This enables physics for our player. Running the file, you should see the dinosaur slowly falling down the screen. 2 things to note here:
    * We base the gravity off of our Display resolution so that scaling our screen does not affect the gravity.
    * ``pos_correction`` is the amount we correct the position of the player every frame if it is colliding with something. Setting it to 1 means that all overlaps are fully corrected in one frame.

Let's also add a hitbox to our player. For simplicity, we will use a rectangular hitbox. Add the following code right after the previous block.

.. literalinclude:: step3_shared.py
    :caption: shared.py
    :lines: 26-33
    :linenos:
    :lineno-start: 26
    :emphasize-lines: 3-

This rectangle won't actually draw unless the following line is added.
Feel free to remove the following line once you've confirmed that the rectangle was added properly.

.. code-block:: python

    rb.Game.debug = True

.. image:: /_static/tutorials_static/platformer/step3/1.png
    :width: 75%
    :align: center

Running the script at this point should show a falling dinosaur.

Next we need to make a player controller. A player controller is a script that defines how the player moves. This could
include things like physics, input handling, movement, and more. Make a new file called :code:`player_controller.py`.

Make a custom component by inheriting from rubato's :func:`Component <rubato.structure.gameobject.component.Component>`.
Then add the components we added by reference from the game object.

.. literalinclude:: step3_player_controller.py
    :caption: player_controller.py
    :lines: 1-11
    :linenos:

Let's add movement. Since we need to check player input every frame, lets create a custom update function.

.. literalinclude:: step3_player_controller.py
    :caption: player_controller.py
    :lines: 5-12,18-26
    :linenos:
    :lineno-start: 5
    :emphasize-lines: 9-

Here we check for player input using :func:`key_pressed() <rubato.utils.rb_input.Input.key_pressed>`. We then update the player's horizontal velocity
in the corresponding direction. We also flip the player's animation depending on the direction we want to face. Now, when you press "a" or "d" you
should be able to move the player left and right.

Next, import the player controller at the top of :code:`shared.py` and add it to the player.

.. literalinclude:: step3_shared.py
    :caption: shared.py
    :lines: 28-
    :lineno-start: 28
    :emphasize-lines: 7

.. admonition:: Cool!
    :class: tip

    The :code:`:=` operator is called the walrus operator. It assigns the value to the variable on the left and returns the value.
    It is equivalent to :code:`player_comp = PlayerController()`. And then passing it to :code:`player.add()`.

Finally, let's add a jump behavior. Unlike moving left and right, we don't want the user to be able to move up forever if they keep holding the jump
key. We also want to limit the number of jumps the player gets. We will do this by creating a jump counter and process the jump through an event
listener.

An event listener is a piece of code that waits for an event to be broadcast and then runs a function. We will create a function to handle jumping
that is called when a key is pressed.

.. literalinclude:: step3_player_controller.py
    :caption: player_controller.py
    :lines: 18-
    :lineno-start: 18
    :emphasize-lines: 11-

For this to work, you must create a jumps variable and register our keydown handler.

.. literalinclude:: step3_player_controller.py
    :caption: player_controller.py
    :lines: 5-16
    :lineno-start: 5
    :emphasize-lines: 9-

Let's break this down.

We check if the keydown event's key is "w" and if you still
have jumps remaining. If so, we set your velocity to 800 (remember that we are in a cartesian system).
We also want to vary the jump animation on your last jump. The first is a regular jump and the second is a somersault.
Finally, we decrement the number of jumps you have left, so you can't jump infinitely.

The :code:`Radio.listen(rb.Events.KEYDOWN, self.handle_keydown)` line is where we tell rubato to listen for a keydown event and run the ``handle_keydown`` function
whenever that event is broadcast.
The :func:`Events <rubato.utils.radio.Events>` class has all other rubato-triggered events that you can listen for.

Running the script at this point should show a falling dinosaur, and let you dump twice and move a little left and right before falling to your doom.
In the next step, we'll be building the level for the player to explore.

Here is what you should have so far if you've been following along:

.. literalinclude:: step3_main.py
    :caption: main.py
    :linenos:

.. literalinclude:: step3_shared.py
    :caption: shared.py
    :linenos:
    :emphasize-lines: 2,20-

.. literalinclude:: step3_player_controller.py
    :caption: player_controller.py
    :linenos:
