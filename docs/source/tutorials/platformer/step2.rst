##########################
Step 2 - Creating a Player
##########################

Welcome to the second part of making a platformer in rubato. In this step, we will be building a simple
animated character.

At this point, you should have a white window with a resolution of 1920 by 1080 pixels.

Before we continue, we first need to understand the rubato heirarchy (we'll explain it first, then walk you
through it). rubato has 3 levels of structure, in order: Scenes, Game Objects, and Components.

:func:`Scenes <rubato.structure.scene.Scene>` hold a set of Game Objects. It also manages a :func:`Camera <rubato.utils.rendering.camera.Camera>`.
Scenes are used to separate different sections of a game. For example, you could have each game
level in a different scene. To move between levels, you would simply switch scenes.

:func:`Game Objects <rubato.structure.gameobject.game_object.GameObject>` are the main objects in a game.
They have a position and z-index, and represent a "thing", such as a player, an enemy, or a platform. Their behavior is almost entirely
determined by the Components that are assigned to them.

:func:`Components <rubato.structure.gameobject.component.Component>` are lightweight "modules" that add to the behavior of a Game Object.
For example, an :func:`Image <rubato.structure.gameobject.sprites.raster.Image>` component draws an image from your
filesystem at the Game Object's position. A :func:`RigidBody <rubato.structure.gameobject.physics.rigidbody.RigidBody>` component registers the Game Object
into the built-in physics engine. A :func:`Hitbox <rubato.structure.gameobject.physics.hitbox.Hitbox>` component gives
a Game Object shape and enables collision.

If this explanation was confusing, hopefully it'll make more sense seeing the system in action.
We'll start by making a scene:

.. literalinclude:: step2_main.py
    :caption: main.py
    :lines: 3-9,12,16-18
    :emphasize-lines: 8
    :lineno-start: 3


Here we introduce the :func:`Color <rubato.utils.color.Color>` class. Colors
are stored in RGBA format but can be loaded from HSV and HEX. The class comes
preloaded with pastel-inspired :func:`default colors <rubato.utils.color.Color.random>` as
well as several methods to mix and manipulate them. In the code above, we use :func:`lighter() <rubato.utils.color.Color.lighter>`
to lighten the shade a little.

Note that we did not have to actually add our scene to the game after creating it.
That's because it happens automatically every time a scene is initialized!

Next, we need to create a player and add it to the scene. Create a new file next to :code:`main.py` called :code:`shared.py`
and add the following code:

.. literalinclude:: step2_shared.py
    :caption: shared.py
    :lines: 1-7
    :linenos:


Here we're introducing a new class: :func:`rb.Vector <rubato.utils.computation.vector.Vector>`.

A rubato :func:`Vector <rubato.utils.computation.vector.Vector>` is an object that contains two numbers, x and y.
A Vector can represent a point, dimensions, a mathematical vector, or anything else that has x and y
parameters. The :func:`Vector <rubato.utils.computation.vector.Vector>` class comes loaded with
many useful transformation functions and lets you utilize intuitive operators like :code:`+` as shown above to do quick vector math.

.. note::
    rubato uses the cartesian coordinate system, where the origin is in the center of the screen and positive y is up.

:func:`rb.Display.center_left <rubato.utils.hardware.display.Display.center_left>` is just the Vector position for the center of the
left side of the screen (i.e. y = 0, x = -screen resolution / 2).

Now in the main file we need to import :code:`shared.py` and add it to the scene (above the call to begin()):

.. note::

    You need to import the shared file **after** having called the rubato init method, so that you can use rubato functions in shared.

.. literalinclude:: step2_main.py
    :caption: main.py
    :lines: 10-15
    :lineno-start: 10
    :emphasize-lines: 1,5,6


If we ran this now, we won't see our player. That's because Game Objects don't draw anything by themselves.
Let's change that by adding a simple Animation to the player.

You will see a few image files inside the ``files/dino`` directory. Each of these image
files is a spritesheet for a single animation. Instead of loading each frame and image ourselves, we can use
:func:`rb.Spritesheet.from_folder() <rubato.structure.gameobject.sprites.spritesheet.Spritesheet.from_folder>` to load them
all at once. This function takes the path to a folder and returns an
:func:`Animation <rubato.structure.gameobject.sprites.animation.Animation>` component that can then be added to a GameObject.

Our spritesheets have a couple of frames. Each frame is 24 pixels by 24 pixels. Be sure to specify the sprite size
when you load them. This will let rubato correctly subdivide the spritesheet into frames.

Animations are made up of different states which we'll be able to switch between. When loading from a folder, the
state names are the names of the files. Some states we have in our example are idle, jump, crouch, and run.

We also should specify the default state. This is the state that the animation will start at and the one that it will
return to when other states finish. In our case, this will be the idle state.

.. literalinclude:: step2_shared.py
    :caption: shared.py
    :lines: 3-
    :lineno-start: 3
    :emphasize-lines: 7-

Now you should have a cute dinosaur bobbing up and down on the left side of the screen:

.. image:: /_static/tutorials_static/platformer/step2/1.png
    :width: 75%
    :align: center

Adorable :)

Here is what you should have so far if you've been following along (cleaned up a bit):

.. literalinclude:: step2_main.py
    :caption: main.py
    :linenos:
    :emphasize-lines: 3, 12-15

.. literalinclude:: step2_shared.py
    :caption: shared.py
    :linenos:
    :emphasize-lines: 1-
