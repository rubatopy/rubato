# """
# A simple button. A button is a text sprite that has mouse over detection.
# """
# from rubato.classes.components import Text
# from rubato.utils import Vector, Configs
# import rubato.input as Input

# class Button(Text):
#     """
#     The button class. It inherits from the text class.
#     """

#     def __init__(self, options={}):
#         """
#         Initializes a button.

#         Args:
#             options: A button config. Defaults to the
#                 |default| for `Button`.
#         """
#         param = Configs.button_defaults | options
#         super().__init__(param)

#     def mouse_is_over(self) -> bool:
#         """
#         Checks if the mouse is above the button.

#         Returns:
#             bool: True if the mouse is over the button. False otherwise.
#         """
#         return Input.mouse_over(
#             self.pos, Vector(self.image.get_width(), self.image.get_height()))
