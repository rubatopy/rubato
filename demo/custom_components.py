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

        # The hitbox (circle) that is drawn to the screen
        self.hitbox: rb.Hitbox = rb.Circle(radius=20, color=rb.Color.red)

        # The text that is drawn to the screen, will use the game object's name in setup.
        self.text: rb.Text = rb.Text(" ", font=rb.Font(color=rb.Color.blue, size=20))
        self.text.offset = rb.Vector(0, -self.hitbox.radius - self.text.font_size / 2)

    def setup(self):
        """
        Here you have access to the GameObject of the component and is where you should set any variables that depend
        on the GameObject.
        Automatically run once before the first update call.
        """
        # once we have access to the game object, we can set the text to the game object's name.
        self.text.text = self.gameobj.name

        # here we need to add all of our components to the game object
        self.gameobj.add(self.hitbox)
        self.gameobj.add(self.text)

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
            self.text.hidden = False
        else:
            self.text.hidden = True

    def speak(self):
        """
        A custom function that can add even move behavior to your component.
        """
        print(f"Hello! My name is {self.name}.")


player = rb.GameObject(name="Player", pos=rb.Display.center)
player.add(PlayerController("Bob"))



main_scene.add(player, rb.wrap(rb.Text("psst... press shift.", anchor=(1,1))))
rb.begin()
