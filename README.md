# <img src="https://github.com/rubatopy/rubato/blob/main/docs/source/_static/full.png?raw=true" alt="rubato" width="160"/>

[![Lisence](https://img.shields.io/github/license/rubatopy/rubato?style=flat-square)](https://www.gnu.org/licenses/gpl-3.0.html)
[![PyPI](https://img.shields.io/pypi/v/rubato?style=flat-square)](https://pypi.org/project/rubato/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/rubato?style=flat-square)](https://pypi.org/project/rubato/)
[![GitHub Release Date](https://img.shields.io/github/release-date/rubatopy/rubato?style=flat-square)](https://github.com/rubatopy/rubato/releases)
[![GitHub Build Status](https://img.shields.io/github/actions/workflow/status/rubatopy/rubato/tests.yml?branch=main&style=flat-square)](https://github.com/rubatopy/rubato/actions/workflows/tests.yml)
[![GitHub Docs Status](https://img.shields.io/github/actions/workflow/status/rubatopy/rubato/nightly.yml?branch=main&label=docs&style=flat-square)](https://rubatopy.github.io/)

[<img src="https://logodownload.org/wp-content/uploads/2017/11/discord-logo-4-1.png" alt="Discord Server" width="25" />](https://discord.gg/rdce5GXRrC)
&nbsp;
[<img src="https://cdn4.iconfinder.com/data/icons/social-media-icons-the-circle-set/48/twitter_circle-512.png" alt="Twitter Page" width="25"/>](https://twitter.com/rubatopy)
&nbsp;
[<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/LinkedIn_icon_circle.svg/2048px-LinkedIn_icon_circle.svg.png" alt="Linkedin Page" width="25"/>](https://www.linkedin.com/company/rubatopy/)
&nbsp;

<!-- If you update this README update the GitHub profile of rubatopy README -->

rubato is a modern 2D engine for game developement in python built in Cython using SDL2. With hardware acceleration, rigidbody support, easy tile map and animations and more, rubato finally gives you the fast development and performance you needed of your python games and prototypes. Moving past 1.0, we plan to maintain complete backwards compatibility with other post-1.0 versions.

_Wondering about the name? rubato is a music term that indicates a phrase that should be performed expressively and freely. We aim to harness that same freedom, bringing a fresh, modern take on game developement in python to a variety of users regardless of their coding background._
<br>

## Getting Started

Using rubato is super easy. First, install rubato through pip:

```bash
pip install rubato
```

After that, getting a screen up only takes 3 lines of code!

```python
import rubato as rb

# initialize rubato
rb.init()

# launch the window
rb.begin()
```

Next up, check out the rubato website for a [basic tutorial](https://docs.rubato.app/latest/tutorials/platformer/) to get you going.

#### Changelog

See [CHANGELOG.md](https://github.com/rubatopy/rubato/blob/main/CHANGELOG.md)

#### Looking to contribute to Rubato?

See [CONTRIBUTING.md](https://github.com/rubatopy/rubato/blob/main/CONTRIBUTING.md). And join our [discord](https://discord.gg/rdce5GXRrC)!

A big thank you to all of our [contributors](https://github.com/rubatopy/rubato/blob/main/CONTRIBUTORS.md) who help make this project possible.

#### Code of Conduct

See [CODE_OF_CONDUCT.md](https://github.com/rubatopy/rubato/blob/main/CODE_OF_CONDUCT.md).
