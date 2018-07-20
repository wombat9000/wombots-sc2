from unittest.mock import Mock

import pytest
from sc2.unit import Unit
from sc2.units import Units

from .context import ZergBot, UnitTypeId


def unit_mock_of(typeId):
    unit: Unit = Mock()
    unit.is_mine = Mock(return_value=True)
    unit.type_id = typeId
    return unit

@pytest.fixture
def zerg_bot():
    bot = ZergBot()
    bot.state = Mock()
    return bot


def test_selects_only_larvae(zerg_bot):
    larva: Unit = unit_mock_of(UnitTypeId.LARVA)
    overlord = unit_mock_of(UnitTypeId.OVERLORD)

    zerg_bot.units = Units([larva, overlord], Mock())

    larvae = zerg_bot.select_larvae()

    assert larva in larvae
    assert overlord not in larvae
