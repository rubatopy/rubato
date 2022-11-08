"""Global Fixtures needed in multiple tests"""
import pytest

import rubato
from rubato.utils.computation.vector import Vector


@pytest.fixture()
def rub():
    """Initialize Rubato"""
    # pylint: disable=unused-argument
    rubato.init(
        window_size=Vector(200, 100),
        res=Vector(400, 200),
        hidden=True,
        window_pos=Vector(0, 0),
    )
    yield
    rubato.Game._initialized = False
    rubato.Radio.broadcast(rubato.Events.EXIT)
    rubato.Game.state = rubato.Game.STOPPED
