Creating a Player
===================

Welcome to the second part of making a platformer in Rubato. In this step, we will be building a simple
character with rudimentary physics.

At this point, you should have a window drawing with a cyan background.

First things first, we need to understand how Rubato is structured (we will explain it first, then walk you
through it). Rubato has 4 different levels: Scenes, Groups, Sprites, and Components.

:func:`Scenes <rubato.classes.scene.Scene>` hold a collection of Sprites and Groups. It also manages a
:func:`Camera <rubato.classes.camera.Camera>`. Scenes are used to compartmentalize code. For example,
you could have each level of your game on a different scene. Then to switch levels you would switch scenes.
Every game has a :func:`Scene Manager <rubato.classes.scene_manager.SceneManager>` which helps you switch between scenes
easily.

:func:`Groups <rubato.classes.group.Group>` also hold a collection of Sprites and other Groups. Their main purpose is to
further compartmentalize items. For example, items in 2 different groups won't collide with each other. In this tutorial,
we won't be using Groups as we don't need this functionality here.

:func:`Sprites <rubato.classes.sprite.Sprite>` are the main item in a game. They hold Components, have a position, and
have a z-index. By themselves, they have very little functionality.

:func:`Components <rubato.classes.component.Component>` are how Sprites get their functionality. Each component adds or
changes something about the Sprite. For example, an Image component draws an image from your filesystem to the game at the
Sprite's position.

Ok now let's see this in action. Let's create a scene and add it to our game right after the initializer but before the
call to :code:`rb.begin()`.

.. code-block:: python

    # Create a scene
    main = rb.Scene()
    # Add the scene to the scene manager and give it a name
    rb.Game.scenes.add(main, "main")

:code:`rb.Game.scenes` is a reference to our Scene Manager. Next, we need to create a player and add it to the scene.

.. code-block:: python

    # Create the player
    player = rb.Sprite({
        "pos": rb.Display.center_left + rb.Vector(50, 0),  # Set the starting position of the player
    })

    # Add the player to the scene
    main.add(player)


:func:`rb.Display.center_left <rubato.utils.display.Display.center_left>` is the Vector position for the center of the
left side of the screen. Currently we won't see anything because Sprites there is nothing to draw.

The source code for this step is available
`here <https://github.com/rubatopy/rubato/tree/main/tutorials/platformer/step2>`__.
