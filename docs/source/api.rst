######################
Full API Documentation
######################
Rubato is a modern 2D game engine for python. Accurate fixed-step physics simulations, robust scene and game object management, event listener system and more all come prepackaged.

Fundamentally, Rubato is built developer-focused. From intricate rigidbody simulations to 2D games, Rubato streamlines development for beginners and the poweruser. And all that finally with some legible documentation.

.. autofunction:: rubato.init

.. autofunction:: rubato.begin

.. _game_class:

____
Game
____
.. automodule:: rubato.game
    :members:

___________________________
Scenes and Their Management
___________________________

:func:`Scenes <rubato.classes.scene.Scene>` hold a collection of Game Objects and Groups. It also manages a
:func:`Camera <rubato.classes.camera.Camera>`. Scenes are used to compartmentalize code. For example,
you could have each level of your game on a different scene. Then to switch levels you would switch scenes.
Every game has a :func:`Scene Manager <rubato.classes.scene_manager.SceneManager>` which helps you switch between scenes
easily.

:func:`Groups <rubato.classes.group.Group>` also hold a collection of Game Objects and other Groups. Their main purpose is to
further compartmentalize items. For example, items in 2 different groups won't collide with each other. In this tutorial,
we won't be using Groups as we don't need this functionality here.


.. _scenemanager:

************
SceneManager
************
.. automodule:: rubato.classes.scene_manager
    :members:


.. _scene:

*****
Scene
*****
.. automodule:: rubato.classes.scene
    :members:

.. _camera:

Camera
------
.. automodule:: rubato.classes.camera
    :members:


.. _group:

*****
Group
*****
.. automodule:: rubato.classes.group
    :members:

__________________________
Game Object and Components
__________________________

:func:`Game Objects <rubato.classes.game_object.GameObject>` are the main item in a game. They hold Components, have a position, and
have a z-index. By themselves, they have very little functionality.

:func:`Components <rubato.classes.components.component.Component>` are how Game Objects get their functionality. Each component adds or
changes something about the Game Object. For example, an Image component draws an image from your filesystem to the game at the
Game Object's position.

.. _gameobj:

***********
Game Object
***********
.. automodule:: rubato.classes.game_object
    :members:

.. _ui:

***********
UI Element
***********
.. automodule:: rubato.classes.ui
    :members:

.. _components:

**********
Components
**********
The default Component class.

.. automodule:: rubato.classes.components.component
    :members:

.. _image:

Image
=========
.. automodule:: rubato.classes.components.image
    :members:

.. _text:

Text
=========
.. automodule:: rubato.classes.components.text
    :members:

.. _animation:

Animation
=========
.. automodule:: rubato.classes.components.animation
    :members:

.. _spritesheet:

Spritesheet
-----------
.. automodule:: rubato.classes.components.spritesheet
    :members:


.. _hitbox:

Hitbox
=========
.. automodule:: rubato.classes.components.hitbox
    :members:

.. _rigidbody:

RigidBody
=========
.. automodule:: rubato.classes.components.rigidbody
    :members:

____________________
Hardware Interaction
____________________

All of these static classes let you interact with the hardware. Either by checking for user input, drawing to the screen
or playing a sound.

.. _display:

*******
Display
*******
.. automodule:: rubato.utils.display
    :members:

.. _input:

*****
Input
*****
.. automodule:: rubato.utils.input
    :members:

.. _sound:

*****
Sound
*****
.. automodule:: rubato.utils.sound
    :members:

_________
Utilities
_________
These classes are utility classes that are used to make certain tasks easier.

.. _vector:

******
Vector
******
.. automodule:: rubato.utils.vector
    :members:

.. _math:

****
Math
****
.. automodule:: rubato.utils.math
    :members:

.. _time:

****
Time
****
.. automodule:: rubato.utils.time
    :members:

.. _color:

*****
Color
*****
.. automodule:: rubato.utils.color
    :members:
    :undoc-members:

.. _font:

****
Font
****
.. automodule:: rubato.utils.font
    :members:
    :undoc-members:

.. _radio:

*****
Radio
*****
.. automodule:: rubato.utils.radio
    :members:

******
Errors
******
.. automodule:: rubato.utils.error
    :members:
