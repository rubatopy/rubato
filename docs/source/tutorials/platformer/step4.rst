###############################
Step 4 - Creating a Level
###############################

In this step, we will be creating a small level for our player to run in.

We will build our level out of basic rectangle hitboxes. We can also pass in a Color to these hitboxes in order for them to draw.

First let's set a variable for the level size. This will be the width of the level. Let's set it to be 120% the resolution of the screen.
Note that it needs to be an integer, because it represents the width of the level in pixels.

.. code-block:: python

    # size of level
    level_size = int(rb.Display.res.x * 1.2)

This should be added right after the init call. Next, we will create our floor. We do this by creating a GameObject and adding a Rectangle hitbox to it.
In the following code we also use the Rectangle's bottom_left property to place the floor correctly. We also give a "ground" tag to our floor. This will be
used later to determine if the player is on the ground.

.. code-block:: python

    # create the ground
    ground = rb.GameObject()
    ground.add(rb.Rectangle(width=level_size, height=50, color=rb.Color.green, tag="ground"))
    ground.get(rb.Rectangle).bottom_left = rb.Display.bottom_left

Place this before ``main.add`` and update that call to add the ground as well:

.. code-block:: python

    main.add(player, ground)

You can also change the player gravity to ``1.5 * rb.Display.res.y``, which will make the game more realistic. It should look like this
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

    .. code-block:: python

        # create platforms
        platforms = [
            rb.GameObject(pos=rb.Vector(200, rb.Display.bottom - 140)
                        ).add(rb.Rectangle(
                            width=90,
                            height=40,
                            tag="ground",
                            color=rb.Color.blue,
                        )),
            rb.GameObject(pos=rb.Vector(400, rb.Display.bottom - 340)
                        ).add(rb.Rectangle(
                            width=150,
                            height=40,
                            tag="ground",
                            color=rb.Color.blue,
                        )),
        ]

        # create obstacles
        obstacles = [
            rb.GameObject(pos=rb.Vector(700)).add(rb.Rectangle(
                width=90,
                height=500,
                tag="ground",
                color=rb.Color.purple,
            )),
            rb.GameObject(pos=rb.Vector(1200)).add(rb.Rectangle(
                width=70,
                height=450,
                tag="ground",
                color=rb.Color.purple,
            )),
        ]

        for obstacle in obstacles:
            obstacle.get(rb.Rectangle).bottom = rb.Display.bottom - 30

        # add them all to the scene
        main.add(player, ground, *platforms, *obstacles)


Now that you have a level built, we need to move around it. You may notice that you are currently able to fall off the world. This is because nothing
is stopping you from doing so. Let's fix this by adding a clear hitbox on either side of the play area.

.. code-block:: python

    # Side boundary
    left = rb.GameObject(pos=rb.Display.center_left - rb.Vector(25, 0))
    left.add(rb.Rectangle(width=50, height=rb.Display.res.y))
    right = rb.GameObject(pos=rb.Display.center_left + rb.Vector(level_size + 25, 0))
    right.add(rb.Rectangle(width=50, height=rb.Display.res.y))

    # add them all to the scene
    main.add(player, ground, left, right, *platforms, *obstacles)

.. admonition:: Remember!
    :class: tip

    To not have the hitbox render, don't pass a color to the hitbox! All other functionality will remain untouched.

You'll now notice that the player is unable to fall off the world. This is because the hitbox is blocking it's path.

There's one big issue, however. Jumps don't come back, even once you hit the ground. Not to worry. We will implement this in :doc:`step5`.

.. dropdown:: Our game file is now getting pretty big! It should currently look like this (with your own level of course!)

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
        # size of level
        level_size = int(rb.Display.res.x * 1.2)

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
            gravity=rb.Vector(y=rb.Display.res.y * 1.5),
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

        # create the ground
        ground = rb.GameObject()
        ground.add(rb.Rectangle(width=level_size, height=50, color=rb.Color.green, tag="ground"))
        ground.get(rb.Rectangle).bottom_left = rb.Display.bottom_left

        # create platforms
        platforms = [
            rb.GameObject(pos=rb.Vector(200, rb.Display.bottom - 140)
                        ).add(rb.Rectangle(
                            width=90,
                            height=40,
                            tag="ground",
                            color=rb.Color.blue,
                        )),
            rb.GameObject(pos=rb.Vector(400, rb.Display.bottom - 340)
                        ).add(rb.Rectangle(
                            width=150,
                            height=40,
                            tag="ground",
                            color=rb.Color.blue,
                        )),
        ]

        # create obstacles
        obstacles = [
            rb.GameObject(pos=rb.Vector(700)).add(rb.Rectangle(
                width=90,
                height=500,
                tag="ground",
                color=rb.Color.purple,
            )),
            rb.GameObject(pos=rb.Vector(1200)).add(rb.Rectangle(
                width=70,
                height=450,
                tag="ground",
                color=rb.Color.purple,
            )),
        ]

        for obstacle in obstacles:
            obstacle.get(rb.Rectangle).bottom = rb.Display.bottom - 30

        # Side boundary
        left = rb.GameObject(pos=rb.Display.center_left - rb.Vector(25, 0))
        left.add(rb.Rectangle(width=50, height=rb.Display.res.y))
        right = rb.GameObject(pos=rb.Display.center_left + rb.Vector(level_size + 25, 0))
        right.add(rb.Rectangle(width=50, height=rb.Display.res.y))

        # add them all to the scene
        main.add(player, ground, left, right, *platforms, *obstacles)

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
