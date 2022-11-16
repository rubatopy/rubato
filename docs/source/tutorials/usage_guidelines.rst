##########################
Usage Guidelines
##########################

Rubato was designed for a very specific flow, we recommend you follow it to get the most out of this library.

.. important::

    It is expected you know how to use rubato, hopefully through the tutorial platformer.

    And how to make a custom component found :doc:`here <advanced/custom_components>`.


In rubato the workflow is as follows:
To make a game you need a scene.
Each Scene is comprised of Game Objects.
And to give these Game Objects functionality you need Components.

About components:
 * They should never add another component to the game object.
 * They should never remove another component from the game object.
 * The only thing that components do is add new behavior to the game object.

The way you can have components talk to each other is by:
 * Using the ``get_component`` / ``get_components`` methods.
 * By passing in a reference to the component.
 * Use generators when making the GO anyways. (preferred)

How to generate specific Game Objects:
**********************

In games you will often want to spawn in a bunch of enemies. In java one might make a list of
enemies and then loop through it to spawn them.
In rubato you can use a `generator` function to do this.
This function would work much like the init function of said enemies. But it would return a
game object with a component adding enemy behaviour instead.


.. code-block:: python

    enemy_list = []
    def generate_enemy(x, y):
        enemy = GameObject()
        enemy.add_component(EnemyBehaviour())
        # all of enemies behaviour is defined in the EnemyBehaviour class
        enemy.pos = rb.Vector(x, y)
        return enemy

    def init(self):
        for i in range(10):
            enemy_list.append(generate_enemy(i*30, 0))


For an in depth generator example see the generator `tutorial <https://github.com/rubatopy/rubato/tree/main/demo/custom_components.py>`__.
