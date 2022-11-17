from rubato import Component, Input, Animation, RigidBody, KeyResponse, Events, Radio


class PlayerController(Component):

    def setup(self):
        # Like the init function of regular classes. Called when added to Game Object.
        # Specifics can be found in the Custom Components tutorial.
        self.initial_pos = self.gameobj.pos.clone()

        self.animation: Animation = self.gameobj.get(Animation)
        self.rigid: RigidBody = self.gameobj.get(RigidBody)

        # Tracks the number of jumps the player has left
        self.jumps = 2

        Radio.listen(Events.KEYDOWN, self.handle_key_down)

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
