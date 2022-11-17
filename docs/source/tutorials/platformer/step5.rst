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

In :code:`shared.py` add the following code, deleting our sporadic adds, and adding a ground detector to the player:

.. code-block:: python


    player.add(
        # add a hitbox to the player with the collider
        rb.Rectangle(width=40, height=64, tag="player"),
        # add a ground detector
        rb.Rectangle(
            width=34,
            height=2,
            offset=rb.Vector(0, -32),
            trigger=True,
            tag="player_ground_detector",
        ),
        # add a rigidbody to the player
        rb.RigidBody(gravity=rb.Vector(y=rb.Display.res.y * -1.5), pos_correction=1, friction=1),
        # add custom player component
        player_comp := PlayerController(),
    )

In :code:`player_controller.py` we get our ground detector and set its on_collide and on_exit callbacks:

.. code-block:: python

        def setup(self):
            self.initial_pos = self.gameobj.pos.clone()

            self.animation: Animation = self.gameobj.get(Animation)
            self.rigid: RigidBody = self.gameobj.get(RigidBody)

            rects = self.gameobj.get_all(Rectangle)
            self.ground_detector: Rectangle = [r for r in rects if r.tag == "player_ground_detector"][0]
            self.ground_detector.on_collide = self.ground_detect
            self.ground_detector.on_exit = self.ground_exit

            self.grounded = False  # tracks the ground state
            self.jumps = 0  # tracks the number of jumps the player has left

            Radio.listen(Events.KEYDOWN, self.handle_key_down)

        def ground_detect(self, col_info: Manifold):
            if "ground" in col_info.shape_b.tag and self.rigid.velocity.y >= 0:
                if not self.grounded:
                    self.grounded = True
                    self.jumps = 2
                    self.animation.set_state("idle", True)

        def ground_exit(self, col_info: Manifold):
            if "ground" in col_info.shape_b.tag:
                self.grounded = False


*************
Camera Scroll
*************

In your testing, you may have also noticed that you are able to walk past the right side of your screen. This is because there is actually more level
space there! Remember that we set our level to be 120% the width of the screen. Lets use rubato's built-in lerp function to make our camera follow the player.

In :code:`player_controller.py` add the following code:

.. code-block:: python

    # define a custom fixed update function
    def fixed_update(self):
        # have the camera follow the player
        current_scene = Game.current()
        camera_ideal = Math.clamp(
            self.gameobj.pos.x + Display.res.x / 4, Display.center.x, shared.level1_size - Display.res.x
        )
        current_scene.camera.pos.x = Math.lerp(current_scene.camera.pos.x, camera_ideal, Time.fixed_delta / 0.4)

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


        player.add(
            # add a hitbox to the player with the collider
            rb.Rectangle(width=40, height=64, tag="player"),
            # add a ground detector
            rb.Rectangle(
                width=34,
                height=2,
                offset=rb.Vector(0, -32),
                trigger=True,
                tag="player_ground_detector",
            ),
            # add a rigidbody to the player
            rb.RigidBody(gravity=rb.Vector(y=rb.Display.res.y * -1.5), pos_correction=1, friction=1),
            # add custom player component
            player_comp := PlayerController(),
        )

        ##### SIDE BOUDARIES #####

        left = rb.GameObject(pos=rb.Display.center_left - rb.Vector(25, 0)).add(rb.Rectangle(width=50, height=rb.Display.res.y))
        right = rb.GameObject().add(rb.Rectangle(width=50, height=rb.Display.res.y))

    :code:`player_controller.py`

    .. code-block:: python

        from rubato import Component, Animation, RigidBody, Rectangle, Manifold, Radio, Events, KeyResponse, \
            Input, Math, Display, Game, Time, Vector
        import shared


        class PlayerController(Component):

            def setup(self):
                self.initial_pos = self.gameobj.pos.clone()

                self.animation: Animation = self.gameobj.get(Animation)
                self.rigid: RigidBody = self.gameobj.get(RigidBody)

                rects = self.gameobj.get_all(Rectangle)
                self.ground_detector: Rectangle = [r for r in rects if r.tag == "player_ground_detector"][0]
                self.ground_detector.on_collide = self.ground_detect
                self.ground_detector.on_exit = self.ground_exit

                self.grounded = False  # tracks the ground state
                self.jumps = 0  # tracks the number of jumps the player has left

                Radio.listen(Events.KEYDOWN, self.handle_key_down)

            def ground_detect(self, col_info: Manifold):
                if "ground" in col_info.shape_b.tag and self.rigid.velocity.y >= 0:
                    if not self.grounded:
                        self.grounded = True
                        self.jumps = 2
                        self.animation.set_state("idle", True)

            def ground_exit(self, col_info: Manifold):
                if "ground" in col_info.shape_b.tag:
                    self.grounded = False

            def handle_key_down(self, event: KeyResponse):
                if event.key == "w" and self.jumps > 0:
                    if self.jumps == 2:
                        self.rigid.velocity.y = 800
                        self.animation.set_state("jump", freeze=2)
                    elif self.jumps == 1:
                        self.rigid.velocity.y = 800
                        self.animation.set_state("somer", True)
                    self.jumps -= 1

            def update(self):
                # Runs once every frame.
                # Movement
                if Input.key_pressed("a"):
                    self.rigid.velocity.x = -300
                    self.animation.flipx = True
                elif Input.key_pressed("d"):
                    self.rigid.velocity.x = 300
                    self.animation.flipx = False
                else:
                    if not self.grounded:
                        self.rigid.velocity.x = 0
                        self.rigid.friction = 0
                    else:
                        self.rigid.friction = 1

                # Running animation states
                if self.grounded:
                    if self.rigid.velocity.x in (-300, 300):
                        if Input.key_pressed("shift") or Input.key_pressed("s"):
                            self.animation.set_state("sneak", True)
                        else:
                            self.animation.set_state("run", True)
                    else:
                        if Input.key_pressed("shift") or Input.key_pressed("s"):
                            self.animation.set_state("crouch", True)
                        else:
                            self.animation.set_state("idle", True)

                # Reset
                if Input.key_pressed("r") or self.gameobj.pos.y < -550:
                    self.gameobj.pos = self.initial_pos.clone()
                    self.rigid.stop()
                    self.grounded = False
                    Game.current().camera.pos = Vector(0, 0)

            # define a custom fixed update function
            def fixed_update(self):
                # have the camera follow the player
                current_scene = Game.current()
                camera_ideal = Math.clamp(
                    self.gameobj.pos.x + Display.res.x / 4, Display.center.x, shared.level1_size - Display.res.x
                )
                current_scene.camera.pos.x = Math.lerp(current_scene.camera.pos.x, camera_ideal, Time.fixed_delta / 0.4)



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

        shared.right.pos = Display.center_left + Vector(shared.level1_size + 25, 0)


        scene.add(shared.player, ground, wrap(platforms), *pillars, shared.left, shared.right)

We're also including a version with some more in-depth features that weren't covered in this tutorial, including
win detection, advanced animation switching, and a respawn system. Also new scenes, with multiple levels. It's the real deal.

Sneak Peak:

.. image:: /_static/tutorials_static/platformer/step5/1.png
    :align: center
    :width: 75%

.. dropdown:: Here is what that code looks like:

    .. literalinclude:: ../../../../demo/platformer/main.py
        :language: python
        :lines: 6-
        :caption: main.py

    .. literalinclude:: ../../../../demo/platformer/level1.py
        :language: python
        :lines: 6-
        :caption: level1.py

    .. literalinclude:: ../../../../demo/platformer/level2.py
        :language: python
        :lines: 6-
        :caption: level2.py

    .. literalinclude:: ../../../../demo/platformer/main_menu.py
        :language: python
        :lines: 6-
        :caption: main_menu.py

    .. literalinclude:: ../../../../demo/platformer/end_menu.py
        :language: python
        :lines: 6-
        :caption: end_menu.py

    .. literalinclude:: ../../../../demo/platformer/shared.py
        :language: python
        :lines: 6-
        :caption: shared.py

    .. literalinclude:: ../../../../demo/platformer/player_controller.py
        :language: python
        :lines: 6-
        :caption: player_controller.py

    .. literalinclude:: ../../../../demo/platformer/moving_platform.py
        :language: python
        :lines: 6-
        :caption: moving_platform.py

We hope this tutorial gave enough detail as to the basics of rubato to let you make your own games and simulations!
If you have questions or feedback, please feel free to contact us on our `Discord server <https://discord.gg/rdce5GXRrC>`_ or by `sending us an email <mailto:info@rubato.app>`_!
