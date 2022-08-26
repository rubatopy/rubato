"""
The Camera module handles where things are drawn.
A camera can zoom, pan, and travel along the z-index.
GameObjects only render if their z-index is not more than that of the camera's.

The current scene's camera can be accessed through :code:`Game.camera`.
"""
from . import Vector, Display, Math, Radio, Events


class Camera:
    """
    An abstraction describing how a scene is viewed.

    Args:
        pos: The position of the camera. Defaults to center of Display.
        zoom: The zoom of the camera.
        z_index: The z-index of the camera.
    """

    def __init__(self, pos: Vector | tuple[float, float] | None = None, zoom: float = 1, z_index: int = Math.INF):
        self.pos: Vector = Vector.create(pos) if pos else Display.center
        """The current position of the camera. Center based i.e. where the camera is looking at."""
        self._zoom = zoom
        self.z_index: int = z_index
        """The current z_index of the camera."""

    @property
    def zoom(self) -> float:
        """The zoom value of the camera."""
        return self._zoom

    @zoom.setter
    def zoom(self, new: float):
        self._zoom = Math.clamp(new, 0.01, Math.INF)
        Radio.broadcast(Events.ZOOM, {"camera": self})

    def transform(self, point: Vector | tuple[float, float]) -> Vector:
        """
        World space coordinates to Screen space coordinates.

        Args:
            point: The point to transform (world space).

        Returns:
            The translated coordinates.
        """
        return Vector(
            (point[0] - self.pos.x) * self.zoom + Display.center.x,
            (point[1] - self.pos.y) * self.zoom + Display.center.y
        )

    def i_transform(self, point: Vector | tuple[float, float]) -> Vector:
        """
        Inverts the transform process, screen space coordinates to world space coordinates.

        Args:
            point: The point to transform (screen space).

        Returns:
            The translated coordinates.
        """
        return Vector(
            (point[0] - Display.center.x) / self.zoom + self.pos.x,
            (point[1] - Display.center.y) / self.zoom + self.pos.y
        )
