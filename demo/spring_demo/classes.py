import rubato as rb

import objects


class Spring(rb.Component):
    def __init__(self, minlength, target: rb.GameObject, spring_coefficient: float, damping_coefficient: float):
        super().__init__()
        self.target = target
        self.targetrb = target.get(rb.RigidBody)
        self.min_length = minlength
        self.k = spring_coefficient
        self.b = damping_coefficient
    # def update(self):
    #     rb.Draw.queue_line(self.target.pos + rb.Vector(5, 0),
    #                        self.target.pos + rb.Vector(5, 0) + self.targetrb.velocity, rb.Color.green, width=5)
    def fixed_update(self):
        if self.targetrb is None:
            return

        # Calculate the spring force
        disp = self.gameobj.pos - self.target.pos
        dir = disp.normalized()

        disp = disp.magnitude - self.min_length
        if disp < 0.1:
            return
        spring_force = disp * self.k

        # Calculate the damping force
        damping_force = self.targetrb.velocity.magnitude * self.b

        # Apply the force
        mag = dir * (spring_force + damping_force)
        print(rb.Time.frames, mag)
        rb.Draw.queue_line(self.target.pos, self.target.pos + mag, rb.Color.blue, width=5)
        self.targetrb.add_force(mag)

class Anchor(rb.Component):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.hitbox = rb.Rectangle(10, 10, color=rb.Color.blue, trigger=True)

        self.player_is_on = False
        self.k = 2
        self.b = 1
        self.length = 50
        self.stretch_length = 200

    def on_collide(self, other: rb.Manifold):
        if other.shape_b.tag == "player":
            self.hitbox.color = rb.Color.green
            if not self.player_is_on:
                self.gameobj.add(Spring(self.length, objects.player, self.k, self.b))
            self.player_is_on = True

    def setup(self):
        self.gameobj.pos = self.pos
        self.hitbox.on_collide = self.on_collide
        self.gameobj.add(self.hitbox)

    def closest_point_on_circle(self, dist: rb.Vector):
        return self.pos + dist.normalized() * self.stretch_length
        # V = (P - C); Answer = C + V / |V| * R;

    def update(self):
        color = rb.Color.blue
        color.a = 100
        # rb.Draw.queue_circle(self.pos, self.stretch_length, fill=color)
        # rb.Draw.queue_circle(self.pos, self.length, fill=rb.Color(255, 0, 0, 100))


        # if self.player_is_on:
        #     dist: rb.Vector = self.pos - objects.player.pos
        #     force = rb.Vector.zero()
        #     if dist.magnitude > self.length:
        #         force = dist.normalized() * (dist.magnitude - self.length) * self.k
        #     objects.player_body.add_force(force)
        #
        #     if dist.mag_sq > self.stretch_length ** 2:
        #         self.hitbox.color = rb.Color.red
        #         # self.player_is_on = False
        #         objects.player.pos = self.closest_point_on_circle(-dist)
        #         objects.player_body.velocity = rb.Vector.zero()
        #         objects.player_body.add_force(dist.normalized() * 1000)
        #
        #     rb.Draw.queue_line(self.pos, objects.player.pos, color=rb.Color.blue, width=5)
        #     rb.Draw.queue_line(objects.player.pos, objects.player.pos + force, color=rb.Color.red, width=5)



