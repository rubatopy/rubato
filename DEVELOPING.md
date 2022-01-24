# For Developers

### To update docs

```
$ make save ver=<version.number>
```

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
