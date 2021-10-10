from pygame.transform import scale
from pgp.utils import Vector, GD


class Camera:
    """
    Cameras handle general visual transformations on all sprites drawn in the current scene.

    :param pos: The coordinates of the Camera
    :param zoom: The initial zoom of the Camera as a number
    """
    def __init__(self, pos: Vector = Vector(), zoom: int = 100):

        self.pos = pos
        self.zoom = zoom

    def transform(self, point: Point) -> Point:
        """
        Translates a given set of coordinates by the camera's.

        :param point: The point to be transformed
        :return: A new offset point in the form of a 2D tuple
        """
        return point.offset2(self.pos).to_tuple2()

    def set_zoom(self, new_zoom: float):
        """
        Sets the zoom of the camera.

        :param new_zoom: The new zoom as a number
        """
        self.zoom = new_zoom
        self.process_zoom()

    def scale_zoom(self, zoom_factor: float):
        """
        Scales the zoom by the zoom factor.

        :param zoom_factor: The number to scale the zoom by
        """
        self.zoom *= zoom_factor
        self.process_zoom()

    def process_zoom(self):
        """Process changes to the camera's zoom"""
        window_width, window_height = GD.display().get_size()
        new_size = (round(window_width / (self.zoom / 100)), round(window_height / (self.zoom/100)))
        GD.set(scale(GD.display(), new_size))