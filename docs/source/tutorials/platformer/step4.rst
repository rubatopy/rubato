###############################
Step 4 - Creating a Level
###############################

In this step, we will be creating a small level for our player to run in.

We will build our level out of basic rectangle hitboxes. We can also pass in a Color to these hitboxes in order for them to draw.

First let's set a variable for the level size. This will be the width of the level. Let's set it to be 120% the resolution of the screen.
Note that it needs to be an integer, because it represents the width of the level in pixels.

save it in :code:`shared.py`

.. code-block:: python

    # size of level
    level1_size = int(rb.Display.res.x * 1.2)

Along with that lets add some colors to our :code:`shared.py` file.

.. code-block:: python

    ##### COLORS #####

    platform_color = rb.Color.from_hex("#b8e994")
    background_color = rb.Color.from_hex("#82ccdd")
    win_color = rb.Color.green.darker(75)

The color darker function allows us to darken a color py an amount. Subtracting this from all values.

.. important::
    Next we will create a new file :code:`level1.py` in it we will define all the elements unique to our level.

The level1 represents a scene with our level in it. All the work we did up until now should have really been put in :code:`level1.py`.
So lets make a scene in level1.py and add all our things there. Deleting our player from main, as well as the main scene.

.. code-block:: python

    import shared
    from rubato import GameObject, Rectangle, Display, Scene

    scene = Scene("level1", background_color=shared.background_color)

    # Add the player to the scene
    scene.add(shared.player)


.. important::
    Finally import :code:`level1.py` from :code:`main.py` instead of :code:`shared.py` and check that it works.


We will create our floor. We do this by creating a GameObject and adding a Rectangle hitbox to it.
In the following code we also use the Rectangle's bottom_left property to place the floor correctly. We also give a "ground" tag to our floor. This will be
used later to determine if the player is on the ground.

In the :code:`level1.py` file, add the following code:

.. code-block:: python

    # create the ground
    ground = GameObject().add(ground_rect := Rectangle(width=1270, height=50, color=shared.platform_color, tag="ground"))
    ground_rect.bottom_left = Display.bottom_left

    # at the bottom
    scene.add(shared.player, ground)


You can also change the player gravity to ``rb.Vector(y=rb.Display.res.y * -1.5)``, which will make the game more realistic. It should look like this
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

        end_location = Vector(Display.left + shared.level1_size - 128, 450)

        # create platforms
        platforms = [
            Rectangle(
                150,
                40,
                offset=Vector(-650, -200),
            ),
            Rectangle(
                150,
                40,
                offset=Vector(500, 40),
            ),
            Rectangle(
                150,
                40,
                offset=Vector(800, 200),
            ),
            Rectangle(256, 40, offset=end_location - (0, 64 + 20))
        ]

        for p in platforms:
            p.tag = "ground"
            p.color = shared.platform_color

        # create pillars
        pillars = [
            GameObject(pos=Vector(-260)).add(Rectangle(
                width=100,
                height=650,
            )),
            GameObject(pos=Vector(260)).add(Rectangle(
                width=100,
                height=400,
            )),
        ]

        for pillar in pillars:
            r = pillar.get(Rectangle)
            r.bottom = Display.bottom + 50
            r.tag = "ground"
            r.color = shared.platform_color

        # add them all to the scene
        # note wrap is a rubato function that allows us to get a game object with a component or components added to it.
        # you will need to import this.
        scene.add(shared.player, ground, wrap(platforms), *pillars)

Now that you have a level built, we need to move around it. You may notice that you are currently able to fall off the world. This is because nothing
is stopping you from doing so. Let's fix this by adding a clear hitbox on either side of the play area.

Add this in the :code:`shared.py` and :code:`level1.py` files.

.. code-block:: python

    # in shared.py
    ##### SIDE BOUDARIES #####

    left = rb.GameObject(pos=rb.Display.center_left - rb.Vector(25, 0)).add(rb.Rectangle(width=50, height=rb.Display.res.y))
    right = rb.GameObject().add(rb.Rectangle(width=50, height=rb.Display.res.y))

    # in level1.py
    # need to be able to set the right side's position especially for each level
    shared.right.pos = Display.center_left + Vector(shared.level1_size + 25, 0)

    # add them all to the scene
    main.add(player, ground, left, right, *platforms, *obstacles)

.. admonition:: Remember!
    :class: tip

    To not have the hitbox render, don't pass a color to the hitbox! All other functionality will remain untouched.

You'll now notice that the player is unable to fall off the world. This is because the hitbox is blocking it's path.

There's one big issue, however. Jumps don't come back, even once you hit the ground. Not to worry. We will implement this in :doc:`step5`.

.. dropdown:: Our game file is now getting pretty big! It should currently look like this (with your own level of course!)

    :code:`main.py`

    .. code-block:: python

        import rubato as rb

        rb.init(
            name="Platformer Demo",  # Set a name
            res=rb.Vector(1920, 1080),  # Set the window resolution (pixel length and height).
            fullscreen="desktop",  # Set the window to be fullscreen
        )

        import level1

        # begin the game
        rb.begin()

    :code:`shared.py`

    .. code-block:: python

        import rubato as rb
        from player_controller import PlayerController

        ##### MISC #####

        level1_size = int(rb.Display.res.x * 1.2)

        ##### COLORS #####

        platform_color = rb.Color.from_hex("#b8e994")
        background_color = rb.Color.from_hex("#82ccdd")
        win_color = rb.Color.green.darker(75)

        ##### PLAYER PREFAB #####

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
            gravity=rb.Vector(y=rb.Display.res.y * -1.5),  # changed to be stronger
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

        ##### SIDE BOUDARIES #####
        # we added side boundaries to the game as well, so you won't fall off the world. The right needs to be programmed in the level.

        left = rb.GameObject(pos=rb.Display.center_left - rb.Vector(25, 0)).add(rb.Rectangle(width=50, height=rb.Display.res.y))
        right = rb.GameObject().add(rb.Rectangle(width=50, height=rb.Display.res.y))

    :code:`player_controller.py`

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


    :code:`level1.py`

    .. code-block:: python

        import shared
        from rubato import GameObject, Rectangle, Display, Scene, Vector, wrap

        scene = Scene("level1", background_color=shared.background_color)


        ground = GameObject().add(ground_rect := Rectangle(width=1270, height=50, color=shared.platform_color, tag="ground"))
        ground_rect.bottom_left = Display.bottom_left

        end_location = Vector(Display.left + shared.level1_size - 128, 450)

        # create platforms
        platforms = [
            Rectangle(
                150,
                40,
                offset=Vector(-650, -200),
            ),
            Rectangle(
                150,
                40,
                offset=Vector(500, 40),
            ),
            Rectangle(
                150,
                40,
                offset=Vector(800, 200),
            ),
            Rectangle(256, 40, offset=end_location - (0, 64 + 20))
        ]

        for p in platforms:
            p.tag = "ground"
            p.color = shared.platform_color

        # create pillars, learn to do it with Game Objects too
        pillars = [
            GameObject(pos=Vector(-260)).add(Rectangle(
                width=100,
                height=650,
            )),
            GameObject(pos=Vector(260)).add(Rectangle(
                width=100,
                height=400,
            )),
        ]

        for pillar in pillars:
            r = pillar.get(Rectangle)
            r.bottom = Display.bottom + 50
            r.tag = "ground"
            r.color = shared.platform_color

        # program the right boundary
        shared.right.pos = Display.center_left + Vector(shared.level1_size + 25, 0)


        scene.add(shared.player, ground, wrap(platforms), *pillars, shared.left, shared.right)
