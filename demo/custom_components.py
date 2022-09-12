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

        self.hitbox: rb.Hitbox = rb.Circle(radius=20, color=rb.Color.red)

        self.text: rb.Text = rb.Text(" ", font=rb.Font(color=rb.Color.blue, size=20), anchor=rb.Vector(1,1))

    def setup(self):
        """
        Here you have access to the GameObject of the component and is where you should set any variables that depend
        on the GameObject.
        Automatically run once before the first update call.
        """
        self.gameobj.add(self.hitbox)
        self.text.text = self.gameobj.name
        self.gameobj.add(self.text)

    def update(self):
        """
        Called once per frame. Before the draw function.
        """
        if rb.Input.mouse_pressed():
            self.hitbox.color = rb.Color.random()
            self.gameobj.pos = rb.world_mouse()
        if rb.Input.key_pressed("shift"):
            self.text.hidden = False
        else:
            # self.text.hidden = True
            pass

    def speak(self):
        """
        A custom function that can add even move behavior to your component.
        """
        print(f"Hello! My name is {self.name}.")


player = rb.GameObject(name="Player", pos=rb.Display.center)
player.add(PlayerController("Bob"))
player.add(rb.Circle(radius=3, color=rb.Color.green, z_index=3))


main_scene.add(player)
rb.begin()
