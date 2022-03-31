###########################
Scenes and Their Management
###########################

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

