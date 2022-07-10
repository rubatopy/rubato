"""
The Camera module handles where things are drawn.
A camera can zoom, pan, and travel along the z-index.
Items only render if their z-index is not more than that of the camera's.

The current scene's camera can be accessed through :code:`Game.camera`.
"""
from .. import Vector, Display, Math, Radio, Events


class Camera:
    """
    The camera class.

    Args:
        pos: The position of the camera. Defaults to center of Display.
        zoom: The zoom of the camera.
        z_index: The z-index of the camera.

    Attributes:
        z_index (int): The current z_index of the camera.
        pos (Vector): The current position of the camera. Center based i.e. where the camera is looking at.
    """

    def __init__(self, pos: Vector = None, zoom: float = 1, z_index: int = Math.INF):
        self.pos = pos if pos else Display.center
        self._zoom = zoom
        self.z_index = z_index

    @property
    def zoom(self) -> float:
        """The zoom value of the camera."""
        return self._zoom

    @zoom.setter
    def zoom(self, new: float):
        self._zoom = Math.clamp(new, 0.01, Math.INF)
        Radio.broadcast(Events.ZOOM, {"camera": self})

    def transform(self, point: Vector) -> Vector:
        """
        World space coordinates to Screen space coordinates.

        Args:
            point (Vector): The point to transform (world space).

        Returns:
            Vector: The translated coordinates.
        """
        return (point - self.pos) * self.zoom + Display.center

    def i_transform(self, point: Vector) -> Vector:
        """
        Inverts the transform process, screen space coordinates to world space coordinates.

        Args:
            point (Vector): The point to transform (screen space).

        Returns:
            Vector: The translated coordinates.
        """
        return (self.pos - Display.center) / self.zoom + point

    def scale(self, dimension):
        """
        Scales a given dimension by the camera zoom.

        Args:
            dimension (Any): The dimension to scale. Can be a scalar or a Vector.

        Returns:
            Any: The scaled dimension.
        """
        return dimension * self.zoom
