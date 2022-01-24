Default Options
===============

.. _defaultgame:

Game
---------
.. code-block:: python

    default_options = {
        "name": "Untitled Game",    # string
        "window_width": 600,        # int
        "window_height": 400,       # int
        "aspect_ratio": 1.5,        # float
        "fps": 60,                  # int
        "reset_display": True,      # bool
        "better_clock": True,       # bool
    }

.. _defaultsprite:

Sprite
---------
.. code-block:: python

    default_options = {
        "pos": Vector(),    # Vector
        "z_index": 0        # int
    }

.. _defaultrigidbody:

RigidBody
---------
.. code-block:: python

    default_options = {
        "pos": Vector(),                                        # Vector
        "mass": 1,                                              # float
        "hitbox": Polygon.generate_polygon(4),                  # Polygon
        "do_physics": True,                                     # bool
        "gravity": 100,                                         # float
        "max_speed": Vector(PMath.INFINITY, PMath.INFINITY),    # Vector
        "min_speed": Vector(-PMath.INFINITY, -PMath.INFINITY),  # Vector
        "friction": Vector(1, 1),                               # Vector
        "img": "default",                                       # string
        "col_type": COL_TYPE.STATIC,                            # COL_TYPE
        "scale": Vector(1, 1),                                  # Vector
        "debug": False,                                         # bool
        "z_index": 0,                                           # int
        "rotation": 0,                                          # float
    }

.. _defaultrectangle:

Rectangle
---------
.. code-block:: python

    default_options = {
        "pos": Vector(),        # Vector
        "dims": Vector(),       # Vector
        "color": Color.black,   # Color
        "z_index": 0            # int
    }


.. _defaultbutton:

Button
---------
.. code-block:: python

    default_options = {
        "text": "default_text", # string
        "pos": Vector(),        # Vector
        "size": 16,             # int
        "z_index": 0,           # int
        "font_name": 'Arial',   # string
        "color": Color.red      # Color
    }

.. _defaulttext:

Text
---------
.. code-block:: python

    default_options = {
        "text": "default_text", # string
        "pos": Vector(),        # Vector
        "size": 16,             # int
        "z_index": 0,           # int
        "font_name": 'Arial',   # string
        "color": Color.black,   # Color
        "static": False,        # bool
        "onto_surface": None,   # Pygame Surface
    }

.. _defaultimage:

Image
---------
.. code-block:: python

    default_options = {
        "image_location": "default",    # string
        "pos": Vector(),                # Vector
        "scale_factor": Vector(1, 1),   # Vector
        "z_index": 0,                   # int
        "rotation": 0                   # float
    }


.. _defaultcamera:

Camera
---------
.. code-block:: python



