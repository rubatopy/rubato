from rubato.sprite import Text
from rubato.utils import Vector, Color
from rubato.scenes import Camera
import rubato.input as Input

class Button(Text):
    """
    A subclass of Text that is a button.

    :param options: A button :ref:`config <defaultbutton>`
    """

    default_options = {
        "text": "default_text",
        "pos": Vector(),
        "size": 16,
        "z_index": 0,
        "font_name": 'Arial',
        "color": Color.black
    }

    def __init__(self, options={}):
        super().__init__(options)

    def mouse_is_over(self) -> bool:
        return Input.mouse_over(self.pos, Vector(self.image.get_width(), self.image.get_height()))

    def draw(self, camera: Camera):
        """
        Draws the text if the z index is below the camera's.

        :param camera: The current Camera viewing the scene.
        """

        super().draw(camera)

