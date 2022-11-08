from rubato import Component, Animation, RigidBody, Rectangle, Manifold, Radio, Events, KeyResponse, JoyButtonResponse \
    , Input


class Player(Component):

    def __init__(self):
        super().__init__()

    def setup(self):
        self.initial_pos = self.gameobj.pos.clone()

        self.animation: Animation = self.gameobj.get(Animation)
        self.rigid: RigidBody = self.gameobj.get(RigidBody)

        rects = self.gameobj.get_all(Rectangle)
        self.ground_detector: Rectangle = [r for r in rects if r.tag == "player_ground_detector"][0]
        self.ground_detector.on_collide = self.ground_dectect

        self.grounded = False  # tracks the ground state
        self.jumps = 0  # tracks the number of jumps the player has left

        Radio.listen(Events.KEYDOWN, self.handle_key_down)
        Radio.listen(Events.JOYBUTTONDOWN, self.handle_controller_button)

    def ground_dectect(self, col_info: Manifold):
        if col_info.shape_b.tag == "ground" and not self.grounded and self.rigid.velocity.y >= 0:
            self.grounded = True
            self.jumps = 2
            self.animation.set_state("idle", True)

    def handle_key_down(self, event: KeyResponse):
        if event.key == "w" and self.jumps > 0:
            self.grounded = False
            self.rigid.velocity.y = 800
            if self.jumps == 2:
                self.animation.set_state("jump", freeze=2)
            elif self.jumps == 1:
                self.animation.set_state("somer", True)
            self.jumps -= 1

    def handle_controller_button(self, event: JoyButtonResponse):
        if event.button == 0:  # xbox a button / sony x button
            self.handle_key_down(KeyResponse(event.timestamp, "w", "", 0, 0))

    def update(self):
        move_axis = Input.controller_axis(Input.controllers - 1, 0)
        centered = Input.axis_centered(move_axis)
        # check for user directional input
        if Input.key_pressed("a") or (move_axis < 0 and not centered):
            self.rigid.velocity.x = -300
            self.animation.flipx = True
            if self.grounded:
                if Input.key_pressed("shift") or Input.key_pressed("s"):
                    self.animation.set_state("sneak", True)
                else:
                    self.animation.set_state("run", True)
        elif Input.key_pressed("d") or (move_axis > 0 and not centered):
            self.rigid.velocity.x = 300
            self.animation.flipx = False
            if self.grounded:
                if Input.key_pressed("shift") or Input.key_pressed("s"):
                    self.animation.set_state("sneak", True)
                else:
                    self.animation.set_state("run", True)
        else:
            self.rigid.velocity.x = 0
            if self.grounded:
                if Input.key_pressed("shift") or Input.key_pressed("s"):
                    self.animation.set_state("crouch", True)
                else:
                    self.animation.set_state("idle", True)

        if Input.key_pressed("r") or Input.controller_button(Input.controllers - 1, 6):
            self.gameobj.pos = self.initial_pos.clone()
            self.rigid.stop()
            self.grounded = False
