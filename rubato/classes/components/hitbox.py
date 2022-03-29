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

    Attributes:
        debug (bool): Whether to draw a green outline around the Polygon or not.
        trigger (bool): Whether this hitbox is just a trigger or not.
        scale (int): The scale of the polygon
        on_collide (Callable): The on_collide function to call when a collision happens with this hitbox.
        color (Color) The color to fill this hitbox with.
        tag (str): The tag of the hitbox (can be used to identify hitboxes)
    """
    hitboxes: List["Hitbox"] = []

    def __init__(self, options: dict = {}):
        """
        Initializes a Hitbox.

        Args:
            options: A Hitbox config. Defaults to the |default| for
                `Hitbox`.
        """
        params = Defaults.hitbox_defaults | options
        super().__init__()
        self.debug: bool = params["debug"]
        self.trigger: bool = params["trigger"]
        self._pos = lambda: Vector(0, 0)
        self.scale: int = params["scale"]
        self.on_collide: Callable = params["on_collide"]
        self.color: Color = params["color"]
        self.singular: bool = False
        self.tag: str = params["tag"]
        self.offset: Vector = params["offset"]

    @property
    def pos(self) -> Vector:
        """The getter method for the position of the hitbox's center"""
        return self._pos() + self.offset

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
        if (col := SAT.overlap(self, other)) is None:
            return

        if not (self.trigger or other.trigger):
            RigidBody.handle_collision(col)

        self.on_collide(col)
        other.on_collide(col.flip())


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
        Initializes a Polygon.

        Args:
            options: A Polygon config. Defaults to the |default| for
                `Polygon`.
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
        new_poly = Polygon(
            {
                "verts": [v.clone() for v in self.verts],
                "rotation": self.rotation,
                "debug": self.debug,
                "trigger": self.trigger,
                "scale": self.scale,
                "on_collide": self.on_collide,
            }
        )
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
        list_of_points: List[tuple] = [Game.camera.transform(v).tuple_int() for v in self.real_verts()]

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

        if self.debug or Game.debug:
            for i in range(len(list_of_points)):
                sdl2.sdlgfx.thickLineRGBA(
                    Display.renderer.sdlrenderer, list_of_points[i][0], list_of_points[i][1],
                    list_of_points[(i + 1) % len(list_of_points)][0], list_of_points[(i + 1) % len(list_of_points)][1],
                    int(2 * Display.display_ratio.x), 0, 255, 0, 255
                )


class Rectangle(Hitbox):
    """
    A rectangle class

    Warning:
        Needs documentation
    """

    def __init__(self, options: dict):
        """
        Initializes a Rectangle.

        Args:
            options: A Rectangle config. Defaults to the |default| for
                `Rectangle`.
        """
        super().__init__(options)
        params = Defaults.rectangle_defaults | options

        self.width: int = int(params["width"])
        self.height: int = int(params["height"])

        self.rotation: float = params["rotation"]

    @property
    def top_left(self):
        """
        The top left corner of the rectangle

        Note:
            This can only be accessed and set after the Rectangle has been
            added to a Game Object.
        """
        if self.gameobj:
            return self.pos - Vector(self.width / 2, self.height / 2)
        else:
            raise Error("Tried to get rect property before game object assignment.")

    @top_left.setter
    def top_left(self, new: Vector):
        if self.gameobj:
            self.gameobj.pos = new + Vector(self.width / 2, self.height / 2)
            self.gameobj.pos = self.gameobj.pos.to_int()
        else:
            raise Error("Tried to set rect property before game object assignment.")

    @property
    def bottom_left(self):
        """
        The bottom left corner of the rectangle

        Note:
            This can only be accessed and set after the Rectangle has been
            added to a Game Object.
        """
        if self.gameobj:
            return self.pos - Vector(self.width / 2, self.height / -2)
        else:
            raise Error("Tried to get rect property before game object assignment.")

    @bottom_left.setter
    def bottom_left(self, new: Vector):
        if self.gameobj:
            self.gameobj.pos = new + Vector(self.width / 2, self.height / -2)
            self.gameobj.pos = self.gameobj.pos.to_int()
        else:
            raise Error("Tried to set rect property before game object assignment.")

    @property
    def top_right(self):
        """
        The top right corner of the rectangle

        Note:
            This can only be accessed and set after the Rectangle has been
            added to a Game Object.
        """
        if self.gameobj:
            return self.pos - Vector(self.width / -2, self.height / 2)
        else:
            raise Error("Tried to get rect property before game object assignment.")

    @top_right.setter
    def top_right(self, new: Vector):
        if self.gameobj:
            self.gameobj.pos = new + Vector(self.width / -2, self.height / 2)
            self.gameobj.pos = self.gameobj.pos.to_int()
        else:
            raise Error("Tried to set rect property before game object assignment.")

    @property
    def bottom_right(self):
        """
        The bottom right corner of the rectangle

        Note:
            This can only be accessed and set after the Rectangle has been
            added to a Game Object.
        """
        if self.gameobj:
            return self.pos - Vector(self.width / -2, self.height / -2)
        else:
            raise Error("Tried to get rect property before game object assignment.")

    @bottom_right.setter
    def bottom_right(self, new: Vector):
        if self.gameobj:
            self.gameobj.pos = new + Vector(self.width / -2, self.height / -2)
            self.gameobj.pos = self.gameobj.pos.to_int()
        else:
            raise Error("Tried to set rect property before game object assignment.")

    @property
    def bottom(self):
        """
        The bottom side of the rectangle

        Note:
            This can only be accessed and set after the Rectangle has been
            added to a Game Object.
        """
        if self.gameobj:
            return self.pos.y - self.height / -2
        else:
            raise Error("Tried to get rect property before game object assignment.")

    @bottom.setter
    def bottom(self, new: float):
        if self.gameobj:
            self.gameobj.pos.y += new + self.height / -2
            self.gameobj.pos = self.gameobj.pos.to_int()
        else:
            raise Error("Tried to set rect property before game object assignment.")

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
        x_1, y_1 = Game.camera.transform(self.top_right).tuple_int()
        x_2, y_2 = Game.camera.transform(self.bottom_left).tuple_int()
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
        if self.debug or Game.debug:
            verts = [(x_1, y_1), (x_1, y_2), (x_2, y_2), (x_2, y_1)]
            for i in range(len(verts)):
                sdl2.sdlgfx.thickLineRGBA(
                    Display.renderer.sdlrenderer, verts[i][0], verts[i][1], verts[(i + 1) % len(verts)][0],
                    verts[(i + 1) % len(verts)][1], int(2 * Display.display_ratio.x), 0, 255, 0, 255
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
        Initializes a Circle.

        Args:
            options: A Circle config. Defaults to the |default| for
                `Circle`.
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
            relative_pos = Game.camera.transform(self.pos)
            scaled_rad = Game.camera.scale(self.radius)
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

        if self.debug or Game.debug:
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

    def flip(self) -> "ColInfo":
        """Flips the reference shape in a collision manifold

        Returns:
            ColInfo: a reference to self.
        """
        self.shape_a, self.shape_b = self.shape_b, self.shape_a
        self.sep *= -1
        return self


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
            r = SAT.circle_polygon_test(shape_b, shape_a)
            return None if r is None else r.flip()

        return SAT.polygon_polygon_test(shape_a, shape_b)

    @staticmethod
    def circle_circle_test(circle_a: Circle, circle_b: Circle) -> Union[ColInfo, None]:
        """Checks for overlap between two circles"""
        t_rad = circle_a.radius + circle_b.radius
        d_x, d_y = circle_a.pos.x - circle_b.pos.x, circle_a.pos.y - circle_b.pos.y
        dist = (d_x * d_x + d_y * d_y)**.5

        if dist > t_rad:
            return None

        return ColInfo(circle_a, circle_b, Vector((t_rad - dist) * d_x / dist, (t_rad - dist) * d_y / dist))

    @staticmethod
    def circle_polygon_test(circle: Circle, polygon: Polygon) -> Union[ColInfo, None]:
        """Checks for overlap between a circle and a polygon"""

        result = ColInfo(circle, polygon)

        shortest = Math.INF

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

        test_b_a = SAT.poly_poly_helper(shape_b, shape_a)
        if test_b_a is None:
            return None

        return test_a_b if test_a_b.sep.mag_squared < test_b_a.sep.mag_squared else test_b_a.flip()

    @staticmethod
    def poly_poly_helper(poly_a: Polygon, poly_b: Polygon) -> Union[ColInfo, None]:
        result = ColInfo(poly_a, poly_b)

        shortest = Math.INF

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

        minval, maxval = Math.INF, -Math.INF

        for v in verts:
            temp = axis.dot(v)
            minval, maxval = min(minval, temp), max(maxval, temp)

        return Vector(minval, maxval)
