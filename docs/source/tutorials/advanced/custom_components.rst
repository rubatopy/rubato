#################
Custom Components
#################

In this tutorial, we will be going over how to create a custom component. We are assuming that you have already completed
the getting started and have an understanding of how to use the built-in components.

Simply put, custom components are a very powerful way of adding a behavior to your GameObjects. Your custom components are
used just like any other component. Below is an example of a custom component PlayerController being added to a GameObject.

.. code-block:: python

    player = rb.GameObject(name="Bob", pos=rb.Display.center)
    player.add(PlayerController())

Below is what this PlayerController component might look like.

.. code-block:: python

    class PlayerController(rb.Component):
        """A custom component that adds player behavior to a GameObject."""

        def __init__(self):
            """
            Here you set up all the variables of the component.
            """
            super().__init__()  # you must call super().__init__()

            # Change any attributes inherited from Component.
            self.singular = True
            self.offset = rb.Vector(0, 20)

            # Initialize any attributes that you want to use in your component.
            self.health = 100
            self.speed = 10

            # The hitbox (circle) that is drawn to the screen
            self.hitbox: rb.Hitbox = rb.Circle(radius=20, color=rb.Color.red)

            # The text that is drawn to the screen, will use the game object's name in setup.
            self.nametag: rb.Text = rb.Text(" ", font=rb.Font(color=rb.Color.blue, size=20))
            self.nametag.offset = rb.Vector(0, -self.hitbox.radius - self.nametag.font_size / 2)

        def setup(self):
            """
            Here you have access to the GameObject of the component and is where you should set any variables that depend
            on the GameObject.
            Automatically run once before the first update call.
            """
            # once we have access to the game object, we can set the text to the game object's name.
            self.nametag.text = self.gameobj.name

            # here we need to add all of our components to the game object
            self.gameobj.add(self.hitbox)
            self.gameobj.add(self.nametag)

            # subscribe to the mouse down event
            rb.Radio.listen(rb.Events.MOUSEDOWN, self.on_mouse_press)

        def on_mouse_press(self):
            self.hitbox.color = rb.Color.random()
            self.gameobj.pos = rb.world_mouse()

        def update(self):
            """
            Called once per frame. Before the draw function.
            """
            if rb.Input.key_pressed("shift"):
                self.nametag.hidden = False
            else:
                self.nametag.hidden = True

        def speak(self):
            """
            A custom function that can add even move behavior to your component.
            """
            print(f"Hello! My name is {self.gameobj.name}.")

Next we will break down each section of the PlayerController component.

.. code-block:: python

    class PlayerController(rb.Component):

Custom components are created by inheriting from the Component class.

|

.. code-block:: python

    def __init__(self):
        """
        Here you set up all the variables of the component.
        """
        super().__init__()  # you must call super().__init__()

        # Change any attributes inherited from Component.
        self.singular = True
        self.offset = rb.Vector(0, 20)

        # Initialize any attributes that you want to use in your component.
        self.health = 100
        self.speed = 10

        # The hitbox (circle) that is drawn to the screen
        self.hitbox: rb.Hitbox = rb.Circle(radius=20, color=rb.Color.red)

        # The text that is drawn to the screen, will use the game object's name in setup.
        self.nametag: rb.Text = rb.Text(" ", font=rb.Font(color=rb.Color.blue, size=20))
        self.nametag.offset = rb.Vector(0, -self.hitbox.radius - self.nametag.font_size / 2)

In the initalizer for your component, you must first call the ``super().__init__()`` function. This will setup the structure
for the component and allow it to work with the rest of the rubato. This also give you access to the attributes in Components
such as offset. The ``__init__()`` function is where you should set up all the attributes you need for your component. Keep in mind
however, that at this point the ``gameobj`` attribute is not yet set. In our example, we initialize a hitbox attribute to None and we
will get it from the GameObject later.

|

.. code-block:: python

    def setup(self):
        """
        Here you have access to the GameObject of the component and is where you should set any variables that depend
        on the GameObject.
        Automatically run once before the first update call.
        """
        # once we have access to the game object, we can set the text to the game object's name.
        self.nametag.text = self.gameobj.name

        # here we need to add all of our components to the game object
        self.gameobj.add(self.hitbox)
        self.gameobj.add(self.nametag)

        # subscribe to the mouse down event
        rb.Radio.listen(rb.Events.MOUSEDOWN, self.on_mouse_press)

The setup function is the first time you get access to the GameObject of the component. This is where you should set any
attributes that require knowledge of the GameObject. In our example, we set our name tags text. As well as adding our
components to the game object.

|

.. code-block:: python

    def update(self):
        """
        Called once per frame. Before the draw function.
        """
        if rb.Input.key_pressed("shift"):
            self.nametag.hidden = False
        else:
            self.nametag.hidden = True

As you should know, components have a couple functions that can be overriden:
``setup``, ``update``, ``fixed_update``, ``draw``, ``delete`` and ``clone``. In these, you have access to every attribute
you've set (including the GameObject). In our example, we are overriding the update function to change the color of the
hitbox and move the player whenever the mouse is pressed.

|

.. code-block:: python

    def speak(self):
        """
        A custom function that can add even move behavior to your component.
        """
        print(f"Hello! My name is {self.gameobj.name}.")

The last thing to know about custom components is that you can define any functions you want. In our example, we are defining
a speak function that prints a message to the console. This speak function can be called from inside the component, but it
can also be called anywhere else in the engine. This is a great way to add behavior to your component.

|
|

In this tutorial, we went over the creation process of custom components and explained how to use them.

The source code for an example is available
`here <https://github.com/rubatopy/rubato/tree/main/demo/custom_components.py>`__.
