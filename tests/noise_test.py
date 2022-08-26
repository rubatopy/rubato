"""Test the noise class"""
import pytest
from rubato.utils.error import InitError
from rubato.utils.noise import Noise


def test_init():
    with pytest.raises(InitError):
        Noise()


@pytest.mark.parametrize(
    "seed, x, expected",
    [
        (0, 0, 0),
        (0, 1, 0.7226187470054966),
        (0, 12345, -0.47312689033321),
        (12345, 1, -0.9030358638784208),
        (12345, 12345, -0.8942219408493851),
    ],
)
def test_noise(seed, x, expected):
    Noise.seed = seed
    assert Noise.noise(x) == expected


@pytest.mark.parametrize(
    "seed, coord, expected",
    [
        (0, (0, 0), 0),
        (0, (1, 1), -0.1286218649348236),
        (0, (12345, 12345), -0.09550433499249332),
        (0, (-94.5, -22.3), 0.17656546228946673),
        (0, (-94.5, -22.2), 0.583482328276395),
        (12345, (1, 1), -0.5461943760920378),
        (12345, (12345, 12345), -0.28019200309000275),
    ],
)
def test_noise2(seed, coord, expected):
    Noise.seed = seed
    assert Noise.noise2(*coord) == expected
