from rubato import Component, Animation, RigidBody, Rectangle, Manifold, Radio, Events, KeyResponse, \
    Input, Math, Display, Game, Time, Vector
import shared


class PlayerController(Component):

    def setup(self):
        self.initial_pos = self.gameobj.pos.clone()

        self.animation: Animation = self.gameobj.get(Animation)
        self.rigid: RigidBody = self.gameobj.get(RigidBody)

        rects = self.gameobj.get_all(Rectangle)
        self.ground_detector: Rectangle = [r for r in rects if r.tag == "player_ground_detector"][0]
        self.ground_detector.on_collide = self.ground_detect
        self.ground_detector.on_exit = self.ground_exit

        self.grounded = False  # tracks the ground state
        self.jumps = 0  # tracks the number of jumps the player has left

        Radio.listen(Events.KEYDOWN, self.handle_key_down)

    def ground_detect(self, col_info: Manifold):
        if "ground" in col_info.shape_b.tag and self.rigid.velocity.y >= 0:
            if not self.grounded:
                self.grounded = True
                self.jumps = 2
                self.animation.set_state("idle", True)

    def ground_exit(self, col_info: Manifold):
        if "ground" in col_info.shape_b.tag:
            self.grounded = False

    def handle_key_down(self, event: KeyResponse):
        if event.key == "w" and self.jumps > 0:
            if self.jumps == 2:
                self.rigid.velocity.y = 800
                self.animation.set_state("jump", freeze=2)
            elif self.jumps == 1:
                self.rigid.velocity.y = 800
                self.animation.set_state("somer", True)
            self.jumps -= 1

    def update(self):
        # Runs once every frame.
        # Movement
        if Input.key_pressed("a"):
            self.rigid.velocity.x = -300
            self.animation.flipx = True
        elif Input.key_pressed("d"):
            self.rigid.velocity.x = 300
            self.animation.flipx = False
        else:
            if not self.grounded:
                self.rigid.velocity.x = 0
                self.rigid.friction = 0
            else:
                self.rigid.friction = 1

        # Running animation states
        if self.grounded:
            if self.rigid.velocity.x in (-300, 300):
                if Input.key_pressed("shift") or Input.key_pressed("s"):
                    self.animation.set_state("sneak", True)
                else:
                    self.animation.set_state("run", True)
            else:
                if Input.key_pressed("shift") or Input.key_pressed("s"):
                    self.animation.set_state("crouch", True)
                else:
                    self.animation.set_state("idle", True)

        # Reset
        if Input.key_pressed("r") or self.gameobj.pos.y < -550:
            self.gameobj.pos = self.initial_pos.clone()
            self.rigid.stop()
            self.grounded = False
            Game.current().camera.pos = Vector(0, 0)

    # define a custom fixed update function
    def fixed_update(self):
        # have the camera follow the player
        current_scene = Game.current()
        camera_ideal = Math.clamp(
            self.gameobj.pos.x + Display.res.x / 4, Display.center.x, shared.level1_size - Display.res.x
        )
        current_scene.camera.pos.x = Math.lerp(current_scene.camera.pos.x, camera_ideal, Time.fixed_delta / 0.4)