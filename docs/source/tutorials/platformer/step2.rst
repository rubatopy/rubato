##########################
Step 2 - Creating a Player
##########################

Welcome to the second part of making a platformer in rubato. In this step, we will be building a simple
character with rudimentary physics.

At this point, you should have a window drawing with a cyan background.

First things first, we need to understand how rubato is structured (we will explain it first, then walk you
through it). rubato has 4 different levels: Scenes, Groups, Game Objects, and Components.

:func:`Scenes <rubato.classes.scene.Scene>` hold a collection of Game Objects and Groups. It also manages a
:func:`Camera <rubato.classes.camera.Camera>`. Scenes are used to compartmentalize code. For example,
you could have each level of your game on a different scene. Then to switch levels you would switch scenes.
Every game has a :func:`Scene Manager <rubato.classes.scene_manager.SceneManager>` which helps you switch between scenes
easily.

:func:`Groups <rubato.classes.group.Group>` also hold a collection of Game Objects and other Groups. Their main purpose is to
further compartmentalize items. For example, items in 2 different groups won't collide with each other. In this tutorial,
we won't be using Groups as we don't need this functionality here.

:func:`Game Objects <rubato.classes.game_object.GameObject>` are the main item in a game. They hold Components, have a position, and
have a z-index. By themselves, they have very little functionality.

:func:`Components <rubato.classes.components.component.Component>` are how Game Objects get their functionality. Each component adds or
changes something about the Game Object. For example, an Image component draws an image from your filesystem to the game at the
Game Object's position.

Ok now let's see this in action. Let's create a scene and add it to our game right after :code:`rb.init()` but before
:code:`rb.begin()`.

.. code-block:: python

    # Create a scene
    main = rb.Scene()

Next, we need to create a player and add it to the scene.

.. code-block:: python

    # Create the player and set its starting position
    player = rb.GameObject(
        pos=rb.Display.center_left + rb.Vector(50, 0),
        z_index=1,
    )

    # Add the player to the scene
    main.add(player)


:func:`rb.Display.center_left <rubato.utils.display.Display.center_left>` is the Vector position for the center of the
left side of the screen. Currently we won't see anything because Game Objects don't draw anything. Let's change that
by adding a simple animation to player.

If you take a look inside the ``platformer_files/dino`` directory, you will see a few image files. Each of these image
files is a spritesheet for a single animation. Instead of loading each frame and image ourselves, we can use
:func:`rb.Spritesheet.from_folder() <rubato.classes.components.spritesheet.Spritesheet.from_folder>` to load them
all at once. This function takes the path to a folder and returns an
:func:`Animation <rubato.classes.components.animation.Animation>` component that can then be added to a GameObject.

Our spritesheets have a couple frames and each frame is 24 pixels by 24 pixels. Be sure to specify the sprite size
when you load them. This will let rubato correctly subdivide the spritesheet into frames.

Animations are made up of different states. Each state is can be triggered at any time. When loading from a folder, the
state names are the names of the files. Some states we have are idle, jump, crouch, and run.

We also should specify the default state. This is the state that the animation will start at and the one that it will
return to when other states finish. In our case, this will be the idle state.

.. code-block:: python

    # Create animation and initialize states
    p_animation = rb.Spritesheet.from_folder(
        rel_path="platformer_files/dino",
        sprite_size=rb.Vector(24, 24),
        default_state="idle",
    )
    p_animation.scale = rb.Vector(4, 4)
    p_animation.fps = 10 # The frames will change 10 times a second
    player.add(p_animation) # Add the animation component to the player

Now you should have a cute dinosaur bobbing up and down on the left side of the screen:

.. image:: /_static/tutorials_static/platformer/step2/1.png
    :width: 75%
    :align: center

So cute! Here is what you should have so far if you've been following along:

.. code-block:: python

    import rubato as rb

    # initialize a new game
    rb.init(
        name="Platformer Demo",  # Set a name
        window_size=rb.Vector(960, 540),  # Set the window size
        background_color=rb.Color.cyan.lighter(),  # Set the background color
        res=rb.Vector(1920, 1080),  # Increase the window resolution
    )

    # Create a scene
    main = rb.Scene()

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
    p_animation.fps = 10 # The frames will change 10 times a second
    player.add(p_animation) # Add the animation component to the player

    # Add the player to the scene
    main.add(player)

    # begin the game
    rb.begin()

