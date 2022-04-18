##########################
Bundling to an Application
##########################

Say you've just made an amazing game in Python and you want to share it with the world. You would need to share the
Python file, make sure you add all of your sprites and tell your users to install python and the needed dependencies. This
isn't very user friendly.

Instead with Rubato, you can bundle you game into a ``.exe`` or a ``.app`` file with everything bundled together, allowing for
easy sharing with others. This tutorial will walk you through the process of bundling your game.

First, make sure you have PyInstaller installed.

.. code-block:: bash

    pip install pyinstaller

Next, we need to get your resources ready. Resources are just non Python files that your project needs. For example, images or
data files that you use are resources. Since you will need to specifiy all these resources, it is recommended that you put them all
in a folder called ``resources`` next to your main python file. For example, your file structure could look like this::

    main.py
    resources/
        images/
            my_image.png
            my_other_image.png
            logo.ico
        data/
            my_data.json

With this file structure run the following command to bundle your game. Make sure that in your python code, you always use
relative paths.

.. tab-set::

    .. tab-item:: Windows

        .. code-block:: bash

            pyinstaller -F -w --add-data "resources;resources" main.py

    .. tab-item:: Mac OS X

        .. code-block:: bash

            pyinstaller -F -w --add-data "resources:resources" main.py

This will create 3 things. A ``.spec`` file, a ``dist`` folder and a ``build`` folder. Inside of the ``dist`` folder you will find
your app (either a ``.exe`` on Windows or a ``.app`` on Mac). You are now able to distribute this app to anyone you want!

.. note::

    In order to load all of your resources correctly, you must use relative paths. This means that if I wanted to access ``my_data.json``,
    I would use ``resources/data/my_data.json``. This simple change will work with all Rubato functions. If you are using a different library or
    built-in functions make sure to wrap your relative paths with the ``rb.get_path()`` function.

Here are a all the options you can add to the pyinstaller command (and we have made sure work):

``-F``

    Create an independant app file. Without this, all of your code will be copied into the dist folder and need to be sent to the end user.


``-w``

    Tells the app to run in a window. Without this, the app will run in a terminal.


``--add-data "src;dest"``

    Add data to the app. This is a way to add resources to the app. src is the path to the resource or folder and dest is where it will be
    accessible to Python (relative to the specified python file).

    .. note::

        On Unix systems (Mac and Linux) use a colon (``:``) instead of the semi-colon (``;``) to separate the src and dest.


``-i FILE``

    Sets the icon for the app. This is not the icon on the taskbar or on the window (that is set in the Python code). This is the icon of the
    app file itself. For Windows, this needs to be a ``.ico`` file. For Mac, this needs to be a ``.icns`` file.

****************
More Information
****************

For more information on bundling, see the following links:

* `PyInstaller Homepage <http://www.pyinstaller.org/>`__
* `PyInstaller Command Reference <https://pyinstaller.org/en/stable/usage.html>`__

