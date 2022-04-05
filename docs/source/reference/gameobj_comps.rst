##########################
Game Object and Components
##########################

:func:`Game Objects <rubato.classes.game_object.GameObject>` are the main item in a game. They hold Components, have a position, and
have a z-index. By themselves, they have very little functionality.

:func:`Components <rubato.classes.component.Component>` are how Game Objects get their functionality. Each component adds or
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
