import rubato as rb
from rubato import Vector, Time, Input

rb.init(res=Vector(500, 500), window_size=Vector(900, 600))

player_img = rb.Image("art/Player1.png")


class PlayerController(rb.Component):

    def __init__(self, speed):

        super().__init__()  # you must call super().__init__()

        self.image = player_img
        self.speed = speed

    @property
    def pos(self):
        return self.gameobj.pos

    @pos.setter
    def pos(self, new):
        self.gameobj.pos = new

    def setup(self):
        """
        Here you have access to the GameObject of the component and is where you should set any variables that depend
        on the GameObject.
        Automatically run once before the first update call.
        """
        # Only here can we get the rect from our game object and assign the image
        self.rect = self.gameobj.get(rb.Rectangle)

        # resizing our image to our hitbox's size
        # self.image.resize(Vector(50, 50))
        self.gameobj.add(self.image)

    def update(self):
        """
        Called once per frame. Before the draw function.
        """
        # We moved the input into here. And changed it all to use delta_time
        if Input.key_pressed("a"):
            self.gameobj.pos.x -= self.speed * Time.delta_time
        if Input.key_pressed("w"):
            self.gameobj.pos.y -= self.speed * Time.delta_time
        if Input.key_pressed("s"):
            self.gameobj.pos.y += self.speed * Time.delta_time
        if Input.key_pressed("d"):
            self.gameobj.pos.x += self.speed * Time.delta_time

        if self.gameobj.pos.x < 0:
            self.gameobj.pos.x = 0
        if self.gameobj.pos.y < 0:
            self.gameobj.pos.y = 0
        if self.gameobj.pos.x > (rb.Display.res * 1.2).x:
            self.gameobj.pos.x = (rb.Display.res * 1.2).x
        if self.gameobj.pos.y > (rb.Display.res * 1.2).y:
            self.gameobj.pos.y = (rb.Display.res * 1.2).y


main_scene = rb.Scene()
player = rb.GameObject(pos=rb.Display.center)
player.add(PlayerController(100))
main_scene.add(player, rb.wrap(rb.Rectangle(20, 20, rb.Color.red), pos=rb.Display.center))


def camera_follow():
    target = player.pos.clamp(rb.Display.center, rb.Display.res * 1.2 - rb.Display.center)
    rb.Game.current().camera.pos = rb.Game.current().camera.pos.lerp(target, .35)


main_scene.update = camera_follow

rb.begin()
