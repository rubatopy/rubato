"""
The Camera module handles where things are drawn.
A camera can zoom, pan, and travel along the z-index.
Items only render if their z-index is not more than that of the camera's.

The current scene's camera can be accessed through :code:`Game.camera`.
"""
from .. import Vector, Display, Math, Radio


class Camera:
    """
    The camera class.

    Attributes:
        pos (Vector): The current position of the camera.
        z_index (int): The current z_index of the camera.
    """

    def __init__(self, pos: Vector = Vector(), zoom: float = 1, z_index: int = 100):
        """Initializes a camera."""
        self.pos = pos
        self._zoom = zoom
        self.z_index = z_index

    @property
    def zoom(self) -> float:
        """The zoom value of the camera."""
        return self._zoom

    @zoom.setter
    def zoom(self, new: float):
        self._zoom = Math.clamp(new, 0.01, Math.INF)
        Radio.broadcast("ZOOM")

    def transform(self, point: Vector) -> Vector:
        """
        Transforms resolution space coordinates according to camera attributes.

        Args:
            point (Vector): The point to transform.

        Returns:
            Vector: The translated coordinates.
        """
        center = Vector(*Display.renderer.logical_size) / 2
        return (point - self.pos - center) * self.zoom + center

    def scale(self, dimension):
        """
        Scales a given dimension by the camera zoom.

        Args:
            dimension (Any): The dimension to scale. Can be a scalar or a Vector.

        Returns:
            Any: The scaled dimension.
        """
        return dimension * self.zoom
