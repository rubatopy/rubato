#############
Event Details
#############

Events can be broadcast with :func:`rb.Radio.broadcast() <rubato.utils.radio.Radio.broadcast>`:

>>> rb.Radio.broadcast("EVENT_NAME", {data})

rubato broadcasts some events already, but you can also define your own events using this function!

These events can also be listened to with :func:`rb.Radio.listen() <rubato.utils.radio.Radio.listen>`. Here is an example
of how you can listen for a key down event:

.. code-block:: python

    def listener(data):
        if data["key"] == "a":
            print("You pressed the 'a' key!")

    rb.Radio.listen("KEYDOWN", listener)

Below is a list of all the events that are broadcast by rubato:

**********
Key Events
**********

There are 3 key events that are broadcast.

.. code-block:: python

    "KEYUP" # Fired when a key is released
    "KEYDOWN" # Fired when a key is pressed
    "KEYHOLD" # Fired when a key is held down (After the initial keydown)

Each event gives a dictionary with the following information:

.. code-block:: python

    {
        "key": str, # The name of the key (see Input Details for the list of key names)
        "unicode": str, # The unicode character for the key (keys without unicode are just empty strings)
        "code": int, # The keycode of the the key. (can be processed with Input.get_name)
        "mods": int, # The code for the currently pressed modifiers. (can be processed with Input.mods_from_code)
    }

**********
Mouse Events
**********

There are 2 key events that are broadcast.

.. code-block:: python

    MOUSEUP = "MOUSEUP"  # Fired when a mouse button is released
    MOUSEDOWN = "MOUSEDOWN"  # Fired when a mouse button is pressed

Each event gives a dictionary with the following information:

.. code-block:: python

    {
        "mouse_button": str,
        "x": event.button.x,
        "y": event.button.y,
        "clicks": event.button.clicks,
        "which": event.button.which,
        "windowID": event.button.windowID,
        "timestamp": event.button.timestamp,
    }

*************
Window Events
*************

There is 1 window event that is broadcast.

.. code-block:: python

    "RESIZE" # Fired when the window is resized

Each event gives a dictionary with the following information:

.. code-block:: python

    { # All values are referencing the window
        "width": int,
        "height": int,
        "old_width": int,
        "old_height": int
    }

*************
Camera Events
*************

There is 1 camera event that is broadcast.

.. code-block:: python

    "ZOOM" # Fired when the camera zoom changes

No additional information is given.


*************
System Events
*************

There is 1 system event that is broadcast

.. code-block:: python

    "EXIT" # Fires right before the program exit

No additional information is given.
