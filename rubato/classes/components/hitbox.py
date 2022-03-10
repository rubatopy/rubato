"""Various hitbox components that enable collisions"""

import math
from typing import Callable, List, Union
from rubato.classes.components.rigidbody import RigidBody
from rubato.utils import Math, Display, Vector, Configs, Color
from rubato.classes.component import Component
from rubato.utils.error import SideError
import rubato as rb
from pygame.gfxdraw import aapolygon, filled_polygon, aacircle, filled_circle


class Hitbox(Component):
    """
    The basic hitbox
    """
    hitboxes: List["Hitbox"] = []

    def __init__(self):
        super().__init__()
        self.debug = False
        self.trigger = False
        self.tags = []
        self._pos = lambda: Vector(0, 0)
        self.scale = 1
        self.callback = lambda c: None

    def update(self):
        self.draw()

    def draw(self):
        pass

    def bounding_box_dimensions(self) -> Vector:
        """
        Returns the dimensions of the bounding box surrounding the polygon.

        Returns:
            Vector: A vector with the x variable holding the width and the y
            variable holding the height.
        """
        return Vector(0, 0)

    def collide(
            self,
            other: "Hitbox",
            callback: Callable = lambda c: None
    ) -> Union["CollisionInfo", None]:
        """
        A simple collision engine for most use cases.

        Args:
            other: The other rigidbody to collide with.
            callback: The function to run when a collision is detected.
                Defaults to None.

        Returns:
            Union[CollisionInfo, None]: Returns a collision info object if a
            collision is detected or nothing if no collision is detected.
        """
        if (col := SAT.overlap(self, other)) is not None:
            if not self.trigger and (
                (self.sprite.get_component(RigidBody) is not None) or
                (other.sprite.get_component(RigidBody) is not None)):

                RigidBody.handle_collision(col)

            callback(col)
            self.callback(col)
            other.callback(col)


class Polygon(Hitbox):
    """
    A custom polygon class with an arbitrary number of vertices

    Attributes:
        verts (List[Vector]): A list of the vertices in the Polygon, in either
            clockwise or anticlockwise direction.
        scale (Union[float, int]): The scale of the polygon.
    """

    def __init__(self, options: dict = {}):
        """
        Initializes a Polygon

        Args:
            verts: A list of the vertices in the Polygon.
            pos: The position of the center of the Polygon as a function.
                Defaults to lambda: Vector(0, 0).
            scale: The scale of the polygon. Defaults to 1.
            rotation: The rotation angle of the polygon in degrees as a
                function. Defaults to lambda: 0.
        """
        params = Configs.merge_params(options, Configs.polygon_defaults)
        super().__init__()
        self.debug: bool = params["debug"]
        self.trigger: bool = params["trigger"]
        self.tags: List[str] = params["tags"]
        self.verts: List[Vector] = params["verts"]
        self.rotation: float = params["rotation"]
        self.color: Color = params["color"]
        self.scale: int = params["scale"]
        self.callback: Callable = params["callback"]

    @staticmethod
    def generate_rect(w: int = 32, h: int = 32) -> List[Vector]:
        """
        Creates a rectangle from its dimensions.

        Args:
            w: The width of the hitbox.
            h: The height of the hitbox.

        Returns:
            List[Vector]: The vertices of the rectangle.
        """

        return [
            Vector(-w / 2, -h / 2),
            Vector(w / 2, -h / 2),
            Vector(w / 2, h / 2),
            Vector(-w / 2, h / 2)
        ]

    @staticmethod
    def generate_polygon(num_sides: int,
                         radius: Union[float, int] = 1) -> List[Vector]:
        """
        Creates a normal polygon with a specified number of sides and
        an optional radius.

        Args:
            num_sides: The number of sides of the polygon.
            radius: The radius of the polygon. Defaults to 1.

        Raises:
            SideError: Raised when the number of sides is less than 3.

        Returns:
            List[Vector]: The vertices of the polygon.
        """
        if num_sides < 3:
            raise SideError(
                "Can't create a polygon with less than three sides")

        rotangle = 2 * math.pi / num_sides
        angle, verts = 0, []

        for i in range(num_sides):
            angle = (i * rotangle) + (math.pi - rotangle) / 2
            verts.append(
                Vector(math.cos(angle) * radius,
                       math.sin(angle) * radius))

        return verts

    @property
    def pos(self) -> Vector:
        """The getter method for the position of the Polygon's center"""
        return self._pos()

    def clone(self) -> "Polygon":
        """Creates a copy of the Polygon at the current position"""
        new_poly = Polygon({
            "verts":
            list(map((lambda v: v.clone()), self.verts)),
            "rotation":
            self.rotation,
            "debug":
            self.debug,
            "trigger":
            self.trigger,
            "tags":
            self.tags,
            "scale":
            self.scale,
            "callback":
            self.callback,
        })
        new_poly._pos = self._pos  # pylint: disable=protected-access
        return new_poly

    def transformed_verts(self) -> List[Vector]:
        """Maps each vertex with the Polygon's scale and rotation"""
        return list(
            map(lambda v: v.transform(self.scale, self.rotation), self.verts))

    def real_verts(self) -> List[Vector]:
        """Returns the a list of vertices in absolute coordinates"""
        return list(
            map(lambda v: self.pos + v.transform(self.scale, self.rotation),
                self.verts))

    def __str__(self):
        return (f"{list(map(str, self.verts))}, {self.pos}, " +
                f"{self.scale}, {self.rotation}")

    def bounding_box_dimensions(self) -> Vector:
        real_verts = self.real_verts()
        x_dir = SAT.project_verts(real_verts, Vector(1, 0))
        y_dir = SAT.project_verts(real_verts, Vector(0, 1))
        return Vector(x_dir.y - x_dir.x, y_dir.y - y_dir.x)

    def draw(self):
        """
        The draw loop
        """
        if self.debug:
            aapolygon(
                Display.global_display,
                list(
                    map(
                        lambda v: rb.Game.scenes.current_scene.camera.
                        transform(v * rb.Game.scenes.current_scene.camera.zoom
                                  ),
                        self.real_verts(),
                    )),
                (0, 255, 0),
            )

        if self.color is not None:
            aapolygon(
                Display.global_display,
                list(
                    map(
                        lambda v: rb.Game.scenes.current_scene.camera.
                        transform(v * rb.Game.scenes.current_scene.camera.zoom
                                  ),
                        self.real_verts(),
                    )),
                self.color.to_tuple(),
            )

            filled_polygon(
                Display.global_display,
                list(
                    map(
                        lambda v: rb.Game.scenes.current_scene.camera.
                        transform(v * rb.Game.scenes.current_scene.camera.zoom
                                  ),
                        self.real_verts(),
                    )),
                self.color.to_tuple(),
            )


class Circle(Hitbox):
    """
    A custom circle class defined by a position, radius, and scale

    Attributes:
        radius (int): The radius of the circle.
        scale (int): The scale of the circle.
    """

    def __init__(self, options: dict = {}):
        """
        Initializes a Circle

        Args:
            pos: The position of the circle as a function.
                Defaults to lambda: Vector(0, 0).
            radius: The radius of the circle. Defaults to 1.
            scale: The scale of the circle. Defaults to 1.
        """
        params = Configs.merge_params(options, Configs.circle_defaults)
        super().__init__()
        self.radius = params["radius"]
        self.color: Color = params["color"]
        self.scale: int = params["scale"]
        self.callback: Callable = params["callback"]
        self.debug: bool = params["debug"]
        self.trigger: bool = params["trigger"]
        self.tags: List[str] = params["tags"]

    @property
    def pos(self) -> Vector:
        """The getter method for the position of the circle's center"""
        return self._pos()

    def clone(self) -> "Circle":
        """Creates a copy of the circle at the current position"""
        new_circle = Circle(self.radius)
        new_circle._pos = self._pos  # pylint: disable=protected-access
        new_circle.scale = self.scale
        return new_circle

    def transformed_radius(self) -> int:
        """Gets the true radius of the circle"""
        return self.radius * self.scale

    def draw(self):
        if self.debug:
            aacircle(
                Display.global_display,
                int(self.pos.x),
                int(self.pos.y),
                int(self.radius),
                self.color.to_tuple(),
            )
        if self.color is not None:
            # aacircle(
            #     Display.global_display,
            #     int(self.pos.x),
            #     int(self.pos.y),
            #     self.radius,
            #     self.color.to_tuple(),
            # )
            filled_circle(
                Display.global_display,
                int(self.pos.x),
                int(self.pos.y),
                int(self.radius),
                self.color.to_tuple(),
            )


class CollisionInfo:
    """
    A class that represents information returned in a successful collision

    Attributes:
        shape_a (Union[Circle, Polygon, None]): A reference to the first shape.
        shape_b (Union[Circle, Polygon, None]): A reference to the second shape.
        seperation (Vector): The vector that would separate the two colliders.
    """

    def __init__(self):
        """
        Initializes a Collision Info
        """
        self.shape_a: Union[Hitbox, None] = None
        self.shape_b: Union[Hitbox, None] = None
        self.sep = Vector()

    def __str__(self):
        return f"{self.sep}"


class SAT:
    """
    A general class that does the collision detection math between
    circles and polygons
    """

    @staticmethod
    def overlap(shape_a: Hitbox,
                shape_b: Hitbox) -> Union[CollisionInfo, None]:
        """
        Checks for overlap between any two shapes (Polygon or Circle)

        Args:
            shape_a: The first shape.
            shape_b: The second shape.

        Returns:
            Union[CollisionInfo, None]: If a collision occurs, a CollisionInfo
            is returned. Otherwise None is returned.
        """

        if isinstance(shape_a, Circle) and isinstance(shape_b, Circle):
            return SAT.circle_circle_test(shape_a, shape_b)

        if isinstance(shape_a, Polygon) and isinstance(shape_b, Polygon):
            test_a_b = SAT.polygon_polygon_test(shape_a, shape_b)
            if test_a_b is None: return None

            test_b_a = SAT.polygon_polygon_test(shape_b, shape_a, True)
            if test_b_a is None: return None

            return (test_b_a, test_a_b)[test_a_b.sep.mag < test_b_a.sep.mag]

        a_is_circle = isinstance(shape_a, Circle)
        return SAT.circle_polygon_test((shape_b, shape_a)[a_is_circle],
                                       (shape_a, shape_b)[a_is_circle],
                                       not a_is_circle)

    @staticmethod
    def circle_circle_test(shape_a: Circle, shape_b: Circle):
        """Checks for overlap between two circles"""
        total_radius = shape_a.radius + shape_b.radius
        distance = (shape_b.pos - shape_a.pos).magnitude

        if distance > total_radius:
            return None

        result = CollisionInfo()
        result.shape_a = shape_a
        result.shape_b = shape_b

        result.sep = (shape_a.pos - shape_b.pos).unit() * (total_radius -
                                                           distance)

        return result

    @staticmethod
    def circle_polygon_test(shape_a: Circle,
                            shape_b: Polygon,
                            flip: bool = False):
        shortest = Math.INFINITY

        result = CollisionInfo()
        result.shape_a = shape_b if flip else shape_a
        result.shape_b = shape_a if flip else shape_b

        verts = shape_b.transformed_verts()
        offset = shape_b.pos - shape_a.pos

        closest = Vector()
        for v in verts:
            dist = (shape_a.pos - (shape_b.pos + v)).magnitude
            if dist < shortest:
                shortest = dist
                closest = shape_b.pos + v

        axis = closest - shape_a.pos
        axis.normalize()

        poly_range = SAT.project_verts(verts, axis) + axis.dot(offset)
        circle_range = Vector(-shape_a.transformed_radius(),
                              shape_a.transformed_radius())

        if ((poly_range.x - circle_range.y > 0)
                or (circle_range.x - poly_range.y > 0)):
            return None

        dist_min = circle_range.y - poly_range.x
        if flip: dist_min *= -1

        shortest = abs(dist_min)

        sep = axis * dist_min

        for i in range(len(verts)):
            axis = SAT.perpendicular_axis(verts, i)

            poly_range = SAT.project_verts(verts, axis) + axis.dot(offset)
            circle_range = Vector(-shape_a.transformed_radius(),
                                  shape_a.transformed_radius())

            if ((poly_range.x - circle_range.y > 0)
                    or (circle_range.x - poly_range.y > 0)):
                return None

            dist_min = circle_range.y - poly_range.x
            if flip: dist_min *= -1

            dist_min_abs = abs(dist_min)
            if dist_min_abs < shortest:
                shortest = dist_min_abs
                sep = axis * dist_min

        result.sep = -sep

        return result

    @staticmethod
    def polygon_polygon_test(shape_a: Polygon,
                             shape_b: Polygon,
                             flip: bool = False) -> Union[CollisionInfo, None]:
        """Checks for overlap between two polygons"""

        shortest_dist = Math.INFINITY

        result = CollisionInfo()
        result.shape_a = shape_a if flip else shape_b
        result.shape_b = shape_b if flip else shape_a

        verts_a = shape_a.transformed_verts()
        verts_b = shape_b.transformed_verts()

        offset = shape_a.pos - shape_b.pos

        for i in range(len(verts_a)):
            axis = SAT.perpendicular_axis(verts_a, i)

            a_range = SAT.project_verts(verts_a, axis) + axis.dot(offset)
            b_range = SAT.project_verts(verts_b, axis)

            if (a_range.x > b_range.y) or (b_range.x > a_range.y):
                return None

            min_dist = (a_range.x - b_range.y, b_range.x - a_range.y)[flip]
            abs_min = abs(min_dist)

            if abs_min < shortest_dist:
                shortest_dist = abs_min
                result.sep = axis * min_dist

        return result

    @staticmethod
    def perpendicular_axis(verts: List[Vector], index: int) -> Vector:
        """Finds a vector perpendicular to a side"""

        pt_1, pt_2 = verts[index], verts[(index + 1) % len(verts)]
        axis = Vector(pt_1.y - pt_2.y, pt_2.x - pt_1.x)
        axis.normalize()
        return axis

    @staticmethod
    def project_verts(verts: List[Vector], axis: Vector) -> Vector:
        """
        Projects the vertices onto a given axis.
        Returns as a vector x is min, y is max
        """

        minval, maxval = Math.INFINITY, -Math.INFINITY

        for v in verts:
            temp = axis.dot(v)
            minval, maxval = min(minval, temp), max(maxval, temp)

        return Vector(minval, maxval)
