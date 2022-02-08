# For Developers

### To publish new version

Bump version number in `setup.py`, `docs/source/conf.py`, and in `docs/index.html` <br>
Update Changelog <br>
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

Create and release a version on Github
