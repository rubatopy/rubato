"""A place to test new WIP features"""
import rubato as rb

rb.init()
rb.Game.debug = True

main = rb.Scene()

a = rb.SimpleTilemap(
    [
        [1, 1, 1, 1, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 1, 0, 1],
        [1, 1, 1, 1, 1],
    ],
    [rb.Surface(32, 32), b := rb.Surface(32, 32)],
    collision=[1],
    scale=(3, 3),
)
b.fill(rb.Color.blue)
main.add(rb.wrap(a))
rb.begin()
