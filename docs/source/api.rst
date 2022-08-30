######################
Full API Documentation
######################
This page describes all user-accessible API components to the rubato project.

.. toctree::
    :hidden:

    events
    key-names

.. autofunction:: rubato.init

.. autofunction:: rubato.begin

.. _game_class:

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


.. _scene:

Scene
=====
.. automodule:: rubato.struct.scene

.. _camera:

Camera
------
.. automodule:: rubato.utils.camera


.. _group:

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

.. _gameobj:

Game Object
============
.. automodule:: rubato.struct.gameobject.game_object

.. _components:

Components
==========
The default Component class.

.. automodule:: rubato.struct.gameobject.component

.. _raster:

Raster
---------
.. automodule:: rubato.struct.gameobject.sprites.raster.Raster


.. _image:

Image
---------
.. automodule:: rubato.struct.gameobject.sprites.raster.Image

.. _text:

Text
---------
.. automodule:: rubato.struct.gameobject.ui.text

.. _button:

Button
---------
.. automodule:: rubato.struct.gameobject.ui.button

.. _slider_:

Slider
---------
.. automodule:: rubato.struct.gameobject.ui.slider

.. _animation:

Animation
---------
.. automodule:: rubato.struct.gameobject.sprites.animation

.. _spritesheet:

Spritesheet
___________
.. automodule:: rubato.struct.gameobject.sprites.spritesheet

.. _particlesystem:

Particle Sytem
--------------
.. automodule:: rubato.struct.gameobject.particles.system

.. _particle:

Particle
________
.. automodule:: rubato.struct.gameobject.particles.particle

.. _hitbox:

Hitbox
-------
Various hitbox components that enable collisions

.. autoclass:: rubato.struct.gameobject.physics.hitbox.Hitbox

.. _rect:

Rectangle
__________
.. autoclass:: rubato.struct.gameobject.physics.hitbox.Rectangle

.. _poly:

Polygon
__________
.. autoclass:: rubato.struct.gameobject.physics.hitbox.Polygon

.. _circle:

Circle
__________
.. autoclass:: rubato.struct.gameobject.physics.hitbox.Circle

.. _rigidbody:

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

.. _engine:

Engine
=======
.. autoclass:: rubato.struct.gameobject.physics.engine.Engine

.. _manifold:

Manifold
==========
.. autoclass:: rubato.struct.gameobject.physics.engine.Manifold

********************
Hardware Interaction
********************

All of these static classes let you interact with the hardware. Either by checking for user input, drawing to the screen
or playing a sound.

.. _display:

Display
=======
.. automodule:: rubato.utils.display

.. _input:

Input
=====
.. automodule:: rubato.utils.rb_input

.. _sound:

Sound
=====
.. automodule:: rubato.utils.sound

*********
Utilities
*********
These classes are utility classes that are used to make certain tasks easier.

.. _surface:

Surface
=======
.. automodule:: rubato.struct.surface

.. _draw:

Draw
====
.. automodule:: rubato.utils.draw

.. _vector:

Vector
======
.. automodule:: rubato.utils.vector

.. _math:

Math
====
.. automodule:: rubato.utils.rb_math

.. _noise:

Noise
------
A utility for generating simple smooth noise in your projects.

.. autoclass:: rubato.utils.noise.Noise


.. _time:

Time
====
.. automodule:: rubato.utils.rb_time

.. _color:

Color
=====

.. automodule:: rubato.utils.color
    :undoc-members:

.. _colordef:

Default Colors
--------------
.. literalinclude:: ../../rubato/utils/color.py
    :language: python
    :start-after: [colordef]
    :end-before: [/colordef]
    :dedent:

.. _grayscaledef:

Default Grayscale Colors
------------------------
.. literalinclude:: ../../rubato/utils/color.py
    :language: python
    :start-after: [grayscaledef]
    :end-before: [/grayscaledef]
    :dedent:

.. _debug:

Debug
=====

.. automodule:: rubato.utils.debug
    :undoc-members:

.. _debugdef:

.. _font:

Font
====
.. automodule:: rubato.utils.font
    :undoc-members:

.. _radio:

Radio
=====
.. automodule:: rubato.utils.radio

.. _errors:

Errors
======
.. automodule:: rubato.utils.error

*************
Miscellaneous
*************
.. automodule:: rubato.misc
