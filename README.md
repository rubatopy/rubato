# rubato


### To publish to PyPi
Bump version number.<br>
Create a new virtual environment.
```
python setup.py sdist bdist_wheel
pip install -e .
```
Here it should successfully install.<br>
```
pip install twine
python -m twine upload --repository dist/*
```