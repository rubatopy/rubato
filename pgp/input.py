from pygame import key, mouse


class Input:
    """
    An abstraction of the PyGame input system. Slightly optimized and plays nice with the rest of pgp.
    """
    key = key
    mouse = mouse

    @staticmethod
    def is_pressed(char: str):
        return Input.key.get_pressed()[Input.key.key_code(char)]