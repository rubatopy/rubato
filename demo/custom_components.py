"""
Custom Component demo.
"""
import rubato as rb
from rubato import Vector

size = Vector(300, 200)
rb.init(res=size, size=size * 2)

main_scene = rb.Scene()


class PlayerController(rb.Component):
    """A custom component that adds player behavior to a GameObject."""

    def __init__(self, name):
        """
            Here you set up all the variables of the component.
            """
        super().__init__()  # you must call super().__init__()

        # Assign arguments to attributes
        self.name = name

        # Change any attributes inherited from Component.
        self.singular = True
        self.offset = rb.Vector(0, 10)

        # Initialize any attributes that you want to use in your component.
        self.health = 100
        self.speed = 10
        self.hitbox = None  # We are going to get this later.

    def setup(self):
        """
        Here you have access to the GameObject of the component and is where you should set any variables that depend
        on the GameObject.
        Automatically run once before the first update call.
        """
        self.hitbox = self.gameobj.get(rb.Hitbox)

    def update(self):
        """
        Called once per frame. Before the draw function.
        """
        if rb.Input.mouse_pressed():
            self.hitbox.color = rb.Color.random()
            self.gameobj.pos = rb.Input.get_mouse_pos()

    def speak(self):
        """
        A custom function that can add even move behavior to your component.
        """
        print(f"Hello! My name is {self.name}.")


player = rb.GameObject(name="Player", pos=rb.Display.center)
player.add(rb.Circle(radius=10, color=rb.Color.red))
player.add(PlayerController("Bob"))

main_scene.add(player)
rb.begin()
