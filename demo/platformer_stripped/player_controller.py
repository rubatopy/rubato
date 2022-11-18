import rubato as rb
import shared


class PlayerController(rb.Component):

    def setup(self):
        # Called when added to Game Object.
        # Specifics can be found in the Custom Components tutorial.
        self.initial_pos = self.gameobj.pos.clone()

        self.animation: rb.Animation = self.gameobj.get(rb.Animation)
        self.rigid: rb.RigidBody = self.gameobj.get(rb.RigidBody)

        rects = self.gameobj.get_all(rb.Rectangle)
        self.detector = [r for r in rects if r.tag == "player_ground_detector"][0]
        self.detector.on_collide = self.ground_detect
        self.detector.on_exit = self.ground_exit

        # Tracks the number of jumps the player has left
        self.jumps = 2
        # Tracks the ground state
        self.grounded = False

        rb.Radio.listen(rb.Events.KEYDOWN, self.handle_key_down)

    def ground_detect(self, col_info: rb.Manifold):
        if "ground" in col_info.shape_b.tag and self.rigid.velocity.y >= 0:
            if not self.grounded:
                self.grounded = True
                self.jumps = 2
                self.animation.set_state("idle", True)

    def ground_exit(self, col_info: rb.Manifold):
        if "ground" in col_info.shape_b.tag:
            self.grounded = False

    def update(self):
        # Runs once every frame.
        # Movement
        if rb.Input.key_pressed("a"):
            self.rigid.velocity.x = -300
            self.animation.flipx = True
        elif rb.Input.key_pressed("d"):
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
                if rb.Input.key_pressed("shift") or rb.Input.key_pressed("s"):
                    self.animation.set_state("sneak", True)
                else:
                    self.animation.set_state("run", True)
            else:
                if rb.Input.key_pressed("shift") or rb.Input.key_pressed("s"):
                    self.animation.set_state("crouch", True)
                else:
                    self.animation.set_state("idle", True)

        # Reset
        if rb.Input.key_pressed("r") or self.gameobj.pos.y < -550:
            self.gameobj.pos = self.initial_pos.clone()
            self.rigid.stop()
            self.grounded = False
            rb.Game.current().camera.pos = rb.Vector(0, 0)

    # define a custom fixed update function
    def fixed_update(self):
        # have the camera follow the player
        current_scene = rb.Game.current()
        camera_ideal = rb.Math.clamp(
            self.gameobj.pos.x + rb.Display.res.x / 4,
            rb.Display.center.x,
            shared.level1_size - rb.Display.res.x,
        )
        current_scene.camera.pos.x = rb.Math.lerp(
            current_scene.camera.pos.x,
            camera_ideal,
            rb.Time.fixed_delta / 0.4,
        )

    def handle_key_down(self, event: rb.KeyResponse):
        if event.key == "w" and self.jumps > 0:
            if self.jumps == 2:
                self.rigid.velocity.y = 800
                self.animation.set_state("jump", freeze=2)
            elif self.jumps == 1:
                self.rigid.velocity.y = 800
                self.animation.set_state("somer", True)
            self.jumps -= 1
