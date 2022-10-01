import rubato as rb
from rubato import Vector as V, GameObject, Display
import classes, objects as objs

rb.init(res=(800, 600), name="Sling shot")

main_scene = rb.Scene()

objs.player = GameObject(pos=Display.center - V(0, 100), name="player_go")
rect = rb.Rectangle(50, 50, color=rb.Color.red, tag="player")
objs.player.add(rect)

objs.player_body = rb.RigidBody(gravity=rb.Vector(0, 10), pos_correction=1, mass=30)
objs.player.add(objs.player_body)

ground = rb.wrap(rb.Rectangle(width=Display.res.x, height=50, color=rb.Color.green, tag="ground"), pos=Display.bottom_center)

# def key_down(data):
#     if data["key"] == "space":
#         objs.player_body.static = not objs.player_body.static
#
# rb.Radio.listen(rb.Events.KEYDOWN, key_down)

main_scene.add(objs.player, ground, rb.wrap(classes.Anchor(Display.center + V(0, 50))))
rb.begin()