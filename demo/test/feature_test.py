"""A place to test new WIP features"""
import rubato as rb

rb.init(window_size=(2000, 2000))
rb.Game.debug = True
main = rb.Scene()
# main.camera.zoom = 3
go = rb.GameObject().add(rb.Tilemap("../sprites/test.tmx", (3, 3)))

main.add(go)
rb.begin()
