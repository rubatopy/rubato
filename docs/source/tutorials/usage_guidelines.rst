#################################
Best Practices / Usage Guidelines
#################################

Although rubato is built to be highly dynamic in its use, certain practices are more effective than others.
On this page you can find generic design guidelines and examples for building certain features with rubato.

The rubato structure is purposefully similar to Unity. In general:
 * Sections of a game are split into Scenes.
 * Each Scene is comprised of Group(s) of Game Objects.
 * Game Objects' behavior should be defined solely by the Components they house.

About components:
 * Although they can, it isn't good design to have Components create new Components
   and add them to the parent GameObject. Component behavior should be transparent:
   each added Component should result in exactly one Component being added to the GameObject.
 * Components should not remove other Components from the GameObject.

The way you can have components talk to each other is by:
 * Using the :func:`get() <rubato.structure.gameobject.game_object.GameObject.get>` and :func:`get_all() <rubato.structure.gameobject.game_object.GameObject.get_all>` GameObject methods.
 * Storing a reference to the component directly.

As a consequence of these guidelines, the design pattern for creating GameObjects in rubato is best handled
by factory / generator methods that create gameobjects and configure them with components as necessary.
We'll explain that in depth now.

*************************************
How to generate multiple Game Objects
*************************************

Many games require creating entities repetitively, such as enemies or coins.
In rubato you can use a factory function to do this.
The method will create a GameObject and then configure it with the necessary components,
returning it afterwards so it can be added to the desired scene.
Here's an example:

.. code-block:: python

    enemy_list = []
    def generate_enemy(x, y):
        enemy = GameObject(pos=(x, y))
        # add some custom EnemyBehavior component we've defined
        enemy.add_component(EnemyBehaviour())
        return enemy

    for i in range(10):
        enemy_list.append(generate_enemy(i*30, 0))

    # you could also invoke generate_enemy at any later point in time, such as when the player reaches the boss room


For an in depth generator example see the generator `demo <https://github.com/rubatopy/rubato/tree/main/demo/rubato_usage/generators.py>`__.
