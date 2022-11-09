from rubato import Component, Time, Vector


class MovingPlatform(Component):

    def __init__(self, speed, direction, bound, pause=0):
        super().__init__()
        self.speed = speed
        self.direction = direction
        if direction == "r":
            self.direction_vect = Vector(1, 0)
        elif direction == "l":
            self.direction_vect = Vector(-1, 0)
        elif direction == "u":
            self.direction_vect = Vector(0, 1)
        elif direction == "d":
            self.direction_vect = Vector(0, -1)
        self.bound = bound
        self.pause = pause
        self.pause_counter = 0

    def setup(self):
        self.initial_pos = self.gameobj.pos.clone()

    def fixed_update(self):
        if self.pause_counter > 0:
            self.pause_counter -= Time.fixed_delta
            return

        self.gameobj.pos += self.direction_vect * self.speed * Time.fixed_delta

        self.old_dir_vect = self.direction_vect.clone()
        if self.direction == "r":
            if self.gameobj.pos.x > self.initial_pos.x + self.bound:
                self.direction_vect = Vector(-1, 0)
            if self.gameobj.pos.x < self.initial_pos.x:
                self.direction_vect = Vector(1, 0)
        elif self.direction == "l":
            if self.gameobj.pos.x < self.initial_pos.x - self.bound:
                self.direction_vect = Vector(1, 0)
            if self.gameobj.pos.x > self.initial_pos.x:
                self.direction_vect = Vector(-1, 0)
        elif self.direction == "u":
            if self.gameobj.pos.y > self.initial_pos.y + self.bound:
                self.direction_vect = Vector(0, -1)
            if self.gameobj.pos.y < self.initial_pos.y:
                self.direction_vect = Vector(0, 1)
        elif self.direction == "d":
            if self.gameobj.pos.y < self.initial_pos.y - self.bound:
                self.direction_vect = Vector(0, 1)
            if self.gameobj.pos.y > self.initial_pos.y:
                self.direction_vect = Vector(0, -1)

        if self.old_dir_vect != self.direction_vect:
            self.pause_counter = self.pause
