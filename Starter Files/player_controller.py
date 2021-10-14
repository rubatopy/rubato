# TODO test every class.
# could include having timer in here and updating it every update

import pygame
from pygame.locals import *

pygame.init()


class Collider:
    colliders = {}
    # { index: [Collider(), hit_something] }
    count = 0

    def __init__(self, rect: pygame.Rect):
        self.rect = rect
        self.moved = False  # used to see if we need to recalculate collisions
        self.enabled = True
        Collider.colliders[str(Collider.count)] = [self, False]
        Collider.count += 1

    @property
    def collider(self):
        return self.rect if self.enabled else None
    @staticmethod
    def hit():
        pass
        # l = []
        # for c in Collider.colliders.values():
        #     if c[1]
    @staticmethod
    def recalculate_colliders():
        SELF = 0
        hit_info = 1
        # worst case O(N^2) ie. no colliders hit eachother and they all moved
        # go through every collider
        for i in range(Collider.count):
            pair = Collider.colliders[str(i)]
            if pair[hit_info] or pair[SELF].move:
                pair[SELF].move = False
                continue
            else:
                # check if it hit every other collider
                for j in range(Collider.count):
                    if i == j:
                        continue
                    collide_check = Collider.colliders[str(i)]
                    if collide_check[SELF].enabled:
                        if collide_check[SELF].rect.colliderect(pair[SELF].rect):
                            pair[hit_info] = True
                            collide_check[hit_info] = True
                            break


class RigidBody2D:
    def __init__(self, rect):
        self.collider = Collider(rect)
        self.velocity = pygame.math.Vector2()

    def AddForce(self, force: pygame.math.Vector2):
        self.velocity += force

    def update(self):
        self.moverb(Collider.colliders.values())

    @staticmethod
    def collision_test(rect, tiles):
        hit_list = []
        for tile in tiles:
            if tile[0].enabled and rect.colliderect(tile[0].rect):
                hit_list.append(tile[0].rect)
        return hit_list

    def moverb(self):
        # self.collider.rect = self.collider.rect.move(self.velocity[0],self.velocity[1])
        collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
        self.collider.rect.x += int(self.velocity[0])
        Collider.recalculate_colliders()
        # hit_list = self.collision_test(self.collider.rect, tiles)
        # for tile in hit_list:
        #     print("here", hit_list)
            # if self.velocity[0] > 0:
            #     self.collider.rect.right = tile.left
            #     collision_types['right'] = True
            # elif self.velocity[0] < 0:
            #     self.collider.rect.left = tile.right
            #     collision_types['left'] = True
        self.collider.rect.y += self.velocity[1]
        # hit_list = self.collision_test(self.collider.rect, tiles)
        # for tile in hit_list:
        #     if self.velocity[1] > 0:
        #         self.collider.rect.bottom = tile.top
        #         collision_types['bottom'] = True
        #     elif self.velocity[1] < 0:
        #         self.collider.rect.top = tile.bottom
        #         collision_types['top'] = True
        # return collision_types


class CharacterController2D:
    k_GroundedRadius: float = .2  # Radius of the overlap circle to determine if grounded
    k_CeilingRadius: float = .2  # Radius of the overlap circle to determine if the player can stand up

    def __init__(self, rb: RigidBody2D, jump_force=400, crouch_speed=.36, smoothing=.6, air_control=True):
        self.m_JumpForce: float = jump_force  # Amount of force added when the player jumps.
        self.m_CrouchSpeed: float = crouch_speed  # Amount of maxSpeed applied to crouching movement. 1 = 100%
        self.m_MovementSmoothing: float = 1 - smoothing  # How much to smooth out the movement
        self.m_AirControl: bool = air_control  # Whether or not a player can steer while jumping
        self.m_WhatIsGround = list()  # A list determining what is ground to the character
        self.m_BodyCollider = rb.collider
        self.m_CrouchCollider = None  # A collider that will be disabled when crouching
        self.m_wasCrouching = False  # whether the player was crouching

        self.m_Grounded: bool = True  # Whether or not the player is grounded.
        self.m_Rigidbody2D: RigidBody2D = rb
        self.m_FacingRight: bool = True  # For determining which way the player is currently facing.
        self.m_Velocity: pygame.math.Vector2 = pygame.math.Vector2()

        # events
        self.OnLandEvent = None
        self.OnCrouchEvent = None

        # image
        self.image = pygame.image.load("idle.png")

    # if (self.OnLandEvent == None):
    # 	OnLandEvent = new UnityEvent()
    #
    # if (self.OnCrouchEvent == None)
    # 	OnCrouchEvent = new BoolEvent()

    def fixed_update(self):
        wasGrounded: bool = self.m_Grounded
        self.m_Grounded = False

        # TODO check if collision with the ground
        # 		self.m_Grounded = True
        # 		if (not wasGrounded):
        # 			self.OnLandEvent.Invoke()

    def move(self, move: float, crouch: bool, jump: bool):
        """
        :param move: left right move
        """

        # If crouching, check to see if the character can stand up
        if not crouch:
            still_crouching = 0
            # If the character has a ceiling preventing them from standing up, keep them crouching
            if still_crouching:
                crouch = True

        # only control the player if grounded or airControl is turned on
        if self.m_Grounded or self.m_AirControl:
            # If crouching
            if (crouch):
                # if you weren't already crouching
                if not self.m_wasCrouching:
                    self.m_wasCrouching = True
                    self.OnCrouchEvent.Invoke()

                # Reduce the speed by the crouchSpeed multiplier
                move *= self.m_CrouchSpeed

            # Disable one of the colliders when crouching (ie. make collider smaller)
            if self.m_CrouchCollider is not None:
                self.m_CrouchCollider.enabled = False
            else:

                # # Enable the collider when not crouching (ie. make collider big again)
                if self.m_CrouchCollider is not None:
                    self.m_CrouchCollider.enabled = True

                if self.m_wasCrouching:
                    self.m_wasCrouching = False

            # Move the character by finding the target velocity
            targetVelocity = pygame.math.Vector2(move * 10, self.m_Rigidbody2D.velocity.y)  # fix
            # And then smoothing it out and applying it to the character
            self.m_Rigidbody2D.velocity = self.m_Rigidbody2D.velocity.lerp(targetVelocity, self.m_MovementSmoothing)
            self.m_Rigidbody2D.velocity[0] = round(self.m_Rigidbody2D.velocity[0], 2)
            self.m_Rigidbody2D.velocity[1] = round(self.m_Rigidbody2D.velocity[1], 2)
            self.m_Rigidbody2D.update()

            # If the input is moving the player right and the player is facing left...
            if move > 0 and not self.m_FacingRight:

                # ... flip the player.
                self.flip()

            # Otherwise if the input is moving the player left and the player is facing right...
            elif move < 0 and self.m_FacingRight:
                # ... flip the player.
                self.flip()

        # If the player should jump...
        if self.m_Grounded and jump:
            # Add a vertical force to the player.
            self.m_Grounded = False
        # m_Rigidbody2D.AddForce(new Vector2(0f, m_JumpForce))

    def flip(self):

        # Switch the way the player is labelled as facing.
        self.m_FacingRight = not self.m_FacingRight

        # Multiply the player's x local scale by -1.
        # TODO actually flip player image
        pygame.transform.flip(self.image, True, False)

    def draw(self, screen: pygame.display):
        position = self.m_CrouchCollider.rect.topleft if self.m_CrouchCollider else self.m_BodyCollider.rect.topleft
        screen.blit(self.image, position)


class Player:
    def __init__(self):
        self.controller = CharacterController2D(RigidBody2D(pygame.Rect(200, 0, 10, 10)))
        self.horizontal = None
        self.crouch = None
        self.jump = None

    def input(self, crouch, jump):
        # pygame.event.pump()
        keypressed = pygame.key.get_pressed()
        self.horizontal = 0
        if keypressed[K_d]:
            self.horizontal = 1
        elif keypressed[K_a]:
            self.horizontal = -1
        self.crouch = crouch
        self.jump = jump

    def update(self):
        delta = 1  # TODO get some deltatime
        self.controller.move(self.horizontal * delta, self.crouch, self.jump)

    def draw(self, screen):
        self.controller.draw(screen)


def library_update():
    Collider.recalculate_colliders()
