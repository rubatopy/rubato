"""
Custom Component demo.
"""  # pylint: disable=all
import rubato as rb

rb.init()

main_scene = rb.Scene()

player = rb.GameObject("red dot", rb.Display.center)


class Player(rb.Component):
    def __init__(self, color):
        """
        Here you set up all the variables of the component.
        """
        super().__init__()
        self.color = color

        # setting all your attributes to None is not required, but does make the code explicit.
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
        if rb.Input.mouse_is_pressed()[0]:
            self.circle.color = rb.Color.random()
            self.gameobj.pos = rb.Input.get_mouse_pos()


player_data = Player(rb.Color.red)
player.add(player_data).add(rb.Circle(radius=10))

main_scene.add(player)
rb.begin()
