Getting Started
===============

Rubato is designed so that you can get started quickly and focus on what matters.

Installation
------------
Installing Rubato is easy! Just run:

.. code-block:: console

    (.venv) $ pip install rubato

.. note::
    | A virtual environment is recommended
    | Python >= 3.10 required

Usage
-----
To get started, import rubato and initilize it.

.. code-block:: python

    import rubato as rb

    rb.init()

| Rubato is uses a sprite based system. This means that everything you see on screen is a :ref:`sprite <sprite>`.

.. code-block:: python

    sprite = Sprite(options)

Example Project
---------------
