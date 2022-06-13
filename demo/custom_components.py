"""
Custom Component demo.
"""
import rubato as rb
from rubato import Vector

size = Vector(400, 300)
rb.init(res=size, window_size=size * 2)

main_scene = rb.Scene()

player = rb.GameObject("red dot", rb.Display.center)


class Player(rb.Component):
    """Custom Player Component"""
    def __init__(self, color):
        """
        Here you set up all the variables of the component.
        """
        # you must call super().__init__()
        super().__init__()

        # assign args to attributes
        self.color = color

        # setting all your attributes to None is not required, but does make the code explicit. Goes in setup.
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


player_data = Player(rb.Color.red)
player.add(player_data).add(rb.Circle(radius=10))

main_scene.add(player)
rb.begin()
