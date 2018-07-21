from typing import Deque
from unittest.mock import Mock

import pytest
from sc2.ids.unit_typeid import UnitTypeId
from sc2.unit import Unit
from sc2.units import Units

from .context import ZergBot
from .context import async_mock, unit_mock_of


def bot_with_bo(build_order) -> ZergBot:
    return ZergBot(Deque(build_order))


@pytest.mark.asyncio
async def test_does_nothing_on_empty_bo():
    bot = bot_with_bo([])
    await bot.on_step(0)

@pytest.mark.asyncio
async def test_build_first_unit_from_bo():
    bot = bot_with_bo([UnitTypeId.DRONE, UnitTypeId.OVERLORD])
    larva: Unit = unit_mock_of(UnitTypeId.LARVA)
    larva.train = Mock(return_value="returnVal")
    bot.units = Units([larva], Mock())
    bot.can_afford = Mock(return_value=True)
    bot.supply_left = 1
    bot.do = Mock(return_value=async_mock(None))

    await bot.on_step(0)

    larva.train.assert_called_once_with(UnitTypeId.DRONE)
    bot.do.assert_called_once_with(larva.train("any"))
    assert UnitTypeId.DRONE not in bot.build_order


@pytest.mark.asyncio
async def test_dont_build_unit_if_cant_afford():
    bot = bot_with_bo([UnitTypeId.DRONE, UnitTypeId.OVERLORD])
    larva: Unit = unit_mock_of(UnitTypeId.LARVA)
    larva.train = Mock(return_value="returnVal")
    bot.units = Units([larva], Mock())
    bot.can_afford = Mock(return_value=False)
    bot.supply_left = 1
    bot.do = Mock()

    await bot.on_step(0)

    larva.train.assert_not_called()
    bot.do.assert_not_called()
    assert UnitTypeId.DRONE in bot.build_order


@pytest.mark.asyncio
async def test_find_supply_for_first_unit_from_bo():
    bot = bot_with_bo([UnitTypeId.OVERLORD])
    larva: Unit = unit_mock_of(UnitTypeId.LARVA)
    larva.train = Mock(return_value="returnVal")
    bot.units = Units([larva], Mock())
    bot.can_afford = Mock(return_value=True)
    bot.supply_left = 0
    bot.do = Mock(return_value=async_mock(None))

    await bot.on_step(0)

    larva.train.assert_called_once_with(UnitTypeId.OVERLORD)
    bot.do.assert_called_once_with(larva.train("any"))
    assert UnitTypeId.OVERLORD not in bot.build_order


@pytest.mark.asyncio
async def test_build_structure_from_bo():
    drone: Unit = unit_mock_of(UnitTypeId.DRONE)
    hatch: Unit = unit_mock_of(UnitTypeId.HATCHERY)
    bot = bot_with_bo([UnitTypeId.SPAWNINGPOOL])
    bot.units = Units([drone, hatch], Mock())
    bot.can_afford = Mock(return_value=True)
    bot.build = Mock(return_value=async_mock(None))

    await bot.on_step(0)

    bot.build.assert_called_once_with(UnitTypeId.SPAWNINGPOOL, hatch)

    assert UnitTypeId.SPAWNINGPOOL not in bot.build_order
