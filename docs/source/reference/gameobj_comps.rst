Game Object and Components
==========================

:func:`Game Objects <rubato.classes.game_object.GameObject>` are the main item in a game. They hold Components, have a position, and
have a z-index. By themselves, they have very little functionality.

:func:`Components <rubato.classes.component.Component>` are how Game Objects get their functionality. Each component adds or
changes something about the Game Object. For example, an Image component draws an image from your filesystem to the game at the
Game Object's position.

.. _gameobj:

Game Object
-----------
The default Game Object class.

.. autoclass:: rubato.classes.game_object.GameObject
    :members:

.. _components:

Components
----------
The default Component class.

.. automodule:: rubato.classes.component
    :members:

.. _image:

Image
_________
.. automodule:: rubato.classes.components.image
    :members:

.. _animation:

Animation
_________
.. automodule:: rubato.classes.components.animation
    :members:

.. _rectangle:

Hitbox
_________
.. automodule:: rubato.classes.components.hitbox
    :members:

.. _rigidbody:

RigidBody
_________
.. automodule:: rubato.classes.components.rigidbody
    :members:
