from pgp.utils import Point

class Camera:
    """
    Cameras handle general visual transformations on all sprites drawn in the current scene.

    :param pos: The coordinates of the Camera
    """
    # TODO Zoom
    def __init__(self, pos: Point = Point()):
        self.pos = pos

    def transform(self, point):
        """
        Translates a given set of coordinates by the camera's.

        :param point: The point to be transformed
        :return: A new offset point in the form of a 2D tuple
        """
        return point.offset2(self.pos).to_tuple2()
