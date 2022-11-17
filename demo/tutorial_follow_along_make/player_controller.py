from rubato import Component, Input, Animation, RigidBody, KeyResponse, Events, Radio, Rectangle, Manifold, Game, Math, \
    Display, Time
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

    def update(self):
        # Runs once every frame.
        # Movement
        if Input.key_pressed("a"):
            self.rigid.velocity.x = -300
            self.animation.flipx = True
        elif Input.key_pressed("d"):
            self.rigid.velocity.x = 300
            self.animation.flipx = False

    def handle_key_down(self, event: KeyResponse):
        if event.key == "w" and self.jumps > 0:
            if self.jumps == 2:
                self.rigid.velocity.y = 800
                self.animation.set_state("jump", freeze=2)
            elif self.jumps == 1:
                self.rigid.velocity.y = 800
                self.animation.set_state("somer", True)
            self.jumps -= 1

    def fixed_update(self):
        # have the camera follow the player
        current_scene = Game.current()
        camera_ideal = Math.clamp(
            self.gameobj.pos.x + Display.res.x / 4, Display.center.x, shared.level1_size - Display.res.x
        )
        current_scene.camera.pos.x = Math.lerp(current_scene.camera.pos.x, camera_ideal, Time.fixed_delta / 0.4)
