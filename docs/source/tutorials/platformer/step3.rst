###############################
Step 3 - Adding Player Behavior
###############################

Welcome to the third part of making a platformer in rubato. In this step, we will be adding player behavior to our character.

We want our character to have to behaviors. First, we want to add movement behavior. This includes moving left, right and jumping. We also want our
player to be affected by physics. This means that our player will be affected by gravity and will collide with other physics objects.

First, let's add physics to our player. To do this, we will add a :func:`RigidBody <rubato.classes.components.rigidbody.RigidBody>` component to our
player. Add the following code after the animation code, but before the ``main.add`` call.

.. code-block:: python

    # define the player rigidbody
    player_body = rb.RigidBody(
        gravity=rb.Vector(y=rb.Display.res.y * 0.05),
        pos_correction=1,
        friction=0.8,
    )
    player.add(player_body)

This enables physics for our player. You should see the dinosaur slowly falling down the screen. 2 things to note here:
    * We base the gravity off of our Display resolution so that scaling our screen does not affect the gravity.
    * ``pos_correction`` is the amount of correction to ensure that our player does not get stuck in the ground.

Let's also add a hitbox to our player. For simplicity, we will use a rectangular hitbox. Add the following code right after the previous block.

.. code-block:: python

    # add a hitbox to the player with the collider
    player.add(rb.Rectangle(
        width=64,
        height=64,
        tag="player",
    ))

Currently the game will look the same as before but adding the following line right after the init call will show you what the hitbox looks like.

.. code-block:: python

    rb.Game.debug = True

.. image:: /_static/tutorials_static/platformer/step3/1.png
    :width: 75%
    :align: center

Next let's add movement. Since we need to check player input every frame, lets create a custom update function.

.. code-block:: python

    # define a custom update function
    # this function is run every frame
    def update():
        pass

    main.update = update

Add the above code between the ``main.add`` and the ``rb.begin`` lines. Anything inside this custom update function will be run every frame. Inside
this function, we will check for player input and update the player's velocity accordingly.

.. code-block:: python

    def update():
        if rb.Input.key_pressed("a"):
            player_body.velocity.x = -300
            p_animation.flipx = True
        elif rb.Input.key_pressed("d"):
            player_body.velocity.x = 300
            p_animation.flipx = False
        else:
            player_body.velocity.x = 0

Here we check for player input using :func:`key_pressed() <rubato.utils.rb_input.Input.key_pressed>`. We then update the player's horizontal velocity
in the corresponding direction. We also flip the player's animation depending on the direction we want to face. Now, when you press "a" or "d" you
should be able to move the player left and right.

Finally, let's add a jump behavior. Unlike moving left and right, we don't want the user to be able to move up forever if they keep holding the jump
key. We also want to limit the number of jumps the player gets. We will do this by creating a jump counter and process the jump through an event
listener.

An event listener is a piece of code that waits for an event to be broadcast and then runs a function. We will create a function to handle jumping
that is called when the "w" key is pressed.

.. code-block:: python

    # define a custom input listener
    def handle_keydown(event):
        global jumps
        if event["key"] == "w" and jumps > 0:
            player_body.velocity.y = -200
            if jumps == 2:
                p_animation.set_current_state("jump", freeze=2)
            elif jumps == 1:
                p_animation.set_current_state("somer", True)
            jumps -= 1

    rb.Radio.listen("KEYDOWN", handle_keydown)

Also at the top of your file, under the debug line, add the following:

.. code-block:: python

    # Tracks the number of jumps the player has left
    jumps = 2

The ``handle_keydown`` function does a lot so let's break it down line by line. First, we use the ``global`` keyword to declare that we are changing
the global jumps variable. This variable will be used later when dealing with ground. Next, we check if the keydown event's key is "w" and if you still
have jumps remaining. If so, we set your upwards velocity to 800 (remember that negative y values are up on the screen). Next depending on how many
jumps you have we set a different jump animation. The first is a regular jump and the second is a summersault. Finally, we decrement the number of
jumps you have left.

The :code:`rb.Radio.listen("KEYDOWN", handle_keydown)` line is where we tell rubato to listen for a keydown event and run the ``handle_keydown`` function
when an event is broadcast.

At this point you should be able to move your character around and jump twice before falling to your doom. In the next step we will add a level for you
to run around in.

.. dropdown:: Here is all the code we have done at this point:

    .. code-block:: python

        import rubato as rb

        # initialize a new game
        rb.init(
            name="Platformer Demo",  # Set a name
            res=rb.Vector(1920, 1080),  # Set the window resolution (pixel length and height).
                # note that since we didn't also specify a window size,
                # the window will be automatically resized to half of the resolution.
        )

        rb.Game.debug = True

        # Tracks the number of jumps the player has left
        jumps = 2

        # Create a scene
        main = rb.Scene(background_color=rb.Color.cyan.lighter())

        # Create the player and set its starting position
        player = rb.GameObject(
            pos=rb.Display.center_left + rb.Vector(50, 0),
            z_index=1,
        )

        # Create animation and initialize states
        p_animation = rb.Spritesheet.from_folder(
            rel_path="platformer_files/dino",
            sprite_size=rb.Vector(24, 24),
            default_state="idle",
        )
        p_animation.scale = rb.Vector(4, 4)
        p_animation.fps = 10  # The frames will change 10 times a second
        player.add(p_animation)  # Add the animation component to the player

        # define the player rigidbody
        player_body = rb.RigidBody(
            gravity=rb.Vector(y=rb.Display.res.y * 0.05),
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

        # Add the player to the scene
        main.add(player)


        # define a custom update function
        # this function is run every frame
        def update():
            if rb.Input.key_pressed("a"):
                player_body.velocity.x = -300
                p_animation.flipx = True
            elif rb.Input.key_pressed("d"):
                player_body.velocity.x = 300
                p_animation.flipx = False
            else:
                player_body.velocity.x = 0

            if rb.Input.key_pressed("space"):
                player_body.ang_vel += 10


        main.update = update


        # define a custom input listener
        def handle_keydown(event):
            global jumps
            if event["key"] == "w" and jumps > 0:
                player_body.velocity.y = -200
                if jumps == 2:
                    p_animation.set_current_state("jump", freeze=2)
                elif jumps == 1:
                    p_animation.set_current_state("somer", True)
                jumps -= 1


        rb.Radio.listen("KEYDOWN", handle_keydown)

        # begin the game
        rb.begin()
