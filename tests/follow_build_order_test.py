import asyncio
from typing import Deque
from unittest.mock import Mock

import pytest
from sc2 import race_worker, Race
from sc2.ids.unit_typeid import UnitTypeId
from sc2.unit import Unit
from sc2.units import Units

from .context import ZergBot
from .context import unit_mock_of


def initial_bot_state(build_order) -> ZergBot:
    bot = ZergBot(Deque(build_order))

    bot.race = Race.Zerg
    bot.units = Units([], Mock())
    bot.supply_left = 10
    return bot


def add_unit_to_bot(unit_type: UnitTypeId, bot: ZergBot, ) -> Unit:
    unit: Unit = unit_mock_of(unit_type)
    bot.units.append(unit)
    bot.workers = bot.units(race_worker[bot.race])
    return unit


@pytest.mark.asyncio
async def test_does_nothing_on_empty_bo():
    bot = initial_bot_state([])
    await bot.on_step(0)


@pytest.mark.asyncio
async def test_build_first_unit_from_bo():
    bot = initial_bot_state([UnitTypeId.DRONE, UnitTypeId.OVERLORD])
    larva: Unit = add_unit_to_bot(UnitTypeId.LARVA, bot)
    larva.train = Mock(return_value="returnVal")
    bot.can_afford = Mock(return_value=True)
    do_stub = Mock(return_value=None)
    bot.do = asyncio.coroutine(do_stub)

    await bot.on_step(0)

    larva.train.assert_called_once_with(UnitTypeId.DRONE)
    do_stub.assert_called_once_with(larva.train("any"))
    assert UnitTypeId.DRONE not in bot.build_order


@pytest.mark.asyncio
async def test_dont_build_unit_if_cant_afford():
    bot = initial_bot_state([UnitTypeId.DRONE, UnitTypeId.OVERLORD])
    larva: Unit = add_unit_to_bot(UnitTypeId.LARVA, bot)
    larva.train = Mock(return_value="returnVal")
    bot.can_afford = Mock(return_value=False)
    do_stub = Mock(return_value=None)
    bot.do = asyncio.coroutine(do_stub)

    await bot.on_step(0)

    larva.train.assert_not_called()
    do_stub.assert_not_called()
    assert UnitTypeId.DRONE in bot.build_order


@pytest.mark.asyncio
async def test_find_supply_for_first_unit_from_bo():
    bot = initial_bot_state([UnitTypeId.OVERLORD])
    larva: Unit = add_unit_to_bot(UnitTypeId.LARVA, bot)
    larva.train = Mock(return_value="returnVal")
    bot.can_afford = Mock(return_value=True)
    do_stub = Mock(return_value=None)
    bot.do = asyncio.coroutine(do_stub)

    await bot.on_step(0)

    larva.train.assert_called_once_with(UnitTypeId.OVERLORD)
    do_stub.assert_called_once_with(larva.train("any"))
    assert UnitTypeId.OVERLORD not in bot.build_order


@pytest.mark.asyncio
async def test_build_structure_from_bo():
    bot = initial_bot_state([UnitTypeId.SPAWNINGPOOL])
    add_unit_to_bot(UnitTypeId.DRONE, bot)
    hatch: Unit = add_unit_to_bot(UnitTypeId.HATCHERY, bot)
    bot.can_afford = Mock(return_value=True)
    build_stub = Mock(return_value=None)
    bot.build = asyncio.coroutine(build_stub)

    await bot.on_step(0)

    build_stub.assert_called_once_with(UnitTypeId.SPAWNINGPOOL, hatch)
    assert UnitTypeId.SPAWNINGPOOL not in bot.build_order


@pytest.mark.asyncio
async def test_dont_build_structure_from_bo_without_drones():
    bot = initial_bot_state([UnitTypeId.SPAWNINGPOOL])
    add_unit_to_bot(UnitTypeId.HATCHERY, bot)
    bot.can_afford = Mock(return_value=True)
    build_stub = Mock(return_value=None)
    bot.build = asyncio.coroutine(build_stub)

    await bot.on_step(0)

    build_stub.assert_not_called()
    assert UnitTypeId.SPAWNINGPOOL in bot.build_order
