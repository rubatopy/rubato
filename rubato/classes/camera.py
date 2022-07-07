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
        pos: The position of the camera.
        zoom: The zoom of the camera.
        z_index: The z-index of the camera.

    Attributes:
        z_index (int): The current z_index of the camera.
    """

    def __init__(self, pos: Vector = Vector(), zoom: float = 1, z_index: int = 100):
        self._pos = pos
        self._zoom = zoom
        self.z_index = z_index

    @property
    def pos(self):
        """
        The current position of the camera. Center based ie. where the camera is looking at.
        Notes:
            Cannot access pos.x or pos.y directly.
        """
        return self._pos + Display.center

    @pos.setter
    def pos(self, pos: Vector):
        self._pos = pos - Display.center

    @property
    def zoom(self) -> float:
        """The zoom value of the camera."""
        return self._zoom

    @zoom.setter
    def zoom(self, new: float):
        self._zoom = Math.clamp(new, 0.01, Math.INF)
        Radio.broadcast(Events.ZOOM, {"camera": self})

    def translate(self, offset: Vector) -> None:
        """
        Translates the camera by the given offset
        Args:
            offset: The offset to translate the camera by.
        """
        self._pos += offset

    def set(self, pos: Vector) -> None:
        """
        sets the camera position to the position given.
        Args:
            pos: The new position of the camera.
        """
        self._pos = pos

    def transform(self, point: Vector) -> Vector:
        """
        Transforms resolution space coordinates according to camera attributes.

        Args:
            point (Vector): The point to transform.

        Returns:
            Vector: The translated coordinates.
        """
        center = Vector(*Display.renderer.logical_size) / 2
        return (point - self._pos - center) * self.zoom + center

    def scale(self, dimension):
        """
        Scales a given dimension by the camera zoom.

        Args:
            dimension (Any): The dimension to scale. Can be a scalar or a Vector.

        Returns:
            Any: The scaled dimension.
        """
        return dimension * self.zoom
