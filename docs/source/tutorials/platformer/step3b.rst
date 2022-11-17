##########################
Step 3b - Creating Player Behaviour
##########################

We need to add Player Behaviour all game object behaviour in rubato is done through components.

Make a new file called :code:`player_controller.py`

Make a custom component by inheriting from rubato's :func:`Component <rubato.struct.gameobject.component.Component>`.
Then add the components we added by reference from the game object.

.. code-block:: python

    from rubato import Component

    class PlayerController(Component):

        def setup(self):
            # Like the init function of regular classes. Called when added to Game Object.
            # Specifics can be found in the Custom Components tutorial.
            self.initial_pos = self.gameobj.pos.clone()

            self.animation: Animation = self.gameobj.get(Animation)
            self.rigid: RigidBody = self.gameobj.get(RigidBody)


Let's add movement. Since we need to check player input every frame, lets create a custom update function.
This function runs once every frame.

.. code-block:: python

        def update(self):
            # Runs once every frame.
            # Movement
            if Input.key_pressed("a"):
                self.rigid.velocity.x = -300
                self.animation.flipx = True
            elif Input.key_pressed("d"):
                self.rigid.velocity.x = 300
                self.animation.flipx = False

.. admonition:: Remember!
    :class: tip

    import Input from rubato and all others.
    :code:`from rubato import Component, Input, Animation, RigidBody`

Next, import the player controller in :code:`shared.py` and add it to the player

.. code-block:: python

    # at top
    from player_controller import PlayerController

    # at bottom
    player.add(player_comp := PlayerController())


Here we check for player input using :func:`key_pressed() <rubato.utils.rb_input.Input.key_pressed>`. We then update the player's horizontal velocity
in the corresponding direction. We also flip the player's animation depending on the direction we want to face. Now, when you press "a" or "d" you
should be able to move the player left and right.

.. admonition:: Cool!
    :class: tip

    The :code:`:=` operator is called the walrus operator. It assigns the value to the variable on the left and returns the value.
    It is equivalent to :code:`player_comp = PlayerController()`. And then passing it to :code:`player.add()`.

Finally, let's add a jump behavior. Unlike moving left and right, we don't want the user to be able to move up forever if they keep holding the jump
key. We also want to limit the number of jumps the player gets. We will do this by creating a jump counter and process the jump through an event
listener.

An event listener is a piece of code that waits for an event to be broadcast and then runs a function. We will create a function to handle jumping
that is called when the "w" key is pressed.

.. code-block:: python

    # don't forget to import KeyResponse from rubato.
    def handle_key_down(self, event: KeyResponse):
        if event.key == "w" and self.jumps > 0:
            if self.jumps == 2:
                self.rigid.velocity.y = 800
                self.animation.set_state("jump", freeze=2)
            elif self.jumps == 1:
                self.rigid.velocity.y = 800
                self.animation.set_state("somer", True)
            self.jumps -= 1

Also in the setup function, to add the jump variable and subscribe our new keydown handling function to the keydown event add the following:

.. code-block:: python

    # Tracks the number of jumps the player has left
    self.jumps = 2

    Radio.listen(Events.KEYDOWN, self.handle_key_down)

.. Note::

    Don't forget to import Event and Radio from rubato.

Let's break this down.

We check if the keydown event's key is "w" and if you still
have jumps remaining. If so, we set your upwards velocity to 800 (remember that we are in a cartesian system).
We also want to vary the jump animation on your last jump. The first is a regular jump and the second is a somersault.
Finally, we decrement the number of jumps you have left, so you can't jump infinitely.

The :code:`Radio.listen(Events.KEYDOWN, self.handle_keydown)` line is where we tell rubato to listen for a keydown event and run the ``handle_keydown`` function
whenever that event is broadcast. Note that you can also replace ``rb.Events.KEYDOWN`` with ``"KEYDOWN"`` and get the same functionality.
:func:`Events <rubato.utils.radio.Events>` have all other rubato-triggered events that you can listen for.

Running the script at this point should show a falling dinosaur, and let you dump twice and move a little left and right before falling to your doom.
In the next step, we'll be building the level for the player to explore.


Here is what you should have so far if you've been following along:

In :code:`main.py`:

.. code-block:: python

    import rubato as rb

    # initialize a new game
    main = rb.Scene(background_color=rb.Color.cyan.lighter())

    rb.init(
        name="Platformer Demo",  # Set a name
        res=rb.Vector(1920, 1080),  # Set the window resolution (pixel length and height).
        fullscreen="desktop",  # Set the window to be fullscreen
    )

    import shared

    # Add the player to the scene
    main.add(shared.player)
    # begin the game
    rb.begin()


AND in :code:`shared.py`:

.. code-block:: python

    import rubato as rb
    from player_controller import PlayerController

    # Create the player and set its starting position
    player = rb.GameObject(
        pos=rb.Display.center_left + rb.Vector(50, 0),
        z_index=1,
    )

    # Create animation and initialize states
    p_animation = rb.Spritesheet.from_folder(
        path="files/dino",
        sprite_size=rb.Vector(24, 24),
        default_state="idle",
    )
    p_animation.scale = rb.Vector(4, 4)
    p_animation.fps = 10  # The frames will change 10 times a second
    player.add(p_animation)  # Add the animation component to the player

    # define the player rigidbody
    player_body = rb.RigidBody(
        gravity=rb.Vector(y=rb.Display.res.y * -0.5),
        pos_correction=1,
        friction=0.8,
    )
    player.add(player_body)

    # add a hitbox to the player with the collider
    player.add(rb.Rectangle(
        width=64,
        height=64,
        tag="player",
    ))
    player.add(player_comp := PlayerController())
    rb.Game.debug = True

AND in :code:`player_controller.py`:

.. code-block:: python

    from rubato import Component, Input, Animation, RigidBody, KeyResponse, Events, Radio


    class PlayerController(Component):

        def setup(self):
            # Like the init function of regular classes. Called when added to Game Object.
            # Specifics can be found in the Custom Components tutorial.
            self.initial_pos = self.gameobj.pos.clone()

            self.animation: Animation = self.gameobj.get(Animation)
            self.rigid: RigidBody = self.gameobj.get(RigidBody)

            # Tracks the number of jumps the player has left
            self.jumps = 2

            Radio.listen(Events.KEYDOWN, self.handle_key_down)

        def update(self):
            # Runs once every frame.
            # Movement
            if Input.key_pressed("a"):
                self.rigid.velocity.x = -300
                self.animation.flipx = True
            elif Input.key_pressed("d"):
                self.rigid.velocity.x = 300
                self.animation.flipx = False

        def handle_key_down(self, event: KeyResponse):
            if event.key == "w" and self.jumps > 0:
                if self.jumps == 2:
                    self.rigid.velocity.y = 800
                    self.animation.set_state("jump", freeze=2)
                elif self.jumps == 1:
                    self.rigid.velocity.y = 800
                    self.animation.set_state("somer", True)
                self.jumps -= 1
