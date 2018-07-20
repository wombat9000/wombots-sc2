from unittest.mock import Mock

import pytest
from sc2.unit import Unit
from sc2.units import Units

from .context import ZergBot, UnitTypeId


async def async_mock(val):
    return val


def unit_mock_of(type_id: UnitTypeId):
    unit: Unit = Mock()
    unit.is_mine = Mock(return_value=True)
    unit.type_id = type_id
    return unit


@pytest.fixture
def zerg_bot():
    bot = ZergBot()
    bot.do = Mock()
    bot.state = Mock()
    return bot


def test_selects_only_larvae(zerg_bot: ZergBot):
    larva: Unit = unit_mock_of(UnitTypeId.LARVA)
    overlord = unit_mock_of(UnitTypeId.OVERLORD)

    zerg_bot.units = Units([larva, overlord], Mock())

    larvae = zerg_bot.select_larvae()

    assert larva in larvae
    assert overlord not in larvae


@pytest.mark.asyncio
async def test_does_not_train_without_larvae(zerg_bot: ZergBot):
    zerg_bot.units = Units([], Mock())

    await zerg_bot.train_unit(UnitTypeId.OVERLORD)

    zerg_bot.do.assert_not_called()


@pytest.mark.asyncio
async def test_does_not_train_if_cant_afford(zerg_bot: ZergBot):
    larva: Unit = unit_mock_of(UnitTypeId.LARVA)
    zerg_bot.units = Units([larva], Mock())
    zerg_bot.can_afford = Mock(return_value=False)

    await zerg_bot.train_unit(UnitTypeId.OVERLORD)

    zerg_bot.do.assert_not_called()


@pytest.mark.asyncio
async def test_does_not_train_if_insufficient_supply(zerg_bot: ZergBot):
    larva: Unit = unit_mock_of(UnitTypeId.LARVA)
    zerg_bot.units = Units([larva], Mock())
    zerg_bot.can_afford = Mock(return_value=True)
    zerg_bot.supply_left = 0

    await zerg_bot.train_unit(UnitTypeId.DRONE, 1)

    zerg_bot.do.assert_not_called()


@pytest.mark.asyncio
async def test_trains_if_sufficient_supply_and_funds(zerg_bot: ZergBot):
    larva: Unit = unit_mock_of(UnitTypeId.LARVA)
    zerg_bot.units = Units([larva], Mock())
    zerg_bot.can_afford = Mock(return_value=True)
    zerg_bot.supply_left = 1
    zerg_bot.do = Mock(return_value=async_mock(None))

    await zerg_bot.train_unit(UnitTypeId.DRONE, 1)

    zerg_bot.do.assert_called_with(larva.train(UnitTypeId.DRONE))
