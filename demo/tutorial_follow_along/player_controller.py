from rubato import Component, Input, Animation, RigidBody

class PlayerController(Component):

    def setup(self):
        # Like the init function of regular classes. Called when added to Game Object.
        # Specifics can be found in the Custom Components tutorial.
        self.initial_pos = self.gameobj.pos.clone()

        self.animation: Animation = self.gameobj.get(Animation)
        self.rigid: RigidBody = self.gameobj.get(RigidBody)
        pass

    def update(self):
        # Runs once every frame.
        # Movement
        if Input.key_pressed("a"):
            self.rigid.velocity.x = -300
            self.animation.flipx = True
        elif Input.key_pressed("d"):
            self.rigid.velocity.x = 300
            self.animation.flipx = False
