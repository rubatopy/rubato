from pygame import Surface


class GD:
    """Global display class that allows any file to access the displayed screen."""
    global_display = Surface((0, 0))

    @staticmethod
    def set(new_surface: Surface):
        """
        Set the global display.

        :param new_surface: The new surface to set.
        """
        GD.global_display = new_surface

    @staticmethod
    def display() -> Surface:
        return GD.global_display

    @staticmethod
    def update(surface: Surface, pos: (int, int)):
        GD.global_display.blit(surface, pos)