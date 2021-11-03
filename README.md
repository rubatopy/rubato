# rubato

Rubato is a Python game engine that builds off of PyGame to make a cleaner and more efficient game engine. We aim to make game development in Python much easier than it currently is. Even though we use PyGame in the backend, when using Rubato, you do not need to ever touch PyGame. <b> This library is still in it's very alpha stages and will be buggy.</b> Documentation will be coming soon.

### Install Rubato:

```
pip install rubato
```

### Current Features:

- Rigidbody physics and collisions
- Sprite loading, grouping, and rendering
- Efficent game creation

## For Developers

### To publish to PyPi

Bump version number in setup.py<br>
Create a new virtual environment.

```
pip install -r requirements.txt
pip install wheel
python setup.py sdist bdist_wheel
pip install -e .
```

Here it should successfully install.<br>

```
pip install twine
python -m twine upload dist/*
```
