"""Various hitbox components that enable collisions"""

import math
from typing import Callable, List, Union
from rubato.classes.components.rigidbody import RigidBody
from rubato.utils import Math, Display, Vector, Defaults, Color
from rubato.classes.component import Component
from rubato.utils.error import Error, SideError
from rubato.game import Game
import sdl2
import sdl2.sdlgfx
from ctypes import c_int16


class Hitbox(Component):
    """
    The basic hitbox
    """
    hitboxes: List["Hitbox"] = []

    def __init__(self, options: dict = {}):
        params = Defaults.hitbox_defaults | options
        super().__init__()
        self.debug: bool = params["debug"]
        self.trigger: bool = params["trigger"]
        self._pos = lambda: Vector(0, 0)
        self.scale: int = params["scale"]
        self.on_collide: Callable = params["on_collide"]
        self.color: Color = params["color"]
        self.multiple = params["multiple"]

    @property
    def pos(self) -> Vector:
        """The getter method for the position of the hitbox's center"""
        return self._pos()

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

    def collide(self, other: "Hitbox") -> Union["ColInfo", None]:
        """
        A simple collision engine for most use cases.

        Args:
            other: The other rigidbody to collide with.
            on_collide: The function to run when a collision is detected.
                Defaults to None.

        Returns:
            Union[ColInfo, None]: Returns a collision info object if a
            collision is detected or nothing if no collision is detected.
        """
        if (col := SAT.overlap(self, other)) is not None:
            if not self.trigger and ((self.sprite.get(RigidBody) is not None) or
                                     (other.sprite.get(RigidBody) is not None)):

                RigidBody.handle_collision(col)

            self.on_collide(col)
            other.on_collide(ColInfo.flip(col))


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
        super().__init__(options)
        params = Defaults.polygon_defaults | options
        self.verts: List[Vector] = params["verts"]
        self.rotation: float = params["rotation"]

    @staticmethod
    def generate_polygon(num_sides: int, radius: Union[float, int] = 1) -> List[Vector]:
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
            raise SideError("Can't create a polygon with less than three sides")

        rotangle = 2 * math.pi / num_sides
        angle, verts = 0, []

        for i in range(num_sides):
            angle = (i * rotangle) + (math.pi - rotangle) / 2
            verts.append(Vector(math.cos(angle) * radius, math.sin(angle) * radius))

        return verts

    def clone(self) -> "Polygon":
        """Creates a copy of the Polygon at the current position"""
        new_poly = Polygon({
            "verts": [v.clone() for v in self.verts],
            "rotation": self.rotation,
            "debug": self.debug,
            "trigger": self.trigger,
            "scale": self.scale,
            "on_collide": self.on_collide,
        })
        new_poly._pos = self._pos  # pylint: disable=protected-access
        return new_poly

    def transformed_verts(self) -> List[Vector]:
        """Maps each vertex with the Polygon's scale and rotation"""
        return [v.transform(self.scale, self.rotation) for v in self.verts]

    def real_verts(self) -> List[Vector]:
        """Returns the a list of vertices in absolute coordinates"""
        return [self.pos + v for v in self.transformed_verts()]

    def __str__(self):
        return f"{[str(v) for v in self.verts]}, {self.pos}, " + f"{self.scale}, {self.rotation}"

    def bounding_box_dimensions(self) -> Vector:
        real_verts = self.real_verts()
        x_dir = SAT.project_verts(real_verts, Vector(1, 0))
        y_dir = SAT.project_verts(real_verts, Vector(0, 1))
        return Vector(x_dir.y - x_dir.x, y_dir.y - y_dir.x)

    def draw(self):
        """
        The draw loop
        """
        list_of_points: List[tuple] = [Game.scenes.current.camera.transform(v).tuple_int() for v in self.real_verts()]

        x_coords, y_coords = zip(*list_of_points)

        vx = (c_int16 * len(x_coords))(*x_coords)
        vy = (c_int16 * len(y_coords))(*y_coords)

        if self.color is not None:
            sdl2.sdlgfx.filledPolygonRGBA(
                Display.renderer.sdlrenderer,
                vx,
                vy,
                len(list_of_points),
                self.color.r,
                self.color.g,
                self.color.b,
                self.color.a,
            )
            sdl2.sdlgfx.aapolygonRGBA(
                Display.renderer.sdlrenderer,
                vx,
                vy,
                len(list_of_points),
                self.color.r,
                self.color.g,
                self.color.b,
                self.color.a,
            )

        if self.debug:
            sdl2.sdlgfx.aapolygonRGBA(
                Display.renderer.sdlrenderer,
                vx,
                vy,
                len(list_of_points),
                0,
                255,
                0,
                255,
            )


class Rectangle(Hitbox):
    """
    A rectangle class

    Warning:
        Needs documentation
    """

    def __init__(self, options: dict):
        super().__init__(options)
        params = Defaults.rectangle_defaults | options

        self.width: int = int(params["width"])
        self.height: int = int(params["height"])

        self.rotation: float = params["rotation"]

    @property
    def topleft(self):
        """
        The top left corner of the rectangle

        Note:
            This can only be accessed and set after the Rectangle has been
            added to a Sprite.
        """
        if self.sprite:
            return self.pos - Vector(self.width / 2, self.height / 2)
        else:
            raise Error("Tried to get rect property before sprite assignment.")

    @topleft.setter
    def topleft(self, new: Vector):
        if self.sprite:
            self.sprite.pos = new + Vector(self.width / 2, self.height / 2)
            self.sprite.pos = self.sprite.pos.to_int()
        else:
            raise Error("Tried to set rect property before sprite assignment.")

    @property
    def bottomleft(self):
        """
        The bottom left corner of the rectangle

        Note:
            This can only be accessed and set after the Rectangle has been
            added to a Sprite.
        """
        if self.sprite:
            return self.pos - Vector(self.width / 2, self.height / -2)
        else:
            raise Error("Tried to get rect property before sprite assignment.")

    @bottomleft.setter
    def bottomleft(self, new: Vector):
        if self.sprite:
            self.sprite.pos = new + Vector(self.width / 2, self.height / -2)
            self.sprite.pos = self.sprite.pos.to_int()
        else:
            raise Error("Tried to set rect property before sprite assignment.")

    @property
    def topright(self):
        """
        The top right corner of the rectangle

        Note:
            This can only be accessed and set after the Rectangle has been
            added to a Sprite.
        """
        if self.sprite:
            return self.pos - Vector(self.width / -2, self.height / 2)
        else:
            raise Error("Tried to get rect property before sprite assignment.")

    @topright.setter
    def topright(self, new: Vector):
        if self.sprite:
            self.sprite.pos = new + Vector(self.width / -2, self.height / 2)
            self.sprite.pos = self.sprite.pos.to_int()
        else:
            raise Error("Tried to set rect property before sprite assignment.")

    @property
    def bottomright(self):
        """
        The bottom right corner of the rectangle

        Note:
            This can only be accessed and set after the Rectangle has been
            added to a Sprite.
        """
        if self.sprite:
            return self.pos - Vector(self.width / -2, self.height / -2)
        else:
            raise Error("Tried to get rect property before sprite assignment.")

    @bottomright.setter
    def bottomright(self, new: Vector):
        if self.sprite:
            self.sprite.pos = new + Vector(self.width / -2, self.height / -2)
            self.sprite.pos = self.sprite.pos.to_int()
        else:
            raise Error("Tried to set rect property before sprite assignment.")

    def vertices(self):
        return [
            Vector(-self.width / 2, -self.height / 2),
            Vector(self.width / 2, -self.height / 2),
            Vector(self.width / 2, self.height / 2),
            Vector(-self.width / 2, self.height / 2)
        ]

    def transformed_verts(self) -> List[Vector]:
        return [v.transform(self.scale, self.rotation) for v in self.vertices()]

    def real_verts(self) -> List[Vector]:
        return [self.pos + v for v in self.vertices()]

    def draw(self):
        x_1, y_1 = Game.scenes.current.camera.transform(self.topright).tuple_int()
        x_2, y_2 = Game.scenes.current.camera.transform(self.bottomleft).tuple_int()
        if self.color is not None:
            sdl2.sdlgfx.boxRGBA(
                Display.renderer.sdlrenderer,
                x_1,
                y_1,
                x_2,
                y_2,
                self.color.r,
                self.color.g,
                self.color.b,
                self.color.a,
            )
        if self.debug:
            sdl2.sdlgfx.rectangleRGBA(
                Display.renderer.sdlrenderer,
                x_1,
                y_1,
                x_2,
                y_2,
                0,
                255,
                0,
                255,
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
        super().__init__(options)
        params = Defaults.circle_defaults | options
        self.radius = params["radius"]

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
        if self.color is not None:
            relative_pos = Game.scenes.current.camera.transform(self.pos)
            scaled_rad = Game.scenes.current.camera.scale(self.radius)
            sdl2.sdlgfx.filledCircleRGBA(
                Display.renderer.sdlrenderer,
                int(relative_pos.x),
                int(relative_pos.y),
                int(scaled_rad),
                self.color.r,
                self.color.g,
                self.color.b,
                self.color.a,
            )
            sdl2.sdlgfx.aacircleRGBA(
                Display.renderer.sdlrenderer,
                int(relative_pos.x),
                int(relative_pos.y),
                int(scaled_rad),
                self.color.r,
                self.color.g,
                self.color.b,
                self.color.a,
            )

        if self.debug:
            sdl2.sdlgfx.aacircleRGBA(
                Display.renderer.sdlrenderer,
                int(relative_pos.x),
                int(relative_pos.y),
                int(scaled_rad),
                0,
                255,
                0,
                255,
            )


class ColInfo:
    """
    A class that represents information returned in a successful collision

    Attributes:
        shape_a (Union[Circle, Polygon, None]): A reference to the first shape.
        shape_b (Union[Circle, Polygon, None]): A reference to the second shape.
        seperation (Vector): The vector that would separate the two colliders.
    """

    def __init__(self, shape_a: Union[Hitbox, None], shape_b: Union[Hitbox, None], sep: Vector = Vector()):
        """
        Initializes a Collision Info manifold
        """
        self.shape_a = shape_a
        self.shape_b = shape_b
        self.sep = sep

    @staticmethod
    def flip(info: "ColInfo") -> Union["ColInfo", None]:
        """Flips which object a manifold is referencing to"""
        if info is None:
            return None
        return ColInfo(info.shape_b, info.shape_a, info.sep * -1)


class SAT:
    """
    A general class that does the collision detection math between
    circles and polygons
    """

    @staticmethod
    def overlap(shape_a: Hitbox, shape_b: Hitbox) -> Union[ColInfo, None]:
        """
        Checks for overlap between any two shapes (Polygon or Circle)

        Args:
            shape_a: The first shape.
            shape_b: The second shape.

        Returns:
            Union[ColInfo, None]: If a collision occurs, a ColInfo
            is returned. Otherwise None is returned.
        """

        if isinstance(shape_a, Circle):
            if isinstance(shape_b, Circle):
                return SAT.circle_circle_test(shape_a, shape_b)

            return SAT.circle_polygon_test(shape_a, shape_b)

        if isinstance(shape_b, Circle):
            return ColInfo.flip(SAT.circle_polygon_test(shape_b, shape_a))

        return SAT.polygon_polygon_test(shape_a, shape_b)

    @staticmethod
    def circle_circle_test(circle_a: Circle, circle_b: Circle) -> Union[ColInfo, None]:
        """Checks for overlap between two circles"""
        total_radius = circle_a.radius + circle_b.radius
        distance = (circle_b.pos - circle_a.pos).magnitude

        if distance > total_radius:
            return None

        return ColInfo(circle_a, circle_b, (circle_a.pos - circle_b.pos).unit() * (total_radius - distance))

    @staticmethod
    def circle_polygon_test(circle: Circle, polygon: Polygon) -> Union[ColInfo, None]:
        """Checks for overlap between a circle and a polygon"""

        result = ColInfo(circle, polygon)

        shortest = Math.INFINITY

        verts = polygon.transformed_verts()
        offset = polygon.pos - circle.pos

        closest = Vector()
        for v in verts:
            dist = (circle.pos - polygon.pos - v).magnitude
            if dist < shortest:
                shortest = dist
                closest = polygon.pos + v

        axis = closest - circle.pos
        axis.magnitude = 1

        poly_range = SAT.project_verts(verts, axis) + axis.dot(offset)
        circle_range = Vector(-circle.transformed_radius(), circle.transformed_radius())

        if poly_range.x > circle_range.y or circle_range.x > poly_range.y:
            return None

        dist_min = poly_range.x - circle_range.y

        shortest = abs(dist_min)
        result.sep = axis * dist_min

        for i in range(len(verts)):
            axis = SAT.perpendicular_axis(verts, i)

            poly_range = SAT.project_verts(verts, axis) + axis.dot(offset)

            if poly_range.x > circle_range.y or circle_range.x > poly_range.y:
                return None

            dist_min = poly_range.x - circle_range.y

            if abs(dist_min) < shortest:
                shortest = abs(dist_min)
                result.sep = axis * dist_min

        return result

    @staticmethod
    def polygon_polygon_test(shape_a: Polygon, shape_b: Polygon) -> Union[ColInfo, None]:
        """Checks for overlap between two polygons"""
        test_a_b = SAT.poly_poly_helper(shape_a, shape_b)
        if test_a_b is None:
            return None

        test_b_a = ColInfo.flip(SAT.poly_poly_helper(shape_b, shape_a))
        if test_b_a is None:
            return None

        return test_a_b if test_a_b.sep.mag < test_b_a.sep.mag else test_b_a

    @staticmethod
    def poly_poly_helper(poly_a: Polygon, poly_b: Polygon) -> Union[ColInfo, None]:
        result = ColInfo(poly_a, poly_b)

        shortest = Math.INFINITY

        verts_a = poly_a.transformed_verts()
        verts_b = poly_b.transformed_verts()

        offset = poly_a.pos - poly_b.pos

        for i in range(len(verts_a)):
            axis = SAT.perpendicular_axis(verts_a, i)

            a_range = SAT.project_verts(verts_a, axis) + axis.dot(offset)
            b_range = SAT.project_verts(verts_b, axis)

            if a_range.x > b_range.y or b_range.x > a_range.y:
                return None

            min_dist = b_range.x - a_range.y

            if abs(min_dist) < shortest:
                shortest = abs(min_dist)
                result.sep = axis * min_dist

        return result

    @staticmethod
    def perpendicular_axis(verts: List[Vector], index: int) -> Vector:
        """Finds a vector perpendicular to a side"""

        pt_1, pt_2 = verts[index], verts[(index + 1) % len(verts)]
        axis = Vector(pt_1.y - pt_2.y, pt_2.x - pt_1.x)
        axis.magnitude = 1
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
