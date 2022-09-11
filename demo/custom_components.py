"""
Custom Component demo.
"""
import rubato as rb
from rubato import Vector

size = Vector(600, 400)
rb.init(res=size, window_size=size)

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
        self.offset = rb.Vector(0, 20)

        # Initialize any attributes that you want to use in your component.
        self.health = 100
        self.speed = 10

        self.hitbox: rb.Hitbox  # we are going to get this later

    def setup(self):
        self.hitbox = self.gameobj.get(rb.Hitbox)

    def update(self):
        """
        Called once per frame. Before the draw function.
        """
        if rb.Input.mouse_pressed():
            self.hitbox.color = rb.Color.random()
            self.gameobj.pos = rb.world_mouse()

    def speak(self):
        """
        A custom function that can add even move behavior to your component.
        """
        print(f"Hello! My name is {self.name}.")


player = rb.GameObject(name="Player", pos=rb.Display.center)
player.add(rb.Circle(radius=20, color=rb.Color.red))
player.add(PlayerController("Bob"))

poly = rb.Polygon(rb.Vector.poly(5, 50), color=rb.Color.green)
main_scene.add(rb.wrap(poly, pos=rb.Display.center + rb.Vector(-30), rotation=30))


def update():
    poly.color = rb.Color.red if poly.contains_pt(rb.world_mouse()) else rb.Color.green


rb.Game.update = update

main_scene.add(player)
rb.begin()
