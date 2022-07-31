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
    :members:

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
    :members:

.. _camera:

Camera
------
.. automodule:: rubato.utils.camera
    :members:


.. _group:

Group
=====
.. automodule:: rubato.struct.group
    :members:

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
    :members:

.. _components:

Components
==========
The default Component class.

.. automodule:: rubato.struct.gameobject.component
    :members:

.. _image:

Image
---------
.. automodule:: rubato.struct.gameobject.sprites.image
    :members:

.. _raster:

Raster
---------
.. automodule:: rubato.struct.gameobject.raster
    :members:

.. _text:

Text
---------
.. automodule:: rubato.struct.gameobject.ui.text
    :members:

.. _button:

Button
---------
.. automodule:: rubato.struct.gameobject.ui.button
    :members:

.. _slider_:

Slider
---------
.. automodule:: rubato.struct.gameobject.ui.slider
    :members:

.. _animation:

Animation
---------
.. automodule:: rubato.struct.gameobject.sprites.animation
    :members:

.. _spritesheet:

Spritesheet
___________
.. automodule:: rubato.struct.gameobject.sprites.spritesheet
    :members:


.. _hitbox:

Hitbox
-------
.. automodule:: rubato.struct.gameobject.physics.hitbox
    :members: Hitbox

.. _rect:

Rectangle
__________
.. autoclass:: rubato.struct.gameobject.physics.hitbox.Rectangle
    :members:

.. _poly:

Polygon
__________
.. autoclass:: rubato.struct.gameobject.physics.hitbox.Polygon
    :members:

.. _circle:

Circle
__________
.. autoclass:: rubato.struct.gameobject.physics.hitbox.Circle
    :members:

.. _rigidbody:

RigidBody
---------
.. automodule:: rubato.struct.gameobject.physics.rigidbody
    :members:

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
    :members:

.. _manifold:

Manifold
==========
.. autoclass:: rubato.struct.gameobject.physics.engine.Manifold
    :members:

********************
Hardware Interaction
********************

All of these static classes let you interact with the hardware. Either by checking for user input, drawing to the screen
or playing a sound.

.. _display:

Display
=======
.. automodule:: rubato.utils.display
    :members:

.. _input:

Input
=====
.. automodule:: rubato.utils.rb_input
    :members:

.. _sound:

Sound
=====
.. automodule:: rubato.utils.sound
    :members:

*********
Utilities
*********
These classes are utility classes that are used to make certain tasks easier.

.. _sprite:

Sprite
======
.. automodule:: rubato.struct.sprite
    :members:

.. _draw:

Draw
====
.. automodule:: rubato.utils.draw
    :members:

.. _vector:

Vector
======
.. automodule:: rubato.utils.vector
    :members:

.. _math:

Math
====
.. automodule:: rubato.utils.rb_math
    :members:

.. _noise:

Noise
------
.. automodule:: rubato.utils.noise
    :members: Noise


.. _time:

Time
====
.. automodule:: rubato.utils.rb_time
    :members:

.. _color:

Color
=====

.. automodule:: rubato.utils.color
    :members:
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
    :members:
    :undoc-members:

.. _debugdef:

.. _font:

Font
====
.. automodule:: rubato.utils.font
    :members:
    :undoc-members:

.. _radio:

Radio
=====
.. automodule:: rubato.utils.radio
    :members:

.. _errors:

Errors
======
.. automodule:: rubato.utils.error
    :members:

*************
Miscellaneous
*************
.. automodule:: rubato.misc
    :members:
