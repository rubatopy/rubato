"""Helper functions for internal use only"""


class classproperty(property):  # pylint: disable=invalid-name
    """A static property"""
    pass


class StaticProperty(type):

    def __new__(mcs, name, bases, props):
        class_properties = {}
        for key, value in props.items():
            if isinstance(value, classproperty):
                class_properties[key] = value

        HoistMeta = type('HoistMeta', (type, ), class_properties)
        return HoistMeta(name, bases, props)
