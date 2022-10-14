######################
Full API Documentation
######################
This page describes all user-accessible API components to the rubato project.

.. toctree::
    :hidden:

    key-names

.. autofunction:: rubato.init

.. autofunction:: rubato.begin

****
Game
****
.. automodule:: rubato.game

***************************
Scenes and Their Management
***************************

:func:`Scenes <rubato.struct.scene.Scene>` holds two Groups. It also manages a
:func:`Camera <rubato.utils.camera.Camera>`. Scenes are used to compartmentalize code. For example,
you could have each level of your game on a different scene. Then to switch levels you would switch scenes.

:func:`Groups <rubato.struct.group.Group>` hold a collection of Game Objects and/or other Groups. Their main purpose is to
further compartmentalize items. For example, items in 2 different groups won't collide with each other. In this tutorial,
we won't be using Groups as we don't need this functionality here.

Scene
=====
.. automodule:: rubato.struct.scene

Camera
------
.. automodule:: rubato.utils.camera

Group
=====
.. automodule:: rubato.struct.group

**************************
Game Object and Components
**************************

:func:`Game Objects <rubato.struct.gameobject.game_object.GameObject>` are the main item in a game. They hold Components, have a position, and
have a z-index. By themselves, they have very little functionality.

:func:`Components <rubato.struct.gameobject.component.Component>` are how Game Objects get their functionality. Each component adds or
changes something about the Game Object. For example, an Image component draws an image from your filesystem to the game at the
Game Object's position.

Game Object
============
.. automodule:: rubato.struct.gameobject.game_object

Components
==========
The default Component class.

.. automodule:: rubato.struct.gameobject.component

Raster
---------
.. autoclass:: rubato.struct.gameobject.sprites.raster.Raster

Image
---------
.. autoclass:: rubato.struct.gameobject.sprites.raster.Image

Text
---------
.. automodule:: rubato.struct.gameobject.ui.text

Button
---------
.. automodule:: rubato.struct.gameobject.ui.button

Slider
---------
.. automodule:: rubato.struct.gameobject.ui.slider

Animation
---------
.. automodule:: rubato.struct.gameobject.sprites.animation

Spritesheet
___________
.. automodule:: rubato.struct.gameobject.sprites.spritesheet

Particle Sytem
--------------
.. automodule:: rubato.struct.gameobject.particles.system

Particle
________
.. automodule:: rubato.struct.gameobject.particles.particle

Hitbox
-------
Various hitbox components that enable collisions

.. autoclass:: rubato.struct.gameobject.physics.hitbox.Hitbox

Rectangle
__________
.. autoclass:: rubato.struct.gameobject.physics.hitbox.Rectangle

Polygon
__________
.. autoclass:: rubato.struct.gameobject.physics.hitbox.Polygon

Circle
__________
.. autoclass:: rubato.struct.gameobject.physics.hitbox.Circle

RigidBody
---------
.. automodule:: rubato.struct.gameobject.physics.rigidbody

*******
Physics
*******

The Engine and Manifold classes comprise rubato's collision engine. Collision and overlap tests inside groups are
automatically handled by rubato, so these classes are here mainly for reference.

In general, it is recommended that you define callback functions for Hitbox objects instead of calling Engine
functions yourself.

Engine
=======
.. autoclass:: rubato.struct.gameobject.physics.engine.Engine

Manifold
==========
.. autoclass:: rubato.struct.gameobject.physics.engine.Manifold

********************
Hardware Interaction
********************

All of these static classes let you interact with the hardware. Either by checking for user input, drawing to the screen
or playing a sound.

Display
=======
.. automodule:: rubato.utils.display

Input
=====
.. automodule:: rubato.utils.rb_input

Sound
=====
.. automodule:: rubato.utils.sound

*********
Utilities
*********
These classes are utility classes that are used to make certain tasks easier.

Surface
=======
.. automodule:: rubato.utils.surface

Draw
====
.. automodule:: rubato.utils.draw

Vector
======
.. automodule:: rubato.utils.vector

Math
====
.. automodule:: rubato.utils.rb_math

Noise
------
A utility for generating simple smooth noise in your projects.

.. autoclass:: rubato.utils.noise.Noise

Time
====
.. automodule:: rubato.utils.rb_time

Color
=====
.. automodule:: rubato.utils.color
    :undoc-members:

Default Colors
--------------
.. literalinclude:: ../../rubato/utils/color.py
    :language: python
    :start-after: [colordef]
    :end-before: [/colordef]
    :dedent:

Default Grayscale Colors
------------------------
.. literalinclude:: ../../rubato/utils/color.py
    :language: python
    :start-after: [grayscaledef]
    :end-before: [/grayscaledef]
    :dedent:

Debug
=====
.. automodule:: rubato.utils.debug
    :undoc-members:

Font
====
.. automodule:: rubato.utils.font
    :undoc-members:

Radio
=====
.. automodule:: rubato.utils.radio

Events
------
.. automodule:: rubato.utils.events

Errors
======
.. automodule:: rubato.utils.error

*************
Miscellaneous
*************
.. automodule:: rubato.misc
