Event Details
=============

Key Events
----------

There are 3 key events that are broadcast.

.. code-block:: python

    "keyup" # Fired when a key is released
    "keydown" # Fired when a key is pressed
    "keyhold" # Fired when a key is held down (After the initial keydown)

Each event gives a dictionary with the following information:

.. code-block:: python

    {
        "key": str, # The name of the key (see Input Details for the list of key names)
        "unicode": str, # The unicode character for the key (keys without unicode are just empty strings)
        "code": int, # The keycode of the the key. (can be processed with Input.get_name)
        "mods": int, # The code for the currently pressed modifiers. (can be processed with Input.mods_from_code)
    }

Window Events
-------------

There is 1 window event that is broadcast.

.. code-block:: python

    "resize"

Each event gives a dictionary with the following information:

.. code-block:: python

    { # All values are referencing the window
        "width": int,
        "height": int,
        "old_width": int,
        "old_height": int
    }
