#################
Custom Components
#################

Assumes you finished getting started.

This is the supported way to create a custom component.

A custom component could be a behaviour that is added to a game object.

Here we defined the PlayerBehaviour class, a custom component, that would control the GameObject it is added to.

.. code-block:: python

    player = GameObject("Player")
    player.add_component(PlayerBehaviour())

Below we show the structure of a generic custom component.

.. code-block:: python

    class CustomComp(rb.Component):
    """Custom Component"""
    def __init__(self, color):
        """
        Here you set up all the variables of the component.
        """
        # you must call super().__init__()
        super().__init__()

        # assign args to attributes
        self.color = color

        # setting all your attributes to None is not required, but does make the code explicit.
        # Actual setting goes in setup.
        self.circle = None
        self.name = None

    def setup(self):
        """
        Here you have access to the GameObject of the component.
        Run before the first update.
        """
        self.circle = self.gameobj.get(rb.Circle)
        self.circle.color = self.color
        self.name = "bob"

    def update(self):
        """
        Called once per frame. Before the draw function.
        """
        if rb.Input.mouse_pressed():
            self.circle.color = rb.Color.random()
            self.gameobj.pos = rb.Input.get_mouse_pos()

    def draw(self, camera):
        """
        Called once per frame. You will most likely not use the camera.
        """
        rb.Debug.circle(Vector(10, 10), 10, self.color)
        rb.Debug.circle(Vector(50, 10), 10, self.color)
        rb.Debug.line(Vector(10, 40), Vector(50, 40), self.color)


We will zoom on each section of the code.
You must define the __init__ method, which must call the super().__init__() method. You can also take in parameters.
Note: There is no access to the GameObject in the __init__ method.

.. code-block:: python

    def __init__(self, color):
        """
        Here you set up all the variables of the component.
        """
        # you must call super().__init__()
        super().__init__()

        # assign args to attributes
        self.color = color

        # setting all your attributes to None is not required, but does make the code explicit.
        # Actual setting goes in setup.
        self.circle = None
        self.name = None

Next is the setup method. This is called before the first update, and is where you can set up all your variables,
while accessing the GameObject.

.. code-block:: python

    def setup(self):
        """
        Here you have access to the GameObject of the component.
        Run before the first update.
        """
        self.circle = self.gameobj.get(rb.Circle)
        self.circle.color = self.color
        self.name = "bob"

Finally there are the update and draw methods. Called in that order each frame. In our custom component, we
are using the draw method to draw a players face, and not doing anything meaningful.

.. code-block:: python

    def update(self):
        """
        Called once per frame. Before the draw function.
        """
        if rb.Input.mouse_pressed():
            self.circle.color = rb.Color.random()
            self.gameobj.pos = rb.Input.get_mouse_pos()

    def draw(self, camera):
        """
        Called once per frame. You will most likely not use the camera.
        """
        rb.Draw.circle(Vector(10, 10), 10, self.color)  # Drawing player face
        rb.Draw.circle(Vector(50, 10), 10, self.color)
        rb.Draw.line(Vector(10, 40), Vector(50, 40), self.color)



The source code for an example is available
`here <https://github.com/rubatopy/rubato/tree/main/demo/custom_components.py>`__.
