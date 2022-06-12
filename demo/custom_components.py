"""
Custom Component demo.
"""  # pylint: disable=all
import rubato as rb
from rubato import Vector

size = Vector(400, 300)
rb.init(res=size, window_size=size * 2)

main_scene = rb.Scene()

player = rb.GameObject("red dot", rb.Display.center)


class Player(rb.Component):
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
        Run the first time it updates.
        """
        self.circle = self.gameobj.get(rb.Circle)
        self.circle.color = self.color
        self.name = "bob"

    def update(self):
        """
        You can create an update that will be called once per frame
        """
        if rb.Input.mouse_pressed():
            self.circle.color = rb.Color.random()
            self.gameobj.pos = rb.Input.get_mouse_pos()

    def draw(self, camera):
        """
        You can create a draw function that will be called once per frame. You will most likely not use the camera.
        """
        rb.Debug.circle(Vector(10, 10), 10, self.color)
        rb.Debug.circle(Vector(50, 10), 10, self.color)
        rb.Debug.line(Vector(10, 40), Vector(50, 40), self.color)


player_data = Player(rb.Color.red)
player.add(player_data).add(rb.Circle(radius=10))

main_scene.add(player)
rb.begin()
