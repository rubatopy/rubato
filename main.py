# pylint: disable=all
from pip import main
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

run = rb.Animation.import_animation_folder("testing/Run")
idle = rb.Animation.import_animation_folder("testing/Idle")

animated_player = rb.Sprite({
    "pos": rb.Vector(50, 50),
})

animation_component = rb.Animation()
animated_player.add_component(animation_component)

animation_component.add_state("run", run)
animation_component.add_state("idle", idle)


class CustomComponent(rb.Component):

    def update(self):
        if rb.Input.is_pressed("w"):
            animation_component.set_current_state("run")
            animated_player.pos += rb.Vector(0, -5)
        elif rb.Input.is_pressed("s"):
            animation_component.set_current_state("run")
            animated_player.pos += rb.Vector(0, 5)
        elif rb.Input.is_pressed("a"):
            animation_component.set_current_state("run")
            animated_player.pos += rb.Vector(-5, 0)
        elif rb.Input.is_pressed("d"):
            animation_component.set_current_state("run")
            animated_player.pos += rb.Vector(5, 0)
        else:
            animation_component.set_current_state("idle")
        if rb.Input.is_pressed("right"):
            animation_component.rotation += 1
        if rb.Input.is_pressed("="):
            animation_component.resize(
                rb.Vector.from_tuple(
                    animation_component.anim_frame.get_size_original()) * 2)
        elif rb.Input.is_pressed("-"):
            animated_player.resize(
                rb.Vector.from_tuple(
                    animated_player.anim_frame.get_size_original()) / 2)
        else:
            animation_component.resize(
                rb.Vector.from_tuple(
                    animation_component.anim_frame.get_size_original()))


empty = rb.Sprite().add_component(CustomComponent())

main_scene.add(image)
main_scene.add(rect)
main_scene.add(rigid)
main_scene.add(animated_player)
main_scene.add(empty)

rb.begin()
