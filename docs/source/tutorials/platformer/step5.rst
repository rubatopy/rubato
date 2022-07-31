###############################
Step 5 - Finishing Touches
###############################

This is the final step! We'll be making small quality-of-life changes to the game to make it play more like a real platformer.

.. important::

    This step covers general game development concepts that are not unique to rubato (grounding detection, camera scrolling, etc). We will not be going
    over how these work, rather we will be focusing on how to implement them in our game. A quick Google search on any of these topics is a great place
    to start learning.

**********
Jump Limit
**********

Right now, when you move around, you'll find that you quickly run out of jumps. This is because we implemented a 2 jump limit. However,
once you run out of jumps, you can't do anything to reset your jump counter. We want this counter to be reset whenever you land on the ground. To do
this, we will add a ground detection hitbox to the player, making sure to set the ``trigger`` parameter to true.

Making a hitbox a "trigger" prevents the hitbox from colliding. It will still detect collisions and call the relevant callbacks.
We will define a player_collide callback that will be called when the player's ground detector collides.
When this happens, we use the provided collision :func:`Manifold <rubato.struct.gameobject.physics.engine.Manifold>` to
make sure the other collider is a ground hitbox, that we are not already grounded, and that we are indeed falling towards the ground.
That code looks like this:

.. code-block:: python

    grounded = False # This line should be under the jump counter variable

    def player_collide(col_info: rb.Manifold):
        global jumps, grounded
        if col_info.shape_b.tag == "ground" and not grounded and player_body.velocity.y >= 0:
            grounded = True
            jumps = 2
            p_animation.set_current_state("idle", True)

    # add a hitbox to the player with the collider
    player.add(rb.Rectangle(width=64, height=64, tag="player")) # This line should already be in your code
    # add a ground detector
    player.add(rb.Rectangle(
        width=10,
        height=2,
        offset=rb.Vector(0, 32),
        trigger=True,
        on_collide=player_collide,
    ))

For this to work, you also need to update the event listner at the bottom to look like this:

.. code-block:: python

    # define a custom input listener
    def handle_keydown(event):
        global jumps, grounded
        if event["key"] == "w" and jumps > 0:
            grounded = False
            player_body.velocity.y = -800
            if jumps == 2:
                p_animation.set_current_state("jump", freeze=2)
            elif jumps == 1:
                p_animation.set_current_state("somer", True)
            jumps -= 1

*************
Camera Scroll
*************

In your testing, you may have also noticed that you are able to walk past the right side of your screen. This is because there is actually more level
space there! Remember that we set our level to be 120% the width of the screen. Lets use rubato's built-in lerp function to make our camera follow the player.

.. code-block:: python

    # define a custom fixed update function
    def fixed_update():
        # have the camera follow the player
        camera_ideal = rb.Math.clamp(
            player.pos.x + rb.Display.res.x / 4, rb.Display.center.x, level_size - rb.Display.res.x / 2
        )
        rb.Game.camera.pos.x = rb.Math.lerp(rb.Game.camera.pos.x, camera_ideal, rb.Time.fixed_delta / 0.4)


    # set the scene's update function
    main.update = update # This line should already exist in your code
    main.fixed_update = fixed_update

``lerp`` and ``clamp`` are both built-in methods to the :func:`rb.Math <rubato.utils.rb_math.Math>` class.
Note that we've used :func:`rb.Time.fixed_delta <rubato.utils.rb_time.Time.fixed_delta>`, which represents the
time elapsed since the last update to the physics engine, in seconds. This is to make our camera follow the player more smoothly,
in line with the fps.

***********
To Conclude
***********

**That's it! You've finished your first platformer in rubato!**

This was just the tip of the iceberg of what rubato can do.

.. dropdown:: If you got lost, here's the full code, just for kicks:

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

        grounded = False
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


        def player_collide(col_info: rb.Manifold):
            global jumps, grounded
            if col_info.shape_b.tag == "ground" and not grounded and player_body.velocity.y >= 0:
                grounded = True
                jumps = 2
                p_animation.set_current_state("idle", True)


        # add a hitbox to the player with the collider
        player.add(rb.Rectangle(width=64, height=64, tag="player"))  # This line should already be in your code
        # add a ground detector
        player.add(rb.Rectangle(
            width=10,
            height=2,
            offset=rb.Vector(0, 32),
            trigger=True,
            on_collide=player_collide,
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


        # define a custom fixed update function
        def fixed_update():
            # have the camera follow the player
            camera_ideal = rb.Math.clamp(
                player.pos.x + rb.Display.res.x / 4, rb.Display.center.x, level_size - rb.Display.res.x / 2
            )
            rb.Game.camera.pos.x = rb.Math.lerp(rb.Game.camera.pos.x, camera_ideal, rb.Time.fixed_delta / 0.4)


        # set the scene's update function
        main.update = update
        main.fixed_update = fixed_update


        # define a custom input listener
        def handle_keydown(event):
            global jumps, grounded
            if event["key"] == "w" and jumps > 0:
                grounded = False
                player_body.velocity.y = -800
                if jumps == 2:
                    p_animation.set_current_state("jump", freeze=2)
                elif jumps == 1:
                    p_animation.set_current_state("somer", True)
                jumps -= 1


        rb.Radio.listen("KEYDOWN", handle_keydown)

        # begin the game
        rb.begin()

We're also including a version with some more in-depth features that weren't covered in this tutorial, including
win detection, advanced animation switching, and a respawn system.

.. dropdown:: Here is what that code looks like:

    .. literalinclude:: ../../../../demo/platformer.py
        :language: python
        :lines: 6-
        :caption: platformer.py

We hope this tutorial gave enough detail as to the basics of rubato to let you make your own games and simulations!
If you have questions or feedback, please feel free to contact us on our `Discord server <https://discord.gg/rdce5GXRrC>`_ or by `sending us an email <mailto:info@rubato.app>`_!
