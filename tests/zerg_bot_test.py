import asyncio
from unittest.mock import Mock

import pytest
from sc2.unit import Unit
from sc2.units import Units

from .context import initial_bot_state, ZergBot, UnitTypeId, add_unit_to_bot, unit_mock_of


@pytest.fixture
def zerg_bot():
    return initial_bot_state([])


@pytest.mark.asyncio
async def test_does_not_train_without_larvae(zerg_bot: ZergBot):
    zerg_bot.units = Units([], Mock())
    do_stub = Mock(return_value=None)
    zerg_bot.do = asyncio.coroutine(do_stub)

    success = await zerg_bot.train_unit(UnitTypeId.OVERLORD)

    assert not success
    do_stub.assert_not_called()


@pytest.mark.asyncio
async def test_does_not_train_if_cant_afford(zerg_bot: ZergBot):
    larva: Unit = unit_mock_of(UnitTypeId.LARVA)
    zerg_bot.units = Units([larva], Mock())
    zerg_bot.can_afford = Mock(return_value=False)
    do_stub = Mock(return_value=None)
    zerg_bot.do = asyncio.coroutine(do_stub)

    success = await zerg_bot.train_unit(UnitTypeId.OVERLORD)

    assert not success
    do_stub.assert_not_called()


@pytest.mark.asyncio
async def test_does_not_build_structure_if_cant_afford(zerg_bot: ZergBot):
    add_unit_to_bot(UnitTypeId.DRONE, zerg_bot)
    add_unit_to_bot(UnitTypeId.HATCHERY, zerg_bot)
    zerg_bot.can_afford = Mock(return_value=False)
    build_stub = Mock(return_value=None)
    zerg_bot.build = asyncio.coroutine(build_stub)

    success = await zerg_bot.build_structure(UnitTypeId.HATCHERY)

    assert not success
    build_stub.assert_not_called()


@pytest.mark.asyncio
async def test_does_not_train_if_insufficient_supply(zerg_bot: ZergBot):
    larva: Unit = unit_mock_of(UnitTypeId.LARVA)
    zerg_bot.units = Units([larva], Mock())
    zerg_bot.can_afford = Mock(return_value=True)
    zerg_bot.supply_left = 0
    do_stub = Mock(return_value=None)
    zerg_bot.do = asyncio.coroutine(do_stub)

    success = await zerg_bot.train_unit(UnitTypeId.DRONE)

    assert not success
    do_stub.do.assert_not_called()


@pytest.mark.asyncio
async def test_trains_if_sufficient_supply_and_funds(zerg_bot: ZergBot):
    larva: Unit = unit_mock_of(UnitTypeId.LARVA)
    zerg_bot.units = Units([larva], Mock())
    zerg_bot.can_afford = Mock(return_value=True)
    zerg_bot.supply_left = 1
    do_stub = Mock(return_value=None)
    zerg_bot.do = asyncio.coroutine(do_stub)

    success = await zerg_bot.train_unit(UnitTypeId.DRONE)

    assert success
    do_stub.assert_called_with(larva.train(UnitTypeId.DRONE))
