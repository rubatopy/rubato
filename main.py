# pylint: disable=all
import rubato as rb

rb.init()

main_scene = rb.Scene()
rb.game.scenes.add(main_scene)

image = rb.Sprite({
    "pos": rb.Vector(100, 100),
}).add_component(rb.Image({
    "scale": rb.Vector(2, 2),
}))

rect = rb.Sprite({
    "pos": rb.Vector(200, 100),
}).add_component(
    rb.Rectangle({
        "dims": rb.Vector(32, 32),
        "color": rb.Color.red,
    }))

rigid = rb.Sprite({
    "pos": rb.Vector(100, 200),
}).add_component(
    rb.RigidBody({
        "mass": 1,
        "friction": rb.Vector(1, 1),
        "max_speed": rb.Vector(100, rb.Math.INFINITY),
        "col_type": rb.COL_TYPE.ELASTIC,
        "hitbox": rb.Polygon.generate_rect(),
        "debug": True,
        "rotation": 0,
    })).add_component(
        rb.Rectangle({
            "dims": rb.Vector(32, 32),
            "color": rb.Color.yellow
        }))

main_scene.add(image)
main_scene.add(rect)
main_scene.add(rigid)

rb.begin()
